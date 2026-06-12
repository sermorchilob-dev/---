from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base
import enum

class HousingType(enum.Enum):
    PILLOW_BLOCK = "PILLOW_BLOCK"          # Стационарный корпус (UCP)
    SQUARE_FLANGE = "SQUARE_FLANGE"        # Квадратный фланец (UCF)
    TWO_BOLT_FLANGE = "TWO_BOLT_FLANGE"    # Двухболтовый фланец (UCFL)
    FLANGE_CARTRIDGE = "FLANGE_CARTRIDGE"  # Фланцевая гильза (UCFC)
    TAKE_UP = "TAKE_UP"                    # Узел натяжения (UCT)
    # Добавьте другие типы по необходимости

class HousingMaterial(enum.Enum):
    CAST_IRON = "CAST_IRON"                 # Чугун
    STAINLESS_STEEL = "STAINLESS_STEEL"     # Нержавеющая сталь
    PRESSED_STEEL = "PRESSED_STEEL"         # Прессованная сталь
    THERMOPLASTIC = "THERMOPLASTIC"         # Термопластик

class BearingUnit(Base):
    __tablename__ = "bearing_units"

    id = Column(Integer, primary_key=True, index=True)
    unit_number = Column(String(50), unique=True, nullable=False, index=True)  # Номер узла, например "UCP 204"
    
    # Характеристики
    shaft_diameter_mm = Column(Numeric(10, 2), nullable=False)  # Диаметр вала
    housing_type = Column(Enum(HousingType), nullable=False)
    housing_material = Column(Enum(HousingMaterial), nullable=False, default=HousingMaterial.CAST_IRON)
    
    # Размеры корпуса (основные, в зависимости от типа могут варьироваться, добавим общие)
    a_mm = Column(Numeric(10, 2))   # длина основания
    e_mm = Column(Numeric(10, 2))   # расстояние между болтами
    i_mm = Column(Numeric(10, 2))   # ширина
    g_mm = Column(Numeric(10, 2))   # высота центра
    l_mm = Column(Numeric(10, 2))   # общая длина
    s_mm = Column(Numeric(10, 2))   # толщина
    b_mm = Column(Numeric(10, 2))   # ширина подшипника
    # Можно добавить другие размеры по мере необходимости
    
    # Масса
    weight_kg = Column(Numeric(10, 3))
    
    # Нагрузки (обычно такие же, как у встроенного подшипника)
    dynamic_load_kn = Column(Numeric(10, 2))
    static_load_kn = Column(Numeric(10, 2))
    
    # Связь с подшипником, который используется в узле (опционально)
    bearing_id = Column(Integer, ForeignKey("bearings.id"), nullable=True)
    bearing = relationship("Bearing", backref="bearing_units")
    
    # Производитель (например, ASAHI)
    manufacturer_id = Column(Integer, ForeignKey("bearing_manufacturers.id"), nullable=True)
    manufacturer = relationship("BearingManufacturer", backref="bearing_units")
    
    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<BearingUnit {self.unit_number}>"
