#先創建pandas DataFrame，再將爬取資料進行處理並存入，最後一次性輸出到Excel
import requests
import bs4
from time import sleep
import pandas as pd
import xlwings as xw
import urllib.parse
swb = xw.Book.caller()

@xw.func
def scrape_jobs(keyword="", area="", jobcat="", max_page=0):
    try:
        # 創建 DataFrame
        columns = ['職缺名稱', '職缺連結', '公司名稱', '工作地區', '薪資待遇', 
                   '給薪方式', '薪資下界', '薪資上界', '平均薪資', '縣市', '鄉鎮市區']
        df = pd.DataFrame(columns=columns)

        # URL encode the keyword
        encoded_keyword = urllib.parse.quote(keyword)

        # 爬取的 URL
        url = f"https://www.104.com.tw/jobs/search/?jobsource=joblist_search&mode=s&order=15&page=1"
        if jobcat:
            url += f"&jobcat={jobcat}"
        if encoded_keyword:
            url += f"&keyword={encoded_keyword}"
        if area:
            url += f"&area={area}"

        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, "html.parser")  # 明確指定解析器
        allJobsInform = soup.find_all('div', class_='info-container')

        page = 1
        while allJobsInform != [] and (max_page == 0 or page <= max_page):
            print(f"=========================== 現在抓到第 {page} 頁資料 ===========================")
            for job in allJobsInform:
                try:
                    # 抓取職缺資訊
                    job_name = job.a.text.strip()
                    job_link = job.a['href']
                    job_company = job.select('a')[1].text.strip()
                    job_area = job.select('a')[3].string.strip()
                    job_salary = job.select('a')[6].string.strip()

                    job_county = job_area[:3]
                    job_section = job_area[3:]
                    PayWay = job_salary[:2]
                    if PayWay == "待遇":
                      PayWay = "面議"

                    salary = ''
                    for char in job_salary:
                      if char.isdigit() or char=='~':
                        salary += char

                    if '~' in salary:
                      lowEndSalary  = salary[:salary.find('~')]
                      highEndSalary = salary[salary.find('~')+1:]
                    else:
                      lowEndSalary  = salary
                      highEndSalary = salary

                    if lowEndSalary != '' and highEndSalary != '':
                      lowEndSalary = int(lowEndSalary)
                      highEndSalary = int(highEndSalary)
                      avgSalary = (lowEndSalary + highEndSalary)/2
                    else:
                      avgSalary = ''

                    # 將資料加入 DataFrame
                    print(job_name, job_link, job_company, job_area, job_salary, PayWay, lowEndSalary, highEndSalary, avgSalary, job_county, job_section)
                    df.loc[len(df)] = [job_name, job_link, job_company, job_area, job_salary, PayWay, lowEndSalary, highEndSalary, avgSalary, job_county, job_section]
                except Exception as e:
                    print(f"資料解析錯誤：{e}")
            sleep(2)

            # 下一頁
            page += 1
            url = f"https://www.104.com.tw/jobs/search/?jobsource=joblist_search&mode=s&order=15&page={page}"
            if jobcat:
                url += f"&jobcat={jobcat}"
            if encoded_keyword:
                url += f"&keyword={encoded_keyword}"
            if area:
                url += f"&area={area}"

            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            allJobsInform = soup.find_all('div', class_='info-container')

        # 寫入指定工作表
        swb.sheets['搜尋職缺'].range('B3').value = url
        swb.sheets['職缺'].cells.clear_contents()
        swb.sheets['職缺'].range('A1').value = df.columns.tolist()
        swb.sheets['職缺'].range('A2').value =df.values

        return "爬蟲完成，資料已儲存至 ./data/104CrawlResult.xlsx"

    except Exception as e:
        swb.sheets['搜尋職缺'].range('C2').value = f"Error: {e}"
        return f"爬蟲過程中發生錯誤: {e}"
