from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import os
driver = webdriver.Chrome()


#XPath
login_page_acc_xpath = '//*[@id="username"]/input'
login_page_pwd_xpath = '//*[@id="password"]/input'
login_page_btn_xpath = '//*[@id="app"]/div/div[2]/div/div/div/form/button'

#file path
login_info_path = r"G:\My Drive\SQL1024\TR and M\Hw_Bot\AutoOnlineQ\login.txt"

with open(login_info_path, 'r', encoding='utf-8') as f:
    # 讀取所有行並去掉每行末尾的換行符號 \n
    lines = [line.strip() for line in f.readlines()]

# 分別賦值
if len(lines) >= 2:
    username = lines[0]
    password = lines[1]

    print(f"帳號讀取成功: {username}")
    print(f"密碼讀取成功: {password}")
else:
    print("檔案內容不足兩行，請檢查帳號密碼是否正確。")
driver.get("https://dxjh.teamslite.com.tw/student/dashboard.html?user=A14dxjh_STUDENT_000242")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, login_page_acc_xpath))
)
login_page_acc_input = driver.find_element(By.XPATH,login_page_acc_xpath)
login_page_pwd_input = driver.find_element(By.XPATH,login_page_pwd_xpath)
login_page_btn_btn = driver.find_element(By.XPATH,login_page_btn_xpath)

#type acc
actions = ActionChains(driver)
actions.click(login_page_acc_input)
actions.send_keys(username)
actions.perform()

#type pwd
actions = ActionChains(driver)
actions.click(login_page_pwd_input)
actions.send_keys(password)
actions.perform()

#click login btn
actions = ActionChains(driver)
actions.click(login_page_btn_btn)
actions.perform()

#open correct page
driver.get("https://dxjh.teamslite.com.tw/student/course.html")
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH,'//*[@id="A14dxjh_COURSE_000898"]/a/span[1]'))
)
subject_btn = driver.find_element(By.XPATH,'//*[@id="A14dxjh_COURSE_000898"]/a/span[1]')
actions = ActionChains(driver)
actions.click(subject_btn)
actions.perform()
chooose_btn = driver.find_element(By.XPATH,'//*[@id="A14dxjh_COURSE_000898"]/ul/li[2]/a')