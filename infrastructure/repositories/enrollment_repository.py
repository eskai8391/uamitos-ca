from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from domain.entities.enrollment import Enrollment
from domain.value_objects import Uuid
from infrastructure.models.enrollment_model import EnrollmentModel
from domain.repositories.base_entity_repository import BaseEntityRepository


class EnrollmentRepository(BaseEntityRepository[Enrollment, EnrollmentModel]):
    """Repository for enrollment operations"""
    
    def __init__(self, db_session: Session):
        self._db_session = db_session
        self._model_class = EnrollmentModel
    
    def get_all(self) -> List[Enrollment]:
        """Get all enrollments"""
        records = self._db_session.query(self._model_class).all()
        return [self._to_entity(record) for record in records]
    
    def get_by_uuid(self, uuid) -> Optional[Enrollment]:
        """Get enrollment by UUID"""
        record = self._db_session.query(self._model_class).filter(
            self._model_class.uuid == str(uuid)
        ).first()
        
        if not record:
            return None
            
        return self._to_entity(record)
    
    def get_by_student(self, student_uuid: str) -> List[Enrollment]:
        """Get enrollments for a student"""
        records = self._db_session.query(self._model_class).filter(
            self._model_class.student_uuid == student_uuid
        ).all()
        
        return [self._to_entity(record) for record in records]
    
    def get_by_subject(self, subject_uuid: str) -> List[Enrollment]:
        """Get enrollments for a subject"""
        records = self._db_session.query(self._model_class).filter(
            self._model_class.subject_uuid == subject_uuid
        ).all()
        
        return [self._to_entity(record) for record in records]
    
    def get_by_student_and_subject(self, student_uuid: str, subject_uuid: str) -> Optional[Enrollment]:
        """Get enrollment for a student in a specific subject"""
        record = self._db_session.query(self._model_class).filter(
            and_(
                self._model_class.student_uuid == student_uuid,
                self._model_class.subject_uuid == subject_uuid
            )
        ).first()
        
        if not record:
            return None
            
        return self._to_entity(record)
    
    def get_by_semester(self, semester: str) -> List[Enrollment]:
        """Get enrollments for a specific semester"""
        records = self._db_session.query(self._model_class).filter(
            self._model_class.semester == semester
        ).all()
        
        return [self._to_entity(record) for record in records]
    
    def create(self, entity: Enrollment) -> Optional[Enrollment]:
        """Create a new enrollment"""
        if not entity.uuid:
            entity.uuid = str(Uuid.generate())
            
        record_model = self._to_model(entity)
        self._db_session.add(record_model)
        self._db_session.commit()
        self._db_session.refresh(record_model)
        
        return self._to_entity(record_model)
    
    def update(self, entity: Enrollment) -> Optional[Enrollment]:
        """Update an existing enrollment"""
        record_model = self._db_session.query(self._model_class).filter(
            self._model_class.uuid == str(entity.uuid)
        ).first()
        
        if not record_model:
            return None
        
        # Update model attributes
        record_model.student_uuid = entity.student_uuid
        record_model.subject_uuid = entity.subject_uuid
        record_model.enrollment_date = entity.enrollment_date
        record_model.semester = entity.semester
        record_model.status = entity.status
        record_model.final_grade = entity.final_grade
        
        self._db_session.commit()
        self._db_session.refresh(record_model)
        
        return self._to_entity(record_model)
    
    def delete(self, uuid) -> bool:
        """Delete an enrollment by UUID"""
        record = self._db_session.query(self._model_class).filter(
            self._model_class.uuid == str(uuid)
        ).first()
        
        if not record:
            return False
            
        self._db_session.delete(record)
        self._db_session.commit()
        
        return True
    
    def _to_entity(self, model: EnrollmentModel) -> Enrollment:
        """Convert model to entity"""
        return Enrollment(
            uuid=model.uuid,
            student_uuid=model.student_uuid,
            subject_uuid=model.subject_uuid,
            enrollment_date=model.enrollment_date,
            semester=model.semester,
            status=model.status,
            final_grade=model.final_grade
        )
    
    def _to_model(self, entity: Enrollment) -> EnrollmentModel:
        """Convert entity to model"""
        return EnrollmentModel(
            uuid=entity.uuid,
            student_uuid=entity.student_uuid,
            subject_uuid=entity.subject_uuid,
            enrollment_date=entity.enrollment_date,
            semester=entity.semester,
            status=entity.status,
            final_grade=entity.final_grade
        )