#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Processing metadata
"""
__authors__ = 'User:Jean-Frédéric'

import sys
import os
import ConfigParser
import codecs
sys.path.append('../pywikipedia')
import wikipedia as pywikibot
import pywikibot.textlib as textlib


def retrieve_alignment_from_wiki(filename, alignment_template):
    """Retrieve the metadata alignment from a given wikipage on disk

    Iterate over the given alignment template occurences,
    """
    #TODO get wikipage from website?
    print "retrieve_alignment_from_wiki " + filename
    wiki_file = os.path.join('wikiin', filename)
    f = codecs.open(wiki_file, mode='r', encoding='utf-8')
    all_templates = textlib.extract_templates_and_params(f.read())
    alignment = dict()
    for x in all_templates:
        if x[0] == alignment_template:
            categories = x[1]['categories'].split(']]')[0].split(':')[-1]
            alignment[x[1]['item']] = (x[1]['value'], categories)
    return alignment


def retrieve_metadata_alignments(fields, alignment_config_items):
    """Retrieve metadata alignments for all fields

    Iterates over the given fields, determines the associate wikipage
    and calls retrieve_alignment_from_wiki on each.
    """
    print 'retrieve_metadata_alignments'
    alignments = dict()
    for field in fields:
        root = alignment_config_items['alignment_pages_root']
        alignment_template = alignment_config_items['alignment_template']
        #wikipage = root + field
        wikipage = field
        alignments[field] = retrieve_alignment_from_wiki(wikipage,
                                                         alignment_template)
    return alignments


def write_dict_as_wiki(aDict, name, directory, alignment_config_items):
    """Write a given dictionary on disk, in template alignment format."""
    with codecs.open(os.path.join(directory, name), 'w', 'utf-8') as wikipage:
        wikipage.write("{|\nItem | Count | Tag | Categories")
        items = aDict.items()
        items.sort(key=lambda x: x[1], reverse=True)
        for item in items:
            values = (alignment_config_items['alignment_template'],
                      {'item': item[0], 'count': item[1],
                      'value': None, 'categories': None} )
            table_line = textlib.glue_template_and_params(values)
            wikipage.write(unicode(table_line))
        wikipage.write("\n|}")


def process():
    pass