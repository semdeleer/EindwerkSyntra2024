from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class Product(Base):
    """
    Product model representing a product in the database.

    Attributes:
    id (int): Unique identifier for the product.
    img_src (str): URL or path to the product image.
    name (str): Name of the product.
    description (str): Description of the product.
    price (str): Price of the product.
    """
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    img_src = Column(Text)
    name = Column(Text)
    description = Column(Text)
    price = Column(Text)

class User(Base):
    """
    User model representing a user in the database.

    Attributes:
    id (int): Unique identifier for the user.
    username (str): Username of the user.
    password (str): Password of the user.
    email (str): Email of the user.
    """
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True)
    password = Column(Text)
    email = Column(Text)

class CartItem(Base):
    """
    CartItem model representing an item in a user's cart.

    Attributes:
    id (int): Unique identifier for the cart item.
    user_id (int): Identifier of the user who owns the cart item.
    product_id (int): Identifier of the product in the cart.
    quantity (int): Quantity of the product in the cart.
    """
    __tablename__ = "cart_item"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)

def connectionDB():
    """
    Establish a connection to the database and create tables.

    Creates an SQLAlchemy engine and binds it to a session factory. All tables defined
    with SQLAlchemy's declarative_base are created in the database if they do not already exist.

    Returns:
    scoped_session: A thread-safe session object for interacting with the database.
    """
    engine = create_engine("postgresql://postgres:mes2102@localhost:5432/fletsyntra")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)

session = connectionDB()

def write_to_db(table_class, **kwargs):
    """
    Write a new record to the database.

    Creates a new record of the given table class with the provided keyword arguments and
    adds it to the session. Attempts to commit the transaction to the database. If an
    IntegrityError occurs, the transaction is rolled back.

    Parameters:
    table_class (Base): The SQLAlchemy model class representing the table to write to.
    **kwargs: Column values for the new record.

    Raises:
    IntegrityError: If there is a database integrity issue, such as a unique constraint violation.

    Examples:
    >>> write_to_db(Product, name="Product1", description="Description", price="10.99")
    Product record added.
    """
    record = table_class(**kwargs)
    session.add(record)
    try:
        session.commit()
        print(f"{table_class.__tablename__} record added.")
    except IntegrityError as e:
        session.rollback()
        print(f"IntegrityError: {e.orig}")
