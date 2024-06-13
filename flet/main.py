import flet as ft
from db import write_to_db, session, Product as DBProduct, User as DBUser, CartItem as DBCartItem
from sqlalchemy.orm.exc import NoResultFound


class Landing(ft.View):
    def __init__(self, page: ft.Page):
        super(Landing, self).__init__(
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
            on_click=lambda e: self.page.go("/sign-in"),
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


class Model(object):
    @staticmethod
    def get_products():
        products = session.query(DBProduct).all()
        return {product.id: {
            "id": product.id,
            "img_src": product.img_src,
            "name": product.name,
            "description": product.description,
            "price": product.price
        } for product in products}

    @staticmethod
    def get_cart(user_id):
        cart_items = session.query(DBCartItem).filter(DBCartItem.user_id == user_id).all()
        return {item.product_id: {
            "id": item.product_id,
            "quantity": item.quantity,
            "name": item.product.name,
            "description": item.product.description,
            "price": item.product.price
        } for item in cart_items}

    @staticmethod
    def add_to_cart(user_id, product_id):
        try:
            cart_item = session.query(DBCartItem).filter(DBCartItem.user_id == user_id, DBCartItem.product_id == product_id).one()
            cart_item.quantity += 1
        except NoResultFound:
            cart_item = DBCartItem(user_id=user_id, product_id=product_id, quantity=1)
            session.add(cart_item)
        session.commit()

    @staticmethod
    def add_user(username: str, password: str, email: str):
        if session.query(DBUser).filter(DBUser.username == username).count() > 0:
            return False
        user = DBUser(username=username, password=password, email=email)
        session.add(user)
        session.commit()
        return True

    @staticmethod
    def check_user(username: str, password: str):
        user = session.query(DBUser).filter(DBUser.username == username, DBUser.password == password).first()
        return user is not None


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
            ft.ElevatedButton(
                content=ft.Text("Buy", size=14),
                width=180,
                height=54,
                on_click=self.buy_items,
            ),
        ]

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
                        icon="settings",
                        on_click=lambda e: self.page.go("/settings"),
                        icon_size=18,
                    ),
                ],
                alignment="spaceBetween",
            )
        )

    def display_product_page_footer(self):
        return ft.Row([ft.Text("Simple X Shop", size=10)], alignment="center")

    def create_products(self, products: dict = Model.get_products()):
        for _, values in products.items():
            img_src = self.create_product_image(values["img_src"])
            texts = self.create_product_text(values["name"], values["description"])
            price = self.create_product_event(values["price"], values["id"])

            item = ft.Column(
                [
                    ft.Container(content=img_src, expand=4, padding=5),
                    ft.Container(content=texts, expand=4, padding=5),
                    ft.Container(content=price, expand=1, padding=5),
                ]
            )

            self.products.controls.append(item)

    def create_product_image(self, img_path: str):
        return ft.Container(
            image_src=img_path, image_fit="fill", border_radius=6, padding=10
        )

    def create_product_text(self, name: str, description: str):
        return ft.Column([ft.Text(name, size=18), ft.Text(description, size=11)])

    def create_product_event(self, price: str, idd: str):
        return ft.Row(
            [
                ft.Text(price, size=14),
                ft.IconButton(
                    "add",
                    data=idd,
                    on_click=self.add_to_cart,
                ),
            ],
            alignment="spaceBetween",
        )

    def add_to_cart(self, e: ft.TapEvent):
        # Here, "current_user" should be replaced with the actual user ID
        current_user_id = 1  # Replace this with the actual logged-in user ID
        Model.add_to_cart(current_user_id, e.control.data)
        print(Model.get_cart(current_user_id))

    def buy_items(self, e: ft.TapEvent):
        self.page.go("/cart")  # Navigate to cart page after clicking Buy


class Cart(ft.View):
    def __init__(self, page: ft.Page):
        super(Cart, self).__init__(route="/cart")
        self.page = page
        self.initialize()

    def initialize(self):
        self.cart_items = ft.Column(expand=True, scroll="auto", spacing=10)
        self.controls = [
            ft.Text("Your Cart", size=24),
            self.cart_items,
            ft.ElevatedButton(
                content=ft.Text("Checkout"),
                on_click=self.checkout,
            ),
        ]
        self.update_cart()

    def update_cart(self):
        # Replace "current_user" with the actual user ID
        current_user_id = 1  # Replace this with the actual logged-in user ID
        current_user_cart = Model.get_cart(current_user_id)
        self.cart_items.controls.clear()

        for item_data in current_user_cart.values():
            item_name = item_data["name"]
            item_quantity = item_data["quantity"]
            item_price = item_data["price"]

            item_view = ft.Row(
                [
                    ft.Text(f"{item_name} x {item_quantity}", size=14),
                    ft.Text(f"Price: {item_price}", size=14),
                ],
                alignment="spaceBetween",
            )

            self.cart_items.controls.append(item_view)

    def checkout(self, e):
        # Implement checkout logic here
        self.page.go("/products")


