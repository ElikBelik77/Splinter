# from .. import Message
# from .. import User
import codecs
import re
from itertools import groupby


def diff(f, s):
    return editDistance(f,s,len(f),len(s)) < 3

# A Naive recursive Python program to fin minimum number
# operations to convert str1 to str2
def editDistance(str1, str2, m, n):
    # If first string is empty, the only option is to
    # insert all characters of second string into first
    if m == 0:
        return n

        # If second string is empty, the only option is to
    # remove all characters of first string
    if n == 0:
        return m

        # If last characters of two strings are same, nothing
    # much to do. Ignore last characters and get count for
    # remaining strings.
    if str1[m - 1] == str2[n - 1]:
        return editDistance(str1, str2, m - 1, n - 1)

        # If last characters are not same, consider all three
    # operations on last character of first string, recursively
    # compute minimum cost for all three operations and take
    # minimum of three values.
    return 1 + min(editDistance(str1, str2, m, n - 1),  # Insert
                   editDistance(str1, str2, m - 1, n),  # Remove
                   editDistance(str1, str2, m - 1, n - 1)  # Replace
                   )


class FilterModel:
    def __init__(self, keys_file_name="good_words_list"):
        # File name of default key words
        self.keys = keys_file_name

    def filter(self, messages):
        """
        Filter a list of messages

        :param messages: list of Message object
        :return: Filtered list of messages
        """
        important_list = []
        with open(self.keys) as file:
            keys = file.readlines()
            for i, msg in enumerate(messages):
                if self.check_by_keys(msg.content, keys) and self.check_by_rules(msg):
                    important_list.append(messages[i])
        return important_list

    def personalized_filter(self, user, messages):
        """
        Filter a list of messages according to specific user

        :param user: User object
        :param messages: list of Message object
        :return: Filtered list of messages
        """
        important_list = []
        for i, msg in enumerate(messages):
            if self.check_by_keys(msg.content, user.preferences) and self.check_by_rules(msg):
                important_list.append(messages[i])
        return important_list

    def check_by_keys(self, message, keys):
        """
        Check a single message by keys
        :param message: a string
        :param keys: a list of strings representing key words
        :return: false if spam and true otherwise
        """
        imp = ",.?:!"
        for item in imp:
            message = message.replace(item, " " + item + " ")
        notimp = '/\\;+-()[]{}"*&^%$#@'
        for item in notimp:
            message = message.replace(item, " ")
        list_message = message.split()
        spam = False
        counter = 0
        for word in list_message:
            for key in keys:
                if diff(word, key):
                    if diff(word, "עזרה") or diff(word, "בבקשה") or diff(word, "?") or diff(word, "אפשר") or diff(word, "דחיה") or diff(word, "הארכה"):
                        counter += 2
                        break
                    counter += 1
                    break
        ratio = counter / len(list_message)
        if len(list_message) < 5:
            if len(list_message) < 2:
                spam = True
            elif ratio < 0.45:
                spam = True
        elif len(list_message) < 20:
            if ratio < 0.35:
                spam = True
        elif len(list_message) < 30:
            if ratio < 0.25:
                spam = True
        elif len(list_message) < 40:
            if ratio < 0.15:
                spam = True
        else:
            if ratio < 0.1:
                spam = True
        return not spam

    def check_by_rules(self, message):
        """
        Check a single message by rules
        :param message:
        :return:
        """
        if len(message) < 2 or len(message.split()) < 2:
            return False
        if len(re.findall("\d\.\d", message)) > 0 or len(re.findall("\d/\d", message)):
            return True
        four_or_more = (char for char, group in groupby(message)
                         if sum(1 for _ in group) >= 4)
        if any(four_or_more):
            return False
        for item in re.findall(".:.", message):
            if item[0] in "&()–[{}]:;',?/*^><" or item[-1] in "&()–[{}]:;',?/*^><":
                return False
        if len(re.findall(",", message)) > 3:
            return True
        return False

    def testing(self):
        f = codecs.open("test_messages", encoding='utf-8', mode='r')
        lines = f.readlines()
        h = codecs.open("good_words_list", encoding='utf-8', mode='r')
        keys = h.readlines()
        for l in lines:
            val = self.check_by_keys(l, keys) or self.check_by_rules(l)
            print(val, "   :", l)




t = FilterModel()

t.testing()
