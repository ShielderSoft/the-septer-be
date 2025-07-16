from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from services.file_upload import save_uploaded_file
from services.ai_handler import call_gemini
from models.log import Log
from models.conversation import Conversation
from models.user import User
from schemas.ai import AIQuery, AIAnswer
from core.db import get_db
from core.security import get_current_user
import uuid

router = APIRouter()


@router.post("/upload")
def upload_log(
    log_type: str = Form(...),
    file: UploadFile = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if log_type not in ["txt", "log", "json", "sarif"]:
        raise HTTPException(status_code=400, detail="Unsupported log type")

    file_path = save_uploaded_file(file, log_type)

    new_log = Log(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        type=log_type,
        file_path=file_path
    )
    db.add(new_log)
    db.commit()

    return {"message": "Log uploaded", "log_id": new_log.id}


@router.post("/ask", response_model=AIAnswer)
def ask_question(
    data: AIQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = db.query(Log).filter(Log.id == data.log_id, Log.user_id == current_user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found or not authorized")

    if not current_user.gemini_api_key:
        raise HTTPException(status_code=403, detail="Gemini API key not set for this user")

    log_path = Path(log.file_path)
    if not log_path.exists():
        raise HTTPException(status_code=404, detail="Log file not found on disk")

    # Use Gemini SDK with file and question
    result = call_gemini(log_file_path=log_path, question=data.question, user=current_user)

    convo = Conversation(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        log_id=log.id,
        question=data.question,
        answer_insights=result["insights"],
        answer_reasoning=result["reasoning"],
        answer_supporting_logs=result["supporting_logs"],
        answer_fixes=result["fixes"]
    )
    db.add(convo)
    db.commit()

    return AIAnswer(**result)
