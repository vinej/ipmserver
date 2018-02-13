# chatserver/room/auth/views.py

from collections import deque
from websockets import ConnectionClosed


class Room:

    def __init__(self, name):
        self.name = name
        self.clients = []
        self.messages = deque([], 3)

    def join(self, client):
        self.clients.append(client)

    def leave(self, client):
        try:
            self.clients.remove(client)
        except ValueError:
            pass  # already removed

    async def send_client_message(self, client, message):
        try:
            await client.send(f'room {self.name} : {message}')
        except ConnectionClosed:
            self.leave(client)

    async def send_old_messages(self, client, welcome):
        for message in self.messages:
            await self.send_client_message(client, message)
        await self.send_client_message(client, welcome)

    async def send_message(self, message):
        self.messages.append(message)
        for receiver in self.clients:
            try:
                await receiver.send(f'room {self.name} : {message}')
            except ConnectionClosed:
                self.leave(receiver)

    def __len__(self):
        return len(self.clients)


if __name__ == "__main__":
    print('running the server...')
