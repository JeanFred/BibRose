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

reload(sys)
sys.setdefaultencoding('utf-8')

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
        for record in self.records:
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
            record_metadata['identifier'] = record.retrieve_bare_ID()
            record_metadata['url'] = record.get_file_URL()
            record_metadata['ARK'] = record.retrieve_ARK()

            yield (record_metadata, record_categories)
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
    #processor.retrieve_metadata_from_records_for_alignment()
    print "Retrieving mapping from wikipages..."
    mapping = pickle.load(open('ancely_alignment', 'r'))
    processor.metadata_mapper = MetadataMapper()
    processor.metadata_mapper.retrieve_metadata_alignments(['type', 'coverage', 'creator', 'subject'])
    print "...done"
    print "Mapping records..."

    from collections import Counter
    all_categories = Counter()
    categories_count_per_file = dict()

    for (record_metadata, record_categories) in processor.loop_over_and_map():
        all_categories.update(record_categories)
        categories_count_per_file[record_metadata['identifier']] = len(record_categories)
        print "= %s =" % record_metadata['identifier']
        template_name = 'User:Jean-Frédéric/Ancely/Ingestion'.encode('utf-8')
        tpl = textlib.glue_template_and_params((template_name,
                                                record_metadata))
        #print "{{collapse|title=%s|1=<pre>\n%s\n</pre>}}" % (record_metadata['identifier'], tpl)
        print tpl
        print "<nowiki>\n%s\n</nowiki>" % make_categories(record_categories)
        print "...done"
    categorisation_statistics(all_categories, categories_count_per_file)


def categorisation_statistics(all_categories, categories_count_per_file):
    """Compute statistics on categorisation."""
    try:
        import numpy

        print "== Per category =="
        print "%s categories, %s distincts" % (sum(all_categories.values()),
                                               len(all_categories))
        print "Mean: %s" % numpy.mean(all_categories.values())
        print "Median: %s" % numpy.median(all_categories.values())
        print "Max %s // Min %s" % (max(all_categories.values()),
                                    min(all_categories.values()))
        print "Top 10:"
        print all_categories.most_common(10)
        print "Lose 10:"
        print all_categories.most_common()[-10:]

        print "== Per file =="
        print "Mean: %s" % numpy.mean(categories_count_per_file.values())
        print "Median: %s" % numpy.median(categories_count_per_file.values())
        print "Max %s // Min %s" % (max(categories_count_per_file.values()),
                                    min(categories_count_per_file.values()))
        print Counter(categories_count_per_file).most_common(5)
        print Counter(categories_count_per_file).most_common()[-5:]
    except ImportError, e:
        "Numpy is needed to have categorisation statistics."


if __name__ == "__main__":
    main()
