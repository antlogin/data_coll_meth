import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

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

#driver.quit()
