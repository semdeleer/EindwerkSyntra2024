import flet as ft
from pages.startscreen import Startscreen
from pages.signin import SignIn  
from pages.products import Product
from pages.register import Register
from pages.cart import Cart

def main(page: ft.Page):
    def router(route):
        page.views.clear()

        if page.route == "/":
            start = Startscreen(page)
            page.views.append(start)
        if page.route == "/signin":
            sign = SignIn(page)
            page.views.append(sign)
        if page.route == "/register":
            reg = Register(page)
            page.views.append(reg)
        if page.route == "/products":
            prod = Product(page)
            page.views.append(prod)
        if page.route == "/cart":
            cart = Cart(page)
            page.views.append(cart)
        
        page.update()

    page.on_route_change = router
    page.go("/")


ft.app(target=main, assets_dir="assets")
