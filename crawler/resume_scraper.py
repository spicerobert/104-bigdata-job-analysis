import time
import os
import xlwings as xw
script_dir = os.path.dirname(os.path.abspath(__file__))
# --- 設定登入資訊 ---
username = "robert@auntstella.com.tw"  # 請在這裡替換成您的 104 帳號，或從外部載入
password = "spice7434"  # 請在這裡替換成您的 104 密碼，或從外部載入

# 模擬登入104
def login_104(USERNAME="", PASSWORD=""):
    wb = xw.Book.caller()
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
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-dev-shm-usage")
    # 啟動 driver
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
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

    try:
        # Wait for the element to be present
        product_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.MultipleProduct__product')))
        # Click the element
        product_element.click()
        logout_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-v-b1877ad6][class="btn btn-secondary-b3 btn--sm btn--responsive"]')))
        logout_button.click()
    except Exception as e:
        wb.sheets['搜尋人力'].range('D3').value = f"未輸入驗證碼，或原帳號未登出"    
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

# 儲存104_Cookies
def save_cookies_to_file(cookies):
    wb = xw.Book.caller()
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

# 載入104_Cookies (for Selenium)
def load_cookies():
    import json
    cookies_file = os.path.join(script_dir, '104_cookies.json')
    try:
        with open(cookies_file, 'r') as f:
            cookies_list = json.load(f)
            print(f"成功從 {cookies_file} 載入 cookies!")
            return cookies_list
    except FileNotFoundError:
        print(f"錯誤：找不到 cookies 檔案於 {cookies_file}。請先執行登入以產生 cookies。")
        return None
    except Exception as e:
        print(f"載入 cookies 發生錯誤： {e}")
        return None


def scrape_resumes(jobcat='',kws='', city='', home='', workInterval='', sex='', workShift='', photo='', auto='', role='', agerange='', plastActionDateType='', updateDateType='',contactPrivacy='0',workExpTimeType='', workExpTimeMin='', workExpTimeMax=''):
    from selenium import webdriver
    # from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    import json

    # 設定 Chrome options
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # options.add_argument("--headless") # 如果不需要看到瀏覽器視窗，可以取消註解此行
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 啟動 driver (假設 chromedriver 已安裝並在 PATH 中)
    service = Service() # 直接使用 Service()，它會嘗試在 PATH 中尋找 chromedriver
    driver = None # Initialize driver to None
    try:
        driver = webdriver.Chrome(service=service, options=options)
        url = "https://vip.104.com.tw"
        driver.get(url) # 導航到 104 的任意頁面

        # 載入並添加 cookies
        cookies = load_cookies()
        if cookies:
            for cookie in cookies:
                # Selenium requires 'expiry' to be an integer
                if 'expiry' in cookie:
                    cookie['expiry'] = int(cookie['expiry'])
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    print(f"添加 cookie 失敗: {cookie['name']}, 錯誤: {e}")
            print("Cookies 已添加到瀏覽器。")
            time.sleep(10) # 給瀏覽器一點時間處理 cookies

        # 導航到實際的履歷頁面
        base_url="https://vip.104.com.tw/search/searchResult?"
        params = []  
        if kws: params.append(f"kws={kws}") #關鍵字
        if plastActionDateType != 0 or plastActionDateType != '0': params.append(f"plastActionDateType={plastActionDateType}") #最近活動日
        if updateDateType != 0 or updateDateType != '0': params.append(f"updateDateType={updateDateType}") #履歷更新日
        if contactPrivacy : params.append(f"contactPrivacy={contactPrivacy}") #可Email和電話聯絡
        if jobcat: params.append(f"jobcat={jobcat}") #希望職類
        if city: params.append(f"city={city}") #希望工作地
        if home: params.append(f"home={home}") #居住地
        if workExpTimeType != "":
            params.append(f"workExpTimeType={workExpTimeType}") #總經歷
            if workExpTimeMin != "0": # 如果 workExpTimeMin 不為 "0"，則加入
                params.append(f"workExpTimeMin={workExpTimeMin}") # 最低經歷年限
            if workExpTimeMax != "0": # 如果 workExpTimeMax 不為 "0"，則加入
                params.append(f"workExpTimeMax={workExpTimeMax}") # 最高經歷年限
        if role: params.append(f"{role}") #工作性質 
        if workInterval: params.append(f"{workInterval}") #上班時段
        if workShift != '0': params.append(f"workShift={workShift}") #是否需要輪班
        if agerange: params.append(f"{agerange}") #年齡範圍
        if sex: params.append(f"sex={sex}") #性別
        if photo != '0': params.append(f"photo={photo}") #是否有照片
        if auto != '0': params.append(f"auto={auto}") #是否有自傳
        params.append(f"sortType=PLASTACTIONDATE")

        resume_url = base_url + "&".join(params)
        # test_resume_url = "https://vip.104.com.tw/search/searchResult?ec=1&kws=%E8%AD%B7%E7%90%86%E5%B8%AB&city=6001001005&home=6001001000,6001002000&plastActionDateType=1&workExpTimeType=all&workExpTimeMin=1&workExpTimeMax=1&sex=2&empStatus=0&updateDateType=1&contactPrivacy=0&sortType=RANK" # 請替換為一個實際的履歷 URL 進行測試
        
        driver.get(resume_url)

        # --- 在這裡加入履歷資料的剖析邏輯 ---
        print("已導航到履歷頁面，請在此處加入剖析邏輯。")

        # 例如：
        # from selenium.webdriver.common.by import By
        # resume_title_element = driver.find_element(By.CSS_SELECTOR, 'h1.resume-title')
        # print(f"履歷標題: {resume_title_element.text}")
        # ... 更多剖析程式碼 ...

        time.sleep(60) # 暫停一下以便觀察 (可移除

    except Exception as e:
        print(f"爬取過程中發生錯誤: {e}")
    finally:
        if driver:
            print("Selenium 操作完成，瀏覽器保持開啟...")
            driver.quit() # 確保瀏覽器和 driver 進程被關閉

if __name__== '__main__':
    # driver = login_104()
    # scrape_data(driver)
    # load_cookies() # 舊的 load_cookies 測試
    # 測試新的 scrape_resumes 函數
    test_resume_url = "https://vip.104.com.tw/search/listSearch" # 請替換為一個實際的履歷 URL 進行測試    
    scrape_resumes()
