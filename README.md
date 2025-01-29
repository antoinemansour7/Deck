# Deck
Web scraping project using Playwright


# PowerCo Data Scraper  

This script uses Playwright to log in to PowerCo's customer dashboard, extract account data, and download bills and statements.  

## Features  
- Logs in using Advanced 2FA authentication  
- Extracts account information (balance, due dates, usage)  
- Downloads bills and recent statements  
- Handles multiple pages of statements  
- Saves extracted data in JSON format  

## Installation  

### Prerequisites  
- Python 3.8+  
- Google Chrome / Chromium  
- pip (Python Package Manager)  

### Install Dependencies  
Run the following command:  
```sh
pip install -r requirements.txt

Install Playwright Browsers
```sh
playwright install


Create a file named config.py in the project directory and add the following:
# Configuration file for scraper  

USERNAME = "admin"
PASSWORD = "password123"
MFA_CODE = "123456" 

BASE_URL = "https://deck-dev-eastus2-academy.yellowrock-2749f805.eastus2.azurecontainerapps.io/"  

DOWNLOAD_DIR = "downloads"  

Running the Script
python scraper.py

