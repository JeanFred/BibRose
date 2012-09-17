#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Processing some records, metadata and stuff.
"""
__authors__ = 'User:Jean-Frédéric'


from OaiRecordHandling import *
import codecs
import os


FIELDS = ['publisher', 'description', 'language', 'format', 'type', 'rights',
          'date', 'relation', 'source', 'coverage', 'contributor', 'title',
          'identifier', 'creator', 'subject']

def process_records1(records):
    """Process the records

    Kind of an ad-hoc, all purpose method.
    """
    print "%s records" % len(records)
    trutatRecords = filter(is_Trutat, records)
    print "%s records left after filtering" % len(trutatRecords)
    # Initialises the sets
    for field in FIELDS:
        exec("%s_set = set()" % (field))
    #Iterates through the records
    for record in trutatRecords:
        for field in FIELDS:
            data = record[1][field]
            # this is the ugly way, will beautify later
            exec("%s_set.update(data)" % field)
    for field in FIELDS:
        fileName = join('metadata', '%s_list.txt' % field)
        mySet = eval("%s_set" % field)
        write_set_to_disk(mySet, fileName)


def process_records2(records):
    """Process the records, differently

    Kind of an ad-hoc, all purpose method.
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


def write_dict_as_wiki(aDict, name, directory):
    with codecs.open(os.path.join(directory, name), 'w', 'utf-8') as wikipage:
        wikipage.write("{|\nItem | Count | Tag | Categories")               
        items = aDict.items()
        items.sort(key=lambda x: x[1], reverse=True)
        for item in items:
            #table_line = "\n| %s | %s | " % (item)
            table_line = """
{{User:Mk-II/AncelyRow
|item       =%s
|count      =%s
|value      =
|categories =
}}""" % item
        
            wikipage.write(unicode(table_line))
        wikipage.write("\n|}")


def updateCountDict(aDict, items):
    for item in items:
        if item in aDict:
            aDict[item] += 1
        else:
            aDict[item] = 1


def write_set_to_disk(mySet, fileName):
    """Write a given set on disk
    """
    print "Writing set to %s" % fileName
    with codecs.open(fileName, 'w', 'utf-8') as f:
        f.write("\n".join(mySet))


def write_dict_as_csv(myDict, name, directory):
    """Write a given dictionary on disk as CSV
    """
    print "Writing dict as %s in %s" % (name, directory)
    items = myDict.items()
    items.sort(key=lambda x: x[1], reverse=True)
    def unicode_join_tuple(item):
        return "|".join(map(unicode, item))
    with codecs.open(os.path.join(directory, name + '.csv'), 'w', 'utf-8') as f:
        f.write("\n".join(map(unicode_join_tuple, items)))


def main():
    """Entry point
    """
    directory = 'ancely'
    #dump_all_records_from_server(directory, 'general:CL21')
    #arks = ['ark:/74899/B315556101_CP0004_09_002',
    #        'ark:/74899/B315556101_CP0004_09_009',
    #        'ark:/74899/B315556101_CP0004_09_014']
    print "Retrieving records from disk..."
    records = retrieve_records_from_disk('ancely')
    print "...done"
    print "Processing records..."
    process_records2(records)
    print "...done"    
    ##records = map(get_record_from_ARK,arks)
    ##dump_all_records_from_server("records")


if __name__ == "__main__":
    main()
