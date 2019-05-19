import time
import threading
from Model import Message
from Model.Selenium import WhatsAppWriter
from Controller import UserDialogLogic
from Model import WhatsAppModel
from Model import MessageEvent
from Model.ML import FilterModel
from Controller.Activities import WhatsAppDigest


class Controller:
    def __init__(self, digest_interval, activities):
        self.stop = False
        self.activities = []
        self.digest_interval = digest_interval
        self.last_digest = time.time()
        self.digest_timer = threading.Timer(self.digest_interval, self.interval_function)
        self.user_interaction_parser = UserDialogLogic.UserDialogLogic()
        self.whats_app_writer = WhatsAppWriter.WhatsAppWriter(r"../Model/chromedriver.exe")
        self.whats_app_reader = self.whats_app_writer
        self.message_event_pusher = MessageEvent.MessageEvent(self.whats_app_reader)
        self.message_event_pusher.add_listener(self.on_message_received)
        self.whats_app_model = WhatsAppModel.WhatsAppModel()
        self.message_filterer = FilterModel.FilterModel(r"../Model/ML/good_words_list")

    def start(self):
        self.digest_timer.start()
        self.whats_app_reader.open_WhatsApp()
        self.message_event_pusher.start()

    def on_message_received(self, messages):
        parsed_messaged = []
        for message in messages:
            if message.sender == message.chat_name:
                self.user_interaction_parser.handle(message, self.whats_app_writer)
            elif not self.whats_app_model.user_exists(message.sender):
                self.whats_app_model.add_user(message.sender)
            parsed_messaged.append(Message.Message(self.whats_app_model.get_user(message.sender), message.content,
                                                   message.time, message.chat_name, None))

        message_to_filter = [message for message in parsed_messaged if message.sender is not message.chat_name]
        messages_to_bot = [message for message in parsed_messaged if message.sender == message.chat_name]
        for x in message_to_filter:
            print(x.sender, 'says', x.content)
        print(message_to_filter)
        print(messages_to_bot)
        for message in messages_to_bot:
            self.user_interaction_parser.handle(message, self.whats_app_writer)

        filtered_message = self.message_filterer.filter(message_to_filter)
        with open("post_fix/data1.csv",'w',encoding='utf-8') as f:
            for x in filtered_message:
                f.write(x.content + ',1\n')
            for x in message_to_filter:
                if x not in filtered_message:
                    f.write(x.content + ',0\n')
        self.whats_app_model.whats_app_storage.push_messages(filtered_message)

    def stop(self):
        self.stop = True

    def interval_function(self):
        start_time = time.time()
        for activity in self.activities:
            activity.execute(self)
        tick_processing_time = start_time - time.time()
        if not self.stop:
            self.digest_timer = threading.Timer(self.digest_interval, self.interval_function)


c = Controller(20, [WhatsAppDigest.WhatsAppDigest()])
c.start()
