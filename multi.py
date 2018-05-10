import GUI
from queue import Queue

def start_event_queue():
    GUI.pd.net.event_queue = Queue()
    event_queue()

def event_queue():
    process_event()
    GUI.pd.window.after(200, event_queue)

def process_event():
    while not GUI.pd.net.event_queue.empty():
        event = GUI.pd.net.event_queue.get()
        method = getattr(GUI, event.name)
        method(*event.args)

class GUIEvent:
    def __init__(self, name, args):
        self.name = name
        self.args = args

def push_event(name, args=[]):
    GUI.pd.net.event_queue.put(GUIEvent(name, args))
