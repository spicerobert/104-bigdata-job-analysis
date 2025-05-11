#先創建pandas DataFrame，再將爬取資料進行處理並存入，最後一次性輸出到Excel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import xlwings as xw
import urllib.parse
# swb = xw.Book.caller()

keyword='食品'
area='6001001000'
jobcat='2001001001'
max_page=3
web_104='https://www.104.com.tw/jobs/search/?isJobList=1&jobsource=joblist_search&order=15'

def scrape_jobs(): #keyword='', area='', jobcat='', max_page=2):
    try:
        # 創建 DataFrame
        columns = ['職缺名稱', '職缺連結', '公司名稱', '網頁標題', '工作地區', '薪資待遇',
                   '給薪方式', '薪資下界', '薪資上界', '平均薪資', '縣市', '鄉鎮市區']
        df = pd.DataFrame(columns=columns)

        # URL encode the keyword
        encoded_keyword = urllib.parse.quote(keyword)
        
        # 爬取的 URL
        url = f"{web_104}&page=1&jobcat={jobcat}&keyword={encoded_keyword}&area={area}"
        # Selenium setup
        options = Options()
        driver = webdriver.Chrome(options=options)
        driver.get(url)  
        # print(f"{driver.title}")
        # swb.sheets['搜尋職缺'].range('C1').value=driver.title
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
                        job_name_element = job.find_element(By.CSS_SELECTOR, 'a.info-job__text')
                        job_name = job_name_element.text.strip()
                        print(f"職缺名稱: {job_name}")
                    #     job_link = job_name_element.get_attribute('href')

                    #     job_company_element = job.find_element(By.CSS_SELECTOR, 'a.info-company__text')
                    #     job_company = job_company_element.text.strip()


                    #     job_area_element = job.find_element(By.CSS_SELECTOR, 'span.info-tags__text a')
                    #     job_area = job_area_element.text.strip()

                    #     job_salary_element = job.find_element(By.CSS_SELECTOR, 'span.info-tags__text a[data-gtm-joblist*="薪資"]')
                    #     job_salary = job_salary_element.text.strip()

                    #     job_county = job_area[:3]
                    #     job_section = job_area[3:]
                    #     PayWay = job_salary[:2]
                    #     if PayWay == "待遇":
                    #         PayWay = "面議"

                    #     salary = ''
                    #     for char in job_salary:
                    #         if char.isdigit() or char=='~':
                    #             salary += char

                    #     if '~' in salary:
                    #         lowEndSalary  = salary[:salary.find('~')]
                    #         highEndSalary = salary[salary.find('~')+1:]
                    #     else:
                    #         lowEndSalary  = salary
                    #         highEndSalary = salary

                    #     if lowEndSalary != '' and highEndSalary != '':
                    #         lowEndSalary = int(lowEndSalary)
                    #         highEndSalary = int(highEndSalary)
                    #         avgSalary = (lowEndSalary + highEndSalary)/2
                    #     else:
                    #         avgSalary = ''

                    #     # 將資料加入 DataFrame
                    #     print(job_name, job_link, job_company, page_title, job_area, job_salary, PayWay, lowEndSalary, highEndSalary, avgSalary, job_county, job_section)
                    #     df.loc[len(df)] = [job_name, job_link, job_company, page_title, job_area, job_salary, PayWay, lowEndSalary, highEndSalary, avgSalary, job_county, job_section]
                    except Exception as e:
                        print(f"資料解析錯誤：{e}")
                        # Print the full traceback for better debugging
                        import traceback
                        traceback.print_exc()
                sleep(10) # Reduced sleep time for faster testing
                page += 1
                url = f"{web_104}&page={page}&jobcat={jobcat}&keyword={encoded_keyword}&area={area}"      
                driver.get(url)
                sleep(10)
                allJobsInform  = driver.find_elements(By.CLASS_NAME, 'info-container')

            # 寫入指定工作表
            # swb.sheets['搜尋職缺'].range('B3').value = page_title
            # swb.sheets['搜尋職缺'].range('C2').value = f"全部頁面爬蟲完成"
            # swb.sheets['職缺'].cells.clear_contents()
            # swb.sheets['職缺'].range('A1').value = df.columns.tolist()
            # swb.sheets['職缺'].range('A2').value =df.values
        except Exception as e:
            print(f"爬蟲過程中發生錯誤: {e}")
            # swb.sheets['搜尋職缺'].range('C2').value=f"爬蟲過程中發生錯誤: {e}"
            driver.quit()
        finally:
            # swb.sheets['搜尋職缺'].range('C2').value=f"Selenium 錯誤：{e}"            
            driver.quit()
    except Exception as e:
        print(f"{e}")
        # swb.sheets['搜尋職缺'].range('C3').value = f"Error: {e}"

if __name__== '__main__':
    scrape_jobs()
    # print(result)
    # driver = login_104()
    # scrape_data(driver)
    # load_cookies()
