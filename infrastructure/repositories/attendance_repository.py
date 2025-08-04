from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from domain.entities.attendance import Attendance
from domain.value_objects import Uuid
from infrastructure.models.attendance_model import AttendanceModel
from domain.repositories.base_entity_repository import BaseEntityRepository


class AttendanceRepository(BaseEntityRepository[Attendance, AttendanceModel]):
    """Repository for attendance operations"""
    
    def __init__(self, db_session: Session):
        self._db_session = db_session
        self._model_class = AttendanceModel
    
    def get_all(self) -> List[Attendance]:
        """Get all attendance records"""
        records = self._db_session.query(self._model_class).all()
        return [self._to_entity(record) for record in records]
    
    def get_by_uuid(self, uuid) -> Optional[Attendance]:
        """Get attendance record by UUID"""
        record = self._db_session.query(self._model_class).filter(
            self._model_class.uuid == str(uuid)
        ).first()
        
        if not record:
            return None
            
        return self._to_entity(record)
    
    def get_by_student(self, student_uuid: str) -> List[Attendance]:
        """Get attendance records for a student"""
        records = self._db_session.query(self._model_class).filter(
            self._model_class.student_uuid == student_uuid
        ).order_by(self._model_class.date.desc()).all()
        
        return [self._to_entity(record) for record in records]
    
    def get_by_subject(self, subject_uuid: str) -> List[Attendance]:
        """Get attendance records for a subject"""
        records = self._db_session.query(self._model_class).filter(
            self._model_class.subject_uuid == subject_uuid
        ).order_by(self._model_class.date.desc()).all()
        
        return [self._to_entity(record) for record in records]
    
    def get_by_student_and_subject(self, student_uuid: str, subject_uuid: str) -> List[Attendance]:
        """Get attendance records for a student in a specific subject"""
        records = self._db_session.query(self._model_class).filter(
            and_(
                self._model_class.student_uuid == student_uuid,
                self._model_class.subject_uuid == subject_uuid
            )
        ).order_by(self._model_class.date.desc()).all()
        
        return [self._to_entity(record) for record in records]
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Attendance]:
        """Get attendance records within a date range"""
        records = self._db_session.query(self._model_class).filter(
            and_(
                self._model_class.date >= start_date,
                self._model_class.date <= end_date
            )
        ).order_by(self._model_class.date).all()
        
        return [self._to_entity(record) for record in records]
    
    def create(self, entity: Attendance) -> Optional[Attendance]:
        """Create a new attendance record"""
        if not entity.uuid:
            entity.uuid = str(Uuid.generate())
            
        record_model = self._to_model(entity)
        self._db_session.add(record_model)
        self._db_session.commit()
        self._db_session.refresh(record_model)
        
        return self._to_entity(record_model)
    
    def update(self, entity: Attendance) -> Optional[Attendance]:
        """Update an existing attendance record"""
        record_model = self._db_session.query(self._model_class).filter(
            self._model_class.uuid == str(entity.uuid)
        ).first()
        
        if not record_model:
            return None
        
        # Update model attributes
        record_model.student_uuid = entity.student_uuid
        record_model.subject_uuid = entity.subject_uuid
        record_model.date = entity.date
        record_model.status = entity.status
        record_model.notes = entity.notes
        
        self._db_session.commit()
        self._db_session.refresh(record_model)
        
        return self._to_entity(record_model)
    
    def delete(self, uuid) -> bool:
        """Delete an attendance record by UUID"""
        record = self._db_session.query(self._model_class).filter(
            self._model_class.uuid == str(uuid)
        ).first()
        
        if not record:
            return False
            
        self._db_session.delete(record)
        self._db_session.commit()
        
        return True
    
    def _to_entity(self, model: AttendanceModel) -> Attendance:
        """Convert model to entity"""
        return Attendance(
            uuid=model.uuid,
            student_uuid=model.student_uuid,
            subject_uuid=model.subject_uuid,
            date=model.date,
            status=model.status,
            notes=model.notes
        )
    
    def _to_model(self, entity: Attendance) -> AttendanceModel:
        """Convert entity to model"""
        return AttendanceModel(
            uuid=entity.uuid,
            student_uuid=entity.student_uuid,
            subject_uuid=entity.subject_uuid,
            date=entity.date,
            status=entity.status,
            notes=entity.notes
        )