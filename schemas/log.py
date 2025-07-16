from pydantic import BaseModel
from typing import Literal
from datetime import datetime


class LogType(str):
    TXT = "txt"
    LOG = "log"
    JSON = "json"
    SARIF = "sarif"


class LogUpload(BaseModel):
    type: Literal["txt", "log", "json", "sarif"]


class LogOut(BaseModel):
    id: str
    user_id: str
    type: str
    uploaded_at: datetime
    file_path: str

    class Config:
        orm_mode = True