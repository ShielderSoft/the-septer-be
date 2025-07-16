from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from core.db import Base
from datetime import datetime
import uuid


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    log_id = Column(String, ForeignKey("logs.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer_insights = Column(Text, nullable=True)
    answer_reasoning = Column(Text, nullable=True)
    answer_supporting_logs = Column(Text, nullable=True)
    answer_fixes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)