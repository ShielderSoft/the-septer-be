from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, GeminiKeyAdd, UserOut
from core.db import get_db
from core.security import encrypt_password, is_strong_password, get_current_user
import uuid

router = APIRouter()


@router.post("/signup", response_model=dict)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email Registered!")

    if data.role != "Hunter":
        raise HTTPException(status_code=400, detail="Unexpected error, you tried to be smart, fcuk you!")

    if not is_strong_password(data.password):
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character"
        )

    new_user = User(
        id=str(uuid.uuid4()),
        email=data.email,
        password=encrypt_password(data.password),
        role="Hunter"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response = {"Message":"Email Registered!"} 
    return response


@router.put("/add-api-key", response_model=dict)
def add_gemini_key(
    data: GeminiKeyAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    current_user.gemini_api_key = data.api_key
    db.commit()
    db.refresh(current_user)

    response= { "Message" : "Key Added!" ,"User" :UserOut(id=current_user.id, email=current_user.email, role=current_user.role)}
    return response