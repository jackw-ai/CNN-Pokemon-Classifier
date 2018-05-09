#pip install python-socketio
#pip install aiohttp
#pip install socketIO-client

from aiohttp import web
import asyncio
import socketio
import random
import GUI
import threading

db = {}

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

def update_item():
    db["item"] = GUI.random_sprite()
    GUI.set_pokemon(db["item"][0], db["item"][1])
    GUI.labels()

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('chat message', namespace='/chat')
async def message(sid, data):
    print("message ", data)
    await sio.emit('reply', sid, room=sid)

@sio.on('request_item', namespace='/chat')
async def request_item(sid, data):
    if "item" not in db:
        update_item()
    db_item = db["item"]
    if data is not None and data[0] == db_item[0] and data[1] == db_item[1]:
        update_item()
    db_item = db["item"]
    print("sending item ", db_item)
    await sio.emit('request_item', db_item, room=sid)

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

#app.router.add_static('/static', 'static')
app.router.add_get('/', index)

class MultiServer(threading.Thread):
    def __init__(self, pd):
        threading.Thread.__init__(self)
        self.pd = pd

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        web.run_app(app)

if __name__ == '__main__':
    GUI.gui()
    t = MultiServer(GUI.pd)
    t.daemon = True
    t.start()
    GUI.pd.window.mainloop()
