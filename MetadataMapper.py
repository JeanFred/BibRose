# -*- coding: latin-1 -*-

"""Mapping metadata."""

__authors__ = 'User:Jean-Frédéric'

import os
import ConfigParser
import codecs


class MetadataMapper:

    """A MetadataMapper maps record content values to (tag, categories) tuple."""

    def __init__(self):
        """Constructor."""
        self.mapper = None
        self.alignment_config_items = None
        self.init_config('metadata_templates.cfg')
        self.populate_processing_methods()

    def init_config(self, configuration_file):
        """Initialise from configuration file."""
        alignment_config = ConfigParser.SafeConfigParser()
        alignment_config.read(configuration_file)
        self.alignment_config_items = dict(alignment_config.items('Ancely'))

    def get_alignment(self, record_contents, field):
        """Retrieve the alignment for a given record contents.

        Args
            record_contents - A collection of contents of a record

            field - The Dublin Core field to retrieve from

        Returns a tuple (tag, categories)

        """
        all_value = ""
        all_categories = []
        for content in record_contents:
            content = content.strip()
            (value, categories) = self.mapper[field].get(content, ("", []))
            all_value += value
            all_categories.extend(categories)
        return (all_value, all_categories)

    def join_all(self, record_contents, field):
        """Join all: returns the concatenation of the alignment values."""
        return ("\n".join(record_contents), [])

    def ignore_field(record_contents, field, alignments=None):
        """Ignore field, returns an empty tuple."""
        return ("", [])

    #def process_relation(record_contents, field, alignments=None):
        #return (record_contents[0], [])

    def populate_processing_methods(self):
        """Associate fields to processing methods."""
        self.FIELDS_PRE_PROCESSING_METHODS = {
            'publisher': self.join_all,
            'description': self.join_all,
            'format': self.get_alignment,
            'language': self.ignore_field,
            'type': self.get_alignment,
            'rights': self.ignore_field,
            'date': self.get_alignment,
            'relation': self.ignore_field,
            'source': self.join_all,
            'coverage': self.get_alignment,
            'contributor': self.get_alignment,
            'title': self.join_all,
            'identifier': self.join_all,
            'subject': self.get_alignment,
            'creator': self.get_alignment
            }

    def get_processing_method(self, field):
        """Return the pre-processing method for the given field."""
        return self.FIELDS_PRE_PROCESSING_METHODS.get(field, None)

    def retrieve_from_wiki(self, filename, alignment_template):
        """Retrieve the metadata mapping from a given wikipage on disk.

        Iterate over the given alignment template occurences,
        retrieve and return the mapping values.

        """
        #TODO get wikipage from website?
        print "retrieve_from_wiki " + filename
        wiki_file = os.path.join('wikiin', filename)
        f = codecs.open(wiki_file, mode='r', encoding='utf-8')
        all_templates = textlib.extract_templates_and_params(f.read())
        field_mapper = dict()
        for x in all_templates:
            if x[0] == alignment_template:
                categories = x[1]['categories'].split(']]')[0].split(':')[-1]
                field_mapper[x[1]['item']] = (x[1]['value'], categories)
        return field_mapper

    def dump_to_file(self, fileName):
        """Dump the mapper on disk under the given filename."""
        alignment_fields = FIELDS
        #alignment_fields = ['publisher', 'language', 'format', 'type', 'rights',
                #'date', 'coverage', 'contributor', 'creator', 'subject']
        alignments = self.retrieve_metadata_alignments(alignment_fields)
        try:
            with open(fileName, 'w') as f:
                pickle.dump(alignments, f)
        except:
            print "Could not pickle aligments"

    def retrieve_metadata_alignments(self, fields):
        """Retrieve metadata alignments from disk for all given fields.

        Iterates over the given fields, determines the associate wikipage
        and calls retrieve_alignment_from_wiki on each.

        """
        print 'retrieve_metadata_alignments'
        alignments = dict()
        for field in fields:
            root = self.alignment_config_items['alignment_pages_root']
            alignment_template = self.alignment_config_items['alignment_template']
            #wikipage = root + field
            wikipage = field
            alignments[field] = retrieve_from_wiki(wikipage,
                                                   alignment_template)
        self.mapper = alignments

    def write_dict_as_wiki(self, aDict, name, directory):
        """Write a given dictionary on disk, in template alignment format."""
        with codecs.open(os.path.join(directory, name), 'w', 'utf-8') as wikipage:
            wikipage.write("{|\nItem | Count | Tag | Categories")
            items = aDict.items()
            items.sort(key=lambda x: x[1], reverse=True)
            for item in items:
                values = (self.alignment_config_items['alignment_template'],
                          {'item': item[0], 'count': item[1],
                           'value': "", 'categories': ""})
                table_line = '\n' + textlib.glue_template_and_params(values)
                wikipage.write(unicode(table_line))
            wikipage.write("\n|}")
