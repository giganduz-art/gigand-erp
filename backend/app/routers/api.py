from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import uuid as uuid_mod
from ..database import get_db
from ..models import *
from ..data.seed_data import DASHBOARD_SUMMARY, ACCOUNT

router = APIRouter(prefix="/api", tags=["api"])

def uid(): return str(uuid_mod.uuid4())[:8]

# === Schemas ===
class EmployeeIn(BaseModel):
    full_name: str
    phone: str = ""
    balance: float = 0
    number: str = ""

class CustomerIn(BaseModel):
    name: str
    phone: str = ""
    balance: float = 0
    responsible: str = ""

class SupplierIn(BaseModel):
    name: str
    phone: str = ""
    address: str = ""
    balance: float = 0

class CategoryIn(BaseModel):
    name: str
    item_count: int = 0
    org_id: str = "org_1"

class WarehouseIn(BaseModel):
    name: str
    org_id: str = "org_1"
    is_main: bool = False
    address: str = ""

class TradeItemIn(BaseModel):
    name: str
    price: float
    qty: int = 1

class TradeIn(BaseModel):
    total_price: float
    responsible_name: str = ""
    org_id: str = "org_1"
    debt: float = 0
    items: list[TradeItemIn] = []

class ProductIn(BaseModel):
    name: str
    sku: str = ""
    barcode: str = ""
    category_id: str = ""
    sell_price: float = 0
    cost_price: float = 0
    stock: int = 0
    org_id: str = "org_1"
    warehouse_id: str = "wh_1"

# === Static ===
@router.get("/account")
def get_account():
    return ACCOUNT

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    d = dict(DASHBOARD_SUMMARY)
    d["total_trades"] = db.query(Trade).count() + 90184
    return d

# === Organizations ===
@router.get("/organizations")
def get_organizations(db: Session = Depends(get_db)):
    items = db.query(Organization).all()
    return {"total": len(items), "data": [{"id": i.id, "name": i.name, "type": i.type, "address": i.address, "phone": i.phone, "is_active": i.is_active, "is_default": i.is_default} for i in items]}

# === Currencies ===
@router.get("/currencies")
def get_currencies(db: Session = Depends(get_db)):
    items = db.query(Currency).all()
    return {"total": len(items), "data": [{"id": i.id, "name": i.name, "code": i.code, "symbol": i.symbol, "is_main": i.is_main, "rate": i.rate} for i in items]}

# === Payment Methods ===
@router.get("/payment-methods")
def get_payment_methods(db: Session = Depends(get_db)):
    items = db.query(PaymentMethod).all()
    return {"total": len(items), "data": [{"id": i.id, "name": i.name, "type": i.type, "shortcut": i.shortcut, "is_enabled": i.is_enabled, "is_default": i.is_default} for i in items]}

# === Warehouses CRUD ===
@router.get("/warehouses")
def get_warehouses(db: Session = Depends(get_db)):
    items = db.query(Warehouse).all()
    return {"total": len(items), "data": [{"id": i.id, "name": i.name, "org_id": i.org_id, "is_main": i.is_main, "status": i.status, "address": i.address} for i in items]}

@router.post("/warehouses")
def create_warehouse(data: WarehouseIn, db: Session = Depends(get_db)):
    w = Warehouse(id="wh_"+uid(), name=data.name, org_id=data.org_id, is_main=data.is_main, address=data.address, status="active")
    db.add(w); db.commit()
    return {"id": w.id, "name": w.name}

# === Employees CRUD ===
def emp_dict(i):
    return {"id": i.id, "number": i.number, "full_name": i.full_name, "phone": i.phone, "balance": i.balance, "is_active": i.is_active}

@router.get("/employees")
def get_employees(db: Session = Depends(get_db), page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=200), search: str = ""):
    q = db.query(Employee)
    if search:
        q = q.filter(Employee.full_name.ilike(f"%{search}%"))
    total = q.count()
    items = q.offset((page - 1) * limit).limit(limit).all()
    return {"total": total, "page": page, "data": [emp_dict(i) for i in items]}

@router.post("/employees")
def create_employee(data: EmployeeIn, db: Session = Depends(get_db)):
    num = str(db.query(Employee).count() + 1)
    e = Employee(id="emp_"+uid(), number=data.number or num, full_name=data.full_name, phone=data.phone, balance=data.balance)
    db.add(e); db.commit()
    return emp_dict(e)

