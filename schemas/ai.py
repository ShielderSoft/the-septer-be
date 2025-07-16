from pydantic import BaseModel
from datetime import datetime


class AIQuery(BaseModel):
    log_id: str
    question: str


class AIAnswer(BaseModel):
    insights: str
    reasoning: str
    supporting_logs: str
    fixes: str


class ConversationOut(BaseModel):
    id: str
    user_id: str
    log_id: str
    question: str
    answer: AIAnswer
    created_at: datetime

    class Config:
        orm_mode = True