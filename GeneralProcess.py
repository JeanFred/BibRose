#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Processing some records, metadata and stuff.
"""
__authors__ = 'User:Jean-Frédéric'


from OaiRecordHandling import *


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
    print "%s records" % len(records)
    #trutatRecords = filter(is_Trutat, records)
    #print "%s records left after filtering" % len(trutatRecords)
    # Initialises the dictionaries
    totalDict = {}
    for field in FIELDS:
        exec("%s_dict = {}" % (field))
        totalDict[field] = 0
    #Iterates through the records
    for record in records:
        for field in FIELDS:
            #print field
            data = record[1][field]
            myDict = eval("%s_dict" % field)
            totalDict[field] += len(record[1][field])
            # this is the ugly way, will beautify later
            #updateCountDict(myDict,data)
    for field in FIELDS:
        fileName = join('metadata', 'dict',  '%s_dict.csv' % field)
        myDict = eval("%s_dict" % field)
        #print mySet
        #write_dict_to_disk(myDict, fileName)
        #exec("print %s_counter" % (field))
    for k, v in totalDict.items():
        print k, v


def updateCountDict(aDict, records):
    for record in records:
        if record in aDict:
            aDict[record] += 1
        else:
            aDict[record] = 1


def write_set_to_disk(mySet, fileName):
    """Write a given set on disk
    """
    print "Writing set to %s" % fileName
    with codecs.open(fileName, 'w', 'utf-8') as f:
        f.write("\n".join(mySet))


def write_dict_to_disk(myDict, fileName):
    """Write a given dictionary on disk as CSV
    """
    print "Writing dict to %s" % fileName
    items = myDict.items()

    def unicode_join_tuple(item):
        return "|".join(map(unicode, item))
    with codecs.open(fileName, 'w', 'utf-8') as f:
        f.write("\n".join(map(unicode_join_tuple, items)))


def main():
    """Entry point
    """
    directory = 'ancely'
    dump_all_records_from_server(directory, 'general:CL21')
    #arks = ['ark:/74899/B315556101_CP0004_09_002',
    #        'ark:/74899/B315556101_CP0004_09_009',
    #        'ark:/74899/B315556101_CP0004_09_014']
    #print "Retrieving records from disk..."
    #records = retrieve_records_from_disk('records')
    #print "...done"
    #print "Processing records..."
    #process_records2(records)
    #print "...done"
    ##records = map(get_record_from_ARK,arks)
    ##dump_all_records_from_server("records")


if __name__ == "__main__":
    main()
