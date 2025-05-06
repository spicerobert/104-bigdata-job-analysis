import requests
import json
import os

# Load cookies from the JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
cookies_file = os.path.join(script_dir, "cookies.json")
with open(cookies_file, "r") as f:
    cookies = json.load(f)

# Create a session object
session = requests.Session()

# Add the cookies to the session
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

# Make a request to the target page
url = "https://vip.104.com.tw/index/index"
response = session.get(url)

# Print the response status code
print(response.status_code)
print(response.raise_for_status())

# Extract the title
if "<title>" in response.text:
    title = response.text.split("<title>")[1].split("</title>")[0]
    print(title)
else:
    print("Error: <title> tag not found in the response.")

# Print the response content (optional)
# print(response.content)
