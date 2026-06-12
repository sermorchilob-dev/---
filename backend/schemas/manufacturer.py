from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ManufacturerBase(BaseModel):
    name: str
    country: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None

class ManufacturerCreate(ManufacturerBase):
    pass

class ManufacturerUpdate(ManufacturerBase):
    name: Optional[str] = None

class Manufacturer(ManufacturerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
