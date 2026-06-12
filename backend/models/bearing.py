from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base

class BearingType(Base):
    """Типы подшипников (шариковый, роликовый, игольчатый и т.д.)"""
    __tablename__ = "bearing_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # Шариковый радиальный
    code = Column(String(50), unique=True)      # DEEP_GROOVE_BALL
    description = Column(Text)
    
    # Связи
    bearings = relationship("Bearing", back_populates="bearing_type")
    
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<BearingType {self.name}>"


class BearingManufacturer(Base):
    """Производители подшипников"""
    __tablename__ = "bearing_manufacturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    country = Column(String(100))
    website = Column(String(255))
    
    # Связи
    bearings = relationship("Bearing", back_populates="manufacturer")
    
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<BearingManufacturer {self.name}>"


class BearingSeries(Base):
    """Серии подшипников (6200, 6300, 16000 и т.д.)"""
    __tablename__ = "bearing_series"

    id = Column(Integer, primary_key=True, index=True)
    series_code = Column(String(20), unique=True, nullable=False)  # 6200
    name = Column(String(100))  # Легкая серия
    bearing_type_id = Column(Integer, ForeignKey("bearing_types.id"))
    description = Column(Text)
    
    # Связи
    bearing_type = relationship("BearingType")
    bearings = relationship("Bearing", back_populates="series")
    
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<BearingSeries {self.series_code}>"


class Bearing(Base):
    """Основная модель подшипника"""
    __tablename__ = "bearings"

    id = Column(Integer, primary_key=True, index=True)
    
    # Основной номер подшипника (например: 6204-2Z)
    bearing_number = Column(String(50), unique=True, nullable=False, index=True)
    alternative_numbers = Column(String(200))  # Альтернативные номера (через запятую)
    
    # Связи с производителем, серией, типом
    manufacturer_id = Column(Integer, ForeignKey("bearing_manufacturers.id"))
    series_id = Column(Integer, ForeignKey("bearing_series.id"))
    bearing_type_id = Column(Integer, ForeignKey("bearing_types.id"))
    
    # Размеры (мм) - основные
    bore_diameter_mm = Column(Numeric(10, 2), nullable=False)      # Внутренний диаметр d
    outer_diameter_mm = Column(Numeric(10, 2), nullable=False)     # Наружный диаметр D
    width_mm = Column(Numeric(10, 2), nullable=False)              # Ширина B
    
    # Дополнительные размеры (для конических роликовых)
    width_inner_mm = Column(Numeric(10, 2))  # B (для конических)
    width_outer_mm = Column(Numeric(10, 2))  # C (для конических)
    
    # Нагрузки (кН)
    dynamic_load_rating_kn = Column(Numeric(10, 2))   # Динамическая грузоподъемность C
    static_load_rating_kn = Column(Numeric(10, 2))    # Статическая грузоподъемность C0
    fatigue_load_limit_kn = Column(Numeric(10, 2))    # Предел усталости Pu
    
    # Скоростные характеристики
    reference_speed_rpm = Column(Integer)              # Справочная скорость (об/мин)
    limiting_speed_rpm = Column(Integer)               # Предельная скорость (об/мин)
    
    # Конструктивные особенности
    seal_type = Column(String(50))     # OPEN, 2Z, 2RS, 2RS1, ZZ, 2RU
    cage_type = Column(String(100))    # Стальной штампованный, Латунный, Полимерный
    clearance = Column(String(20))     # CN (нормальный), C3, C4, C5
    tolerance_class = Column(String(20))  # P0 (нормальный), P6, P5, P4
    
    # Материалы
    material_type = Column(String(50))  # Хромистая сталь, Нержавеющая сталь, Керамика
    
    # Смазка
    lubrication_type = Column(String(100))  # Пластичная смазка, Масло, Сухая
    
    # Вес и цена
    weight_kg = Column(Numeric(10, 3))
    price = Column(Numeric(15, 2))
    currency = Column(String(3), default="RUB")
    
    # Применение
    application = Column(String(500))  # Для каких применений рекомендуется
    
    # Изображения и документы
    image_url = Column(String(500))
    drawing_url = Column(String(500))
    datasheet_url = Column(String(500))
    
    # Связи для доступа к связанным данным
    manufacturer = relationship("BearingManufacturer", back_populates="bearings")
    series = relationship("BearingSeries", back_populates="bearings")
    bearing_type = relationship("BearingType", back_populates="bearings")
    
    # Совместимость с двигателями (многие-ко-многим)
    compatible_motors = relationship(
        "Product",
        secondary="bearing_motor_compatibility",
        back_populates="compatible_bearings"
    )
    
    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Bearing {self.bearing_number}>"


class BearingMotorCompatibility(Base):
    """Таблица связи подшипников и двигателей"""
    __tablename__ = "bearing_motor_compatibility"

    id = Column(Integer, primary_key=True, index=True)
    bearing_id = Column(Integer, ForeignKey("bearings.id"), nullable=False)
    motor_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Позиция установки
    position = Column(String(50))  # 'DE' (drive end), 'NDE' (non-drive end), 'BOTH'
    
    # Примечания
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class BearingSpecification(Base):
    """Дополнительные спецификации подшипников (ключ-значение)"""
    __tablename__ = "bearing_specifications"

    id = Column(Integer, primary_key=True, index=True)
    bearing_id = Column(Integer, ForeignKey("bearings.id"), nullable=False)
    
    spec_group = Column(String(50))      # material, lubrication, application
    spec_key = Column(String(100))        # material_type, grease_type
    spec_name = Column(String(200))       # Тип материала, Тип смазки
    spec_value = Column(String(500))      # Хромистая сталь, Литол-24
    spec_unit = Column(String(50))        # единица измерения
    
    # Для числовых значений (для фильтрации)
    numeric_value = Column(Numeric(15, 6))
    
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<BearingSpec {self.spec_key}: {self.spec_value}>"
