import unittest
import json
from app import application


class CountryViewTestCase(unittest.TestCase):

    def test_if_returns_code_200(self):
        test_client = application.test_client()
        n = test_client.get('/api/countries/')
        self.assertEqual(n.status_code, 200)

    def test_returns_list(self):
        test_client = application.test_client()
        n = test_client.get('/api/countries/')
        data = json.loads(n.data.decode('utf8'))
        self.assertEqual(type(data), list)