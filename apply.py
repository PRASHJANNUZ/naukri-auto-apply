from playwright.sync_api import sync_playwright
import os
import time

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://www.naukri.com/nlogin/login")

    page.fill("#usernameField", EMAIL)
    page.fill("#passwordField", PASSWORD)

    page.click("button[type='submit']")
    page.wait_for_timeout(8000)

    # Go to profile
    page.goto("https://www.naukri.com/mnjuser/profile")

    page.wait_for_timeout(5000)

    print("Profile refreshed")

    # Search Java jobs
    page.goto("https://www.naukri.com/java-developer-jobs")

    page.wait_for_timeout(5000)

    jobs = page.locator("a.title").all()

    count = 0

    for job in jobs:

        if count >= 20:
            break

        try:
            job.click()
            page.wait_for_timeout(4000)

            apply_btn = page.locator("button:has-text('Apply')")
            apply_btn.click()

            print("Applied to job")

            count += 1

            page.wait_for_timeout(4000)

        except:
            pass

    browser.close()
