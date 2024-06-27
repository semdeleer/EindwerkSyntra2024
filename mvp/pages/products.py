import flet as ft
from pages.model import Model
import os

class Product(ft.View):
    def __init__(self, page: ft.Page):
        super(Product, self).__init__(route="/products")
        self.page = page
        self.initialize()

    def initialize(self):
        self.products = ft.Row(expand=True, scroll="auto", spacing=30)
        self.create_products()

        self.controls = [
            self.display_product_page_header(),
            ft.Text("Shop", size=32),
            ft.Text("Select items from the list below"),
            self.products,
            self.display_product_page_footer(),
        ]

    def display_product_page_footer(self):
        return ft.Row([ft.Text("Simple X Shop", size=10)], alignment="center")

    def display_product_page_header(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(
                        icon="shopping_cart_outlined",  
                        on_click=lambda e: self.page.go("/cart"),
                        icon_size=18,
                    ),
                    ft.IconButton(
                        icon="logout",  
                        on_click=lambda e: self.page.go("/"),
                        icon_size=18,
                    ),
                ],
                alignment="spaceBetween",
            )
        )

    def create_products(self, products: dict = Model.get_products()):
        for _, values in products.items():
            name = values.get("name", "")
            description = values.get("description", "")
            idd = values.get("id", 0)
            price = self.create_product_event(values.get("price", ""), idd)

            texts = self.create_product_text(name, description)
            image_path = self.get_image_path(name)

            self.create_full_item_view(image_path, texts, price)

    def create_full_item_view(self, image_path, texts, price):
        item = ft.Column()

        item.controls.append(self.create_product_image(image_path))
        item.controls.append(self.create_product_container(4, texts))
        item.controls.append(self.create_product_container(1, price))

        self.products.controls.append(self.create_item_wrapper(item))

    def create_item_wrapper(self, item: ft.Column):
        return ft.Container(
            width=250, height=450, content=item, padding=8, border_radius=6
        )

    def create_product_text(self, name: str, description: str):
        return ft.Column([ft.Text(name, size=18), ft.Text(description, size=11)])

    def create_product_event(self, price: str, idd: int):
        return ft.Row(
            [
                ft.Text(price, size=14),
                ft.IconButton(
                    icon="add_shopping_cart_outlined",
                    on_click=lambda e: self.add_to_cart(idd),
                    icon_size=18,
                )
            ],
            alignment="spaceBetween",
        )

    def create_product_container(self, expand: int, control: ft.Control):
        return ft.Container(content=control, expand=expand, padding=5)

    def create_product_image(self, image_path: str):
        return ft.Image(src=image_path, width=200, height=200, fit="contain")

    def get_image_path(self, product_name: str):
        # Assuming image folder is in the same directory as this script
        return f"mvp/images/{product_name}.webp"

    def add_to_cart(self, product_id: int):
        user_session = self.page.session.get("user_session")
        if user_session:
            Model.add_to_cart(user_session, product_id)
            self.page.snack_bar = ft.SnackBar(ft.Text("Product added to cart"))
            self.page.snack_bar.open = True
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please sign in first"))
            self.page.snack_bar.open = True
        self.page.update()
