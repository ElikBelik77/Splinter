from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import re

class WhatsAppWriter(object):
    def __init__(self, group_name):
        self.group_name = group_name
    def open_WhatsApp(self):
        self.driver = webdriver.Chrome(executable_path=r"../chromedriver")
        self.driver.get("https://web.whatsapp.com/")
        input("click after connected")
    def write(self, msg):
        user = self.driver.find_element_by_xpath('//span[@title = "%s"]'%self.group_name)
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
    def read(self, since):
        user = self.driver.find_element_by_xpath('//span[@title = "%s"]' % self.group_name)
        user.click()
        url = self.driver.page_source
        soup = bs(url, "lxml")
        i = 0
        permission = 0
        msg = []
        # for s in soup.strings:
        #     if (s == self.group_name):
        #         i+=1
        #     if (i == 3):
        #         pattern = re.compile("\d\d:\d\d")
        #         if(pattern.match(s)):
        #             if (self.compareTimes(s, since) == 0 or self.compareTimes(s, since) == 1):
        #                 permission = 1
        #     if (permission):
        #         if(pattern.match(s)):
        #             msg.append([prev, s])
        #     if (i == 2):
        #         i+=1
        #     print(s)
        #     prev = s
        soupp = list(soup.strings)
        pattern1 = re.compile("\d\d:\d\d")
        pattern2 = re.compile("[+]\d\d\d \d\d-\d\d\d-\d\d\d\d")
        next = 0
        user = []
        msg = []
        for s in reversed(soupp):
            if (s == self.group_name):
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


        return msg












if __name__ == "__main__":
    bot = WhatsAppWriter("hack")
    bot.open_WhatsApp()
    #bot.write("hi")
    l = bot.read("15:55")
    print(l)

