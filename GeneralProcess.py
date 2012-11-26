#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Processing some records, metadata and stuff.
"""
__authors__ = 'User:Jean-Frédéric'


from OaiRecordHandling import *
from MetadataCrunching import *
from CommonsFunctions import *
from InputOutput import *
import codecs
import os


alignment_config = ConfigParser.SafeConfigParser()
alignment_config.read('metadata_templates.cfg')
alignment_config_values = dict(alignment_config.items('Ancely'))

FIELDS = ['publisher', 'description', 'language', 'format', 'type', 'rights',
          'date', 'relation', 'source', 'coverage', 'contributor', 'title',
          'identifier', 'creator', 'subject']


def get_alignment(record_contents, field, alignments):
    """Retrieve the alignment for a given record contents.

    An alignment processing method.
    Concatenates the various values retrieved through the alignment

    Args
        record_contents
            A collection of contents of a record

        field
            The Dublin Core field to retrieve from

        alignments
            The master alignment data structure

    Returns
        A tuple (tag, categories)
    """
    all_value = ""
    all_categories = []
    for content in record_contents:
        content = content.strip()
        (value, categories) = alignments[field][content]
        all_value += value
        all_categories.extend(categories)
    return (all_value, all_categories)


def join_all(record_contents, field, alignments=None):
    """Join all 

    An alignment processing method.
    Concatenates the various values for retrieved through the alignment
    """
    return ("\n".join(record_contents), [])


def ignore_field(record_contents, field, alignments=None):
    return ("", [])


#def process_relation(record_contents, field, alignments=None):
    #return (record_contents[0], [])


FIELDS_PRE_PROCESSING_METHODS = {
    'publisher' : join_all,
    'description' : join_all,
    'format' : get_alignment,
    'language' : ignore_field,
    'type' : get_alignment,
    'rights' : ignore_field,
    'date' : get_alignment,
    'relation'  : ignore_field,
    'source' : join_all,
    'coverage' : get_alignment,
    'contributor' : get_alignment,
    'title' : join_all,
    'identifier': join_all,
    'subject' : get_alignment,
    'creator' : get_alignment
}


def retrieve_unique_metadata_values(records):
    """Retrieve all metadata values (per field)

    - Iterate through the given records
    - For each record, for each field, add the metadata values to a set
    - Write the set on disk, in text format
    """
    print "%s records" % len(records)
    # Initialises the sets
    sets = dict()
    for field in FIELDS:
        sets[field] = set()
    # Iterates through the records
    for record in records:
        for field in FIELDS:
            data = record[1][field]
            sets[field].update(data)
    for field in FIELDS:
        fileName = join('metadata', '%s_list.txt' % field)
        write_set_to_disk(sets[field], fileName)


def retrieve_metadata_from_records_for_alignment(records):
    """Retrieve the metadata from the records and write them on disk

    - Iterate through the given records
    - For each record, for each field, store the metadata values
    - Write the result on disk, in both CSV and wiki format
      (ordered by descending number of occurences)
    """
    # Initialises the dictionaries
    totalDict = {}
    master_dict = {}
    for field in FIELDS:
        master_dict[field] = {}
        totalDict[field] = 0
    #Iterates through the records
    for record in records:
        for field in FIELDS:
            updateCountDict(master_dict[field], record[1][field])
            totalDict[field] += len(record[1][field])

    for field in FIELDS:
        fileName = os.path.join('metadata', 'dict',  '%s_dict.csv' % field)
        write_dict_as_csv(master_dict[field], field, 'csv')
        write_dict_as_wiki(master_dict[field], field, 'wiki')

    for k, v in totalDict.items():
        print k, v


def process_records3(records, alignments):
    """Process the records, differently
    """
    fields = FIELDS
    recordsbis = list(records)[0:5]
    print "Processing %s records" % len(recordsbis)
    for record in recordsbis:
        print "== Processing record"
        record_metadata = dict()
        record_categories = []
        for field in fields:
            record_metadata_dict = dict()
            record_contents = record[1][field]
            processing_method = FIELDS_PRE_PROCESSING_METHODS.get(field, None)
            if processing_method:
                #print "==== Processing field %s" % field
                #print processing_method
                (value, categories) = processing_method(record_contents, field, alignments)
                #print value
                #print categories
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


def updateCountDict(aDict, items):
    for item in items:
        if item in aDict:
            aDict[item] += 1
        else:
            aDict[item] = 1



def retrieve_metadata_alignments_and_dump_to_file(fileName):
    #alignment_fields = ['publisher', 'language', 'format', 'type', 'rights',
              #'date', 'coverage', 'contributor', 'creator', 'subject']
    alignment_fields = FIELDS
    alignments = retrieve_metadata_alignments(alignment_fields, alignment_config_values)
    try:
        with open(fileName, 'w') as f:
            pickle.dump(alignments, f)
    except:
        print "Could not pickle aligments"

        
def main():
    """Entry point
    """
    directory = 'ancely'
    #dump_all_records_from_server(directory, 'general:CL21')
    #retrieve_metadata_alignments_and_dump_to_file('ancely_alignment')
    #arks = ['ark:/74899/B315556101_CP0004_09_002',
    #        'ark:/74899/B315556101_CP0004_09_009',
    #        'ark:/74899/B315556101_CP0004_09_014']
    print "Retrieving records from disk..."
    records = retrieve_records_from_disk('ancely')
    print "...done"
    print "Retrieving alignments from disk..."
    alignments = pickle.load(open('ancely_alignment', 'r'))
    print "...done"
    #print "Processing records..."
    process_records3(records, alignments)
    print "...done"    
    ##records = map(get_record_from_ARK,arks)
    ##dump_all_records_from_server("records")


if __name__ == "__main__":
    main()
