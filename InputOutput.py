#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Some Input/Output methods"""

import codecs
import os


def write_set_to_disk(mySet, fileName):
    """Write a given set on disk."""
    print "Writing set to %s" % fileName
    with codecs.open(fileName, 'w', 'utf-8') as f:
        f.write("\n".join(mySet))


def write_dict_as_csv(myDict, name, directory):
    """Write a given dictionary on disk as CSV."""
    print "Writing dict as %s in %s" % (name, directory)
    items = myDict.items()
    items.sort(key=lambda x: x[1], reverse=True)

    def unicode_join_tuple(item):
        return "|".join(map(unicode, item))

    with codecs.open(os.path.join(directory, name + '.csv'), 'w', 'utf-8') as f:
        f.write("\n".join(map(unicode_join_tuple, items)))
