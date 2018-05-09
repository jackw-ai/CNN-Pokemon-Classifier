from socketIO_client import SocketIO, BaseNamespace

class Namespace(BaseNamespace):

    def on_connect(self):
        print('[Connected]')

    def on_reconnect(self):
        print('[Reconnected]')

    def on_disconnect(self):
        print('[Disconnected]')

socketIO = SocketIO('http://127.0.0.1', 8080)
chat_namespace = socketIO.define(Namespace, '/chat')


while True:
    s = input('Send message: ')
    chat_namespace.emit("chat message", s)
