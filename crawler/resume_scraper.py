import time
import os
import xlwings as xw
wb = xw.Book.caller()
script_dir = os.path.dirname(os.path.abspath(__file__))

# --- 設定登入資訊 ---
# username = "robert@auntstella.com.tw"  # 請在這裡替換成您的 104 帳號，或從外部載入
# password = "spice7434"  # 請在這裡替換成您的 104 密碼，或從外部載入

def login_104(USERNAME="", PASSWORD=""):
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import json
    # Get the path to the ChromeDriver executable
    chromedriver_path = ChromeDriverManager().install()
    print(chromedriver_path)
    # Correct the path to point to chromedriver.exe@
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
    # target_url = "https://vip.104.com.tw/index/index"  # 登入後要前往的目標頁面

    driver.get(login_url)
    # Find the username and password input fields and the login button
    wait = WebDriverWait(driver, 20)
    username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa-id="loginUserName"]')))
    username_field.send_keys(USERNAME)
    password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa-id="loginPassword"]')))
    password_field.send_keys(PASSWORD)
    remember_label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="remember"]')))
    remember_label.click()
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa-id="loginButton"]')))
    login_button.click()
    time.sleep(30)  # 等待輸入驗證碼

    # Wait for the element to be present
    product_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.MultipleProduct__product')))
    # Click the element
    product_element.click()

    try:
        logout_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-v-b1877ad6][class="btn btn-secondary-b3 btn--sm btn--responsive"]')))
        logout_button.click()
    except Exception as e:
        wb.sheets['搜尋人力'].range('D3').value = f"登出按鈕未找到或無法點擊: {e}"
    
    time.sleep(10) # 等待跳轉
    try:
        # Get the title from the current page
        title = driver.title
        wb.sheets['搜尋人力'].range('D3').value = title
        time.sleep(5)  # Wait for 5 seconds to ensure driver stability
        try:
            cookies = driver.get_cookies()
            print(f"Cookies: {cookies}")
            save_cookies_result = save_cookies_to_file(cookies)
            wb.sheets['搜尋人力'].range('D4').value =str(save_cookies_result)
            print(f"{save_cookies_result}")
        except Exception as e:
            print(f"Error getting cookies: {e}")
            wb.sheets['搜尋人力'].range('D4').value = f"取得cookies發生錯誤： {e}"
    finally:
        driver.quit() # 確保瀏覽器和 driver 進程被關閉

def save_cookies_to_file(cookies):
    import json
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cookies_file = os.path.join(script_dir, "104_cookies.json")
    try:
        with open(cookies_file, "w") as f:
            json.dump(cookies, f, indent=4)
        return "成功儲存104_cookies.json"
    except Exception as e:
        error_message = f"儲存cookies發生錯誤： {e}, file path: {cookies_file}"
        return error_message


def load_cookies():
    import requests
    import json
    session = requests.Session()
    try:
        with open(os.path.join(script_dir, '104_cookies.json'), 'r') as f:
            cookies_list = json.load(f)
            for cookie in cookies_list:
                session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
        print("Cookies loaded successfully!")

        url = "https://vip.104.com.tw/index/index"
        response = session.get(url)

        # Print the response status code
        print(response.status_code)
        response.raise_for_status()

        # Extract the title
        if "<title>" in response.text:
            title = response.text.split("<title>")[1].split("</title>")[0]
            wb.sheets['搜尋人力'].range('H3').value =title
            print(title)
        else:
            print("Error: <title> tag not found in the response.")
            wb.sheets['搜尋人力'].range('H3').value = "Error: <title> tag not found in the response."

    except FileNotFoundError as e:
        print("Cookie file not found. Please generate cookies first.")
        wb.sheets['搜尋人力'].range('H4').value = f"取得cookies發生錯誤： {e}"
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        wb.sheets['搜尋人力'].range('H4').value = f"取得cookies發生錯誤： {e}"
    except Exception as e:
        print(f"An error occurred: {e}")
        wb.sheets['搜尋人力'].range('H4').value = f"取得cookies發生錯誤： {e}"

def scrape_data(session):
    print("在這裡執行您的爬蟲代碼...")
    # --- 爬蟲邏輯 ---
    # 使用 session.get() 抓取需要登入才能看到的頁面
    # 例如：
    response = session.get("https://vip.104.com.tw/index/index")
    print(response.status_code)
    print(response.raise_for_status())

    # Extract the title
    if "<title>" in response.text:
        title = response.text.split("<title>")[1].split("</title>")[0]
        print(title)
    else:
        print("Error: <title> tag not found in the response.")
    # soup = BeautifulSoup(response.text, "html.parser")
    # ... (解析頁面)

    # 爬完資料記得關掉 driver
    print("Selenium 操作完成，正在關閉瀏覽器...")
    #driver.quit() # 確保瀏覽器和 driver 進程被關閉

if __name__== '__main__':
    # driver = login_104()
    # scrape_data(driver)
    load_cookies()
