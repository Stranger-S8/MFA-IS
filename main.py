import smtplib
import customtkinter as ctk
from PIL import Image
import tkinter as tk
import firebase_admin
from firebase_admin import  credentials
from tkinter import messagebox
import random
import time
from firebase_admin import firestore
from encryption import  Credentials

class Main(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.width = 1366
        self.height = 768

        self.creds = credentials.Certificate("key.json")
        firebase_admin.initialize_app(self.creds)
        self.a = Credentials()
        self.admin = self.a.load_decrypted_credentials()

        self.db = firestore.client()

        self.find_center()
        self.title("Multi Factor Authentication")
        self.minsize(1366, 768)
        self.geometry(f"{self.width}x{self.height}+{self.c_x}+{self.c_y}")
        self.resizable(False, False)
        self.login_page()

        self.verification_code = None
        self.expiration_time = None

    def find_center(self):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()

        self.c_x = int(width / 2 - self.width / 2)
        self.c_y = int(height / 2 - self.height / 2)

    def generate_code(self):
        return str(random.randint(100000, 999999))

    def send_email_verification(self, email):
        try:
            sender_email = self.admin[0]
            sender_password = self.admin[1]
            smtp_server = "smtp.gmail.com"
            smtp_port = 587

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            self.verification_code = self.generate_code()
            self.expiration_time = time.time() + 180



            subject = "Your Verification Code"
            body = f"Your Verification Code is : {self.verification_code}"
            message = f"Subject : {subject}\n\n{body}"

            server.sendmail(sender_email, email, message)
            server.quit()
            print(f"Verification Code Successfully Sent to : {email}")
        except Exception as e:
            print(f"Error Sending Email : {e}")

    def register_user(self, email, password):
        existing_user = self.db.collection("users").document(email).get()

        if existing_user.exists:
            messagebox.showwarning("Error", "User Already Exists")
        else:
            A = self.db.collection("users").document(email).set({
                "email": email,
                "password": password
        })

    def verify_code(self, user_code):
        if time.time() > self.expiration_time:
            messagebox.showerror("Timeout", "Verification Code has Expired")
        elif self.verification_code == user_code:
            messagebox.showinfo("Success", "Verification Successful")
            self.mainpage()
        else:
            messagebox.showerror("Error", "Invalid Verification Code")

    def mainpage(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="#c4d5e1")
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        label = ctk.CTkLabel(self.main_frame, text="تم یہاں کیا کر رہے ہو بیوقوف، واپس جاؤ اور اپنا کام کرو", font=("Noto Nastaliq Urdu", 30))
        label.place(relx=0.3, rely=0.45)


    def next_to_login(self, email, password):
        if hasattr(self, "login_window_left"):
            self.login_window_left.destroy()

        self.send_email_verification(email)

        self.login_window_ver = ctk.CTkFrame(self.login_window_log, fg_color="#ffffff", corner_radius=0)
        self.login_window_ver.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        self.heading_label = ctk.CTkLabel(
            self.login_window_ver,
            text="Enter the Verification Code",
            text_color="#15B4BF",
            fg_color="#ffffff",
            font=("Roboto", 28, "bold"),
        )
        self.heading_label.place(relx=0.15, rely=0.2)

        code_entry = ctk.CTkEntry(self.login_window_ver, placeholder_text="Enter 6 Digit Code", corner_radius=10)
        code_entry.place(relx=0.15, rely=0.4, relwidth=0.7, relheight=0.08)

        self.login_button = ctk.CTkButton(
            self.login_window_ver,
            text="LOGIN",
            fg_color="#15B4BF",
            text_color="#ffffff",
            hover=False,
            cursor="hand2",
            corner_radius=40,
            font=("Roboto", 20, "bold"),
            command=lambda: self.verify_code(code_entry.get())
        )
        self.login_button.place(relx=0.25, rely=0.65, relwidth=0.5, relheight=0.08)

    def process_credentials(self, email, password):
        check = self.db.collection("users").document(email).get()

        if check.exists:
            if check.to_dict()["password"] == password:
                self.next_to_login(email, password)
            else:
                messagebox.showerror("Error", "Invalid Password")
        else:
            messagebox.showerror("Error", "User does not exist")

    def login_page(self):
        self.login_frame = ctk.CTkFrame(self, fg_color="#c4d5e1")
        self.login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.login_bg_image = ctk.CTkImage(light_image=(Image.open("images/login_bg.jpg")),
                                           size=(self.width, self.height))

        self.login_bg_image_lbl = ctk.CTkLabel(self.login_frame, text="", image=self.login_bg_image)
        self.login_bg_image_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.login_window_log = ctk.CTkFrame(self.login_frame, fg_color="#ffffff", corner_radius=0)
        self.login_window_log.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.7)

        self.login_window_left = ctk.CTkFrame(self.login_window_log, fg_color="#ffffff", corner_radius=0)
        self.login_window_left.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        self.login_window_right = ctk.CTkFrame(self.login_window_log, fg_color="#34D1DC", corner_radius=0)
        self.login_window_right.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        temp = Image.open("images/login_head_pic.png")
        self.login_image = ctk.CTkImage(light_image=temp, size=(500, 355))
        self.login_image_label = ctk.CTkLabel(self.login_window_right, text="", image=self.login_image)
        self.login_image_label.place(relx=0.05, rely=0)

        self.login_heading_label = ctk.CTkLabel(
            self.login_window_right,
            text="WELCOME",
            fg_color="#34D1DC",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Roboto", size=30, weight="bold"),
        )
        self.login_heading_label.place(relx=0.2, rely=0.7)

        self.login_slogan_label = ctk.CTkLabel(
            self.login_window_right,
            text="Your Shop, Our Smarts – Strange Solutions Inside",
            fg_color="#34D1DC",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Roboto", size=12, weight="bold"),
        )
        self.login_slogan_label.place(relx=0.2, rely=0.76)

        self.heading_account = ctk.CTkLabel(
            self.login_window_left,
            text="Hello! Welcome Back",
            text_color="#15B4BF",
            fg_color="#ffffff",
            font=("Roboto", 30, "bold"),
        )
        self.heading_account.place(relx=0.25, rely=0.1)

        email_entry = ctk.CTkEntry(self.login_window_left, placeholder_text="Email", corner_radius=20)
        email_entry.place(relx=0.15, rely=0.3, relwidth=0.7, relheight=0.08)

        password_entry = ctk.CTkEntry(self.login_window_left, placeholder_text="Password",
                                           corner_radius=20, show="*")
        password_entry.place(relx=0.15, rely=0.42, relwidth=0.7, relheight=0.08)

        self.proceed_button = ctk.CTkButton(
            self.login_window_left,
            text="PROCEED",
            fg_color="#15B4BF",
            text_color="#ffffff",
            hover=False,
            cursor="hand2",
            corner_radius=40,
            font=("Roboto", 20, "bold"),
            command=lambda: self.process_credentials(email_entry.get(), password_entry.get())
        )
        self.proceed_button.place(relx=0.25, rely=0.65, relwidth=0.5, relheight=0.08)


if __name__ == "__main__":
    App = Main()
    App.mainloop()

# App = Main()
# App.register_user("stranger1122r@gmail.com", "12345")