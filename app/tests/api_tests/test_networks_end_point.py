import unittest
import json
from app import application


class NetworksTestCase(unittest.TestCase):

    def test_route_api_networks_returns_code_200(self):
        test_client = application.test_client()
        n = test_client.get('/api/networks/')
        self.assertEqual(n.status_code, 200)

    def test_route_api_networks_returns_list(self):
        test_client = application.test_client()
        n = test_client.get('/api/networks/')
        data = json.loads(n.data.decode('utf8'))
        self.assertEqual(type(data), list)