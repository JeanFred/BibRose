#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Methods to query the OAI-PMH Metadata server of Toulouse BibNum
"""
__authors__ = 'User:Jean-Frédéric'

import ConfigParser

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader


class OaiClient:

    def __init__(self, configuration_file):
        """Constructor."""
        self.oai_config = ConfigParser.SafeConfigParser()
        self.oai_config.read(configuration_file)
        self.current_config = 'ToulouseBis'

        registry = MetadataRegistry()
        registry.registerReader('oai_dc', oai_dc_reader)
        self.client = Client(self._get_config_value('url'), registry)

    def _get_config_value(self, field):
        """Return the config value for the given field."""
        return self.oai_config.get(self.current_config, field)

    def get_record_from_ARK(self, ark):
        """Retrieve a OAI Record from the OAI server based on the ARK."""
        identifier = '%s:/%s' % (self._get_config_value('identifier_root'), ark)
        return self.client.GetRecord(identifier=identifier,
                                     metadataPrefix='oai_dc')

    def dump_all_records_from_server(self, directory, oai_set):
        """Retrieve all records from distant server and dump it on disk."""
        for record in self.client.ListRecords(metadataPrefix='oai_dc',
                                              set=oai_set):
            try:
                oai_record = OaiRecord(record)
                oai_record .pickle_record(directory)
            except:
                pass
