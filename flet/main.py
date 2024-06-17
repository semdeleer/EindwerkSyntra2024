import flet as ft
from db import write_to_db, session, Product as DBProduct, User as DBUser, CartItem as DBCartItem
from sqlalchemy.orm.exc import NoResultFound

class Landing(ft.View):
    """
    The landing page view displaying the store name and options to sign in or register.
    
    Attributes:
        page (ft.Page): The main application page.
        cart_logo (ft.Icon): The shopping cart icon.
        title (ft.Text): The title of the store.
        signin_page_btn (ft.ElevatedButton): Button to navigate to the sign-in page.
        register_page_btn (ft.ElevatedButton): Button to navigate to the register page.
        controls (list): List of controls to be displayed on the page.
    """
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
    """
    The model class responsible for handling database operations.

    Methods:
        get_products(): Retrieves all products from the database.
        get_cart(user_id): Retrieves the cart items for a specific user.
        add_to_cart(user_id, product_id): Adds a product to the user's cart.
        add_user(username, password, email): Adds a new user to the database.
        check_user(username, password): Checks if the user credentials are valid.
    """
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
    """
    The product page view displaying a list of products available for purchase.
    
    Attributes:
        page (ft.Page): The main application page.
        products (ft.Row): The row containing product items.
        controls (list): List of controls to be displayed on the page.
    """
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
        """
        Displays the header of the product page containing navigation icons.
        
        Returns:
            ft.Container: The header container.
        """
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
        """
        Displays the footer of the product page.
        
        Returns:
            ft.Row: The footer row.
        """
        return ft.Row([ft.Text("Simple X Shop", size=10)], alignment="center")

    def create_products(self, products: dict = Model.get_products()):
        """
        Creates the product items to be displayed on the page.
        
        Args:
            products (dict): A dictionary of product details.
        """
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
        """
        Creates the product image container.
        
        Args:
            img_path (str): The path to the product image.
        
        Returns:
            ft.Container: The container for the product image.
        """
        return ft.Container(
            image_src=img_path, image_fit="fill", border_radius=6, padding=10
        )

    def create_product_text(self, name: str, description: str):
        """
        Creates the product text container.
        
        Args:
            name (str): The product name.
            description (str): The product description.
        
        Returns:
            ft.Column: The container for the product text.
        """
        return ft.Column([ft.Text(name, size=18), ft.Text(description, size=11)])

    def create_product_event(self, price: str, idd: str):
        """
        Creates the product event container.
        
        Args:
            price (str): The product price.
            idd (str): The product ID.
        
        Returns:
            ft.Row: The container for the product event.
        """
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
        """
        Adds a product to the cart.
        
        Args:
            e (ft.TapEvent): The tap event.
        """
        current_user_id = 1  # Replace this with the actual logged-in user ID
        Model.add_to_cart(current_user_id, e.control.data)
        print(Model.get_cart(current_user_id))

    def buy_items(self, e: ft.TapEvent):
        """
        Navigates to the cart page after clicking Buy.
        
        Args:
            e (ft.TapEvent): The tap event.
        """
        self.page.go("/cart")


class Cart(ft.View):
    """
    The cart page view displaying the items in the user's cart.
    
    Attributes:
        page (ft.Page): The main application page.
        cart_items (ft.Column): The column containing cart items.
        controls (list): List of controls to be displayed on the page.
    """
    def __init__(self, page: ft.Page):
        super(Cart, self).__init__(route="/cart")
        self.page = page
