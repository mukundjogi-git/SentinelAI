from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    metric = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    severity = Column(String, default="medium")
    status = Column(String, default="open")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))