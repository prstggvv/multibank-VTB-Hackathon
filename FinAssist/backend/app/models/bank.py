from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.database.database import Base

class BankConnection(Base):
    __tablename__ = "bank_connection"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    

    bank_name = Column(String(50), nullable=False, index=True)
    
   
    consent_id = Column(String(100), unique=True, index=True)  
    external_client_id = Column(String(100))  
    

    is_active = Column(Boolean, default=True)
    
   
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
 
    user = relationship("User", back_populates="bank_connections")

    def __repr__(self):
        return f"<BankConnection(id={self.id}, bank='{self.bank_name}', user_id={self.user_id})>"