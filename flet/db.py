from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    img_src = Column(Text)
    name = Column(Text)
    description = Column(Text)
    price = Column(Text)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True)
    password = Column(Text)
    email = Column(Text)

class CartItem(Base):
    __tablename__ = "cart_item"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)

def connectionDB():
    engine = create_engine("postgresql://postgres:mes2102@localhost:5432/fletsyntra")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)

session = connectionDB()

def write_to_db(table_class, **kwargs):
    record = table_class(**kwargs)
    session.add(record)
    try:
        session.commit()
        print(f"{table_class.__tablename__} record added.")
    except IntegrityError as e:
        session.rollback()
        print(f"IntegrityError: {e.orig}")
