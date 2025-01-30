# Deck
Web scraping project using Playwright

## PowerCo Data Scraper

This script uses Playwright to log in to PowerCo's customer dashboard, extract account data, and download bills and statements.

### Features
- Logs in using Advanced 2FA authentication
- Extracts account information (balance, due dates, usage)
- Downloads bills and recent statements
- Handles multiple pages of statements
- Saves extracted data in JSON format
- Converts downloaded PDFs to JSON

### Installation

#### Prerequisites
- Python 3.8+
- Google Chrome / Chromium
- pip (Python Package Manager)

#### Install Dependencies
Run the following command:
```sh
pip install -r requirements.txt
```

#### Install Playwright Browsers
Run the following command:
```sh
playwright install
```

#### Configuration
Create a file named `config.py` in the `src` directory and add the following:
```python
# Configuration file for scraper

USERNAME = "admin"
PASSWORD = "password123"
MFA_CODE = "123456"

BASE_URL = "https://deck-dev-eastus2-academy.yellowrock-2749f805.eastus2.azurecontainerapps.io/"

DOWNLOAD_DIR = "downloads"
```

### Running the Script
Navigate to the `src` directory and run the following command:
```sh
python scraper.py
```

### Usage
1. Ensure that the `config.py` file is correctly configured with your credentials and settings and is located in the `src` directory.
2. Navigate to the `src` directory.
3. Run the script using the command mentioned above.
4. The script will log in to the PowerCo dashboard, extract account data, and download bills and statements.
5. Extracted data will be saved in `dashboard_data.json` and downloaded files will be saved in the `downloads` directory.

### Testing
To run the tests, navigate to the `src/tests` directory and run the following command:
```sh
pytest test_scraper.py -s
```

### Troubleshooting
- **Timeout Errors**: If you encounter timeout errors, try increasing the timeout values in the script.
- **Login Issues**: Ensure that your credentials in `config.py` are correct.
- **Missing Elements**: If the script fails to find certain elements, verify that the selectors used in the script match the current structure of the website.
- **Dependencies**: Ensure all dependencies are installed correctly by running `pip install -r requirements.txt` and `playwright install`.



