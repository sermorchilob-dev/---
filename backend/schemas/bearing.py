from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# ============== Схемы для типа подшипника ==============

class BearingTypeBase(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None

class BearingTypeCreate(BearingTypeBase):
    pass

class BearingTypeUpdate(BearingTypeBase):
    name: Optional[str] = None

class BearingType(BearingTypeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ============== Схемы для производителя подшипников ==============

class BearingManufacturerBase(BaseModel):
    name: str
    country: Optional[str] = None
    website: Optional[str] = None

class BearingManufacturerCreate(BearingManufacturerBase):
    pass

class BearingManufacturerUpdate(BearingManufacturerBase):
    name: Optional[str] = None

class BearingManufacturer(BearingManufacturerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ============== Схемы для серии подшипников ==============

class BearingSeriesBase(BaseModel):
    series_code: str
    name: Optional[str] = None
    bearing_type_id: Optional[int] = None
    description: Optional[str] = None

class BearingSeriesCreate(BearingSeriesBase):
    pass

class BearingSeriesUpdate(BearingSeriesBase):
    series_code: Optional[str] = None

class BearingSeries(BearingSeriesBase):
    id: int
    bearing_type: Optional[BearingType] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ============== Основные схемы для подшипника ==============

class BearingBase(BaseModel):
    bearing_number: str
    alternative_numbers: Optional[str] = None
    manufacturer_id: Optional[int] = None
    series_id: Optional[int] = None
    bearing_type_id: Optional[int] = None
    
    # Размеры
    bore_diameter_mm: Decimal
    outer_diameter_mm: Decimal
    width_mm: Decimal
    width_inner_mm: Optional[Decimal] = None
    width_outer_mm: Optional[Decimal] = None
    
    # Нагрузки
    dynamic_load_rating_kn: Optional[Decimal] = None
    static_load_rating_kn: Optional[Decimal] = None
    fatigue_load_limit_kn: Optional[Decimal] = None
    
    # Скорости
    reference_speed_rpm: Optional[int] = None
    limiting_speed_rpm: Optional[int] = None
    
    # Конструкция
    seal_type: Optional[str] = None
    cage_type: Optional[str] = None
    clearance: Optional[str] = None
    tolerance_class: Optional[str] = None
    material_type: Optional[str] = None
    lubrication_type: Optional[str] = None
    
    # Вес и цена
    weight_kg: Optional[Decimal] = None
    price: Optional[Decimal] = None
    currency: str = "RUB"
    
    # Применение
    application: Optional[str] = None
    
    # Файлы
    image_url: Optional[str] = None
    drawing_url: Optional[str] = None
    datasheet_url: Optional[str] = None

class BearingCreate(BearingBase):
    pass

class BearingUpdate(BearingBase):
    bearing_number: Optional[str] = None
    bore_diameter_mm: Optional[Decimal] = None
    outer_diameter_mm: Optional[Decimal] = None
    width_mm: Optional[Decimal] = None

class Bearing(BearingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class BearingWithRelations(Bearing):
    manufacturer: Optional[BearingManufacturer] = None
    series: Optional[BearingSeries] = None
    bearing_type: Optional[BearingType] = None
    manufacturer_name: Optional[str] = None
    series_code: Optional[str] = None
    type_name: Optional[str] = None

# ============== Схемы для совместимости ==============

class BearingMotorCompatibilityBase(BaseModel):
    bearing_id: int
    motor_id: int
    position: Optional[str] = None
    notes: Optional[str] = None

class BearingMotorCompatibilityCreate(BearingMotorCompatibilityBase):
    pass

class BearingMotorCompatibility(BearingMotorCompatibilityBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ============== Схемы для спецификаций ==============

class BearingSpecificationBase(BaseModel):
    bearing_id: int
    spec_group: str
    spec_key: str
    spec_name: str
    spec_value: str
    spec_unit: Optional[str] = None
    numeric_value: Optional[Decimal] = None

class BearingSpecificationCreate(BearingSpecificationBase):
    pass

class BearingSpecification(BearingSpecificationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ============== Схемы для фильтрации ==============

class BearingFilter(BaseModel):
    search: Optional[str] = None
    manufacturer_id: Optional[int] = None
    series_id: Optional[int] = None
    bearing_type_id: Optional[int] = None
    bore_diameter_min: Optional[Decimal] = None
    bore_diameter_max: Optional[Decimal] = None
    outer_diameter_min: Optional[Decimal] = None
    outer_diameter_max: Optional[Decimal] = None
    width_min: Optional[Decimal] = None
    width_max: Optional[Decimal] = None
    seal_type: Optional[str] = None
    clearance: Optional[str] = None
    material_type: Optional[str] = None
    skip: int = 0
    limit: int = 100
