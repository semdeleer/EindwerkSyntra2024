import flet as ft
from pages.model import Model

class SignIn(ft.View):
    def __init__(self, page: ft.Page):
        super(SignIn, self).__init__(
            route="/signin",
            vertical_alignment="center",
            horizontal_alignment="center",
        )

        self.page = page
        self.username = ft.TextField(label="Username", autofocus=True)
        self.password = ft.TextField(label="Password", password=True)
        self.sign_in_btn = ft.ElevatedButton(
            content=ft.Text("Sign In"),
            on_click=self.sign_in,
        )

        self.controls = [
            ft.Text("Sign-In", size=24),
            self.username,
            self.password,
            self.sign_in_btn,
            ft.ElevatedButton(
                content=ft.Text("Back to Home"),
                on_click=lambda e: self.page.go("/"),
            ),
        ]

    def sign_in(self, e):
        user = Model.check_user(self.username.value, self.password.value)
        if user:
            user_session = Model.set_session(self.username.value)
            self.page.session.set("user_session", user_session.id)
            self.page.go("/products")
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Wrong credentials"))
            self.page.snack_bar.open = True
            self.page.update()
