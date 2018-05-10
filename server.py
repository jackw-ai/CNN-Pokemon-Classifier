#pip install python-socketio
#pip install aiohttp
#pip install socketIO-client

from aiohttp import web
import asyncio
import socketio
import random
import multi
import threading
import client
from GUI import random_sprite

class ServerDB:
    #db.scores
    #db.item
    def __init__(self):
        self.scores = {}
        self.started = True

    def start_game(self):
        print("starting game")
        self.update_item()

    def update_item(self):
        self.item = random_sprite()
        #multi.push_event('set_pokemon', db["item"])
        #multi.push_event('labels')
        #GUI.set_pokemon(db["item"][0], db["item"][1])
        #GUI.labels()

    async def send_item(self):
        print("sending item ", self.item)
        await sio.emit('request_item', self.item)

db = ServerDB()

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)
    if db.started:
        db.send_item()


@sio.on('chat message', namespace='/chat')
async def message(sid, data):
    print("message ", data)
    await sio.emit('reply', sid, room=sid)

@sio.on('game_start', namespace='/chat')
async def game_start(sid, data):
    db.start_game()
    db.send_item()

@sio.on('request_item', namespace='/chat')
async def request_item(sid, data):
    db_item = db.item
    if data is not None and data[0] == db_item[0] and data[1] == db_item[1]:
        db.update_item()
        db_item = db.item
    await db.send_item()

#@sio.on('request_item', namespace='/chat')
#data[0]: (boolean) correct
#data[1]: (long) millis
#async def submit_answer(sid, data):

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

#app.router.add_static('/static', 'static')
app.router.add_get('/', index)

class MultiServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        web.run_app(app)

if __name__ == '__main__':
    t = MultiServer()
    t.daemon = True
    t.start()
    client.start_client('127.0.0.1', 8080, True)
