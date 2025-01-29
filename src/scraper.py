from playwright.sync_api import sync_playwright
import time

# Define credentials
USERNAME = "admin"
PASSWORD = "password123"
MFA_CODE = "123456"  # Predefined MFA code for testing

def login_to_site():
    """Automates the login process with Advanced 2FA"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set True to run in headless mode
        page = browser.new_page()

        # Step 1: Open the login page
        page.goto("https://deck-dev-eastus2-academy.yellowrock-2749f805.eastus2.azurecontainerapps.io/")

        # Step 2: Click on 'Advanced 2FA' login button
        page.click("text='Try Advanced 2FA'")  # Finds button with text and clicks it

        page.click("text='Allow all cookies'")  # Finds button with text and clicks it

        # Step 3: Fill in the username and password
        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        
        # Step 4: Click the "Continue to MFA Selection" button
        page.click("text='Continue to MFA Selection'")
        time.sleep(2)  # Wait for the MFA selection page to load

        # Step 5: Wait for and select the MFA method (e.g., Email)
        page.wait_for_selector("text='Select'", timeout=10000)  # Ensure MFA selection is available
        mfa_buttons = page.locator("text='Select'")  # Get all "Select" buttons

        if mfa_buttons.count() > 0:
            mfa_buttons.nth(0).click()  # Click the first available MFA method (adjust index if needed)
        else:
            print("No MFA method found!")
            browser.close()
            return  # Exit the function if no MFA method is found

        time.sleep(3)  # Wait for transition to the MFA code input page

     # Step 6: Wait for the MFA input field and enter the verification code
        page.wait_for_selector("#mfa_code", timeout=10000)  # Wait for the correct input field
        page.fill("#mfa_code", MFA_CODE)

        time.sleep(2)  # Small delay before clicking the button

        # Step 6.1: Click the "Verify" button to submit MFA code
        page.click("button[type='submit']")  # Clicks the verify button

        time.sleep(2)  # Wait for redirection to dashboard

        # Step 7: Verify if login was successful by checking for the correct page elements
        page.wait_for_load_state("networkidle")  # Ensures all content is loaded

        if page.is_visible("h2:text('PowerCo Dashboard')") or page.is_visible("text='Welcome back, John Smith'"):
            print("Login successful!")
            return "Login successful!"
        else:
            print("Login failed!")
            return "Login failed!"

        browser.close()  # ✅ Now inside the 'with' block, ensuring Playwright stops properly

# Run the function for testing
if __name__ == "__main__":
    login_to_site()