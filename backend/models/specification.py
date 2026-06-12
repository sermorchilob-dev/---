from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base

class Specification(Base):
    """Модель для дополнительных характеристик (ключ-значение)"""
    __tablename__ = "specifications"

    id = Column(Integer, primary_key=True, index=True)
    
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Ключ-значение
    spec_key = Column(String(100), nullable=False)
    spec_name = Column(String(200), nullable=False)
    spec_value = Column(String(500), nullable=False)
    spec_unit = Column(String(50))
    
    # Для числовых значений (для фильтрации)
    numeric_value = Column(Numeric(15, 6))
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с продуктом
    product = relationship("Product", backref="specifications")

    def __repr__(self):
        return f"<Specification {self.spec_key}: {self.spec_value}>"
