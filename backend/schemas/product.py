from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class ProductBase(BaseModel):
    product_code: str
    name: str
    description: Optional[str] = None
    power_kw: Optional[Decimal] = None
    speed_rpm: Optional[int] = None
    voltage: Optional[str] = None
    mounting_type: Optional[str] = None
    ip_rating: Optional[str] = None
    price: Optional[Decimal] = None
    currency: str = "RUB"
    in_stock: bool = True
    manufacturer_id: Optional[int] = None
    category_id: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    product_code: Optional[str] = None
    name: Optional[str] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class ProductWithRelations(Product):
    manufacturer_name: Optional[str] = None
    category_name: Optional[str] = None
