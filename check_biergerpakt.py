import requests
import sys
from datetime import datetime

KEYWORDS = [
    "orientation day",
    "journée d'orientation",
    "orientatiounsdag",
]
SEPTEMBER_KEYWORDS = ["september", "septembre"]
URL = "https://biergerpakt.zesummeliewen.lu/en/new-2/welcome-to-the-biergerpakt/"

def fetch_page():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text.lower()

def is_september_orientation_open(page_text):
    has_orientation = any(kw in page_text for kw in KEYWORDS)
    has_september = any(kw in page_text for kw in SEPTEMBER_KEYWORDS)
    return has_orientation and has_september

def main():
    print(f"Checking Biergerpakt at {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}...")

    page_text = fetch_page()

    if is_september_orientation_open(page_text):
        print("🚨 SEPTEMBER ORIENTATION DAY REGISTRATION IS OPEN!")
        print(f"Go register now: {URL}")
        sys.exit(1)  # This causes the workflow to "fail" → GitHub emails you
    else:
        print("Nothing yet. Will check again tomorrow.")

if __name__ == "__main__":
    main()
