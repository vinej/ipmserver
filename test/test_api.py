import unittest
from httplib2 import Http
import json

root = "http://127.0.0.1:8000"


class ApiTestCase(unittest.TestCase):

    def __init__(self, name):
        print('doing ...' + name)
        unittest.TestCase.__init__(self, name)
        self.h = None
        self.headers = None

    def setUp(self):
        self.h = Http()
        self.headers = {'connection': 'close'}

    def tearDown(self):
        self.h.request(root+"/admin/drop_users", "GET", headers=self.headers)

    def test_api_no_token(self):
        (resp_headers, content) = self.h.request(root + "/api/companies", "GET", headers=self.headers)
        self.assertTrue(resp_headers.status == 401)

    def test_api_with_token(self):
        data = {'email': 'jyvinet2@hotmail.ca', 'password': '123456'}
        (resp_headers, content) = self.h.request(root + "/auth/register", "POST",
                                                 headers=self.headers, body=json.dumps(data))

        body = json.loads(content)

        self.headers["Authorization"] = "Bearer " + body["auth_token"]
        (resp_headers, content) = self.h.request(root + "/api/companies", "GET", headers=self.headers)
        self.assertTrue(resp_headers.status != 200)
