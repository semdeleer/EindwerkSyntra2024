from sqlalchemy import Column, Integer, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text, unique=True)  # Ensure email is unique
    password = Column(Text)
    sessions = relationship('Sessions', backref='user')

class Sessions(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    carts = relationship('Carts', backref='session')

class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    price = Column(Integer)
    carts = relationship('Carts', backref='product')

class Carts(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

def connectionDB():
    engine = create_engine("postgresql://postgres:mes2102@localhost:5432/rts")
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
        return record
    except IntegrityError as e:
        session.rollback()
        print(f"IntegrityError: {e.orig}")
        return None

