import datetime
import logging
import os

import sickle
from sickle import models
from sickle.iterator import OAIItemIterator
from sickle.utils import xml_to_dict
from requests.exceptions import SSLError

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def opener_664_permissions(path, flags):
    return os.open(path, flags, 0o664)


class SickleRecord(models.Record):

    def __init__(self, record_element, strip_ns=True):
        models.Record.__init__(self, record_element, strip_ns=strip_ns)

    def get_metadata(self):
        try:
            self.metadata = xml_to_dict(
                self.xml.find(
                    './/' + self._oai_namespace + 'metadata'
                ).getchildren()[0], strip_ns=self._strip_ns)
        except AttributeError:
            self.metadata = None


def harvest(org_harvest_info, org_key, write_path, verbosity):
    """
    Manatus harvest function

    :param dict org_harvest_info: Dict of data from ``manatus_harvests.cfg``.
        Includes the key, value pairs :py:data:`oaiendpoint`, :py:data:`setlist`, and :py:data:`metadataprefix`.
        See :doc:`configuration` for more information.
    :param str org_key: Section key in ``manatus_harvests.cfg``. Appended to :py:data:`write_path`
    :param str write_path: File path to write data. Taken from ``manatus.cfg``
    :param int verbosity: Set verbosity

    """
    logger.debug('cli.harvest called')
    # check for dir path
    if not os.path.exists(os.path.join(write_path, org_key)):
        logger.debug(f'Creating path {os.path.join(write_path, org_key)}')
        os.makedirs(os.path.join(write_path, org_key), mode=0o774)

    # OAI-PMH endpoint URL from config
    oai = org_harvest_info['OAIEndpoint']

    # metadataPrefix from config
    metadata_prefix = org_harvest_info['MetadataPrefix']

    # iterate through sets to harvest
    for set_spec in org_harvest_info['SetList'].split(', '):
        logger.info(f'Harvesting {org_key} set {set_spec}')

        # Config value 'all' in harvest set list will harvest whole repository
        if set_spec.lower() == 'all':
            set_spec = None
            set_spec_string = 'all'
        else:
            set_spec_string = set_spec.replace(":", "_")

        # open XML file for appending
        with open(os.path.join(write_path, org_key, f'{set_spec_string}_{datetime.date.today()}.xml'), 'a',
                  encoding='utf-8', opener=opener_664_permissions) as fp:

            # Sickle harvester
            harvester = sickle.Sickle(oai, iterator=OAIItemIterator, encoding='utf-8',
                                      headers={"User-Agent": "manatus-ssdn/1.0"})  # todo: make this dynamic some day
            harvester.class_mapping['ListRecords'] = SickleRecord
            logger.debug(f'Sickle harvester options: {harvester.__dict__}')

            # Sickle harvester ListRecords
            try:
                records = harvester.ListRecords(set=set_spec, metadataPrefix=metadata_prefix, ignore_deleted=True)
                logger.debug(
                    f'Sickle request options: set={set_spec}, metadataPrefix={metadata_prefix}, ignore_deleted=True')
            except SSLError:
                logger.warning(f'SSL certification failed: falling back to unencrypted connection')
                harvester = sickle.Sickle(oai, iterator=OAIItemIterator, encoding='utf-8',
                                          headers={"User-Agent": "manatus-ssdn/1.0"}, verify=False)
                records = harvester.ListRecords(set=set_spec, metadataPrefix=metadata_prefix, ignore_deleted=True)
                logger.debug(
                    f'Sickle request options: set={set_spec}, metadataPrefix={metadata_prefix}, ignore_deleted=True')

            logger.info(f'Writing records {fp.name}')
            fp.write('<oai>')
            for record in records:
                fp.write(record.raw)
                logger.debug(f'Record: {record}')
            fp.write('</oai>')
