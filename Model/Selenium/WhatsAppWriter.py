from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

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
    def read(self):
        #load the latest html code
        url = self.driver.page_source
        soup = bs(url, 'lxml')
        try:
            gotdiv = soup.find_all("div", {"class": "msg msg-group"})[-1]
        except IndexError:
            gotdiv = 'null'



if __name__ == "__main__":
    bot = WhatsAppWriter("hack")
    bot.open_WhatsApp()
    bot.write("hi")

