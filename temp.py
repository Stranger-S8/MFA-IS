import firebase_admin
from firebase_admin import credentials, auth
import random
import smtplib

# Initialize Firebase Admin SDK
def initialize_firebase():
    cred = credentials.Certificate("key.json")  # Replace with your Firebase Admin SDK JSON file path
    firebase_admin.initialize_app(cred)

# Function to register a new user
def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        print(f"User {email} created successfully.")
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

# Function to generate a random verification code
def generate_code():
    return str(random.randint(100000, 999999))

# Function to send email with the verification code
def send_email_verification(email, code):
    try:
        sender_email = "zeeshanchudri1234@gmail.com"  # Replace with your email
        sender_password = "aabu jidy xrpc bpip"  # Replace with your email password
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Set up the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Prepare and send the email
        subject = "Your Verification Code"
        body = f"Your verification code is: {code}"
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, email, message)
        server.quit()
        print(f"Verification code sent to {email}.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to verify the code entered by the user
def verify_code(input_code, sent_code):
    return input_code == sent_code

# Main login flow
def user_login_flow():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    # Step 1: Register the user
    user = register_user(email, password)
    if user is None:
        return

    # Step 2: Generate and send verification code
    code = generate_code()
    send_email_verification(email, code)

    # Step 3: Verify the code
    input_code = input("Enter the verification code sent to your email: ")
    if verify_code(input_code, code):
        print("Login successful!")
    else:
        print("Invalid code. Login failed.")

# Entry point
if __name__ == "__main__":
    # Step 1: Initialize Firebase
    initialize_firebase()

    # Step 2: Start the user login flow
    send_email_verification("stranger1122r@gmail.com", "123456")
