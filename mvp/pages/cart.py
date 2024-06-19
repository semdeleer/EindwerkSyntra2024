import flet as ft
from pages.model import Model

class Cart(ft.View):
    def __init__(self, page: ft.Page):
        super(Cart, self).__init__(route="/cart")
        self.page = page
        self.initilize()

    def initilize(self):
        self.cart_items = ft.Column(spacing=20)
        self.create_cart()

        self.controls = [
            ft.Row(
                [
                    ft.IconButton(
                        "arrow_back_ios_new_outlined",
                        on_click=lambda e: self.page.go("/products"),
                        icon_size=16,
                    )
                ],
                alignment="spaceBetween",
            ),
            ft.Text("Cart", size=32),
            ft.Text("Your cart items"),
            self.cart_items,
            ft.ElevatedButton(text="Checkout", on_click=self.checkout),
        ]

    def create_cart(self):
        user_session = self.page.session.get("user_session")
        if user_session:
            cart = Model.get_cart(user_session)
            self.cart_items.controls.clear()
            for _, values in cart.items():
                quantity = self.create_item_quantity(values["quantity"])
                name = self.create_item_name(values["name"])
                price = self.create_item_price(values["price"])
                self.compile_cart_item(quantity, name, price)
        else:
            self.cart_items.controls.append(ft.Text("Your cart is empty or you are not signed in."))

    def create_cart_item(self):
        return ft.Row(alignment="spaceBetween")

    def compile_cart_item(self, quantity, name, price):
        row = self.create_cart_item()

        row.controls.append(name)
        row.controls.append(quantity)
        row.controls.append(price)

        self.cart_items.controls.append(self.create_item_wrap(row))

    def create_item_wrap(self, control: ft.Control):
        return ft.Container(
            content=control,
            padding=10,
            border=ft.border.all(1, "white10"),
            border_radius=6,
        )

    def create_item_quantity(self, quantity: int):
        return ft.Text(f"{quantity} X")

    def create_item_name(self, name: str):
        return ft.Text(name, size=16)

    def create_item_price(self, price: int):
        return ft.Text(f"${price}")

    def checkout(self, e):
        user_session = self.page.session.get("user_session")
        if user_session:
            result = Model.checkout(user_session)
            if result:
                self.page.snack_bar = ft.SnackBar(ft.Text("Checkout successful"))
                self.page.snack_bar.open = True
                self.page.go("/products")
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Checkout failed, please try again."))
                self.page.snack_bar.open = True
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please sign in first"))
            self.page.snack_bar.open = True
        self.page.update()
