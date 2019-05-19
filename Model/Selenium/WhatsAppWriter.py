from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import re
from Model import Message

class WhatsAppWriter(object):
    def __init__(self,driver_path):
        self.driver_path = driver_path

    def read_contact(self):
        url = self.driver.page_source
        soup = bs(url, "lxml")

        soupp = list(soup.strings)
        pattern1 = re.compile("[+]\d\d\d \d\d-\d\d\d-\d\d\d\d")
        pattern2 = re.compile("\d\d:\d\d")

        clients = []
        prev = ""
        for s in soupp:
            if (prev != ""):
                if (pattern2.match(s)):
                    if (pattern1.search(prev)):
                        prev = prev[1:-1]
                    if (prev not in clients):
                        clients.append(prev)

            prev = s
        self.clients = clients


    def open_WhatsApp(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.driver.get("https://web.whatsapp.com/")
        self.driver.add_cookie({'name': 'wa_ul', 'value': '351a3843-72fa-1a71-5f08-dc35c6f010ca'})
        input("click after connected")


    def get_contact(self):

        self.driver.get("http://www.google.com/")

        # open tab
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        # You can use (Keys.CONTROL + 't') on other OSs

        # Load a page
        self.driver.get("https://web.whatsapp.com/")
        # Make the tests...

        # close the tab
        # (Keys.CONTROL + 'w') on other OSs.
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
        return self.read_contact()

    def write(self, msg, name):
        user = self.driver.find_element_by_xpath('//span[@title = "%s"]' % name)
        user.click()
        inp_xpath = "//div[@contenteditable='true']"
        input_box = self.driver.find_element_by_xpath(inp_xpath)
        input_box.send_keys(msg)
        input_box.send_keys(Keys.ENTER)

    def compareTimes(self, one, two):
        one_l = one.split(':')
        two_l = two.split(':')
        if (int(one_l[0]) == int(two_l[0]) and int(one_l[1]) == int(two_l[1])):
            return 0
        if (int(one_l[0]) > int(two_l[0])):
            return 1
        if (int(two_l[0]) > int(one_l[0])):
            return 2
        if (int(one_l[1]) > int(two_l[1])):
            return 1
        return 2

    def read(self, since, name):
        user = self.driver.find_element_by_xpath('//span[@title = "%s"]' % name)
        user.click()
        url = self.driver.page_source
        soup = bs(url, "lxml")

        soupp = list(soup.strings)
        pattern1 = re.compile("\d\d:\d\d")
        pattern2 = re.compile("[+]\d\d\d \d\d-\d\d\d-\d\d\d\d")
        next = 0
        user = []
        msg = []
        for s in reversed(soupp):
            if (s == name):
                break

            if (next):
                user.append(s)
                next = 0

            if (pattern1.match(s)):
                if (self.compareTimes(s, since) == 0 or self.compareTimes(s, since) == 1):
                    user.append(s)
                    next = 1

            if (pattern2.match(s)):
                if (user != []):
                    user.append(s)
                msg.append(user)

                user = []
        non_empty_messages = [x for x in msg if len(x)!=0]
        for x in non_empty_messages:
            x.reverse()
        return self.format_messages(non_empty_messages, name)


    def format_messages(self, messages, group_name):
        formatted_messages = []
        for i in range(0,len(messages)):
            j = 1
            while j < len(messages[i]):
                if i == 0 and j >= len(messages[i]) - 2:
                    break
                formatted_messages.append(Message.Message(messages[i][0],messages[i][j],messages[i][j+1],group_name,None))
                j += 2
        return formatted_messages


if __name__ == "__main__":
    bot = WhatsAppWriter(r"../chromedriver")
    bot.open_WhatsApp()
    # print(bot.clients)
    bot.get_contact()
    # bot.write("hi")
    #l = bot.read("15:55", "hack")
    #print(l)
