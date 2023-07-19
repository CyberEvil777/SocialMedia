from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    id: int
    title: str
    text: str
    created_at: datetime
    user_id: int


class PostUpdate(BaseModel):
    title: str
    text: str
    created_at: datetime
