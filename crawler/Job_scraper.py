#先創建pandas DataFrame，再將爬取資料進行處理並存入，最後一次性輸出到Excel
import requests
import bs4
from time import sleep
import pandas as pd
import os

# 創建 DataFrame
columns = ['職缺名稱', '職缺連結', '公司名稱', '工作地區', '薪資待遇', 
           '給薪方式', '薪資下界', '薪資上界', '平均薪資', '縣市', '鄉鎮市區']
df = pd.DataFrame(columns=columns)


# 爬取的 URL
url = "https://www.104.com.tw/jobs/search/?jobcat=2009004008,2009004001&jobsource=joblist_search&keyword=%E8%81%B7%E6%A5%AD%E5%AE%89%E5%85%A8%E8%A1%9B%E7%94%9F%E7%AE%A1%E7%90%86%E5%93%A1&mode=s&order=15&page=1&area=6001001000"
res = requests.get(url)
soup = bs4.BeautifulSoup(res.text, "html.parser")  # 明確指定解析器
allJobsInform = soup.find_all('div', class_='info-container')

page = 1
while allJobsInform != []:
    print(f"=========================== 現在抓到第 {page} 頁資料 ===========================")
    for job in allJobsInform:
        try:
            # 抓取職缺資訊
            job_name = job.a.text.strip()
            job_link = "https:" + job.a['href']
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
    url = f"https://www.104.com.tw/jobs/search/?jobcat=2009004008,2009004001&jobsource=joblist_search&keyword=%E8%81%B7%E6%A5%AD%E5%AE%89%E5%85%A8%E8%A1%9B%E7%94%9F%E7%AE%A1%E7%90%86%E5%93%A1&mode=s&order=15&page={page}"+f"&area=6001001000"
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    allJobsInform = soup.find_all('div', class_='info-container')

# 確保輸出目錄存在
os.makedirs('./data', exist_ok=True)

# 將 DataFrame 輸出至 Excel
df.to_excel('./data/104CrawlResult.xlsx', index=False)
print(f"爬蟲完成，共獲取 {len(df)} 筆資料，已儲存至 './data/104CrawlResult.xlsx'")
