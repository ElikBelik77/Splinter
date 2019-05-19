from Model import Message


class UserDialogLogic:
    def __init__(self):
        self.user_dialogs = {}
        pass

    def handle(self, message: Message, whats_app_sender):
        # TODO: if there is time, implement a better dialog system ?
        if message.content.find("groups:"):
            message.user.preferred_groups = message.content[7:].split(',')
        elif message.content.find("words:"):
            message.user.preferences = message.content[6:].split(',')
