"""
This module defines the SQLAlchemy ORM mappings for various tables in a Django-like database schema, 
provides a function to establish a connection to the database, and includes a function to write records to the database.

Classes:
    DjangoContentType: ORM mapping for the `django_content_type` table.
    AuthGroupPermissions: ORM mapping for the `auth_group_permissions` table.
    AuthGroup: ORM mapping for the `auth_group` table.
    AuthPermission: ORM mapping for the `auth_permission` table.
    AuthUserGroups: ORM mapping for the `auth_user_groups` table.
    AuthUserUserPermissions: ORM mapping for the `auth_user_user_permissions` table.
    AuthUser: ORM mapping for the `auth_user` table.
    DjangoAdminLog: ORM mapping for the `django_admin_log` table.
    DjangoMigrations: ORM mapping for the `django_migrations` table.
    DjangoSession: ORM mapping for the `django_session` table.
    StoreCustomer: ORM mapping for the `store_customer` table.
    StoreOrder: ORM mapping for the `store_order` table.
    StoreOrderItem: ORM mapping for the `store_orderitem` table.
    StoreProduct: ORM mapping for the `store_product` table.
    StoreShippingAddress: ORM mapping for the `store_shippingaddress` table.

Functions:
    connectionDB(): Establishes a connection to the PostgreSQL database and returns a session factory.
    write_to_db(table_class, **kwargs): Writes a record to the specified table in the database.
"""

import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Float, ForeignKey, SmallInteger, Index, UniqueConstraint, CheckConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class DjangoContentType(Base):
    """
    ORM mapping for the `django_content_type` table.
    """
    __tablename__ = "django_content_type"
    __table_args__ = (
        UniqueConstraint('app_label', 'model', name='django_content_type_app_label_model_76bd3d3b_uniq'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)

class AuthGroupPermissions(Base):
    """
    ORM mapping for the `auth_group_permissions` table.
    """
    __tablename__ = "auth_group_permissions"
    __table_args__ = (
        Index('auth_group_permissions_group_id_b120cbf9', 'group_id'),
        UniqueConstraint('group_id', 'permission_id', name='auth_group_permissions_group_id_permission_id_0cd325b0_uniq'),
        Index('auth_group_permissions_permission_id_84c5c92e', 'permission_id')
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('auth_group.id', deferrable=True, initially='DEFERRED'), nullable=False)
    permission_id = Column(Integer, ForeignKey('auth_permission.id', deferrable=True, initially='DEFERRED'), nullable=False)


class AuthGroup(Base):
    """
    ORM mapping for the `auth_group` table.
    """
    __tablename__ = "auth_group"
    __table_args__ = (
        UniqueConstraint('name', name='auth_group_name_key'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, unique=True)

class AuthPermission(Base):
    """
    ORM mapping for the `auth_permission` table.
    """
    __tablename__ = "auth_permission"
    id = Column(Integer, primary_key=True)
    content_type_id = Column(Integer)
    codename = Column(Text)
    name = Column(Text)

class AuthUserGroups(Base):
    """
    ORM mapping for the `auth_user_groups` table.
    """
    __tablename__ = "auth_user_groups"
    __table_args__ = (
        Index('auth_user_groups_group_id_97559544', 'group_id'),
        Index('auth_user_groups_user_id_6a12ed8b', 'user_id'),
        UniqueConstraint('user_id', 'group_id', name='auth_user_groups_user_id_group_id_94350c0c_uniq'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('auth_user.id', deferrable=True, initially='DEFERRED'), nullable=False)
    group_id = Column(Integer, ForeignKey('auth_group.id', deferrable=True, initially='DEFERRED'), nullable=False)

class AuthUserUserPermissions(Base):
    """
    ORM mapping for the `auth_user_user_permissions` table.
    """
    __tablename__ = "auth_user_user_permissions"
    __table_args__ = (
        Index('auth_user_user_permissions_permission_id_1fbb5f2c', 'permission_id'),
        Index('auth_user_user_permissions_user_id_a95ead1b', 'user_id'),
        UniqueConstraint('user_id', 'permission_id', name='auth_user_user_permissions_user_id_permission_id_14a6b632_uniq'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('auth_user.id', deferrable=True, initially='DEFERRED'), nullable=False)
    permission_id = Column(Integer, ForeignKey('auth_permission.id', deferrable=True, initially='DEFERRED'), nullable=False)

class AuthUser(Base):
    """
    ORM mapping for the `auth_user` table.
    """
    __tablename__ = "auth_user"
    __table_args__ = (
        UniqueConstraint('username', name='auth_user_username_key'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime)
    is_superuser = Column(Boolean, nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime, nullable=False)
    first_name = Column(String(150), nullable=False)

class DjangoAdminLog(Base):
    """
    ORM mapping for the `django_admin_log` table.
    """
    __tablename__ = "django_admin_log"
    __table_args__ = (
        Index('django_admin_log_content_type_id_c4bce8eb', 'content_type_id'),
        Index('django_admin_log_user_id_c564eba6', 'user_id'),
        CheckConstraint('action_flag >= 0', name='check_action_flag_non_negative'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    object_id = Column(Text)
    object_repr = Column(String(200), nullable=False)
    action_flag = Column(SmallInteger, nullable=False)
    change_message = Column(Text, nullable=False)
    content_type_id = Column(Integer, ForeignKey('django_content_type.id', deferrable=True, initially='DEFERRED'))
    user_id = Column(Integer, ForeignKey('auth_user.id', deferrable=True, initially='DEFERRED'), nullable=False)
    action_time = Column(DateTime, nullable=False)

class DjangoMigrations(Base):
    """
    ORM mapping for the `django_migrations` table.
    """
    __tablename__ = "django_migrations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DateTime, nullable=False)

class DjangoSession(Base):
    """
    ORM mapping for the `django_session` table.
    """
    __tablename__ = "django_session"
    __table_args__ = (
        Index('django_session_expire_date_a5c62663', 'expire_date'),
    )

    session_key = Column(String(40), primary_key=True)
    session_data = Column(Text, nullable=False)
    expire_date = Column(DateTime, nullable=False)

class StoreCustomer(Base):
    """
    ORM mapping for the `store_customer` table.
    """
    __tablename__ = "store_customer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    email = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('auth_user.id', deferrable=True, initially='DEFERRED'), unique=True)

class StoreOrder(Base):
    """
    ORM mapping for the `store_order` table.
    """
    __tablename__ = "store_order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_ordered = Column(DateTime, nullable=False)
    complete = Column(Boolean, nullable=False)
    transaction_id = Column(String(100))
    customer_id = Column(Integer, ForeignKey('store_customer.id', deferrable=True, initially='DEFERRED'))

class StoreOrderItem(Base):
    """
    ORM mapping for the `store_orderitem` table.
    """
    __tablename__ = "store_orderitem"

    id = Column(Integer, primary key=True, autoincrement=True)
    quantity = Column(Integer)
    date_added = Column(DateTime, nullable=False)
    order_id = Column(Integer, ForeignKey('store_order.id', deferrable=True, initially='DEFERRED'))
    product_id = Column(Integer, ForeignKey('
