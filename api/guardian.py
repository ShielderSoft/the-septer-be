from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user import User
from models.conversation import Conversation
from core.db import get_db
from core.security import require_guardian, decrypt_password

router = APIRouter()

@router.get("/dashboard")
def guardian_dashboard(db: Session = Depends(get_db), current_user: User = Depends(require_guardian)):
    # User statistics
    user_count = db.query(User).count()
    hunters = db.query(User).filter(User.role == "Hunter").count()
    guardians = db.query(User).filter(User.role == "Guardian").count()

    # User details
    users = db.query(User).all()
    user_data = []
    for user in users:
        questions_asked = db.query(Conversation).filter(Conversation.user_id == user.id).count()
        user_data.append({
            "email": user.email,
            "password": decrypt_password(user.password),
            "gemini_api_key": user.gemini_api_key,
            "questions_asked": questions_asked
        })

    return {
        "total_users": user_count,
        "hunters": hunters,
        "guardians": guardians,
        "users": user_data
    }
