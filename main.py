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
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to send email

EMAIL_SENDER = '@gmail.com'
# Consider using environment variables for security
EMAIL_PASSWORD = ''
EMAIL_RECEIVER = '@gmail.com'


def send_email(email_sender, email_password, email_receiver, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.elasticemail.com', 2525)
        server.starttls()
        server.login(email_sender, email_password)
        text = msg.as_string()
        server.sendmail(email_sender, email_receiver, text)
        server.quit()
        print(f"Email successfully sent to {email_receiver}")
    except Exception as e:
        print(f"Failed to send email: {e}")


# # Telegram Bot Token and Channel ID
# TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
# CHANNEL_ID = YOUR_CHANNEL_ID
# Options for Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; ARM Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.129 Safari/537.36"
)
chrome_options.add_argument('--headless')

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# URLs
url_dynamic = "https://www.woolworths.com.au/shop/productdetails/118647/friskies-adult-indoor-delights-dry-cat-food"
url_static = "https://www.coles.com.au/product/chobani-oat-milk-barista-edition-1l-5443825"

while True:
    try:
        # URL for the dynamically loaded content
        driver.get(url_dynamic)
        time.sleep(5)  # Wait for content to load

        # Extract the dynamic price
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "price-frame")))
        price_element = driver.find_element(By.CLASS_NAME, 'price-frame')
        dynamic_content = price_element.text

        # Format the dynamic content to remove new lines and spaces
        formatted_dynamic_content = re.sub(r'\s+', '', dynamic_content.strip())

        # Use regular expression to extract the price per kg
        match = re.search(r'\$\d+\.?\d*', formatted_dynamic_content)
        if match:
            price_per_kg = match.group()
            print("Price of Woolworths Item:", price_per_kg)
        else:
            print("Price of Woolworths Item not found")

    except Exception as e:
        print(f"Error extracting content: {e}")

    try:
        # URL for the static content
        response = requests.get(url_static)
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find('script', type='application/ld+json')

        # Extract the static price
        data = json.loads(script.string)
        static_price = data['offers'][0]['price']

        print(f"Price of Coles Item: ${static_price}")

        # Prepare message
        message = f"Price per KG: {price_per_kg}\nColes Price: ${static_price}"

        # Send message to Telegram channel
        subject = "Price Update"
        send_email(EMAIL_SENDER, EMAIL_PASSWORD,
                   EMAIL_RECEIVER, subject, message)

    except Exception as e:
        print("Error extracting static price:", e)

    # Wait for 60 seconds before the next iteration
    time.sleep(60)

# Note: To stop the script, you'll need to manually interrupt it.
