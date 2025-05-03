import requests

# 將 cookie 轉換為 dict 格式
cookies = {
    "ithp": "eyJ0eXAiOiJpZC10b2tlbitqd3QiLCJraWQiOiI5ZGUyNmI0MC01YTQ2LTQzOTktODE1Mi1lN2FjMGZkOGMxMzkiLCJhbGciOiJFUzI1NiJ9.eyJhenAiOiJmNTA3MTYxYi0xN2RjLTRkMWItYWZkZS0wZGI2NmM5ODFjZTIiLCJub25jZSI6IjNlMTQzMWExLTI2MTktNDQ2Ny05NDQzLTYxMjMzZjM4NDlhNCIsImF1dGhfdGltZSI6MTc0NjI2NjQ1MSwidXJuOjEwNDp2MzplbnRpdHk6dHJhY2VfaWQiOiIwZjYwM2YzODMyNzE5YzZiZjRmMGNlOTQ1ODI2Y2QwNSIsInVybjoxMDQ6djM6ZW50aXR5OmxvZ2luX25vIjoiODkzMjA0NTg1NTkxNTE2ODM3IiwidXJuOjEwNDp2MzplbnRpdHk6Y29tcGFueV9pZCI6IjIzMjI1ODg5MDAwIiwidXJuOjEwNDp2MzplbnRpdHk6cGlkIjoiMTcyNTk4NDciLCJ1cm46MTA0OnYzOmVudGl0eTppbXBlcnNvbmF0b3JfaWQiOiIiLCJ1cm46MTA0OnYzOmVudGl0eTppbXBlcnNvbmF0b3JfbmFtZSI6IiIsInVybjoxMDQ6djM6ZW50aXR5OmF0c19zdGF0ZSI6ImluYWN0aXZlIiwidXJuOjEwNDp2MjpzZXNzaW9uIjoiZXlKaGJHY2lPaUpGUTBSSUxVVlRLMEV5TlRaTFZ5SXNJbVZ1WXlJNklrRXlOVFpIUTAwaUxDSnJhV1FpT2lJeVl6azFObVZrWVMxbFlUUXhMVFF6TkdVdFlqZGhZeTFpTWpnMlpXTmtOakF5T0dNaUxDSmxjR3NpT25zaWVDSTZJbVJEUTNkWVpYVkNWazU1ZEdSSGQweElOMkpWVDFoTU0zTkZUSE5pWWtRd00yNUJSakY0VVhweFIwRWlMQ0pqY25ZaU9pSlFMVEkxTmlJc0ltdDBlU0k2SWtWRElpd2llU0k2SW1Kd1gzQllWbFl4YkZsME0zQkJNemxaVGs1eVFucFBWMHd5TmxsR2FGOUVjMDFMUm5Od2VGcGZNbEVpZlgwLlQ1XzFOa004Y2JCellyVk1FbkF4TmJhTVZTaC1lNXh4MHlRLVREbk9kWjYwY0sxQlJPelhQZy5EdEtTT2tVaWM0YlIxT01oLld3R0trR183LTQyeUtqN2JXVUFMMDBIQmtqV0JaOWFqbnFIZE5NMjBCNzQ4RXlwZE8yM053bjAtQUFRRVZ3c1dqd2h6T0ZoVGNGVW1OM2dJd2JyRC43Qy1yMDBtMTdjczFyX1Zna2hrdXNnIiwidXJuOjEwNDp2MjppbXBlcnNvbmF0aW9uIjoiIiwidXJuOjEwNDp2MjplbnRpdHk6dXNlcl9pZCI6IlVsdWgzWjNGOTZZVzV3NXZRTGJNIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLXNlcnZlci52aXAuMTA0LmNvbS50dyIsImF1ZCI6WyJmNTA3MTYxYi0xN2RjLTRkMWItYWZkZS0wZGI2NmM5ODFjZTIiLCJodHRwczovL2F1dGgtc2VydmVyLnZpcC4xMDQuY29tLnR3Il0sInN1YiI6InJvYmVydEBhdW50c3RlbGxhLmNvbS50dyIsImV4cCI6MTc0NjM1Mjg0OSwianRpIjoiYTdiZGNmZjgtNDAxMi00N2M1LWFlZGEtYjFlZGRiNjA4NjBjIiwiaWF0IjoxNzQ2MjY2NDQ5fQ"
}

# 指定一個需要使用 cookies 的 URL
url = "https://bsignin.104.com.tw/login"

# 發送帶有 cookies 的 GET 請求
response = requests.get(url, cookies=cookies)

# 顯示回應狀態碼與部分內容
print(response.status_code)
print(response.text[:500])  # 輸出前 500 字符供確認

