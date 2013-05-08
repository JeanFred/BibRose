#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Processing some records, metadata and stuff."""
__authors__ = 'User:Jean-Frédéric'

import os
import sys
import re
import pickle
import itertools
from collections import Counter
sys.path.append('../pywikipedia-rewrite')
sys.path.append('../pywikipedia-rewrite/scripts')
import pywikibot
import pywikibot.textlib as textlib
import upload
import data_ingestion
from data_ingestion import Photo, DataIngestionBot
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
            record_categories = set()
            for field in fields:
                record_metadata_dict = dict()
                record_contents = record.metadata[field]
                processing_method = self.metadata_mapper.get_processing_method(field)
                if processing_method:
                    #print "==== Processing field %s" % field
                    #print processing_method
                    (value, categories) = processing_method(record_contents, field)
                    record_metadata[field] = value
                    record_categories.update(categories)
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
            record_metadata['ARK'] = record.retrieve_ARK()
            record_metadata['categories'] = make_categories(record_categories)
            photo = data_ingestion.Photo(URL=record.get_file_URL(),
                                         metadata=record_metadata)
            yield photo
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
    #mapping = pickle.load(open('ancely_alignment', 'r'))
    processor.metadata_mapper = MetadataMapper()
    processor.metadata_mapper.retrieve_metadata_alignments(['type', 'coverage', 'creator', 'date', 'subject'])
    print "...done"
    print "Mapping records..."

    from collections import Counter
    all_categories = Counter()
    categories_count_per_file = dict()

    reader = processor.loop_over_and_map()
    template_name = 'User:Jean-Frédéric/Ancely/Ingestion'.encode('utf-8')
    front_titlefmt = ""
    variable_titlefmt = "%(title)s"
    rear_titlefmt = " - Fonds Ancely - %(identifier)s.%(_ext)s"
        #upload_file(photo, categories)
        #all_categories.update(record_categories)
        #categories_count_per_file[record_metadata['identifier']] = len(record_categories)
        #print "= %s =" % record_metadata['identifier']
        #template_name = 'User:Jean-Frédéric/Ancely/Ingestion'.encode('utf-8')
        #tpl = textlib.glue_template_and_params((template_name,
                                                #record_metadata))
        #print "{{collapse|title=%s|1=<pre>\n%s\n</pre>}}" % (record_metadata['identifier'], tpl)
        #print tpl
        #print "<nowiki>\n%s\n</nowiki>" % make_categories(record_categories)

        #upload_file(url=url,
                    #description="\n\n".join([tpl, make_categories(record_categories)]),
                    #title=title)

        #print "...done"
    #categorisation_statistics(all_categories, categories_count_per_file)
    reader_slice = itertools.islice(reader, 300, 500)
    #TODO 285
    uploadBot = CustomDataIngestionBot(reader=reader_slice,
                                     front_titlefmt=front_titlefmt,
                                     rear_titlefmt=rear_titlefmt,
                                     variable_titlefmt=variable_titlefmt,
                                     pagefmt=template_name)
    print "Uploading..."
    uploadBot.run()


def _cut_title(fixed_front, variable, fixed_rear, MAX_LENGTH=255):
    """Return the given title smartly cut"""
    fixed_length = len(fixed_front) + len(fixed_rear)
    available_length = MAX_LENGTH - fixed_length
    chunked = variable.split()
    part = 1
    while len(variable) > available_length:
        variable = " ".join(chunked[:-part]) + "..."
        part += 1
    return fixed_front + variable + fixed_rear


def make_title(entries, fixed_front_fmt, fixed_rear_fmt, variable_fmt):
    """Return a title based on the metadata and format strings.

    This method uses three format strings: the fixed front, the variable,
    and the fixed rear.

    """
    fixed_front = fixed_front_fmt % entries
    fixed_rear = fixed_rear_fmt % entries
    variable = variable_fmt % entries
    return cleanUpTitle(_cut_title(fixed_front, variable, fixed_rear,
                                   MAX_LENGTH=255))


class CustomDataIngestionBot(DataIngestionBot):

    """Overload of DataIngestionBot."""

    def __init__(self, reader, front_titlefmt, rear_titlefmt,
                 variable_titlefmt, pagefmt,
                 site=pywikibot.getSite(u'commons', u'commons')):
        self.reader = reader
        self.front_titlefmt = front_titlefmt
        self.rear_titlefmt = rear_titlefmt
        self.variable_titlefmt = variable_titlefmt
        self.pagefmt = pagefmt
        self.site = site
        #super(self.__class__, self).__init__()

    def _doUpload(self, photo):
        duplicates = photo.findDuplicateImages(self.site)
        if duplicates:
            pywikibot.output(u"Skipping duplicate of %r" % (duplicates, ))
            return duplicates[0]

        title = make_title(photo.metadata, self.front_titlefmt,
                           self.rear_titlefmt, self.variable_titlefmt)

        description = textlib.glue_template_and_params((self.pagefmt,
                                                        photo.metadata))
        print title

        bot = upload.UploadRobot(url = photo.URL,
                                 description = description,
                                 useFilename = title,
                                 keepFilename = True,
                                 verifyDescription = False,
                                 targetSite = self.site)
        bot._contents = photo.downloadPhoto().getvalue()
        bot._retrieved = True
        bot.run()
        return title


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


def cleanUpTitle(title):
    ''' Clean up the title of a potential mediawiki page. Otherwise the title of
    the page might not be allowed by the software.

    '''
    title = title.strip()
    title = re.sub(u"[<{\\[]", u"(", title)
    title = re.sub(u"[>}\\]]", u")", title)
    title = re.sub(u"[ _]?\\(!\\)", u"", title)
    title = re.sub(u",:[ _]", u", ", title)
    title = re.sub(u"[;:][ _]", u", ", title)
    title = re.sub(u"[\t\n ]+", u" ", title)
    title = re.sub(u"[\r\n ]+", u" ", title)
    title = re.sub(u"[\n]+", u"", title)
    title = re.sub(u"[?!]([.\"]|$)", u"\\1", title)
    title = re.sub(u"[&#%?!]", u"^", title)
    title = re.sub(u"[;]", u",", title)
    title = re.sub(u"[/+\\\\:]", u"-", title)
    title = re.sub(u"--+", u"-", title)
    title = re.sub(u",,+", u",", title)
    title = re.sub(u"[-,^]([.]|$)", u"\\1", title)
    title = title.replace(u" ", u"_")
    return title

if __name__ == "__main__":
    main()
