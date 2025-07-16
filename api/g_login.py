# api/g_login.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from core.security import verify_password, create_access_token
from models.user import User
from schemas.user import UserLogin, UserOut

router = APIRouter()


@router.post("/login", response_model=dict)
def guardian_login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password) or user.role != "Guardian":
        raise HTTPException(status_code=401, detail="Invalid email or password or insufficient privileges")
    response = {"access_token":create_access_token({"sub": user.id, "role": user.role}), "User":UserOut(id=user.id, email=user.email, role=user.role)}
    return response