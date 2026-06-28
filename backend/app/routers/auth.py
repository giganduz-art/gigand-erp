from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..auth import verify_password, create_token, hash_password

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Login yoki parol noto'g'ri")
    token = create_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer", "user": {"username": user.username, "full_name": user.full_name, "role": user.role}}

@router.get("/me")
def me(db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        return {"username": "admin", "full_name": "GIGAND XOLDING", "role": "admin"}
    return {"username": user.username, "full_name": user.full_name, "role": user.role}
