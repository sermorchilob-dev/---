from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base

class Category(Base):
    """Модель категории продуктов"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    
    # Тип категории: 'motor', 'bearing', 'cylinder'
    category_type = Column(String(50), nullable=False, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связь с продуктами
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"
