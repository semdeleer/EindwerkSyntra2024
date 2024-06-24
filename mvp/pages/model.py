from database.dbs import session, Products, Users, Carts, Sessions
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import IntegrityError
from database.dbs import write_to_db
import smtplib


class Model(object):

    @staticmethod
    def add_user(username: str, password: str, email: str) -> bool:
        try:
            existing_user = session.query(Users).filter(Users.name == username, Users.email == email).one_or_none()
            if existing_user:
                return False  # User already exists

            write_to_db(Users, name=username, password=password, email=email)
            return True  # User added successfully

        except IntegrityError as e:
            session.rollback()
            print(f"IntegrityError occurred: {e}")
            return False

    @staticmethod
    def check_user(username: str, password: str) -> Users:
        try:
            return session.query(Users).filter(Users.name == username, Users.password == password).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    @staticmethod
    def check_username(username: str):
        existing_username = session.query(Users).filter(Users.name == username).one_or_none()
        if existing_username:
            return False
        else:
            return True

    @staticmethod
    def set_session(username: str) -> Sessions:
        user = session.query(Users).filter(Users.name == username).one()
        user_session = session.query(Sessions).filter(Sessions.user_id == user.id).order_by(Sessions.id.desc()).first()
        if not user_session:
            user_session = Sessions(user_id=user.id)
            session.add(user_session)
            session.commit()
        return user_session

    @staticmethod
    def get_products() -> Products:
        products = session.query(Products).all()
        return {product.id: {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price
        } for product in products}

    @staticmethod
    def get_cart(session_id: int) -> dict:
        cart_items = session.query(Carts).filter(Carts.session_id == session_id).all()
        return {item.id: {
            "id": item.id,
            "name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity
        } for item in cart_items}

    @staticmethod
    def add_to_cart(session_id: int, product_id: int) -> Carts:
        cart_item = session.query(Carts).filter(Carts.session_id == session_id,
                                                Carts.product_id == product_id).one_or_none()
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = Carts(session_id=session_id, product_id=product_id, quantity=1)
            session.add(cart_item)
        try:
            session.commit()
            return cart_item
        except IntegrityError as e:
            session.rollback()
            print(f"IntegrityError: {e.orig}")
            return None

    @staticmethod
    def checkout(session_id: int):
        cart = Model.get_cart(session_id)
        total_amount = sum(item["quantity"] * item["price"] for item in cart.values())

        # Fetch user's email from the Users table
        user = session.query(Users).join(Sessions).filter(Sessions.id == session_id).one()
        user_email = user.email

        # Setting up email
        try:
            s = smtplib.SMTP("smtp.gmail.com", 578)
            s.starttls()
            s.login("rsteindwerk@gmail.com", "rsteindwerk1#")
            message = f"Subject: Order Confirmation\n\nThank you for your order, we will deliver it soon. Here is your receipt:\n\n{cart}\n\nTotal amount: ${total_amount}"
            s.sendmail("rsteindwerk@gmail.com", user_email, message)
            s.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")
            return None

        print(f"Sending total amount ${total_amount} to {user_email}")
        new_session = Sessions(user_id=user.id)
        session.add(new_session)
        session.commit()
        return new_session
