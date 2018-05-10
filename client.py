from socketIO_client import SocketIO, BaseNamespace
import GUI
import multi
import threading
import sys

class Namespace(BaseNamespace):

    #Pass in a multiclient
    def bind(self, pd):
        self.pd = pd

    def on_connect(self):
        print('[Connected]')

    def on_reconnect(self):
        print('[Reconnected]')

    def on_disconnect(self):
        print('[Disconnected]')

    def on_reply(self, *args):
        print('reply', args)

    def on_request_response(self, *args):
        print('on_request_response', args)
        self.pd.net.last_item = args
        multi.push_event('set_pokemon', args)
        multi.push_event('labels')
        #GUI.set_pokemon(args[0], args[1])
        #GUI.labels()


class MultiClient(threading.Thread):
    def __init__(self, pd, host, port):
        threading.Thread.__init__(self)
        self.pd = pd
        self.pd.hook = self
        self.host = host
        self.port = port

    def run(self):
        print("abc")

        socketIO = SocketIO('http://' + str(self.host), self.port)
        chat_namespace = socketIO.define(Namespace, '/chat')
        chat_namespace.bind(self.pd)
        socketIO.on('reply', chat_namespace.on_reply)
        socketIO.on('request_item', chat_namespace.on_request_response)
        chat_namespace.emit('request_item', None)
        socketIO.wait(seconds=1)

        while True:
            #s = input('Send message: ')
            #chat_namespace.emit("chat message", s)
            #socketIO.wait(seconds=0.1)
            event = self.pd.net.queue.get()
            chat_namespace.emit('request_item', self.pd.net.last_item)
            socketIO.wait(seconds=1)

if __name__ == '__main__':
    GUI.pd.multi = True
    GUI.gui()
    multi.start_event_queue()
    host = '127.0.0.1'
    port = 8080
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])
    t = MultiClient(GUI.pd, host, port)
    t.daemon = True
    t.start()
    GUI.pd.window.mainloop()
