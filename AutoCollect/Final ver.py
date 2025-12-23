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
import sys
import os
import shutil
from datetime import datetime, timedelta
from tqdm import tqdm

# 強制設定標準輸出為 UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# --- 設定區 ---
PROFILE_PATH = r""
DRIVER_PATH = r""
LOGIN_INFO_PATH = r""  # 儲存帳號密碼的檔案路徑
# 目標頻道網址
TARGET_URL = "https://discord.com/channels/1446838276249096228/1447604334845235261"

shutil.rmtree(PROFILE_PATH)
os.makedirs(PROFILE_PATH)

def human_type(element, text):
    """模擬真人逐字輸入"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

def login(driver):
    print("正在執行登入流程...")
    try:
        # 1. 處理「在瀏覽器中繼續」按鈕 (攔截頁面)
        try:
            print("嘗試尋找『在瀏覽器中繼續』按鈕...")
            # 透過尋找包含該文字的 span，並定位到它的父層 button
            continue_btn_xpath = "//button[.//span[contains(text(), '在瀏覽器中繼續')]]"
            
            # 等待按鈕出現並點擊
            continue_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, continue_btn_xpath))
            )
            
            # 使用 ActionChains 確保點擊有效
            actions = ActionChains(driver)
            actions.move_to_element(continue_btn).click().perform()
            
            print("已成功點擊『在瀏覽器中繼續』")
            time.sleep(5)  # 等待頁面跳轉到帳密輸入框
        except Exception as e:
            print("未發現攔截按鈕或已在登入頁面，跳過點擊步驟。")

        # 2. 讀取 login.txt 帳密
        if not os.path.exists(LOGIN_INFO_PATH):
            print(f"找不到檔案: {LOGIN_INFO_PATH}")
            return

        with open(LOGIN_INFO_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if len(lines) < 2:
                print("login.txt 格式錯誤，需要兩行（帳號與密碼）")
                return
            email = lines[0].strip()
            password = lines[1].strip()

        # 3. 輸入 Email (改用更穩定的選擇器)
        print("正在輸入帳號...")
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.click()
        human_type(email_input, email)

        # 4. 輸入 Password
        print("正在輸入密碼...")
        pass_input = driver.find_element(By.NAME, "password")
        pass_input.click()
        human_type(pass_input, password)

        # 5. 送出登入
        time.sleep(1)
        pass_input.send_keys(Keys.ENTER)
        print("已送出登入資訊，等待跳轉頻道...")

        # 6. 確認是否成功進入頻道（看到輸入框才算成功）
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="textbox"]'))
        )
        print("登入成功且已進入頻道！")

    except Exception as e:
        print(f"登入流程發生錯誤: {e}")

def wait_until_next_hour():
    now = datetime.now()
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    wait_seconds = int((next_hour - now).total_seconds())
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"現在時間: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"預計在 {next_hour.strftime('%Y-%m-%d %H:%M:%S')} 開始執行")
    
    for _ in tqdm(range(wait_seconds), desc="等待下個整點", unit="秒", leave=False, dynamic_ncols=True):
        time.sleep(1)
    time.sleep(random.randrange(5, 15))

# 啟動前先等待
# wait_until_next_hour()

while True:
    options = Options()
    # 關鍵：設定 Firefox Profile
    options.add_argument("-profile")
    options.add_argument(PROFILE_PATH)
    
    # 建議：隱藏自動化偵測特徵 (選配)
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference('useAutomationExtension', False)

    driver = webdriver.Firefox(service=Service(DRIVER_PATH), options=options)
    
    try:
        driver.get(TARGET_URL)
        
        # 1. 偵測登入狀態：等待對話框出現
        # Discord 的訊息輸入框通常帶有 role='textbox'
        print("正在檢查登入狀態...")
        try:
            input_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="textbox"]'))
            )
            print("偵測到已登入狀態，跳過登入")
        except:
            print("未發現輸入框，嘗試進行登入...")
            login(driver)
            # 登入完重新跳轉一次頻道
            driver.get(TARGET_URL)
            input_box = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="textbox"]'))
            )

        # 2. 執行簽到動作
        time.sleep(random.uniform(2, 5))
        input_box.click()
        
        # 模擬打字 /hourly 
        # 注意：Discord 的斜線指令通常需要打完後等一下選單彈出
        human_type(input_box, "/hourly ")
        time.sleep(2)
        input_box.send_keys(Keys.ENTER) # 送出指令
        
        print(f"已於 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 完成簽到")
        time.sleep(5) # 確保訊息送出
        
    except Exception as e:
        print(f"發生異常: {e}")
    finally:
        driver.quit()
        
    wait_until_next_hour()