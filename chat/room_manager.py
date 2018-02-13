
from uuid import uuid4
from InfoNetPm.chatserver.room import Room


class RoomManager:
    """
    one room by client
    By default the client is added to the global room
    """
    DEFAULT_ROOL = 'global'
    JOIN = '/join'

    def __init__(self):
        self.rooms = {}
        self.client_room = {}

    def get_room(self, client):
        if client.id in self.client_room:
            return self.client_room[client.id]
        else:
            return self.join(RoomManager.DEFAULT_ROOL, client)

    def join(self, name, client):
        if name in self.rooms:
            room = self.rooms[name]
        else:
            room = self.rooms[name] = Room(name)

        room.join(client)
        self.client_room[client.id] = room
        return room

    async def manage(self, client, message):
        print(message)
        if not hasattr(client, 'id'):
            client.id = uuid4()

        if message[0] == '/':
            await self.execute(client, message)
        else:
            room = self.get_room(client)
            await room.send_message(message)

    def leave(self, client):
        if hasattr(client, 'id'):
            if client.id in self.client_room:
                self.client_room[client.id].leave(client)

    async def execute(self, client, message):
        cmd = message.split(' ')
        if cmd[0] == '/join':
            name = cmd[1]
            if client.id in self.client_room:
                room = self.client_room[client.id]
                room.leave(client)

            room = self.join(name, client)
            self.client_room[client.id] = room
            await room.send_old_messages(client, 'new client added: ' + str(client.id))
            return

        if cmd[0] == '/list':
            room = self.get_room(client)
            new_message = ','.join([r.name for r in list(self.rooms.values())])
            await room.send_message(new_message)

        if cmd[0] == '/leave':
            if client.id in self.client_room:
                room = self.client_room[client.id]
                room.leave(client)
