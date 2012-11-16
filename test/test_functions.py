#!/usr/bin/env python
# -*- coding: latin-1 -*-

import unittest
import pickle
from os.path import join, dirname
from OaiRecordHandling import *
from CommonsFunctions import *


class TestFunctions(unittest.TestCase):
    """Testing some functions defined in OaiRecordHandling"""
    @classmethod
    def setUpClass(cls):
        """Retrieve the OAI records from disk by deserialiazation"""
        record_files = ['B315556101_TRUB1035', 'B315556101_A_JACOTTET_2_026']
        func = lambda x: pickle.load(open(join(dirname(__file__), 'data', x)))
        cls.records = map(func, record_files)

    def test_get_file_URL(self):
        """Test get_file_URL, which returns the URL associated with a record"""
        expected_result = [u'http://numerique.bibliotheque.toulouse.fr/collect'
        '/general/index/assoc//ark:/74899/B315556101_TRUB1035.dir/B0001035.jpg',
        'http://numerique.bibliotheque.toulouse.fr/collect/general/index/assoc//'
        'ark:/74899/B315556101_A_JACOTTET_2_026.dir/B315556101_A_JACOTTET_2_026.jpg']
        self.assertListEqual(expected_result, map(get_file_URL, self.records))

    def test_retrieve_bare_ID(self):
        """Test retrieve_bare_ID, which returns the ID from a record"""
        expected_result = ['B315556101_TRUB1035',
                           'B315556101_A_JACOTTET_2_026']
        self.assertListEqual(expected_result,
                             map(retrieve_bare_ID, self.records))

    def test_is_Trutat(self):
        """Test is_Trutat"""
        expected_result = [True, False]
        self.assertListEqual(expected_result,
                             map(is_Trutat, self.records))

    def test_retrieve_ARK(self):
        """Test retrieve_ARK"""
        expected_result = ['ark:/74899/B315556101_TRUB1035',
                           'ark:/74899/B315556101_A_JACOTTET_2_026']
        self.assertListEqual(expected_result,
                             map(retrieve_ARK, self.records))

    def test_retrieve_title(self):
        """Test retrieve_title"""
        expected_result = ['Le Boulou, cours du Tech',
                    u'Entr\xe9e des Eaux Bonnes (Basses Pyr\xe9n\xe9es)']
        self.assertListEqual(expected_result,
                             map(retrieve_title, self.records))

    def test_build_Commons_title(self):
        """Test build_Commons_title"""
        expected_result = ['Le Boulou, cours du Tech - Fonds Trutat',
        u'Entr\xe9e des Eaux Bonnes (Basses Pyr\xe9n\xe9es) - Fonds Trutat']
        self.assertListEqual(expected_result,
                             map(build_Commons_title, self.records))

    def test_make_categories(self):
        """Test make_categories"""
        data = [['A'], ['A', 'B'], ['A', 'B', 'C'], [], ['É', 'È']]
        expected_result = ['[[Category:A]]', '[[Category:A]]\n[[Category:B]]',
                           '[[Category:A]]\n[[Category:B]]\n[[Category:C]]',
                           '', '[[Category:É]]\n[[Category:È]]']
        self.assertListEqual(expected_result,
                             map(make_categories, data))


if __name__ == "__main__":
    unittest.main()
