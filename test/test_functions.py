import unittest
import pickle
from os.path import join, dirname
from OaiRecordHandling import *
from CommonsFunctions import *

class TestFunctions(unittest.TestCase):
    """Testing some functions defined in OaiRecordHandling"""
    @classmethod
    def setUpClass(cls):
        """Retrieve the OAI record from disk by deserialiazation"""
        record_file = join(dirname(__file__), 'data', 'B315556101_TRUB1035')
        cls.record = pickle.load(open(record_file, 'r'))

    def test_get_file_URL(self):
        """Test get_file_URL, which returns the URL associated with a record"""
        expected_result = u'http://numerique.bibliotheque.toulouse.fr/\
collect/general/index/assoc//ark:/74899/B315556101_TRUB1035.dir/B0001035.jpg'
        self.assertEquals(get_file_URL(self.record), expected_result)

    def test_retrieve_bare_ID(self):
        """Test retrieve_bare_ID, which returns the ID from a record"""
        expected_result = 'B315556101_TRUB1035'
        self.assertEquals(retrieve_bare_ID(self.record), expected_result)

    def test_is_Trutat(self):
        """Test is_Trutat"""
        self.assertTrue(is_Trutat(self.record))

    def test_retrieve_ARK(self):
        """Test retrieve_ARK"""
        expected_result = 'ark:/74899/B315556101_TRUB1035'
        self.assertEquals(retrieve_ARK(self.record), expected_result)
        
    def test_retrieve_title(self):
        """Test retrieve_title"""
        expected_result = 'Le Boulou, cours du Tech'
        self.assertEquals(retrieve_title(self.record), expected_result)

    def test_build_Commons_title(self):
        """Test build_Commons_title"""
        expected_result = 'Le Boulou, cours du Tech - Fonds Trutat'
        self.assertEquals(build_Commons_title(self.record), expected_result)
