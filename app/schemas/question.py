from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class QuestionStatus(str, Enum):
    pending = "pending"
    answered = "answered"


class QuestionCreate(BaseModel):
    question: str


class QuestionOut(BaseModel):
    id: int
    document_id: int
    question: str
    answer: Optional[str]
    status: QuestionStatus
    created_at: datetime

    class Config:
        orm_mode = True
