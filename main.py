import requests
import re
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Function to send message to Telegram channel


def send_message_to_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response.json()


# Telegram Bot Token and Channel ID
TOKEN = "6842825878:AAHoVEDTmvZJX3aPJf9U2A1vonX3t02A9LU"
CHANNEL_ID = -1002118829646

# Options for Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; ARM Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.129 Safari/537.36")
chrome_options.add_argument('--headless')

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# URL input
url_dynamic = input("Enter the URL for dynamic content: ")
url_static = input("Enter the URL for static content: ")

while True:
    # URL for the dynamically loaded content
    driver.get(url_dynamic)
    time.sleep(5)  # Wait for content to load

    # Extract the dynamic price
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-panel")))
        price_element = driver.find_element(By.CLASS_NAME, 'product-panel')
        dynamic_content = price_element.text

        # Use regular expression to extract the price per kg
        match = re.search(r'\$\d+\.?\d* \/ 1KG', dynamic_content)
        if match:
            price_per_kg = match.group()
            print("Price per KG:", price_per_kg)
        else:
            print("Price per KG not found")
    except Exception as e:
        print(f"Error extracting content: {e}")

    # URL for the static content
    response = requests.get(url_static)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find('script', type='application/ld+json')

    # Extract the static price
    try:
        data = json.loads(script.string)
        static_price = data['offers'][0]['price']
        print("Coles Price: $", static_price)
    except Exception as e:
        print("Error extracting static price:", e)

    # Prepare message
    message = f"Price per KG: {price_per_kg}\nColes Price: ${static_price}"

    # Send message to Telegram channel
    send_message_to_telegram(TOKEN, CHANNEL_ID, message)

    # Wait for 60 seconds before the next iteration
    time.sleep(60)

# Note: To stop the script, you'll need to manually interrupt it.
