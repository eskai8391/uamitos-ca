from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.database.db import Base


class EventModel(Base):
    __tablename__ = "events"
    
    uuid = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=False)
    organizer_uuid = Column(String(36), ForeignKey("users.uuid"), nullable=False)
    event_type = Column(String(50), nullable=False)
    all_day = Column(Boolean, default=False)
    max_participants = Column(Integer, nullable=True)
    
    # Relationships
    organizer = relationship("UserModel", back_populates="organized_events")