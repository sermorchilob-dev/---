from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base

class Product(Base):
    """Модель продукта (электродвигатель, цилиндр и т.д.)"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    
    # Основная информация
    product_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Технические характеристики
    power_kw = Column(Numeric(10, 2))
    speed_rpm = Column(Integer)
    voltage = Column(String(50))
    current_a = Column(Numeric(10, 2))
    efficiency = Column(Numeric(5, 2))
    
    # Монтажные размеры
    mounting_type = Column(String(50))
    shaft_diameter_mm = Column(Numeric(10, 2))
    shaft_length_mm = Column(Numeric(10, 2))
    flange_size = Column(String(50))
    
    # Габариты и вес
    length_mm = Column(Numeric(10, 2))
    width_mm = Column(Numeric(10, 2))
    height_mm = Column(Numeric(10, 2))
    weight_kg = Column(Numeric(10, 3))
    
    # Защита и исполнение
    ip_rating = Column(String(10))
    insulation_class = Column(String(10))
    
    # Цена и наличие
    price = Column(Numeric(15, 2))
    currency = Column(String(3), default="RUB")
    in_stock = Column(Boolean, default=True)
    
    # Внешние ключи
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Связи
    manufacturer = relationship("Manufacturer", back_populates="products")
    category = relationship("Category", back_populates="products")
    
    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Связь с подшипниками
    compatible_bearings = relationship(
        "Bearing",
        secondary="bearing_motor_compatibility",
        back_populates="compatible_motors"
    )

    def __repr__(self):
        return f"<Product {self.product_code}>"
