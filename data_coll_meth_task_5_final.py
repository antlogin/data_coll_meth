import time
import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['mail_database']
letters_Mongo = db.letters_collection

driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get('https://mail.ru')

elem = driver.find_element(By.XPATH, "//input[contains(@name,'login')]")
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)
time.sleep(5)
elem = driver.find_element(By.XPATH, "//input[contains(@name,'password')]")
elem.send_keys('NextPassword172#')
elem.send_keys(Keys.ENTER)
time.sleep(5)

# Открываем верхнее письмо
link = driver.find_element(By.XPATH, "//div[@class='dataset__items']/a[1]").get_attribute('href')
driver.get(link)

end_handle = True
i=0
while end_handle:
    try:
# проверяем не пустое ли открытое письмо, если пустое - прекращаем перебор
        next_mail = driver.find_element(By.CLASS_NAME, "dataset__empty")
        end_handle = False;
    except:
        letter_author = driver.find_element(By.XPATH, "//div[@class='letter__author']/span").get_attribute('title')
        subject = driver.find_element(By.XPATH, "//div[@class='thread__subject-line']/h2").text
        date = driver.find_element(By.XPATH, "//div[@class='letter__date']").text
        content = driver.find_element(By.XPATH, "//div[@class='letter-body']").text
# открываем следующее письмо "кликнув" на кнопку
        elem = driver.find_element(By.XPATH, "//div[@class='portal-menu__group']/div[2]")
        ac = ActionChains(driver)
        ac.click(elem).perform()
        letters_Mongo.append([{'letter_author': letter_author, 'subject': subject, 'date': date,
                                   'content': content}], ignore_index=True)
#driver.quit()
