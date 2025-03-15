from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
from faker import Faker

fake = Faker()

# Random user details
first_name = fake.first_name()
last_name = fake.last_name()
password = fake.password(length=12)
dob_day = str(random.randint(1, 28))
dob_month = str(random.randint(1, 12))
dob_year = str(random.randint(1985, 2003))

# Manually enter email
email = input("\n📧 Enter your email: ")
gender = input("🚻 Enter gender (male/female): ").strip().lower()

# Setup Selenium WebDriver (Make sure you have Chrome and Chromedriver installed)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Open browser in fullscreen
driver = webdriver.Chrome(options=options)

# Open Facebook Signup Page
driver.get("https://www.facebook.com/r.php?entry_point=login")
time.sleep(3)  # Wait for page to load

# Fill in the signup form
driver.find_element(By.NAME, "firstname").send_keys(first_name)
driver.find_element(By.NAME, "lastname").send_keys(last_name)
driver.find_element(By.NAME, "reg_email__").send_keys(email)
driver.find_element(By.NAME, "reg_passwd__").send_keys(password)
driver.find_element(By.NAME, "birthday_day").send_keys(dob_day)
driver.find_element(By.NAME, "birthday_month").send_keys(dob_month)
driver.find_element(By.NAME, "birthday_year").send_keys(dob_year)

# Select gender
if gender == "male":
    driver.find_element(By.XPATH, "//input[@value='2']").click()
elif gender == "female":
    driver.find_element(By.XPATH, "//input[@value='1']").click()

# Submit the form
driver.find_element(By.NAME, "websubmit").click()
time.sleep(5)  # Wait for processing

print(f"\n✅ Signup Submitted! Check {email} for OTP.")

# Wait for OTP input manually
otp_code = input("\n📥 Enter the OTP received in email: ")

# Fill in OTP
otp_input = driver.find_element(By.NAME, "code")  # Locate OTP field
otp_input.send_keys(otp_code)
otp_input.send_keys(Keys.RETURN)

time.sleep(5)  # Wait for confirmation

# Check if signup was successful
if "confirmed" in driver.page_source.lower():
    print("✅ Email Confirmed Successfully!")
else:
    print("❌ Email Confirmation Failed! Check OTP and try again.")

# Keep browser open for review
input("\nPress Enter to close the browser...")
driver.quit()
