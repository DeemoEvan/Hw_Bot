from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
driver = webdriver.Firefox()
driver.get("https://dxjh.teamslite.com.tw/student/dashboard.html?user=A14dxjh_STUDENT_000242")
