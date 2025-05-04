import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# --- 設定登入資訊 ---
USERNAME = "robert@auntstella.com.tw"  # 請在這裡替換成您的 104 帳號，或從外部載入
PASSWORD = "spice7434"  # 請在這裡替換成您的 104 密碼，或從外部載入

# Get the path to the ChromeDriver executable
chromedriver_path = ChromeDriverManager().install()
print(chromedriver_path)

# Correct the path to point to chromedriver.exe
chromedriver_path = os.path.join(os.path.dirname(chromedriver_path), "chromedriver.exe")

# 設定 Chrome options
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--disable-dev-shm-usage")

# 啟動 driver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

login_url = "https://bsignin.104.com.tw/login"
target_url = "https://vip.104.com.tw/index/index"  # 登入後要前往的目標頁面

driver.get(login_url)
# Find the username and password input fields and the login button
wait = WebDriverWait(driver, 20)
username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa-id="loginUserName"]')))
username_field.send_keys(USERNAME)
password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa-id="loginPassword"]')))
password_field.send_keys(PASSWORD)
remember_label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="remember"]')))
remember_label.click() # <- 加上括號 () 來執行點擊
login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa-id="loginButton"]')))
login_button.click()
time.sleep(60)  # 等待登入完成，根據網速調整時間

# Navigate to the target URL
driver.get(target_url)
print(f"頁面標題: {driver.title}")
# Find and click the logout button
try:
    logout_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-v-b1877ad6][class="btn btn-secondary-b3 btn--sm btn--responsive"]')))
    logout_button.click()
    print("登出按鈕已點擊")
except Exception as e:
    print(f"登出按鈕未找到或無法點擊: {e}")

print("在這裡執行您的爬蟲代碼...")
# --- 爬蟲邏輯 ---
# 使用 session.get() 抓取需要登入才能看到的頁面
# 例如：
# response = session.get("https://example.com/secret_page")
# soup = BeautifulSoup(response.text, "html.parser")
# ... (解析頁面)

# 爬完資料記得關掉 driver
print("Selenium 操作完成，正在關閉瀏覽器...")
driver.quit() # 確保瀏覽器和 driver 進程被關閉
