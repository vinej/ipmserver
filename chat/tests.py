import unittest

from chat.room import Room


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
