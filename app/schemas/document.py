from pydantic import BaseModel
from typing import List, Optional


class DocumentCreate(BaseModel):
    title: str
    content: str


class DocumentOut(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True
