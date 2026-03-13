from playwright.sync_api import sync_playwright
import os

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    )

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        viewport={"width": 1280, "height": 800}
    )

    page = context.new_page()

    print("Opening Naukri homepage")

    page.goto("https://www.naukri.com", timeout=60000)
    page.wait_for_load_state("networkidle")

    print("Opening login page")

    page.goto("https://www.naukri.com/nlogin/login", timeout=60000)

    page.wait_for_load_state("domcontentloaded")

    # Wait for email field
    page.wait_for_selector('input[placeholder="Enter your active Email ID / Username"]', timeout=60000)

    print("Entering login credentials")

    page.fill('input[placeholder="Enter your active Email ID / Username"]', EMAIL)
    page.fill('input[placeholder="Enter your password"]', PASSWORD)

    page.click('button[type="submit"]')

    page.wait_for_timeout(10000)

    print("Login attempted")

    # Visit profile to refresh activity
    page.goto("https://www.naukri.com/mnjuser/profile", timeout=60000)

    page.wait_for_load_state("networkidle")

    print("Profile opened successfully")

    browser.close()

print("Automation finished")
