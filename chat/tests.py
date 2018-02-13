import unittest

from .room import Room
from .server import app


class Server(unittest.TestCase):
    def test_index_returns_200(self):
        request, response = app.test_client.get('/')
        print(response.status)
        assert response.status == 200


class RoomTest(unittest.TestCase):
    def setUp(self):
        self.room = Room("global")

    def test_join(self):
        self.room.join(1)
        assert len(self.room) == 1

    def test_leave(self):
        self.room.join(1)

        self.room.leave(1)
        assert len(self.room) == 0


if __name__ == '__main__':
    unittest.main()