@router.put("/employees/{eid}")
def update_employee(eid: str, data: EmployeeIn, db: Session = Depends(get_db)):
    e = db.query(Employee).filter(Employee.id == eid).first()
    if not e: raise HTTPException(404, "Xodim topilmadi")
    e.full_name = data.full_name; e.phone = data.phone; e.balance = data.balance
    if data.number: e.number = data.number
    db.commit()
    return emp_dict(e)

@router.delete("/employees/{eid}")
def delete_employee(eid: str, db: Session = Depends(get_db)):
    e = db.query(Employee).filter(Employee.id == eid).first()
    if not e: raise HTTPException(404, "Xodim topilmadi")
    db.delete(e); db.commit()
    return {"ok": True}

# === Categories CRUD ===
def cat_dict(i):
    return {"id": i.id, "name": i.name, "item_count": i.item_count, "org_id": i.org_id}

@router.get("/categories")
def get_categories(db: Session = Depends(get_db), page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=200), search: str = ""):
    q = db.query(Category)
    if search:
        q = q.filter(Category.name.ilike(f"%{search}%"))
    total = q.count()
    items = q.order_by(Category.item_count.desc()).offset((page - 1) * limit).limit(limit).all()
    return {"total": total, "page": page, "data": [cat_dict(i) for i in items]}

@router.post("/categories")
def create_category(data: CategoryIn, db: Session = Depends(get_db)):
    c = Category(id="cat_"+uid(), name=data.name, item_count=data.item_count, org_id=data.org_id)
    db.add(c); db.commit()
    return cat_dict(c)

@router.put("/categories/{cid}")
def update_category(cid: str, data: CategoryIn, db: Session = Depends(get_db)):
    c = db.query(Category).filter(Category.id == cid).first()
    if not c: raise HTTPException(404, "Kategoriya topilmadi")
    c.name = data.name; c.item_count = data.item_count; c.org_id = data.org_id
    db.commit()
    return cat_dict(c)

@router.delete("/categories/{cid}")
def delete_category(cid: str, db: Session = Depends(get_db)):
    c = db.query(Category).filter(Category.id == cid).first()
    if not c: raise HTTPException(404, "Kategoriya topilmadi")
    db.delete(c); db.commit()
    return {"ok": True}

# === Customers CRUD ===
def cust_dict(i):
    return {"id": i.id, "name": i.name, "phone": i.phone, "balance": i.balance, "total_sale": i.total_sale, "responsible": i.responsible}

@router.get("/customers")
def get_customers(db: Session = Depends(get_db), page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=200), search: str = ""):
    q = db.query(Customer)
    if search:
        q = q.filter(Customer.name.ilike(f"%{search}%"))
    total = q.count()
    items = q.offset((page - 1) * limit).limit(limit).all()
    return {"total": total, "page": page, "data": [cust_dict(i) for i in items]}

@router.post("/customers")
def create_customer(data: CustomerIn, db: Session = Depends(get_db)):
    c = Customer(id="cust_"+uid(), name=data.name, phone=data.phone, balance=data.balance, responsible=data.responsible or "GIGAND XOLDING")
    db.add(c); db.commit()
    return cust_dict(c)

@router.put("/customers/{cid}")
def update_customer(cid: str, data: CustomerIn, db: Session = Depends(get_db)):
    c = db.query(Customer).filter(Customer.id == cid).first()
    if not c: raise HTTPException(404, "Mijoz topilmadi")
    c.name = data.name; c.phone = data.phone; c.balance = data.balance; c.responsible = data.responsible
    db.commit()
    return cust_dict(c)

@router.delete("/customers/{cid}")
def delete_customer(cid: str, db: Session = Depends(get_db)):
    c = db.query(Customer).filter(Customer.id == cid).first()
    if not c: raise HTTPException(404, "Mijoz topilmadi")
    db.delete(c); db.commit()
    return {"ok": True}

# === Suppliers CRUD ===
def sup_dict(i):
    return {"id": i.id, "name": i.name, "phone": i.phone, "address": i.address, "type": i.type, "balance": i.balance, "total_sale": i.total_sale}

@router.get("/suppliers")
def get_suppliers(db: Session = Depends(get_db), page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=200), search: str = ""):
    q = db.query(Supplier)
    if search:
        q = q.filter(Supplier.name.ilike(f"%{search}%"))
    total = q.count()
    items = q.offset((page - 1) * limit).limit(limit).all()
    return {"total": total, "page": page, "data": [sup_dict(i) for i in items]}

@router.post("/suppliers")
def create_supplier(data: SupplierIn, db: Session = Depends(get_db)):
    s = Supplier(id="sup_"+uid(), name=data.name, phone=data.phone, address=data.address, balance=data.balance)
    db.add(s); db.commit()
    return sup_dict(s)

