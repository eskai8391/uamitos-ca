from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date

from domain.entities.event import Event
from infrastructure.database import get_db
from infrastructure.repositories.event_repository import EventRepository
from presentation.api.dependencies import get_current_user

router = APIRouter()

@router.get("/events", response_model=List[Event])
def get_events(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get all events"""
    repo = EventRepository(db)
    return repo.get_all()

@router.get("/events/upcoming", response_model=List[Event])
def get_upcoming_events(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get upcoming events within a specified number of days"""
    repo = EventRepository(db)
    return repo.get_upcoming(days)

@router.get("/events/{event_uuid}", response_model=Event)
def get_event(
    event_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get a specific event by UUID"""
    repo = EventRepository(db)
    event = repo.get_by_id(event_uuid)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.get("/events/by-date/{date}", response_model=List[Event])
def get_events_by_date(
    date: date,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get events for a specific date"""
    # Convert date to datetime
    date_as_datetime = datetime(date.year, date.month, date.day)
    
    repo = EventRepository(db)
    return repo.get_by_date(date_as_datetime)

@router.get("/events/by-organizer/{organizer_uuid}", response_model=List[Event])
def get_events_by_organizer(
    organizer_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get events organized by a specific user"""
    repo = EventRepository(db)
    return repo.get_by_organizer(organizer_uuid)

@router.post("/events", response_model=Event)
def create_event(
    event: Event,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Create a new event"""
    repo = EventRepository(db)
    return repo.create(event)

@router.put("/events", response_model=Event)
def update_event(
    event: Event,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Update an existing event"""
    repo = EventRepository(db)
    return repo.update(event)

@router.delete("/events/{event_uuid}")
def delete_event(
    event_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete an event"""
    repo = EventRepository(db)
    success = repo.delete(event_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}