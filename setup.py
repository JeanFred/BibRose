#!/usr/bin/env python

from distutils.core import setup

setup(name='BibRose',
    version      = '0.1',
    description  = '',
    py_modules = ['OaiRecordHandling', 'OaiServerTools', 'GeneralProcess', 'CommonsFunctions'],
    author       = 'Jean-Frederic',
    author_email = 'jeanfred@github',
    license      = 'Biopython License',
    install_requires     = ['pyoai', 'pywikipedia'],
    data_files=[('', ['oai_servers.cfg'])],
    )
