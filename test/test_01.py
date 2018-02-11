import unittest
from httplib2 import Http
import json


class SimpleWidgetTestCase(unittest.TestCase):

    def setUp(self):
        print('setup')

    def tearDown(self):
        print('tear down')

    def test_login(self):
        h = Http(".cache")
        (resp_headers, content) = h.request("http://127.0.0.1:8000/auth/login", "POST")
        print(content)

    def test_real_login(self):
        h = Http(".cache")
        data = { 'id':'vinej', 'email':'jyvinet@hotmail.ca', 'password':'123456'}
        (resp_headers, content) = h.request("http://127.0.0.1:8000/auth/login", "POST", json.dumps(data))
        print(content)

