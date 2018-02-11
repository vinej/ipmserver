import unittest
from httplib2 import Http
import json

root = "http://127.0.0.1:8000"


class AuthTestCase(unittest.TestCase):

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

    def test_resister(self):
        data = {'email': 'jyvinet2@hotmail.ca', 'password': '123456'}
        (resp_headers, content) = self.h.request(root+"/auth/register", "POST",
                                                 headers=self.headers, body=json.dumps(data))
        body = json.loads(content)
        self.assertTrue(resp_headers.status == 201)
        self.assertTrue('auth_token' in body)

    def test_login(self):
        data = {'email': 'jyvinet2@hotmail.ca', 'password': '123456'}
        self.h.request(root + "/auth/register", "POST", headers=self.headers, body=json.dumps(data))

        data = {'email': 'jyvinet2@hotmail.ca', 'password': '123456'}
        (resp_headers, content) = self.h.request(root+"/auth/login", "POST",
                                                 headers=self.headers, body=json.dumps(data))
        body = json.loads(content)
        self.assertTrue(resp_headers.status == 200)
        self.assertTrue('auth_token' in body)

    def test_logout(self):
        data = {'email': 'jyvinet2@hotmail.ca', 'password': '123456'}
        self.h.request(root + "/auth/register", "POST", headers=self.headers, body=json.dumps(data))

        (resp_headers, content) = self.h.request(root+"/auth/login", "POST",
                                                 headers=self.headers, body=json.dumps(data))
        body = json.loads(content)
        self.headers["Authorization"] = "Bearer " + body["auth_token"]

        (resp_headers, content) = self.h.request(root+"/auth/logout", "POST", headers=self.headers)
        self.assertTrue(resp_headers.status == 200)
