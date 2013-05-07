#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Methods tied to Commons specificities."""

__authors__ = 'User:Jean-Frédéric'


def build_Commons_title(record):
    """Build the file title for Wikimedia Commons for the given record.

    The naming convention is: "<Title> - Fonds Trutat.jpg"

    """

    return "%s - Fonds Ancely - %s" % (record.metadata['title'][0].strip(),
                                       record.retrieve_bare_ID())

def make_categories(categories):
    """Build the wikitext for a given list of category names."""
    return "\n".join(["[[Category:%s]]" % x for x in categories])
