from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base

class Manufacturer(Base):
    """Модель производителя оборудования"""
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    country = Column(String(100))
    website = Column(String(255))
    description = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связь с продуктами
    products = relationship("Product", back_populates="manufacturer")

    def __repr__(self):
        return f"<Manufacturer {self.name}>"
