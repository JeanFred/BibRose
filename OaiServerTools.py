#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Methods to query the OAI-PMH Metadata server of Toulouse BibNum
"""
__authors__ = 'User:Jean-Frédéric'

import sys
import ConfigParser

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

sys.path.append('..')

oai_config = ConfigParser.SafeConfigParser()
oai_config.read('oai_servers.cfg')
current_config = 'ToulouseBis'

registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)
client = Client(oai_config.get(current_config, 'url'), registry)


def get_record_from_ARK(ark):
    """Retrieve a OAI Record from the OAI server based on the ARK identifier
    """
    identifier_root = oai_config.get(current_config, 'identifier_root')
    return client.getRecord(identifier='%s:/%s' % (identifier_root, ark),
                            metadataPrefix='oai_dc')


def dump_all_records_from_server(directory, oai_set):
    """Retrieve all records from distant server and dump it on disk
    """
    for record in client.listRecords(metadataPrefix='oai_dc', set=oai_set):
        try:
            pickle_record(record, directory)
        except:
            pass
