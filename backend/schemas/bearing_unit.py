from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from models.bearing_unit import HousingType, HousingMaterial

class BearingUnitBase(BaseModel):
    unit_number: str
    shaft_diameter_mm: Decimal
    housing_type: HousingType
    housing_material: HousingMaterial = HousingMaterial.CAST_IRON
    a_mm: Optional[Decimal] = None
    e_mm: Optional[Decimal] = None
    i_mm: Optional[Decimal] = None
    g_mm: Optional[Decimal] = None
    l_mm: Optional[Decimal] = None
    s_mm: Optional[Decimal] = None
    b_mm: Optional[Decimal] = None
    weight_kg: Optional[Decimal] = None
    dynamic_load_kn: Optional[Decimal] = None
    static_load_kn: Optional[Decimal] = None
    bearing_id: Optional[int] = None
    manufacturer_id: Optional[int] = None

class BearingUnitCreate(BearingUnitBase):
    pass

class BearingUnitUpdate(BearingUnitBase):
    unit_number: Optional[str] = None
    shaft_diameter_mm: Optional[Decimal] = None
    housing_type: Optional[HousingType] = None
    housing_material: Optional[HousingMaterial] = None

class BearingUnit(BearingUnitBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class BearingUnitWithRelations(BearingUnit):
    bearing: Optional[dict] = None
    manufacturer: Optional[dict] = None
