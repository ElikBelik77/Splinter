from selenium import webdriver

class WhatsAppWriter(object):
    def __init__(self, group_name, driver):
        self.group_name = group_name
        self.driver = driver
    def open_WhatsApp(self):
        self.driver.get("https://web.whatsapp.com/")
        input("click after connected")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    
