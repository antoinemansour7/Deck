import pytest
from scraper import login_to_site

def test_login():
    """Tests if the login function works correctly"""
    result = login_to_site()
    assert result == "Login successful!", "❌ Login test failed!"