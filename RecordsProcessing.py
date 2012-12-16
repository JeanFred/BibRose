#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Processing some records, metadata and stuff."""
__authors__ = 'User:Jean-Frédéric'

import os
import sys
import pickle
from collections import Counter
sys.path.append('../pywikipedia')
import wikipedia as pywikibot
import pywikibot.textlib as textlib
from OaiRecord import OaiRecord
from OaiClient import OaiClient
from MetadataMapper import MetadataMapper
from CommonsFunctions import *
from InputOutput import *


class RecordsProcessing:

    """Processing a collection of Records in various ways."""

    def __init__(self):
        self.FIELDS = ['publisher', 'description', 'language', 'format',
                       'type', 'rights', 'date', 'relation', 'source',
                       'coverage', 'contributor', 'title', 'identifier',
                       'creator', 'subject']
        self.records = []
        self.metadata_mapper = None

    def retrieve_unique_metadata_values(self):
        """Retrieve all metadata values (per field).

        - Iterate through the given records
        - For each record, for each field, add the metadata values to a set
        - Write the set on disk, in text format

        """
        print "%s records" % len(self.records)
        # Initialises the sets
        sets = dict()
        for field in self.FIELDS:
            sets[field] = set()
        # Iterates through the records
        for record in self.records:
            for field in self.FIELDS:
                data = record.metadata[field]
                sets[field].update(data)
        for field in self.FIELDS:
            fileName = join('metadata', '%s_list.txt' % field)
            write_set_to_disk(sets[field], fileName)

    def retrieve_metadata_from_records_for_alignment(self):
        """Retrieve the metadata from the records and write them on disk.

        - Iterate through the given records
        - For each record, for each field, store the metadata values
        - Write the result on disk, in both CSV and wiki format
        (ordered by descending number of occurences)

        """
        # Initialises the Counters
        field_counter = Counter()
        field_values_counters_dict = {}
        for field in self.FIELDS:
            field_values_counters_dict[field] = Counter()

        #Iterates through the records
        for record in self.records:
            for field in self.FIELDS:
                for field_contents in record.metadata[field]:
                    field_values_counters_dict[field][field_contents] += 1
                field_counter[field] += len(record.metadata[field])

        for field in self.FIELDS:
            fileName = os.path.join('metadata', 'dict',  '%s_dict.csv' % field)
            write_dict_as_csv(field_values_counters_dict[field], field, 'csv')

            self.metadata_mapper = MetadataMapper()
            self.metadata_mapper.write_dict_as_wiki(field_values_counters_dict[field],
                                                field, 'wiki')
        for k, v in field_counter.items():
            print k, v

    def loop_over_and_map(self):
        """Loop over the record collection and proceeds to the mapping."""
        fields = self.FIELDS
        recordsbis = list(self.records)[5:50]
        print "Processing %s records" % len(recordsbis)
        for record in recordsbis:
            print "== Processing record"
            record_metadata = dict()
            record_categories = []
            for field in fields:
                record_metadata_dict = dict()
                record_contents = record.metadata[field]
                processing_method = self.metadata_mapper.get_processing_method(field)
                if processing_method:
                    #print "==== Processing field %s" % field
                    #print processing_method
                    (value, categories) = processing_method(record_contents, field)
                    record_metadata[field] = value
                    record_categories.extend(categories)
                else:
                    print "==== Ignored field %s ====" % field
                    print "\n".join(record_contents)
                    print "=========================="
                #contents = [u'SecondItem']
                #if field in alignment_fields:
                    #for content in record_contents:

                #else:  # We do not need to align anything for these fields
                    #pass
            print textlib.glue_template_and_params(('User:Mk-II/Ancely', record_metadata))
            print make_categories(record_categories)
        pass

    def retrieve_records_from_disk(self, directory):
        """Unpickle all OAI records from a given directory.

        If anything bad happens during the reading of the File
        (file reading error, impossible to pickle), file is ignored.

        """
        for fileName in [os.path.join(directory, x) for x in os.listdir(directory)]:
            try:
                yield OaiRecord(pickle.load(open(fileName, 'r')))
            except:
                pass


def main():
    """Main entry point."""
    directory = 'ancely'
    #configuration_file = 'oai_servers.cfg'
    #oaiclient = OaiClient(configuration_file)
    #oaiclient.dump_all_records_from_server(directory, 'general:CL21')
    #retrieve_metadata_alignments_and_dump_to_file('ancely_alignment')
    #arks = ['ark:/74899/B315556101_CP0004_09_002',
           #'ark:/74899/B315556101_CP0004_09_009',
           #'ark:/74899/B315556101_CP0004_09_014']
    #records = map(oaiserver.get_record_from_ARK, arks)
    #for record in records:
        #print records
    processor = RecordsProcessing()
    print "Retrieving records from disk..."
    processor.records = list(processor.retrieve_records_from_disk('ancely'))
    print "...done"
    processor.retrieve_metadata_from_records_for_alignment()
    print "Retrieving mapping from disk..."
    mapping = pickle.load(open('ancely_alignment', 'r'))
    processor.metadata_mapper = MetadataMapper()
    processor.metadata_mapper.mapper = mapping
    print "...done"
    print "Mapping records..."
    processor.loop_over_and_map()
    print "...done"
    ##
    ##dump_all_records_from_server("records")


if __name__ == "__main__":
    main()
