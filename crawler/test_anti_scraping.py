import requests

url = "https://www.104.com.tw/jobs/search/?jobsource=joblist_search&mode=s&order=15&page=1&keyword=%E9%A3%9F%E5%93%81"  # Replace with the URL you are targeting

try:
    response = requests.get(url, timeout=5)  # Added a timeout to prevent indefinite hanging

    print("Status Code:", response.status_code)
    print("Headers:", response.headers)

    if response.status_code == 200:
        print("Request successful. Checking content type...")
        if 'text/html' in response.headers.get('Content-Type', ''):
            print("Content type is HTML. Likely not blocked.")
        else:
            print("Content type is not HTML. May be blocked or receiving unexpected data.")
    elif response.status_code == 403:
        print("Status code 403: Forbidden. Likely blocked.")
    elif response.status_code == 429:
        print("Status code 429: Too Many Requests. Rate limited.")
    else:
        print("Request failed with status code:", response.status_code)

except requests.exceptions.RequestException as e:
    print("Request failed:", e)
