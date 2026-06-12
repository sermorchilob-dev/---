from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base
import enum

class GearboxType(enum.Enum):
    """Типы редукторов по кинематической схеме"""
    WORM = "WORM"                    # Червячный
    HELICAL = "HELICAL"              # Цилиндрический соосный
    HELICAL_BEVEL = "HELICAL_BEVEL"  # Коническо-цилиндрический
    PARALLEL_SHAFT = "PARALLEL_SHAFT" # Плоскоцилиндрический
    VARIATOR = "VARIATOR"             # Вариатор
    INDUSTRIAL = "INDUSTRIAL"         # Индустриальный

class MountingPosition(enum.Enum):
    """Монтажное положение редуктора (M1...M6)"""
    M1 = "M1"
    M2 = "M2"
    M3 = "M3"
    M4 = "M4"
    M5 = "M5"
    M6 = "M6"

class Gearbox(Base):
    __tablename__ = "gearboxes"

    id = Column(Integer, primary_key=True, index=True)
    
    # Основная идентификация
    gearbox_number = Column(String(100), unique=True, nullable=False, index=True)  # Например "NMRW 030-80"
    name = Column(String(200))  # Описательное имя, можно заполнить позже
    
    # Производитель (ESQ)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"), nullable=True)
    manufacturer = relationship("Manufacturer", backref="gearboxes")
    
    # Тип и серия
    gearbox_type = Column(Enum(GearboxType), nullable=False)
    series = Column(String(50))  # Например "NMRW", "R", "KA", "UDL"
    
    # Количество ступеней
    stages = Column(Integer, default=1)  # 1, 2, 3
    
    # Технические параметры
    input_power_kw = Column(Numeric(10, 2))       # Мощность на входе, кВт
    output_torque_nm = Column(Numeric(10, 2))      # Крутящий момент на выходе, Нм
    ratio = Column(Numeric(10, 2))                  # Передаточное число
    input_speed_rpm = Column(Integer)                # Частота вращения входного вала (обычно 1400/1500)
    output_speed_rpm = Column(Numeric(10, 2))        # Частота вращения выходного вала
    service_factor = Column(Numeric(5, 2))           # Сервис-фактор (f.s.)
    efficiency = Column(Numeric(5, 2))               # КПД, % (или доля)
    
    # Габариты и вес
    weight_kg = Column(Numeric(10, 3))
    
    # Монтажное положение (по умолчанию M1)
    mounting_position = Column(Enum(MountingPosition), default=MountingPosition.M1)
    
    # Параметры выходного вала
    output_shaft_diameter_mm = Column(Numeric(10, 2))
    output_shaft_length_mm = Column(Numeric(10, 2))
    output_flange_type = Column(String(20))          # FA, FB, FC и т.д.
    hollow_shaft = Column(Boolean, default=False)    # Наличие полого вала
    
    # Масло
    oil_volume_l = Column(Numeric(10, 2))
    
    # Допустимая радиальная нагрузка (если есть)
    radial_load_n = Column(Numeric(10, 2))
    
    # Цена
    price = Column(Numeric(15, 2))
    currency = Column(String(3), default="RUB")
    
    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Gearbox {self.gearbox_number}>"