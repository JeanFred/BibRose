#!/usr/bin/env python

from setuptools import setup
#from distutils.core import setup

setup(name='BibRose',
    version      = '0.1',
    description  = '',
    py_modules = ['OaiRecordHandling', 'OaiServerTools', 'GeneralProcess', 'CommonsFunctions'],
    author       = 'Jean-Frederic',
    author_email = 'jeanfred@github',
    license      = 'GPL',
    install_requires     = ['pyoai'],
    data_files=[('', ['oai_servers.cfg'])],
    )
