from sanic import (
    Sanic,
    response
)
from websockets.exceptions import ConnectionClosed

from InfoNetPm.chatserver.room_manager import RoomManager


app = Sanic()
# the default room will be create when the first
# client send a message
room_manager = RoomManager()


@app.route("/")
async def test(request):
        return await response.file('./static/index.html')


@app.websocket('/chat')
async def feed(request, ws):
    while True:
        try:
            message = await ws.recv()
        except ConnectionClosed:
            room_manager.leave(ws)
            break
        else:
            await room_manager.manage(ws, message)


if __name__ == "__main__":
    print('running the server...')
    app.run(host="0.0.0.0", port=8000)
