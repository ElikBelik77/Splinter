class WhatsAppMessageStorage():
    def __init__(self):
        self.message_dictionary = {}

    def push_messages(self, messages):
        for message in messages:
            if message.chat_name in self.message_dictionary:
                self.message_dictionary[message.chat_name].append(message)
            else:
                self.message_dictionary[message.chat_name] = [message]

    def get_messages(self):
        return self.message_dictionary

    def clear_messages(self):
        self.message_dictionary.clear()
