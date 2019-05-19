

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
        res = self.filter_by_keys(massages) + self.filter_by_rules(massages)
        return []

    def personalized_filter(self, user, massages):
        """
        Filter a list of massages according to specific user

        :param massages: list of Message object
        :return: Filtered list of massages
        """
        res = self.filter_by_rules(massages)
        return []

    def filter_by_keys(self, massages):
        pass

    def filter_by_rules(self, massages):
        pass
