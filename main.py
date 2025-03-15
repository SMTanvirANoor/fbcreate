import requests
import random
import string
from faker import Faker
from bs4 import BeautifulSoup

fake = Faker()

# Facebook URLs
FB_SIGNUP_URL = "https://www.facebook.com/r.php?entry_point=login"
FB_CONFIRM_URL = "https://www.facebook.com/confirmemail.php"

# Random User-Agent List
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36",
]

# Generate Random User Data
def generate_user():
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = input("\n📧 Enter your email: ")  # Manual email input
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    dob = f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(1985, 2003)}"
    gender = input("🚻 Enter gender (male/female): ").strip().lower()

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "dob": dob,
        "gender": gender,
    }

# Extract CSRF Tokens
def get_csrf_tokens(session):
    response = session.get("https://www.facebook.com/")
    soup = BeautifulSoup(response.text, "html.parser")
    
    fb_dtsg = soup.find("input", {"name": "fb_dtsg"})["value"] if soup.find("input", {"name": "fb_dtsg"}) else None
    jazoest = soup.find("input", {"name": "jazoest"})["value"] if soup.find("input", {"name": "jazoest"}) else None
    
    return fb_dtsg, jazoest

# Simulate Signup Request
def signup_facebook():
    user_data = generate_user()
    
    session = requests.Session()
    fb_dtsg, jazoest = get_csrf_tokens(session)

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://www.facebook.com/",
    }

    payload = {
        "firstname": user_data["first_name"],
        "lastname": user_data["last_name"],
        "reg_email__": user_data["email"],
        "reg_passwd__": user_data["password"],
        "birthday_day": user_data["dob"].split("/")[0],
        "birthday_month": user_data["dob"].split("/")[1],
        "birthday_year": user_data["dob"].split("/")[2],
        "sex": "1" if user_data["gender"] == "female" else "2",
        "submit": "Sign Up",
        "fb_dtsg": fb_dtsg,
        "jazoest": jazoest,
    }

    response = session.post(FB_SIGNUP_URL, headers=headers, data=payload)

    print("\n🔹 **Signup Response:**")
    print(response.text[:1000])  # Debugging: Show first 1000 chars of response

    if "checkpoint" in response.text.lower():
        print("🚨 Facebook detected a security checkpoint (possible block or phone verification needed).")
        return

    if response.status_code == 200:
        print(f"\n✅ Signup Successful! Check your email for OTP.")
        print(f"🔑 Password: {user_data['password']}")

        otp_code = input("\n📥 Enter the OTP received in email: ")

        confirm_payload = {
            "code": otp_code,
            "fb_dtsg": fb_dtsg,
            "jazoest": jazoest,
            "submit[Submit Code]": "Confirm"
        }

        confirm_response = session.post(FB_CONFIRM_URL, headers=headers, data=confirm_payload)

        print("\n🔹 **OTP Submission Response:**")
        print(confirm_response.text[:1000])  # Debugging: Show response from Facebook

        if "confirmed" in confirm_response.text.lower():
            print("✅ Email Confirmed Successfully!")
        else:
            print("❌ Email Confirmation Failed! Check OTP and try again.")

    else:
        print(f"\n❌ Signup Failed ({response.status_code}) - {response.text}")

# Run Signup
signup_facebook()
