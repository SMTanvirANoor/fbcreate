import time
import random
from faker import Faker
from playwright.sync_api import sync_playwright

fake = Faker()

# Generate Random User Data
first_name = fake.first_name()
last_name = fake.last_name()
password = fake.password(length=12)
dob_day = str(random.randint(1, 28))
dob_month = str(random.randint(1, 12))
dob_year = str(random.randint(1985, 2003))

# Get manual email input
email = input("\n📧 Enter your email: ")
gender = input("🚻 Enter gender (male/female): ").strip().lower()

# Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set headless=True if you don't want UI
    page = browser.new_page()

    # Open Facebook Signup Page
    page.goto("https://www.facebook.com/r.php?entry_point=login")
    time.sleep(3)

    # Fill the form
    page.fill("input[name='firstname']", first_name)
    page.fill("input[name='lastname']", last_name)
    page.fill("input[name='reg_email__']", email)
    page.fill("input[name='reg_passwd__']", password)
    page.select_option("select[name='birthday_day']", dob_day)
    page.select_option("select[name='birthday_month']", dob_month)
    page.select_option("select[name='birthday_year']", dob_year)

    # Select Gender
    if gender == "male":
        page.click("input[value='2']")
    elif gender == "female":
        page.click("input[value='1']")

    # Submit the form
    page.click("button[name='websubmit']")
    time.sleep(5)

    print(f"\n✅ Signup Submitted! Check {email} for OTP.")

    # Manually enter OTP
    otp_code = input("\n📥 Enter the OTP received in email: ")

    # Fill in OTP and confirm
    page.fill("input[name='code']", otp_code)
    page.press("input[name='code']", "Enter")

    time.sleep(5)

    # Check if confirmation was successful
    if "confirmed" in page.content().lower():
        print("✅ Email Confirmed Successfully!")
    else:
        print("❌ Email Confirmation Failed! Check OTP and try again.")

    input("\nPress Enter to close the browser...")
    browser.close()
