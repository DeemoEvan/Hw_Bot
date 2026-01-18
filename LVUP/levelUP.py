from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import random
import time
def human_type(element, text):
    """模擬真人逐字輸入"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

driver = webdriver.Firefox()
driver.get("https://discord.com/channels/1446838276249096228/1447184848841080903")
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div/div[1]/div/div/div/section/div[2]/div[3]/button/span').click()
time.sleep(2)
human_type(driver.find_element(By.XPATH, '//*[@id="uid_15"]'), '')
human_type(driver.find_element(By.XPATH, '//*[@id="uid_17"]'), '')
driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/div[4]/button/div').click()
time.sleep(6)
# driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div/div[1]/div/div[2]/div/div/div/div[2]/div[1]/nav/ul/div/div/div[4]/div[1]/span[1]/div/div/svg').click()
# driver.find_element(By.XPATH, '//*[@id="channels"]/ul/li[13]/div/div[2]/a/div/div[2]').click()
input_box = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="textbox"]'))
)
input_box.click()
for i in range(10):
    human_type(input_box, '滴某不是南娘 大家接受現實吧')
    input_box.send_keys(Keys.ENTER)
    time.sleep(2)