@router.delete("/suppliers/{sid}")
def delete_supplier(sid: str, db: Session = Depends(get_db)):
    s = db.query(Supplier).filter(Supplier.id == sid).first()
    if not s: raise HTTPException(404, "Yetkazuvchi topilmadi")
    db.delete(s); db.commit()
    return {"ok": True}

# === Trades CRUD ===
def trade_dict(i):
    return {"id": i.id, "number": i.number, "uuid": i.uuid, "total_price": i.total_price, "debt": i.debt, "state": i.state, "org_id": i.org_id, "responsible_name": i.responsible_name, "sold_at": str(i.sold_at) if i.sold_at else ""}

@router.get("/trades")
def get_trades(db: Session = Depends(get_db), page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=200), search: str = ""):
    q = db.query(Trade)
    if search:
        q = q.filter(Trade.uuid.ilike(f"%{search}%"))
    total = q.count()
    items = q.order_by(Trade.sold_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return {"total": total, "page": page, "data": [trade_dict(i) for i in items]}

@router.post("/trades")
def create_trade(data: TradeIn, db: Session = Depends(get_db)):
    last = db.query(Trade).order_by(Trade.number.desc()).first()
    num = str(int(last.number) + 1) if last else "170128"
    last_uuid = db.query(Trade).order_by(Trade.sold_at.desc()).first()
    uuid_num = int(last_uuid.uuid[1:]) + 1 if last_uuid else 29814
    t = Trade(id="t_"+uid(), number=num, uuid="W"+str(uuid_num), total_price=data.total_price, debt=data.debt, state="done", org_id=data.org_id, responsible_name=data.responsible_name or "GIGAND XOLDING", sold_at=datetime.utcnow())
    db.add(t)
    for item in data.items:
        p = db.query(Product).filter(Product.name == item.name).first()
        if p and p.stock >= item.qty:
            p.stock -= item.qty
    db.commit()
    return trade_dict(t)

# === Products CRUD ===
def prod_dict(i):
    return {"id": i.id, "name": i.name, "sku": i.sku, "barcode": i.barcode, "category_id": i.category_id, "sell_price": i.sell_price, "cost_price": i.cost_price, "stock": i.stock, "org_id": i.org_id, "warehouse_id": i.warehouse_id}

@router.get("/products")
def get_products(db: Session = Depends(get_db), page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=200), search: str = "", category_id: str = ""):
    q = db.query(Product)
    if search:
        q = q.filter(Product.name.ilike(f"%{search}%"))
    if category_id:
        q = q.filter(Product.category_id == category_id)
    total = q.count()
    items = q.order_by(Product.name).offset((page - 1) * limit).limit(limit).all()
    return {"total": total, "page": page, "data": [prod_dict(i) for i in items]}

@router.post("/products")
def create_product(data: ProductIn, db: Session = Depends(get_db)):
    p = Product(id="prod_"+uid(), name=data.name, sku=data.sku, barcode=data.barcode, category_id=data.category_id, sell_price=data.sell_price, cost_price=data.cost_price, stock=data.stock, org_id=data.org_id, warehouse_id=data.warehouse_id)
    db.add(p); db.commit()
    if data.category_id:
        cat = db.query(Category).filter(Category.id == data.category_id).first()
        if cat:
            cat.item_count += 1
            db.commit()
    return prod_dict(p)

@router.put("/products/{pid}")
def update_product(pid: str, data: ProductIn, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == pid).first()
    if not p: raise HTTPException(404, "Mahsulot topilmadi")
    p.name = data.name; p.sku = data.sku; p.barcode = data.barcode; p.category_id = data.category_id
    p.sell_price = data.sell_price; p.cost_price = data.cost_price; p.stock = data.stock
    db.commit()
    return prod_dict(p)

@router.delete("/products/{pid}")
def delete_product(pid: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == pid).first()
    if not p: raise HTTPException(404, "Mahsulot topilmadi")
    db.delete(p); db.commit()
    return {"ok": True}

# === Stats ===
@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return {
        "organizations": db.query(Organization).count(),
        "employees": db.query(Employee).count(),
        "categories": db.query(Category).count(),
        "customers": db.query(Customer).count(),
        "suppliers": db.query(Supplier).count(),
        "warehouses": db.query(Warehouse).count(),
        "trades": db.query(Trade).count(),
        "products": db.query(Product).count(),
        "currencies": db.query(Currency).count(),
        "payment_methods": db.query(PaymentMethod).count(),
    }
