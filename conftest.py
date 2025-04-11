import pytest
from playwright.sync_api import sync_playwright

# staci, kdyz zadam conftest.py a test_projekt.py do stejneho adresare?

# DEF PROHLÍŽEČE CHROME
@pytest.fixture(scope="session")
def browser():
   with sync_playwright() as playwright:  # správně použít sync_playwright
        browser = playwright.chromium.launch(headless=False)  # Otevře prohlížeč
        yield browser  # Vrátí prohlížeč pro testy
        browser.close()
        
# DEF NOVEHO PRÁZDNÉHO OKNA
@pytest.fixture()
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()

