from database.dbs import session, Products, Users, Carts, Sessions
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import IntegrityError
from database.dbs import write_to_db
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
            return True
        else:
            return False

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
        items = "\n".join(f"{item['name']} price:{item['price']} quantity:{item['quantity']}" for item in cart.values())
        
        # Fetch user's email from the Users table
        user = session.query(Users).join(Sessions).filter(Sessions.id == session_id).one()
        user_email = user.email

        # Setting up email
        try:
            s = smtplib.SMTP("smtp.gmail.com", 587)
            s.starttls()
            s.login("rsteindwerk@gmail.com", "prab wdwt asbv zbbc")
            
            subject = "Order Confirmation"
            body = f"Thank you for your order, we will deliver it soon. Here is your receipt:\n\n{items}\n\nTotal amount: ${total_amount}"
            
            message = MIMEMultipart()
            message["From"] = "rsteindwerk@gmail.com"
            message["To"] = user_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            
            s.sendmail("rsteindwerk@gmail.com", user_email, message.as_string())
            s.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")
            return None

        print(f"Sending total amount ${total_amount} to {user_email}")
        
        # Assuming session and session.commit() are set up correctly elsewhere
        new_session = Sessions(user_id=user.id)
        session.add(new_session)
        session.commit()
        
        return new_session