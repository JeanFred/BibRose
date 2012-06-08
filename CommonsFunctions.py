#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Methods tied to Commons specificities
"""
__authors__ = 'User:Jean-Frédéric'

from OaiRecordHandling import retrieve_title


def build_Commons_title(record):
    """Builds the file title for Wikimedia Commons for the given record

    The naming convention is: "<Title> - Fonds Trutat.jpg"
    """
    recordTitle = record[1]['title'][0]
    return "%s - Fonds Trutat" % retrieve_title(record)