def scrape_resume():
  #先創建Excel，再將爬取資料進行處裡並一一填入
  import requests
  import bs4
  session = requests.Session()

  # 取得登入頁面，取得 CSRF token（如果有的話）
  res = session.get('https://bsignin.104.com.tw/login')
  soup = bs4(res.text, 'html.parser')

  # 觀察有無 hidden 欄位，像 csrf token
  # token = soup.find('input', {'name': 'csrf_token'})['value']

  # 模擬登入資訊（根據觀察的欄位名稱）
  payload = {
      'username': 'robert@auntstella.com.tw',
      'password': 'spice7434',
      # 'csrf_token': token,  # 若有需要的話
  }

  headers = {
      'User-Agent': 'Mozilla/5.0',
      'Referer': 'https://bsignin.104.com.tw/login'
  }

  # 根據觀察到的 POST 登入 API URL
  login_response = session.post('https://bsignin.104.com.tw/login', data=payload, headers=headers)

  # 登入成功後進一步抓取目標頁面
  target_url = 'https://somepage.104.com.tw/data'
  resp = session.get(target_url)
  soup = bs4(resp.text, 'html.parser')

  print(soup.prettify())
  # 創建 Excel 檔案
  # wb = openpyxl.Workbook()
  # ws = wb.active

  # # 設定 Excel 標題
  # ws['A1'] = '職缺名稱'
  # ws['B1'] = '職缺連結'
  # ws['C1'] = '公司名稱'
  # ws['D1'] = '工作地區'
  # ws['E1'] = '薪資待遇'
  # ws['F1'] = '給薪方式'
  # ws['G1'] = '薪資下界'
  # ws['H1'] = '薪資上界'
  # ws['I1'] = '平均薪資'
  # ws['J1'] = '縣市'
  # ws['K1'] = '鄉鎮市區'

  # 爬取的 URL
  # url = f"https://vip.104.com.tw/search/searchResult?loadTime=2025-04-29%2014%3A13%3A36&ec=102&jobcat=2009001000&city=6001001000,6001002000&plastActionDateType=1&workExpTimeType=all&workExpTimeMin=1&workExpTimeMax=1&sex=2&empStatus=0&updateDateType=1&contactPrivacy=0&sortType=PLASTACTIONDATE"
  # res = requests.get(url)
  # soup = bs4.BeautifulSoup(res.text, "html.parser")  # 明確指定解析器
  # # allResumesInform = soup.find_all('div', class_='resume-card-item resume-card__center cellspcr-40')
  
 
  # if allResumesInform:
  #   print("allResumesInform 容器中有物件。")
  # else:
  #   print("allResumesInform 容器是空的。")
  
  # page = 1
  # while allResumesInform != []:
  #     print(f"=========================== 現在抓到第 {page} 頁資料 ===========================")
  #     for resume in allResumesInform:
  #         try:
  #             # 抓取職缺資訊
  #             name_tag=resume.find('a',class_='name word-break-all')
  #             if name_tag:
  #               resume_name=name_tag.text.strip()
  #               print(f"找到名字: {resume_name}") # 驗證一下
              # job_link = "https:" + job.a['href']
              # job_company = job.select('a')[1].text.strip()
              # job_area = job.select('a')[3].string.strip()
              # job_salary = job.select('a')[6].string.strip()

              # job_county = job_area[:3]
              # job_section = job_area[3:]
              # PayWay = job_salary[:2]
              # if PayWay == "待遇":
              #   PayWay = "面議"

              # salary = ''
              # for char in job_salary:
              #   if char.isdigit() or char=='~':
              #     salary += char

              # if '~' in salary:
              #   lowEndSalary  = salary[:salary.find('~')]
              #   highEndSalary = salary[salary.find('~')+1:]
              # else:
              #   lowEndSalary  = salary
              #   highEndSalary = salary

              # if lowEndSalary != '' and highEndSalary != '':
              #   lowEndSalary = int(lowEndSalary)
              #   highEndSalary = int(highEndSalary)
              #   avgSalary = (lowEndSalary + highEndSalary)/2
              # else:
              #   avgSalary = ''

              # 寫入 Excel
              # print(resume_name, job_link, job_company, job_area, job_salary, PayWay, lowEndSalary, highEndSalary, avgSalary, job_county, job_section)
              # ws.append([job_name, job_link, job_company, job_area, job_salary, PayWay, lowEndSalary, highEndSalary, avgSalary, job_county, job_section])
          # except Exception as e:
          #     print(f"資料解析錯誤：{e}")
      # sleep(2)

      # 下一頁
      # page += 1
      # url = f"https://www.104.com.tw/jobs/search/?jobsource=index_s&keyword=%E5%A4%A7%E6%95%B8%E6%93%9A&mode=s&page={page}"
      # res = requests.get(url)
      # soup = bs4.BeautifulSoup(res.text, "html.parser")
      # allJobsInform = soup.find_all('div', class_='info-container')
      # wb.save('./data/104CrawlResult.xlsx')

if __name__ == "__main__":
    # This block allows you to run the script directly for testing
    scrape_resume()
