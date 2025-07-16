from sqlalchemy import Column, String, ForeignKey, DateTime
from core.db import Base
from datetime import datetime
import uuid


class Log(Base):
    __tablename__ = "logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)  # log type: txt, json, etc.
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String, nullable=False)