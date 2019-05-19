from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs



class WhatsAppWriter(object):
    def __init__(self, group_name):
        self.group_name = group_name

    def open_WhatsApp(self):
        self.driver = webdriver.Chrome(executable_path=r"../chromedriver.exe")
        self.driver.get("https://web.whatsapp.com/")
        delay = 10  # seconds
        try:
            myElem = WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'legal-attribute-row')))
        except:
            print("Loading took too much time!")
        input("click after connected")

    def write(self, msg):
        user = self.driver.find_element_by_xpath('//span[@title = "%s"]' % self.group_name)
        user.click()
        inp_xpath = "//div[@contenteditable='true']"
        input_box = self.driver.find_element_by_xpath(inp_xpath)
        input_box.send_keys(msg)
        input_box.send_keys(Keys.ENTER)

    def read(self):
        user = self.driver.find_element_by_xpath('//span[@title = "%s"]' % self.group_name)
        user.click()
        # load the latest html code
        url = self.driver.page_source
        print(self.driver.page_source)
        html = self.driver.execute_script("return document.documentElement.innerHTML;")
        print(html)
        soup = bs(url, 'lxml')
        try:
            gotdiv = soup.find_all("div", {"class": "msg msg-group"})[-1]
        except IndexError:
            gotdiv = 'null'
        #print(soup.prettify())
        #soup[]


if __name__ == "__main__":
    bot = WhatsAppWriter("hack")
    bot.open_WhatsApp()
    bot.read()
   # bot.write("hi")
