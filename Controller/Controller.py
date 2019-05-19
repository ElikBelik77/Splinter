import time
import threading
from Controller import UserDialogLogic
from Model import Message
from Model.Selenium import WhatsAppWriter
from Model import WhatsAppModel
from Model import MessageEvent


class Controller:
    def __init__(self, digest_interval, activities):
        self.stop = False
        self.activities = []
        self.digest_interval = digest_interval
        self.last_digest = time.time()
        self.digest_timer = threading.Timer(self.digest_interval, self.interval_function)
        self.user_interaction_parser = UserDialogLogic.UserDialogLogic()
        self.whats_app_writer = WhatsAppWriter.WhatsAppWriter()
        self.whats_app_reader = None
        self.message_event_pusher = MessageEvent.MessageEvent(self.whats_app_reader)
        self.message_event_pusher.add_listener(self.on_message_received)
        self.whats_app_model = WhatsAppModel.WhatsAppModel()
        self.message_filterer = None

    def on_message_received(self, messages):
        parsed_messaged = []
        for message in messages:
            if message.sender == message.group:
                self.user_interaction_parser.handle(message, self.whats_app_writer)
            elif not self.whats_app_model.user_exists(message.sender):
                self.whats_app_model.add_user(message.sender)
            parsed_messaged = Message.Message(self.whats_app_model.get_user(message.sender), message.content,
                                              message.time, message.chat_name, None)

        message_to_filter = [message for message in parsed_messaged if message.sender is not message.chat_name]
        messages_to_bot = [message for message in parsed_messaged if message.sender == message.chat_name]
        for message in messages_to_bot:
            self.user_interaction_parser.handle(message, self.whats_app_writer)

        filtered_message = self.message_filterer.filter(message_to_filter)
        self.whats_app_model.whats_app_storage.push_messages(filtered_message)

    def stop(self):
        self.stop = True

    def interval_function(self):
        start_time = time.time()
        for activity in self.activities:
            activity(self)
        tick_processing_time = start_time - time.time()
        if not self.stop:
            self.digest_timer = threading.Timer(self.digest_interval, self.interval_function)