class Settings(ft.View):
    def __init__(self, page: ft.Page):
        super(Settings, self).__init__(route="/settings")
        self.page = page
        self.initialize()

    def initialize(self):
        self.controls = [
            ft.Text("Settings", size=24),
            ft.ElevatedButton(
                content=ft.Text("View Purchases"),
                on_click=self.view_purchases,
            ),
            ft.ElevatedButton(
                content=ft.Text("Log Out"),
                on_click=self.log_out,
            ),
        ]

    def view_purchases(self, e):
        self.page.go("/purchases")  # Navigate to purchases page

    def log_out(self, e):
        self.page.go("/")  # Redirect to landing page on logout


class SignIn(ft.View):
    def __init__(self, page: ft.Page):
        super(SignIn, self).__init__(route="/sign-in")
        self.page = page
        self.initialize()

    def initialize(self):
        self.username = ft.TextField(label="Username")
        self.password = ft.TextField(label="Password", password=True)
        self.signin_button = ft.ElevatedButton(
            content=ft.Text("Sign In"),
            on_click=self.sign_in,
        )

        self.controls = [
            ft.Text("Sign In", size=24),
            self.username,
            self.password,
            self.signin_button,
        ]

    def sign_in(self, e):
        username = self.username.value
        password = self.password.value
        if Model.check_user(username, password):
            # Here you would set the logged-in user ID
            # This example assumes you have a way to store the logged-in user context
            self.page.go("/products")
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Invalid username or password"))
            self.page.snack_bar.open = True
            self.page.update()


class Register(ft.View):
    def __init__(self, page: ft.Page):
        super(Register, self).__init__(route="/register")
        self.page = page
        self.initialize()

    def initialize(self):
        self.username = ft.TextField(label="Username")
        self.password = ft.TextField(label="Password", password=True)
        self.email = ft.TextField(label="Email")
        self.register_button = ft.ElevatedButton(
            content=ft.Text("Register"),
            on_click=self.register,
        )

        self.controls = [
            ft.Text("Register", size=24),
            self.username,
            self.password,
            self.email,
            self.register_button,
        ]

    def register(self, e):
        username = self.username.value
        password = self.password.value
        email = self.email.value
        if Model.add_user(username, password, email):
            self.page.go("/products")
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Username already exists"))
            self.page.snack_bar.open = True
            self.page.update()


class Purchases(ft.View):
    def __init__(self, page: ft.Page):
        super(Purchases, self).__init__(route="/purchases")
        self.page = page
        self.initialize()

    def initialize(self):
        self.purchases_list = ft.Column(expand=True, scroll="auto", spacing=10)
        self.create_purchases_list()

        self.controls = [
            ft.Text("Your Purchases", size=24),
            ft.Text("Here are your purchased items:"),
            self.purchases_list,
            ft.ElevatedButton(
                content=ft.Text("Back to Products"),
                on_click=self.back_to_products,
            ),
        ]

    def create_purchases_list(self):
        current_user_id = 1  # Replace this with the actual logged-in user ID
        current_user_cart = Model.get_cart(current_user_id)
        for product_data in current_user_cart.values():
            item = ft.Row(
                [
                    ft.Text(product_data["name"], size=18),
                    ft.Text(product_data["price"], size=14),
                    ft.Text(f"Quantity: {product_data['quantity']}"),
                ],
                alignment="spaceBetween"
            )
            self.purchases_list.controls.append(item)

    def back_to_products(self, e):
        self.page.go("/products")  # Navigate back to products page


def main(page: ft.Page):
    def router(route):
        page.views.clear()

        if page.route == "/":
            landing = Landing(page)
            page.views.append(landing)

        if page.route == "/products":
            products = Product(page)
            page.views.append(products)

        if page.route == "/cart":
            cart = Cart(page)
            page.views.append(cart)

        if page.route == "/sign-in":
            sign_in = SignIn(page)
            page.views.append(sign_in)

        if page.route == "/register":
            register = Register(page)
            page.views.append(register)

        if page.route == "/settings":
            settings = Settings(page)
            page.views.append(settings)

        if page.route == "/purchases":
            purchases = Purchases(page)
            page.views.append(purchases)

        page.update()

    page.on_route_change = router
    page.go("/")


ft.app(target=main, assets_dir="assets")
