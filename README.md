BibRose
=======

Dealing with an OAI-PMH server, managing metadata, uploading to Wikimedia Commons.

Concepts
--------
* [OAI-PMH](http://www.openarchives.org/OAI/openarchivesprotocol.html)
([Wikipedia](http://en.wikipedia.org/wiki/OAI-PMH))
* ARK ([Wikipedia](http://en.wikipedia.org/wiki/Archival_Resource_Key))

Dependencies
------------
* OAI server handling and record management use
[pyoai](http://pypi.python.org/pypi/pyoai/)
* Upload to Wikimedia Commons use
[Pywikipedia](http://www.mediawiki.org/wiki/Manual:Pywikipediabot) and its
[upload.py](http://www.mediawiki.org/wiki/Manual:Pywikipediabot/upload.py)

Files
-----

* OaiServerTools.py: 
Interface with the OAI-PMH repository
* OaiRecordHandling.py: 
Basic manipulation of OAI records, extraction and transcription.
* CommonsFunctions.py: 
Methods tied to Wikimedia Commons specificities.
* oai_servers.cfg: 
OAI servers information, to be read with
[ConfigParser](http://docs.python.org/library/configparser.html)
* test/test_functions.py: unit tests 
(use [unittest](http://docs.python.org/library/unittest.html)
and [pickle](http://docs.python.org/library/pickle.html))
* setup.py: setuptools installation script