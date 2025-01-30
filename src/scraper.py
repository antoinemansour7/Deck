from playwright.sync_api import sync_playwright
import time
import json
import os
import re
import pdfplumber  # To extract text from PDFs
import config  # Import configuration settings

# Ensure the download directory exists
if not os.path.exists(config.DOWNLOAD_DIR):
    os.makedirs(config.DOWNLOAD_DIR)

def login_to_site(page):
    """Logs into Deck Academy using Advanced 2FA and returns login status."""
    page.goto(config.BASE_URL)

    # Click 'Advanced 2FA' login button
    page.click("text='Try Advanced 2FA'")

    # Accept cookies if present
    try:
        page.click("text='Allow all cookies'", timeout=5000)
    except:
        print("Cookies banner not found, continuing...")

    # Fill in credentials
    page.fill('input[name="username"]', config.USERNAME)
    page.fill('input[name="password"]', config.PASSWORD)

    # Click "Continue to MFA Selection" button
    page.click("text='Continue to MFA Selection'")
    time.sleep(2)

    # Select MFA method
    try:
        page.wait_for_selector("text='Select'", timeout=10000)
        mfa_buttons = page.locator("text='Select'")
        if mfa_buttons.count() > 0:
            mfa_buttons.nth(0).click()
        else:
            print("No MFA method found!")
            return False
    except:
        print("Error: MFA method selection timeout.")
        return False

    time.sleep(3)

    # Enter MFA code
    try:
        page.wait_for_selector("#mfa_code", timeout=10000)
        page.fill("#mfa_code", config.MFA_CODE)
        time.sleep(2)
        page.click("button[type='submit']")
        time.sleep(3)
    except:
        print("Error: MFA input field not found.")
        return False

    # Verify login success
    page.wait_for_load_state("networkidle")
    if not (page.is_visible("text='PowerCo Dashboard'") or page.is_visible("text='Welcome back, John Smith'")):
        print("Login failed!")
        return False

    print("Login successful!")
    return True




import pdfplumber
import json
import os
import re

def extract_data_from_pdf(pdf_path):
    """Extracts structured data from a PDF bill and saves it as JSON."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

        data = {}

        # Extract Account Number
        match = re.search(r"Account No\.?:?\s*(\d+)", text, re.IGNORECASE)
        if match:
            data["account_number"] = match.group(1)

        # Extract Service Address
        match = re.search(r"Service Address:\s*([\w\s,]+)", text, re.IGNORECASE)
        if match:
            data["service_address"] = match.group(1).strip()

        # Extract Water & Sewer Charges
        match = re.search(r"Water/Sewer Services(?:.*?)?\$([\d,]+\.\d{2})", text, re.IGNORECASE)
        if match:
            data["water_sewer_charges"] = float(match.group(1).replace(",", ""))

        # Extract Solid Waste Charges
        match = re.search(r"Solid Waste Management Services(?:.*?)?\$([\d,]+\.\d{2})", text, re.IGNORECASE)
        if match:
            data["solid_waste_charges"] = float(match.group(1).replace(",", ""))

        # Extract Total Charges
        match = re.search(r"Total\s*\$([\d,]+\.\d{2})", text, re.IGNORECASE)
        if match:
            data["total_charges"] = float(match.group(1).replace(",", ""))


        match = re.search(r"Consumption\s*([\d,]+\.\d{2})\s*m3", text, re.IGNORECASE)
        if match:
            data["consumption_m3"] = float(match.group(1).replace(",", ""))

        # Save extracted data to JSON
        json_filename = os.path.splitext(pdf_path)[0] + ".json"
        with open(json_filename, "w") as json_file:
            json.dump(data, json_file, indent=4)

    except Exception as e:
        pass  # Ignore errors silently

    
def download_all_statements(page):
    """Downloads all recent statements across multiple pages, ensuring unique filenames."""
    page.wait_for_selector("table tbody tr td a[href$='.pdf']")
    
    while True:
        statement_rows = page.locator("tbody tr")  # Get all statement rows
        
        for i in range(statement_rows.count()):
            try:
                row = statement_rows.nth(i)
                
                # Extract the account number and statement date
                account = row.locator("td:nth-child(1)").text_content().strip()  # First column
                statement_date = row.locator("td:nth-child(2)").text_content().strip()  # Second column
                
                # Format the filename as statement_ACCOUNTNUMBER_STATEMENTDATE.pdf
                formatted_date = statement_date.replace(" ", "")  # Remove spaces
                filename = f"statement_{account.replace(' ', '')}_{formatted_date}.pdf"

                # Click the download link
                with page.expect_download() as download_info:
                    row.locator("td:nth-child(5) a[href$='.pdf']").click()
                
                download = download_info.value
                download_path = os.path.join(config.DOWNLOAD_DIR, filename)
                download.save_as(download_path)
                print(f"Downloaded: {download_path}")

                # Extract data from the downloaded PDF
                extract_data_from_pdf(download_path)

            except Exception as e:
                print(f"Failed to download statement for {account} ({statement_date}): {e}")

        # Check for pagination and click "Next" if available
        next_button = page.locator("text='Next'")
        if next_button.is_visible():
            next_button.click()
            time.sleep(2)  # Delay to avoid rate-limiting
        else:
            break  # No more pages, exit the loop


def extract_and_download_data(page):
    """Extracts user account data and downloads bills/statements."""
    data = []
    accounts = page.locator("div.grid.md\\:grid-cols-2.gap-6.mb-8 > div.bg-white.rounded-lg.shadow-md.p-6")

    for i in range(accounts.count()):
        try:
            account = accounts.nth(i)
            address = account.locator("h3.text-xl.font-semibold.text-gray-800").text_content().strip()
            account_number = account.locator("p.text-gray-600").text_content().strip().replace("Account #:", "").strip()
            current_balance = account.locator("span.font-semibold").text_content().strip()
            due_date = account.locator("div.flex.justify-between:nth-child(2) > span:nth-child(2)").text_content().strip()
            last_month_usage = account.locator("div.flex.justify-between:nth-child(3) > span:nth-child(2)").text_content().strip()

            # Get the bill download link
            bill_link = account.locator("a.bg-blue-600").get_attribute("href")

            # Save extracted data
            data.append({
                "address": address,
                "account_number": account_number,
                "current_balance": current_balance,
                "due_date": due_date,
                "last_month_usage": last_month_usage,
                "bill_link": bill_link
            })

        except:
            print(f"Error extracting data for account {i+1}, skipping...")

    # Save extracted data to JSON
    with open("dashboard_data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("Extracted data saved to dashboard_data.json")

    # Download all bills
    for entry in data:
        try:
            if entry["bill_link"]:
                with page.expect_download() as download_info:
                    page.click(f"a[href='{entry['bill_link']}']")
                download = download_info.value
                download_path = os.path.join(config.DOWNLOAD_DIR, f"{entry['account_number']}_latest_bill.pdf")
                download.save_as(download_path)
                print(f"Downloaded: {download_path}")

                # Extract data from the downloaded PDF
                extract_data_from_pdf(download_path)

        except:
            print(f"Failed to download bill for {entry['account_number']}")

    # Download all recent statements
    download_all_statements(page)


def main():
    """Runs the login, checks authentication, and extracts data."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Run in visible mode
        context = browser.new_context(accept_downloads=True)  # Enable downloads
        page = context.new_page()

        if login_to_site(page):
            extract_and_download_data(page)
        else:
            print("Login failed, exiting...")

        browser.close()


if __name__ == "__main__":
    main()