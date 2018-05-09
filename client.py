from socketIO_client import SocketIO, BaseNamespace
import GUI
import threading

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
        GUI.set_pokemon(args[0], args[1])
        GUI.labels()


class MultiClient(threading.Thread):
    def __init__(self, pd):
        threading.Thread.__init__(self)
        self.pd = pd

    def run(self):
        print("abc")

        socketIO = SocketIO('http://127.0.0.1', 8080)
        chat_namespace = socketIO.define(Namespace, '/chat')
        chat_namespace.bind(self.pd)
        socketIO.on('reply', chat_namespace.on_reply)
        socketIO.on('request_item', chat_namespace.on_request_response)
        chat_namespace.emit('request_item', {})
        socketIO.wait(seconds=1)

        while True:
            s = input('Send message: ')
            chat_namespace.emit("chat message", s)
            socketIO.wait(seconds=0.1)

if __name__ == '__main__':
    GUI.gui()
    MultiClient(GUI.pd).start()
    GUI.pd.window.mainloop()
