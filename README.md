# 104-bigdata-job-analysis
Analyze Big Data-related job listings from 104.com.tw with web scraping and salary comparison by city. Includes data cleaning, visualization, and optional dashboard.

## 🔍 Features
- 🕷 Web scraping with `requests` + `BeautifulSoup`
- 📄 Export raw data to Excel and clean with `pandas`
- 📈 Salary analytics by city and pay method
- 📊 Visualization with `matplotlib` and `seaborn`
- 🌐 (Optional) Interactive dashboard with Streamlit

## 📁 Project Structure
104-bigdata-job-analysis/  
├── crawler/ # Web crawler  
├── data/ # Raw and cleaned datasets  
├── analysis/ # Jupyter Notebooks for salary analysis  
├── dashboard/ # Streamlit app (optional)  
├── README.md  
└── requirements.txt  

## 📊 Sample Insights
- 台北市大數據職缺平均薪資最高

## 🚀 Getting Started
```bash
# 安裝所需套件
pip install -r requirements.txt

# 執行爬蟲
python crawler/104_scraper.py

# 啟動分析
jupyter notebook analysis/salary_analysis.ipynb

# 啟動 Streamlit 儀表板（可選）
streamlit run dashboard/streamlit_app.py
```
## 📌 Tech Stack
Python, requests, BeautifulSoup

pandas, matplotlib, seaborn

Streamlit (optional)
