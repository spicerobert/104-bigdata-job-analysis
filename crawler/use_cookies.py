import requests
import json
import os

def load_cookies(file_path='crawler/104_cookies.json'):
    """Loads cookies from a JSON file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(script_dir, file_path)
    try:
        with open(abs_file_path, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        print(f"Successfully loaded {len(cookies)} cookies from {abs_file_path}")  # Confirmation message
        return cookies
    except FileNotFoundError:
        print(f"Error: Cookie file not found at {abs_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {abs_file_path}")
        return []

# Load cookies
cookies = load_cookies()

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
response.raise_for_status()

# Extract the title
if "<title>" in response.text:
    title = response.text.split("<title>")[1].split("</title>")[0]
    print(title)
else:
    print("Error: <title> tag not found in the response.")
