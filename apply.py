from playwright.sync_api import sync_playwright
import os
import time

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )

    context = browser.new_context()
    page = context.new_page()

    print("Opening login page...")

    page.goto("https://www.naukri.com/nlogin/login", timeout=60000)

    page.wait_for_load_state("networkidle")

    # Wait for login fields
    page.wait_for_selector('input[type="text"]', timeout=60000)

    print("Entering credentials...")

    page.fill('input[type="text"]', EMAIL)
    page.fill('input[type="password"]', PASSWORD)

    page.click('button[type="submit"]')

    page.wait_for_timeout(8000)

    print("Login attempted")

    # Go to profile page
    page.goto("https://www.naukri.com/mnjuser/profile", timeout=60000)

    page.wait_for_load_state("networkidle")

    print("Profile page opened (this refreshes activity)")

    # Open job search
    page.goto("https://www.naukri.com/java-developer-jobs", timeout=60000)

    page.wait_for_load_state("networkidle")

    jobs = page.locator("a.title").all()

    applied = 0

    for job in jobs:

        if applied >= 10:
            break

        try:
            job.click()
            page.wait_for_timeout(4000)

            apply_btn = page.locator("button:has-text('Apply')")

            if apply_btn.count() > 0:
                apply_btn.first.click()
                applied += 1
                print("Applied to job", applied)

            page.wait_for_timeout(4000)

        except:
            print("Skipping job")
            continue

    browser.close()

print("Script completed")
