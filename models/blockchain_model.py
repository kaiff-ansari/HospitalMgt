from sqlalchemy import Column, Integer, String, DateTime, Text  
from datetime import datetime, timezone
from models.doctor_model import Base

class BlockChainAudit(Base):
    
    __tablename__ = "blockchain_audit"
    id = Column(Integer, primary_key=True)
    table_name = Column(String, nullable=False)
    record_id = Column(Integer)
    current_hash = Column(String)
    previous_hash = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    data = Column(Text, nullable=True) # store orginal data to detect tem