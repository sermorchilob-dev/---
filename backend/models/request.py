from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.connection import Base

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    customer_email = Column(String(100), nullable=False)
    customer_phone = Column(String(20))
    company_name = Column(String(200))
    comment = Column(Text)
    items = Column(Text)  # JSON: [{"id":1,"type":"bearing","name":"6204","quantity":1}]
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="new")  # new, processed, completed, cancelled
