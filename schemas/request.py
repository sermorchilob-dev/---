from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RequestItem(BaseModel):
    id: int
    type: str  # 'product', 'bearing', 'gearbox', 'bearing_unit'
    name: str
    quantity: int = 1

class RequestCreate(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    company_name: Optional[str] = None
    comment: Optional[str] = None
    items: List[RequestItem]

class RequestOut(BaseModel):
    id: int
    customer_name: str
    customer_email: str
    created_at: datetime
    status: str

    class Config:
        from_attributes = True
