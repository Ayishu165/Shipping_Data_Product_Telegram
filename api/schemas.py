# api/schemas.py
from pydantic import BaseModel

class TopProduct(BaseModel):
    product: str
    count: int

class ChannelActivity(BaseModel):
    date: str
    message_count: int

class SearchMessage(BaseModel):
    message: str
    date: str
    channel: str
