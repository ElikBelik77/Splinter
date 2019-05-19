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

    def check_by_keys(self, massage, keys):
        """
        Check a single massage by keys
        :param massage:
        :param keys:
        :return:
        """
        pass

    def check_by_rules(self, massage):
        """
        Check a single massage by rules
        :param massage:
        :return:
        """
        pass
