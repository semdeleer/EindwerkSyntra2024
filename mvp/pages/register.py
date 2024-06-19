import flet as ft
from pages.model import Model

class Register(ft.View):
    def __init__(self, page: ft.Page):
        super(Register, self).__init__(route="/register")
        self.page = page
        self.action()

    def action(self):
        self.username = ft.TextField(label="Username", autofocus=True)
        self.email = ft.TextField(label="Email")
        self.password = ft.TextField(label="Password", password=True)
        self.controls = [
            ft.Text("Register", size=24),
            self.username,
            self.email,
            self.password,
            ft.ElevatedButton(
                content=ft.Text("Register"),
                on_click=self.register,
            ),
            ft.ElevatedButton(
                content=ft.Text("Back to Home"),
                on_click=lambda e: self.page.go("/"),
            ),
        ]
    def register(self, e):
        if Model.add_user(self.username.value, self.password.value, self.email.value):
            self.page.snack_bar = ft.SnackBar(ft.Text("Registration successful. Please sign in."))
            self.page.snack_bar.open = True
            self.page.go("/signin")
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Username already exists."))
            self.page.snack_bar.open = True
        self.page.update()