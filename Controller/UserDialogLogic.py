from Model import Message


class UserDialogLogic:
    def __init__(self):
        self.user_dialogs = {}
        pass

    def handle(self, message: Message, whats_app_sender):
        # TODO: if there is time, implement a better dialog system ?
        if message.sender not in self.user_dialogs:
            whats_app_sender.send("Noted ! Hope you have a good time with bot")
            self.user_dialogs[message.sender] = 1
        else:
            whats_app_sender.send("Noted ! Hope you have a good time with bot")
        return message.content.split(',')