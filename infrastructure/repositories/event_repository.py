from typing import List, Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from domain.entities.event import Event
from domain.value_objects import Uuid
from infrastructure.models.event_model import EventModel
from domain.repositories.base_entity_repository import BaseEntityRepository


class EventRepository(BaseEntityRepository[Event, EventModel]):
    """Repository for event operations"""
    
    def __init__(self, db_session: Session):
        self._db_session = db_session
        self._model_class = EventModel
    
    def get_all(self) -> List[Event]:
        """Get all events"""
        events = self._db_session.query(self._model_class).all()
        return [self._to_entity(event) for event in events]
    
    def get_by_uuid(self, uuid) -> Optional[Event]:
        """Get event by UUID"""
        event = self._db_session.query(self._model_class).filter(
            self._model_class.uuid == str(uuid)
        ).first()
        
        if not event:
            return None
            
        return self._to_entity(event)
    
    def get_upcoming(self, days: int = 30) -> List[Event]:
        """Get upcoming events within a specified number of days"""
        now = datetime.now()
        end_date = now + timedelta(days=days)
        
        events = self._db_session.query(self._model_class).filter(
            and_(
                self._model_class.start_date >= now,
                self._model_class.start_date <= end_date
            )
        ).order_by(self._model_class.start_date).all()
        
        return [self._to_entity(event) for event in events]
    
    def get_by_date(self, date: datetime) -> List[Event]:
        """Get events for a specific date"""
        start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0)
        end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)
        
        events = self._db_session.query(self._model_class).filter(
            or_(
                # Event starts or ends on this day
                and_(
                    self._model_class.start_date >= start_of_day,
                    self._model_class.start_date <= end_of_day
                ),
                and_(
                    self._model_class.end_date >= start_of_day,
                    self._model_class.end_date <= end_of_day
                ),
                # All-day events or multi-day events that span this day
                and_(
                    self._model_class.start_date <= start_of_day,
                    self._model_class.end_date >= end_of_day
                )
            )
        ).order_by(self._model_class.start_date).all()
        
        return [self._to_entity(event) for event in events]
    
    def get_by_organizer(self, organizer_uuid: str) -> List[Event]:
        """Get events organized by a specific user"""
        events = self._db_session.query(self._model_class).filter(
            self._model_class.organizer_uuid == organizer_uuid
        ).order_by(self._model_class.start_date).all()
        
        return [self._to_entity(event) for event in events]
    
    def create(self, entity: Event) -> Optional[Event]:
        """Create a new event"""
        if not entity.uuid:
            entity.uuid = str(Uuid.generate())
            
        event_model = self._to_model(entity)
        self._db_session.add(event_model)
        self._db_session.commit()
        self._db_session.refresh(event_model)
        
        return self._to_entity(event_model)
    
    def update(self, entity: Event) -> Optional[Event]:
        """Update an existing event"""
        event_model = self._db_session.query(self._model_class).filter(
            self._model_class.uuid == str(entity.uuid)
        ).first()
        
        if not event_model:
            return None
        
        # Update model attributes
        event_model.title = entity.title
        event_model.description = entity.description
        event_model.start_date = entity.start_date
        event_model.end_date = entity.end_date
        event_model.location = entity.location
        event_model.organizer_uuid = entity.organizer_uuid
        event_model.event_type = entity.event_type
        event_model.all_day = entity.all_day
        event_model.max_participants = entity.max_participants
        
        self._db_session.commit()
        self._db_session.refresh(event_model)
        
        return self._to_entity(event_model)
    
    def delete(self, uuid) -> bool:
        """Delete an event by UUID"""
        event = self._db_session.query(self._model_class).filter(
            self._model_class.uuid == str(uuid)
        ).first()
        
        if not event:
            return False
            
        self._db_session.delete(event)
        self._db_session.commit()
        
        return True
    
    def _to_entity(self, model: EventModel) -> Event:
        """Convert model to entity"""
        return Event(
            uuid=model.uuid,
            title=model.title,
            description=model.description,
            start_date=model.start_date,
            end_date=model.end_date,
            location=model.location,
            organizer_uuid=model.organizer_uuid,
            event_type=model.event_type,
            all_day=model.all_day,
            max_participants=model.max_participants
        )
    
    def _to_model(self, entity: Event) -> EventModel:
        """Convert entity to model"""
        return EventModel(
            uuid=entity.uuid,
            title=entity.title,
            description=entity.description,
            start_date=entity.start_date,
            end_date=entity.end_date,
            location=entity.location,
            organizer_uuid=entity.organizer_uuid,
            event_type=entity.event_type,
            all_day=entity.all_day,
            max_participants=entity.max_participants
        )