#先創建pandas DataFrame，再將爬取資料進行處理並存入，最後一次性輸出到Excel
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import NoSuchElementException
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
import random
import pandas as pd
import xlwings as xw
import urllib.parse
swb = xw.Book.caller()

# keyword='食品'
# area='6001001000'
# jobcat='2001001001'
# max_page=2
web_104='https://www.104.com.tw/jobs/search/?isJobList=1&jobsource=joblist_search&order=15'

def scrape_jobs( keyword='', area='', jobcat='', max_page=0):
    try:
        # 創建 DataFrame
        columns = ['職缺名稱', '職缺連結', '公司名稱', '工作地區', '薪資待遇',
                   '給薪方式', '薪資下界', '薪資上界', '平均薪資', '縣市', '鄉鎮市區']
        df = pd.DataFrame(columns=columns)

        # URL encode the keyword
        encoded_keyword = urllib.parse.quote(keyword)
        
        # 爬取的 URL
        url = f"{web_104}&page=1&jobcat={jobcat}&keyword={encoded_keyword}&area={area}"
        # Selenium setup
        options = Options()
        # options.add_argument("--headless")  # 無頭模式，不開啟瀏覽器界面
        # options.add_argument("--disable-gpu")
        # options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # 初始化 WebDriver
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver = webdriver.Chrome(options=options)
        driver.get(url)  
        # print(f"{driver.title}")
        page_title = driver.title
        swb.sheets['搜尋職缺'].range('C1').value= page_title
        # Use Selenium to find all job elements
        page=1

        allJobsInform  = driver.find_elements(By.CLASS_NAME, 'info-container')
        try:
            while allJobsInform!=[] and page <= max_page:
                print(f"=========================== 現在抓到第 {page} 頁資料 ===========================")
                print(f"本頁包含幾個職缺{len(allJobsInform)}")
                for job in allJobsInform:
                    try:
                        # 抓取職缺資訊 using Selenium                        
                        job_name = job.find_element(By.CSS_SELECTOR, 'a').text.strip()
                        # print(f"職缺名稱: {job_name}")
                        job_link_redirect = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                        # Parse the redirected URL and extract the actual job link
                        parsed_url = urllib.parse.urlparse(job_link_redirect)
                        query_params = urllib.parse.parse_qs(parsed_url.query)
                        job_link = urllib.parse.unquote(query_params.get('url', [''])[0])
                        # print(f"職缺連結: {job_link}")
                        job_company = job.find_elements(By.CSS_SELECTOR, 'a')[1].text.strip()
                        # print(f"公司名稱: {job_company}")
                        job_area = job.find_elements(By.CSS_SELECTOR, 'a')[3].text.strip()
                        # print(f"工作地區: {job_area}")
                        job_salary = job.find_elements(By.CSS_SELECTOR, 'a')[6].text.strip()        
                        # print(f"薪資條件: {job_salary}")
                        job_county = job_area[:3]
                        job_section = job_area[3:]
                        PayWay = job_salary[:2]
                        if PayWay == "待遇":
                            PayWay = "面議"
                        salary = ''
                        for char in job_salary:
                            if char.isdigit() or char == '~':
                                salary += char
                        
                        if '~' in salary:
                            lowEndSalary = salary[:salary.find('~')]
                            highEndSalary = salary[salary.find('~')+1:]
                        else:
                            lowEndSalary = salary
                            highEndSalary = salary
                        
                        if lowEndSalary != '' and highEndSalary != '':
                            lowEndSalary = int(lowEndSalary)
                            highEndSalary = int(highEndSalary)
                            avgSalary = (lowEndSalary + highEndSalary)/2
                        else:
                            avgSalary = ''

                        # 將資料加入 DataFrame
                        # print(job_name, job_link, job_company, job_area, job_salary, PayWay, lowEndSalary, highEndSalary, avgSalary, job_county, job_section)
                        df.loc[len(df)] = [job_name, job_link, job_company, job_area, job_salary, PayWay, lowEndSalary, highEndSalary, avgSalary, job_county, job_section]
                    except Exception as e:
                        # print(f"資料解析錯誤：{e}")
                        swb.sheets['搜尋職缺'].range('C3').value=f"資料解析錯誤：{e}"
                sleep(2) # Reduced sleep time for faster testing
                # 下一頁
                page += 1
                if page > max_page:
                    break                
                url = f"{web_104}&page={page}&jobcat={jobcat}&keyword={encoded_keyword}&area={area}"
                driver.get(url)
                sleep(random.uniform(6, 10))
                allJobsInform  = driver.find_elements(By.CLASS_NAME, 'info-container')
            swb.sheets['搜尋職缺'].range('C2').value = f"全部頁面爬蟲完成"
            swb.sheets['職缺'].cells.clear_contents()
            swb.sheets['職缺'].range('A1').value = df.columns.tolist()
            swb.sheets['職缺'].range('A2').value =df.values
            driver.quit()
        except Exception as e:
            # print(f"爬蟲過程中發生錯誤: {e}")
            swb.sheets['搜尋職缺'].range('C3').value=f"爬蟲過程中發生錯誤: {e}"
            driver.quit()
        finally:
            driver.quit()
    except Exception as e:
        print(f"{e}")
        swb.sheets['搜尋職缺'].range('C3').value = f"Error: {e}"

if __name__== '__main__':
    scrape_jobs()
    # print(result)
    # driver = login_104()
    # scrape_data(driver)
    # load_cookies()
