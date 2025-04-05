# 104-bigdata-job-analysis
Analyze Big Data-related job listings from 104.com.tw with web scraping and salary comparison by city. Includes data cleaning and visualization.

## 🔍 Features
- 🕷 Web scraping with `requests` + `BeautifulSoup`
- 📄 Export raw data to Excel nd clean with `pandas`
- 📈 Salary analytics by city and pay method
- 📊 Visualization with `plotly`

## 📁 Project Structure
104-bigdata-job-analysis/  
├── crawler/ # Web crawler  
├── data/ # Raw and cleaned datasets  
├── analysis/ # Jupyter Notebooks for salary analysis    
├── README.md  
└── requirements.txt  

## 📊 Sample Insights
- 嘉義縣大數據職缺平均月薪薪資最高
- 台中市大數據職缺平均月薪薪資勝過台北市
- 台中市各鄉鎮地區大數據職缺平均月薪薪資差異勝過台北市

## 🚀 Getting Started
```bash
# 安裝所需套件
pip install -r requirements.txt

# 執行爬蟲
python crawler/104_scraper.py

# 啟動分析
jupyter notebook analysis/salary_analysis.ipynb

```
## 📌 Tech Stack
Python, requests, BeautifulSoup

pandas, plotly
