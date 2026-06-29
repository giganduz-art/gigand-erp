from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import engine, Base, SessionLocal
from .models import *
from .routers import auth, api
from .auth import hash_password
from .data.seed_data import (
    ORGANIZATIONS, CURRENCIES, PAYMENT_METHODS, WAREHOUSES,
    EMPLOYEES, CATEGORIES, CUSTOMERS, SUPPLIERS, PRODUCTS
)
from datetime import datetime
import os

app = FastAPI(title="GIGAND ERP", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(api.router)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
LANDING_DIR = os.path.join(BASE_DIR, "landing")

@app.get("/manifest.json")
def serve_manifest():
    fp = os.path.join(FRONTEND_DIR, "manifest.json")
    if os.path.exists(fp):
        return FileResponse(fp, media_type="application/manifest+json")
    return {}

@app.get("/")
def serve_landing():
    fp = os.path.join(LANDING_DIR, "index.html")
    if os.path.exists(fp):
        return FileResponse(fp)
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/erp")
def serve_erp():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Organization).count() > 0:
            return

        for o in ORGANIZATIONS:
            db.add(Organization(**o))
        for c in CURRENCIES:
            db.add(Currency(**c))
        for p in PAYMENT_METHODS:
            db.add(PaymentMethod(**p))
        for w in WAREHOUSES:
            db.add(Warehouse(**{k: v for k, v in w.items()}))
        for e in EMPLOYEES:
            db.add(Employee(**e))
        for c in CATEGORIES:
            db.add(Category(**c))
        for c in CUSTOMERS:
            db.add(Customer(**c))
        for s in SUPPLIERS:
            db.add(Supplier(**{k: v for k, v in s.items() if k != "type"}))
        for p in PRODUCTS:
            db.add(Product(**p))

        trades_data = [
            ("t_1", "170127", "W29813", 10000, 0, "org_1", "CHORI TURDIYEV", "2026-06-28 15:54:51"),
            ("t_2", "170126", "W29812", 13500, 0, "org_1", "CHORI TURDIYEV", "2026-06-28 14:26:00"),
            ("t_3", "170125", "W29811", 5000, 0, "org_1", "CHORI TURDIYEV", "2026-06-28 14:24:14"),
            ("t_4", "170124", "W29810", 40000, 0, "org_1", "CHORI TURDIYEV", "2026-06-28 14:14:35"),
            ("t_5", "170123", "W29809", 10000, 0, "org_1", "CHORI TURDIYEV", "2026-06-28 14:13:13"),
            ("t_6", "170122", "W29808", 20000, 0, "org_1", "CHORI TURDIYEV", "2026-06-28 14:05:43"),
            ("t_7", "170121", "W29807", 20000, 0, "org_1", "CHORI TURDIYEV", "2026-06-28 13:33:42"),
            ("t_8", "170120", "W29806", 30000, 0, "org_1", "CHORI TURDIYEV", "2026-06-28 13:23:04"),
            ("t_9", "170119", "W29805", 13000, 0, "org_1", "CHORI TURDIYEV", "2026-06-28 13:17:08"),
            ("t_10", "170118", "W29804", 15000, 0, "org_1", "CHORI TURDIYEV", "2026-06-28 12:47:18"),
        ]
        for t in trades_data:
            db.add(Trade(id=t[0], number=t[1], uuid=t[2], total_price=t[3], debt=t[4], state="done", org_id=t[5], responsible_name=t[6], sold_at=datetime.fromisoformat(t[7])))

        db.add(User(username="admin", hashed_password=hash_password("gigand2026"), full_name="GIGAND XOLDING", role="admin"))
        db.add(User(username="rustam", hashed_password=hash_password("rustam123"), full_name="Tursunov Rustam", role="manager"))
        db.add(User(username="chori", hashed_password=hash_password("chori123"), full_name="CHORI TURDIYEV", role="cashier"))

        db.commit()
        print("GIGAND ERP: Database seeded!")
    finally:
        db.close()


@app.on_event("startup")
def startup():
    seed_database()
