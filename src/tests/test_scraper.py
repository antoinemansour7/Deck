import pytest
from playwright.sync_api import sync_playwright
import config
from scraper import login_to_site, extract_and_download_data, download_all_statements


@pytest.fixture(scope="module")
def browser_context():
    """Set up Playwright browser instance for testing."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run in headless mode for testing
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        yield page  # Provide the page instance to tests
        browser.close()


def test_login(browser_context):
    """Test the login function."""
    page = browser_context
    result = login_to_site(page)
    assert result is True, "Login test failed!"


def test_extract_data(browser_context):
    """Test if account data extraction works correctly."""
    page = browser_context
    page.goto(config.BASE_URL)

    # Perform login first
    assert login_to_site(page), "Login failed, cannot test data extraction."

    # Extract data
    extract_and_download_data(page)

    # Verify that dashboard_data.json exists and contains data
    import json
    with open("dashboard_data.json", "r") as f:
        data = json.load(f)

    assert isinstance(data, list), "Extracted data is not a list."
    assert len(data) > 0, "No account data found."
    assert "address" in data[0], "Missing expected field in extracted data."
    assert "account_number" in data[0], "Missing expected field in extracted data."
    print(" Data extraction test passed!")


def test_statement_downloads(browser_context):
    """Test downloading of statements and pagination handling."""
    page = browser_context
    page.goto(config.BASE_URL)

    # Perform login first
    assert login_to_site(page), "Login failed, cannot test downloads."

    # Run statement extraction & download
    download_all_statements(page)

    import os
    downloaded_files = os.listdir(config.DOWNLOAD_DIR)
    
    assert any("statement_" in file for file in downloaded_files), "No statements downloaded."
    print(" Statement download test passed!")


if __name__ == "__main__":
    pytest.main()