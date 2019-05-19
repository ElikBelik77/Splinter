import threading
import time
from datetime import datetime

class MessageEvent(object):
    # Constructor
    def __init__(self, whatsapp_reader) -> None:
        super().__init__()

        self.reader = whatsapp_reader
        self.listeners = []
        self.time_in_seconds = 2
        self.timer_func = self.get_message
        self.timer = None
        self.stop = False


    def add_listener(self, listener):
        self.listeners.append(listener)

    def notify(self, messages):
        for l in self.listeners:
            l(messages)

    def get_message(self):
        while True:
            message = self.reader.read("00:00", "🔥PYROX🔥")
            length = len(message)
            if length > 0:
                self.notify(message)
            else:
                print("empty")
            time.sleep(2)

    def start(self):
        self.timer = threading.Timer(self.time_in_seconds, self.timer_func).start()
        # if not self.stop:
        #     self.listening()

    def stop(self):
        self.stop = True

    def change_timing(self, time):
        self.time_in_seconds = time


