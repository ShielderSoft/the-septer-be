from sqlalchemy import Column, String, Enum, DateTime
from core.db import Base
import enum
from datetime import datetime
import uuid


class RoleEnum(str, enum.Enum):
    Hunter = "Hunter"
    Guardian = "Guardian"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.Hunter)
    gemini_api_key = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)