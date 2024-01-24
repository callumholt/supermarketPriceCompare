Supermarket Price Comparison Script
Project Overview
This script is designed to automate the process of comparing prices for specific products from different supermarkets. It fetches prices from both dynamic and static web pages, formats the data, and sends an email with the price comparison. This is particularly useful for tracking price changes over time or for comparing prices across different retailers.

Features
Extracts prices from dynamic web pages using Selenium WebDriver.
Retrieves prices from static web pages using BeautifulSoup.
Regular expression for text formatting and price extraction.
Sends email notifications with price comparisons.
Continuous looping for periodic price checks.
Dependencies
Python 3.6 or higher
Requests: pip install requests
BeautifulSoup4: pip install beautifulsoup4
Selenium: pip install selenium
smtplib (standard library)
re (standard library)
json (standard library)
time (standard library)
Setup
Ensure Python 3.6+ is installed on your system.
Install the required dependencies using pip:

pip install requests beautifulsoup4 selenium

Clone this repository or download the script to your local machine.
Set up a configuration file (config.py) with your email credentials and other sensitive information.

Configuration
Create a config.py file with the following content:

EMAIL_SENDER = 'your-email@example.com'
EMAIL_PASSWORD = 'your-password'
EMAIL_RECEIVER = 'receiver-email@example.com'

Replace the placeholder values with your actual email details.

Usage
Run the script using:

python main.py
The script will start checking the prices on the specified websites and send email updates.

Important Notes
The script currently targets specific web elements for price extraction. If the website structure changes, the script might need updates.
The script runs in an infinite loop and sends emails periodically. To stop it, manually interrupt the execution.
Contributing
Feel free to fork this project and submit pull requests for improvements.

License
MIT License
