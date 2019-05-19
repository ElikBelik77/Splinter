from Model import WhatsAppMessageStorage
from Model import User
class WhatsAppModel:
    def __init__(self):
        self.users = {}
        self.whats_app_storage = WhatsAppMessageStorage.WhatsAppMessageStorage()

    def add_user(self, user_name):
        if user_name in self.users:
            return
        self.users[user_name] = User.User(user_name)

    def user_exists(self, user_name):
        return user_name in self.users

    def get_messages_for_user(self, username):
        return self.whats_app_storage.message_dictionary[username]

    def get_user(self,user_name):
        return self.users[user_name]