from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user import User
from models.conversation import Conversation
from core.db import get_db
from core.security import require_guardian

router = APIRouter()

@router.get("/dashboard")
def guardian_dashboard(db: Session = Depends(get_db), current_user: User = Depends(require_guardian)):
    # Total number of questions
    total_questions = db.query(Conversation).count()
    
    # Questions asked by different users
    users_with_questions = (
        db.query(User.email, Conversation.question, Conversation.created_at)
        .join(Conversation, User.id == Conversation.user_id)
        .order_by(Conversation.created_at.desc())
        .all()
    )
    
    # Format the questions data
    questions_by_users = []
    for user_email, question, created_at in users_with_questions:
        questions_by_users.append({
            "user_email": user_email,
            "question": question,
            "asked_at": created_at
        })

    return {
        "total_questions": total_questions,
        "questions_by_users": questions_by_users
    }
