import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Float, ForeignKey, SmallInteger, Index, UniqueConstraint, CheckConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class DjangoContentType(Base):
    __tablename__ = "django_content_type"
    __table_args__ = (
        UniqueConstraint('app_label', 'model', name='django_content_type_app_label_model_76bd3d3b_uniq'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)

class AuthGroupPermissions(Base):
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
    __tablename__ = "auth_group"
    __table_args__ = (
        UniqueConstraint('name', name='auth_group_name_key'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, unique=True)

class AuthPermission(Base):
    __tablename__ = "auth_permission"
    __table_args__ = (
        Index('auth_permission_content_type_id_2f476e4b', 'content_type_id'),
        UniqueConstraint('content_type_id', 'codename', name='auth_permission_content_type_id_codename_01ab375a_uniq'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    content_type_id = Column(Integer, ForeignKey('django_content_type.id', deferrable=True, initially='DEFERRED'), nullable=False)
    codename = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)

class AuthUserGroups(Base):
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
    __tablename__ = "django_migrations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DateTime, nullable=False)

class DjangoSession(Base):
    __tablename__ = "django_session"
    __table_args__ = (
        Index('django_session_expire_date_a5c62663', 'expire_date'),
    )

    session_key = Column(String(40), primary_key=True)
    session_data = Column(Text, nullable=False)
    expire_date = Column(DateTime, nullable=False)

class StoreCustomer(Base):
    __tablename__ = "store_customer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    email = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('auth_user.id', deferrable=True, initially='DEFERRED'), unique=True)

class StoreOrder(Base):
    __tablename__ = "store_order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_ordered = Column(DateTime, nullable=False)
    complete = Column(Boolean, nullable=False)
    transaction_id = Column(String(100))
    customer_id = Column(Integer, ForeignKey('store_customer.id', deferrable=True, initially='DEFERRED'))

class StoreOrderItem(Base):
    __tablename__ = "store_orderitem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)
    date_added = Column(DateTime, nullable=False)
    order_id = Column(Integer, ForeignKey('store_order.id', deferrable=True, initially='DEFERRED'))
    product_id = Column(Integer, ForeignKey('store_product.id', deferrable=True, initially='DEFERRED'))

class StoreProduct(Base):
    __tablename__ = "store_product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    digital = Column(Boolean)
    image = Column(String(100))

class StoreShippingAddress(Base):
    __tablename__ = "store_shippingaddress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(200))
    city = Column(String(200))
    state = Column(String(200))
    zipcode = Column(String(200))
    date_added = Column(DateTime, nullable=False)
    customer_id = Column(Integer, ForeignKey('store_customer.id', deferrable=True, initially='DEFERRED'))
    order_id = Column(Integer, ForeignKey('store_order.id', deferrable=True, initially='DEFERRED'))

def connectionDB():
    engine = create_engine("postgresql://postgres:mes2102@localhost:5432/rejectthesickness")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    return Session