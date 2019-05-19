import threading



class MessageEvent:
    # Constructor
    def __init__(self, whatsapp_reader) -> None:
        self.reader = whatsapp_reader
        self.listeners = []
        self.time_in_seconds = 10
        self.timer_func = self.get_message
        self.timer = None
        super().__init__()

    def add_listener(self, listener):
        self.listeners.append(listener)

    def notify(self, messages):
        for l in self.listeners:
            l(messages)

    def get_message(self):
        message = self.reader.send_message
        length = len(message)
        if length > 0:
            self.notify(message)

    def listening(self):
        self.timer = threading.Timer(self.time_in_seconds, self.timer_func).start()

    def stop(self):
        self.timer.stop()

    def change_timing(self, time):
        self.time_in_seconds = time


