#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Methods to deal with OAI records
"""
__authors__ = 'User:Jean-Frédéric'


import pickle
from os.path import join

from OaiServerTools import *
import CommonsFunctions


FIELDS = ['publisher', 'description', 'language', 'format', 'type', 'rights',
          'date', 'relation', 'source', 'coverage', 'contributor', 'title',
          'identifier', 'creator', 'subject']


def get_file_URL(record):
    """Build the full resolution file URL for the given record.

    As this URL is not given in the OAI record,
    it is built from the thumbnail ('vignette') URL,
    assuming this always follows the same pattern.

    - Take the last relation Dublin Core element
    - Take the last split() to get rid of the "vignette:" etc.
    - Cut the eleven last characters ("_thumb.jpeg")
    - Append the file extension '.jpg'
      (Oddly, Trutat files use uppercase 'JPG' but Ancely use lowercase 'jpg')

    (Works in 100% of the 4 attempts)
    """
    return record[1]['relation'][-1].split()[-1][:-11] + '.jpg'


def retrieve_ARK(record):
    """Retrieve the ARK of a given OAI record"""
    return record[0].identifier()


def retrieve_bare_ID(record):
    """Retrieve the bare ID of a given OAI record.

    A bare ID is defined as the last part of the ARK identifier
    (eg for 'ark:/74899/B315556101_BIBLC0028' it is 'B315556101_BIBLC0028')
    as it needs to be so to be clean (eg no slashes) for file naming.
    """
    return retrieve_ARK(record).split('ark:/74899/')[1]

def retrieve_title(record):
    """Retrieve the title  from a given record
    
    TODO : chomp whitespace at start and end
    """
    return record[1]['title'][0]

def print_metadata(record):
    """Display the metadata of a given OAI record in a not-so-crappy format.
    """
    for item in ["%s %s" % (k, v) for k, v in record[1].getMap().items()]:
        print item


def print_dict(element):
    """Display the elements of a dictionary"""
    print "\n".join(["%s %s" % (k, v) for k, v in element.__dict__.items()])


def is_Trutat(record):
    """Indicate whether a record is from the Trutat set.

    Compares the creator Dublin Core field to the expected Trutat string.
    Runs into Unicode problems, going for partial match
    """
    #creatorField = u"Trutat, Eugéne (1840-1910). Photographe"
    try:
        return 'Trutat' in record[1]['creator'][0]
    except:
        return False


def pickle_record(record, directory):
    """Write an OAI record on disk in a given repository
    """
    fileName = join(directory, retrieve_bare_ID(record))
    try:
        with open(fileName, 'w') as f:
            pickle.dump(record, f)
    except:
        pass


def retrieve_records_from_disk(directory):
    """Unpickle all OAI records from a given directory

    If anything bad happens during the reading of the File
    (file reading error, impossible to pickle), file is ignored.
    """
    records = []
    for fileName in [join(directory, x) for x in listdir(directory)]:
        try:
            records.append(pickle.load(open(fileName, 'r')))
        except:
            pass
    return records
