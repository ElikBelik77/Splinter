class Message:
    def __init__(self, sender, content, time, chat_name, ancestor_message):
        self.sender = sender
        self.content = content
        self.time = time
        self.ancestor_message = ancestor_message
        self.chat_name = chat_name
