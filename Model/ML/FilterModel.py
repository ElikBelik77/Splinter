from .. import Message
from .. import User

class FilterModel:
    def __init__(self, keys_file_name):
        # File name of default key words
        self.keys = keys_file_name

    def filter(self, massages):
        """
        Filter a list of massages

        :param massages: list of Message object
        :return: Filtered list of massages
        """
        important_list = []
        with open(self.keys) as file:
            keys = file.readlines()
            for i, msg in enumerate(massages):
                if self.check_by_keys(msg.content, keys) or self.check_by_rules(msg):
                    important_list.append(massages[i])
        return important_list

    def personalized_filter(self, user, massages):
        """
        Filter a list of massages according to specific user

        :param massages: list of Message object
        :return: Filtered list of massages
        """
        important_list = []
        for i, msg in enumerate(massages):
            if self.check_by_keys(msg.content, user.preferences) or self.check_by_rules(msg):
                important_list.append(massages[i])
        return important_list

    def check_by_keys(self, message, keys):
        """
        Check a single massage by keys
        :param message: a string
        :param keys: a list of string representing key words
        :return: false if spam and true otherwise
        """
        imp = ",.?:!"
        for item in imp:
            message = message.replace(item, " " + item + " ")
        notimp = '/\\;+-()[]"*&^%$#@'
        for item in notimp:
            message = message.replace(item, " ")
        list_message = message.split()
        spam = false
        counter = 0
        for word in list_message:
            for key in keys:
                if word == key:
                    if word == "עזרה" or word == "בבקשה" or word == "?" or word == "אפשר":
                        counter += 2
                        break
                    counter += counter
                    break
        ratio = counter / len(message)
        if len(message) < 5:
            if ratio < 0.5:
                spam = true
        elif len(message) < 20:
            if ratio < 0.4:
                spam = true
        elif len(message) < 30:
            if ratio < 0.3:
                spam = true
        elif len(message) < 40:
            if ratio < 0.2:
                spam = true
        else:
            if ratio < 0.1:
                spam = true
        return not spam

    def check_by_rules(self, massage):
        """
        Check a single massage by rules
        :param massage:
        :return:
        """
        pass
