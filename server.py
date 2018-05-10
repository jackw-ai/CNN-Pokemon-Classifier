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
import operator
from GUI import random_sprite

class ServerDB:
    #db.scores
    #db.item
    def __init__(self):
        self.round_num = 0
        self.game_round = {}
        self.scores = {}
        self.started = False
        self.sleep_time = 5

    def start_game(self):
        print("starting game")
        self.update_item()
        self.started = True

    def update_item(self):
        self.round_num += 1
        (a, b) = random_sprite()
        self.item = (self.round_num, a, b, self.sleep_time * 1000)

    async def send_item(self):
        print("sending item ", self.item)
        await sio.emit('request_item', self.item)

    async def countdown_loop(self):
        print('starting countdown loop')
        while True:
            await self.countdown()

    async def countdown(self):
        print('starting countdown')
        self.game_round = {}
        await asyncio.sleep(self.sleep_time)
        min_key = None
        min_millis = None
        for key in self.game_round:
            (correct, millis) = self.game_round[key]
            update_min = False
            if correct:
                if min_key == None:
                    update_min = True
                elif millis < min_millis:
                    update_min = True
            if update_min:
                min_key = key
                min_millis = millis
        if min_key is not None:
            self.scores[min_key] += 1
        for key in self.scores:
            scores = {}
            high = max([val for kx, val in self.scores.items() if kx != key], default = 0)
            scores["high"] = high
            scores["self"] = self.scores[key]
            await sio.emit('update_score', scores, room=key)
        self.update_item()
        await self.send_item()

    def submit_answer(self, sid, round_num, correct, millis):
        if round_num == self.round_num and sid not in self.game_round:
            self.game_round[sid] = (correct, millis)

db = ServerDB()

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('connect', namespace='/chat')
async def connect(sid, environ):
    print("connect ", sid)
    db.scores[sid] = 0
    #if db.started:
    #    await db.send_item()


@sio.on('chat message', namespace='/chat')
async def message(sid, data):
    print("message ", data)
    await sio.emit('reply', sid, room=sid)

@sio.on('game_start', namespace='/chat')
async def game_start(sid, data):
    db.start_game()
    #await db.send_item()

#@sio.on('request_item', namespace='/chat')
#async def request_item(sid, data):
#    pass
    #db_item = db.item
    #if data is not None and data[0] == db_item[0] and data[1] == db_item[1]:
    #    db.update_item()
    #    db_item = db.item
    #await db.send_item()

@sio.on('submit_answer', namespace='/chat')
async def submit_answer(sid, data):
    try:
        print('submit ', data)
        round_num = int(data[0])
        correct = data[1]
        millis = int(data[2])
        db.submit_answer(sid, round_num, correct, millis)
    except ValueError:
        print('invalid submission')

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

#app.router.add_static('/static', 'static')
app.router.add_get('/', index)

class MultiWebApp(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.ensure_future(db.countdown_loop())
        web.run_app(app)

if __name__ == '__main__':
    t = MultiWebApp()
    t.daemon = True
    t.start()
    client.start_client('127.0.0.1', 8080, True)
