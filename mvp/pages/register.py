import flet as ft
from pages.model import Model
import string
import re


class Register(ft.View):
    def __init__(self, page: ft.Page):
        super(Register, self).__init__(route="/register")
        self.password_row = None
        self.email_row = None
        self.username_row = None
        self.password = None
        self.email = None
        self.username = None
        self.error_label_pw = None
        self.error_label_email = None
        self.valid_icon_pw = None
        self.valid_icon_email = None
        self.page = page
        self.action()

    def action(self):
        self.valid_icon_email = ft.Icon(color=ft.colors.GREEN_300, name=ft.icons.CHECK_CIRCLE_OUTLINED, visible=False)
        self.valid_icon_pw = ft.Icon(color=ft.colors.GREEN_300, name=ft.icons.CHECK_CIRCLE_OUTLINED, visible=False)
        self.error_label_email = ft.Text(value="", color=ft.colors.RED_300)
        self.error_label_pw = ft.Text(value="", color=ft.colors.RED_300)
        self.username = ft.TextField(label="Username", autofocus=True)
        self.email = ft.TextField(label="Email", on_change=self.email_checker)
        self.password = ft.TextField(label="Password", password=True, can_reveal_password=True,
                                     on_change=self.password_checker)

        self.username_row = ft.Row([self.username])
        self.email_row = ft.Row([self.email, self.valid_icon_email, self.error_label_email])
        self.password_row = ft.Row([self.password, self.valid_icon_pw, self.error_label_pw])

        self.controls = [
            ft.Text("Register", size=24),
            self.username_row,
            self.email_row,
            self.password_row,
            ft.ElevatedButton(
                content=ft.Text("Register"),
                on_click=self.register,
            ),
            ft.ElevatedButton(
                content=ft.Text("Back to Home"),
                on_click=lambda e: self.page.go("/"),
            ),
        ]

    def error_text_pw(self, message):
        if message == "Valid Password!":
            self.valid_icon_pw.visible = True
            self.error_label_pw.value = ""
        else:
            self.valid_icon_pw.visible = False
            self.error_label_pw.value = message
        self.update()

    def error_text_email(self, message):
        if message == "Valid Email!":
            self.valid_icon_email.visible = True
            self.error_label_email.value = ""
        else:
            self.valid_icon_email.visible = False
            self.error_label_email.value = message
        self.update()

    def password_checker(self, e):

        user_passwd = str(e.control.value)
        if len(user_passwd) < 12:
            self.error_text_pw("Password must be at least 12 characters long.")
            return

        contains_uppercase = contains_lowercase = contains_number = contains_punctuation = False

        for char in user_passwd:
            if char in string.ascii_uppercase:
                contains_uppercase = True
            elif char in string.ascii_lowercase:
                contains_lowercase = True
            elif char.isdigit():
                contains_number = True
            elif char in string.punctuation:
                contains_punctuation = True

        if not contains_uppercase:
            self.error_text_pw("Password must contain at least one uppercase letter.")
        elif not contains_lowercase:
            self.error_text_pw("Password must contain at least one lowercase letter.")
        elif not contains_number:
            self.error_text_pw("Password must contain at least one number.")
        elif not contains_punctuation:
            self.error_text_pw("Password must contain at least one symbol.")
        else:
            self.error_text_pw("Valid Password!")

    def email_checker(self, e):
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$'
        if re.match(email_pattern, e.control.value):
            self.error_text_email("Valid Email!")
            return
        else:
            self.error_text_email("Please enter a valid email address")
            return

    def register(self):
        if Model.add_user(self.username.value, self.password.value, self.email.value):
            self.page.snack_bar = ft.SnackBar(ft.Text("Registration successful. Please sign in."))
            self.page.snack_bar.open = True
            self.page.go("/signin")
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Username already exists."))
            self.page.snack_bar.open = True
        self.page.update()
