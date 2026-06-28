from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, default="ordinary")
    address = Column(String, default="")
    phone = Column(String, default="")
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class Currency(Base):
    __tablename__ = "currencies"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    symbol = Column(String, default="")
    is_main = Column(Boolean, default=False)
    rate = Column(Float, default=1)

class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    shortcut = Column(String, default="")
    is_enabled = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)

class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    org_id = Column(String, ForeignKey("organizations.id"))
    is_main = Column(Boolean, default=False)
    status = Column(String, default="active")
    address = Column(String, default="")

class Employee(Base):
    __tablename__ = "employees"
    id = Column(String, primary_key=True)
    number = Column(String)
    full_name = Column(String, nullable=False)
    phone = Column(String, default="")
    balance = Column(Float, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    item_count = Column(Integer, default=0)
    org_id = Column(String, ForeignKey("organizations.id"))

class Customer(Base):
    __tablename__ = "customers"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, default="")
    balance = Column(Float, default=0)
    total_sale = Column(Integer, default=0)
    responsible = Column(String, default="")
    created_at = Column(DateTime, server_default=func.now())

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, default="")
    address = Column(String, default="")
    type = Column(String, default="natural")
    balance = Column(Float, default=0)
    total_sale = Column(Integer, default=0)

class Trade(Base):
    __tablename__ = "trades"
    id = Column(String, primary_key=True)
    number = Column(String)
    uuid = Column(String)
    total_price = Column(Float, default=0)
    debt = Column(Float, default=0)
    state = Column(String, default="done")
    org_id = Column(String, ForeignKey("organizations.id"))
    responsible_name = Column(String, default="")
    sold_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    sku = Column(String, default="")
    barcode = Column(String, default="")
    category_id = Column(String, default="")
    sell_price = Column(Float, default=0)
    cost_price = Column(Float, default=0)
    stock = Column(Integer, default=0)
    org_id = Column(String, default="org_1")
    warehouse_id = Column(String, default="wh_1")
    created_at = Column(DateTime, server_default=func.now())

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, default="")
    role = Column(String, default="admin")
    is_active = Column(Boolean, default=True)
