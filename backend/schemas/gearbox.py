from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from models.gearbox import GearboxType, MountingPosition

class GearboxBase(BaseModel):
    gearbox_number: str
    name: Optional[str] = None
    manufacturer_id: Optional[int] = None
    gearbox_type: GearboxType
    series: Optional[str] = None
    stages: int = 1
    input_power_kw: Optional[Decimal] = None
    output_torque_nm: Optional[Decimal] = None
    ratio: Optional[Decimal] = None
    input_speed_rpm: Optional[Decimal] = None
    output_speed_rpm: Optional[Decimal] = None
    service_factor: Optional[Decimal] = None
    efficiency: Optional[Decimal] = None
    weight_kg: Optional[Decimal] = None
    mounting_position: MountingPosition = MountingPosition.M1
    output_shaft_diameter_mm: Optional[Decimal] = None
    output_shaft_length_mm: Optional[Decimal] = None
    output_flange_type: Optional[str] = None
    hollow_shaft: bool = False
    oil_volume_l: Optional[Decimal] = None
    radial_load_n: Optional[Decimal] = None
    price: Optional[Decimal] = None
    currency: str = "RUB"

class GearboxCreate(GearboxBase):
    pass

class GearboxUpdate(GearboxBase):
    gearbox_number: Optional[str] = None
    gearbox_type: Optional[GearboxType] = None

class Gearbox(GearboxBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class GearboxWithManufacturer(Gearbox):
    manufacturer: Optional[dict] = None
