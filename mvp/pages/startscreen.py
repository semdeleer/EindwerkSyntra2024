import flet as ft

class Startscreen(ft.View):
    def __init__(self, page: ft.Page):
        super(Startscreen, self).__init__(
            route="/", horizontal_alignment="center", vertical_alignment="center"
        )

        self.page = page

        self.cart_logo = ft.Icon(name="shopping_cart_outlined", size=64)
        self.title = ft.Text("SIMPLE STORE".upper(), size=28, weight="bold")

        self.signin_page_btn = ft.ElevatedButton(
            content=ft.Text("Sign-In", size=14),
            width=180,
            height=54,
            style=ft.ButtonStyle(
                bgcolor={"": "#202020"},
                shape={"": ft.RoundedRectangleBorder(radius=8)},
                side={"": ft.BorderSide(2, "white54")},
            ),
            on_click=lambda e: self.page.go("/signin"),
        )

        self.register_page_btn = ft.ElevatedButton(
            content=ft.Text("Register", size=14),
            width=180,
            height=54,
            style=ft.ButtonStyle(
                bgcolor={"": "#202020"},
                shape={"": ft.RoundedRectangleBorder(radius=8)},
                side={"": ft.BorderSide(2, "white54")},
            ),
            on_click=lambda e: self.page.go("/register"),
        )

        self.controls = [
            self.cart_logo,
            ft.Divider(height=25, color="transparent"),
            self.title,
            ft.Divider(height=10, color="transparent"),
            self.signin_page_btn,
            ft.Divider(height=10, color="transparent"),
            self.register_page_btn,
        ]

