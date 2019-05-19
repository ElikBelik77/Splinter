import time
import threading
from Controller import UserDialogLogic
from Model import Message
from Model.Selenium import WhatsAppWriter
from Model import WhatsAppMessageStorage
class Controller:
    def __init__(self, digest_interval, activities):
        self.stop = False
        self.activities = []
        self.digest_interval = digest_interval
        self.last_digest = time.time()
        self.digest_timer = threading.Timer(self.digest_interval, self.interval_function)
        self.user_interaction_parser = UserDialogLogic.UserDialogLogic()
        self.whats_app_writer = WhatsAppWriter.WhatsAppWriter()
        self.whats_app_message_storage = WhatsAppMessageStorage.WhatsAppMessageStorage()

    def stop(self):
        self.stop = True

    def interval_function(self):
        start_time = time.time()
        for activity in self.activities:
            activity(self)
        tick_processing_time = start_time - time.time()

    def on_message_received(self, messages: Message):
        for message in messages:
            if message.sender == message.group:
                self.user_interaction_parser.handle(message, self.whats_app_writer)
            else:
                self.whats_app_model.do(message)
