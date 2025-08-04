from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from domain.entities.grade import Grade
from domain.value_objects import Uuid
from infrastructure.models.grade_model import GradeModel
from domain.repositories.base_entity_repository import BaseEntityRepository


class GradeRepository(BaseEntityRepository[Grade, GradeModel]):
    """Repository for grade operations"""
    
    def __init__(self, db_session: Session):
        self._db_session = db_session
        self._model_class = GradeModel
    
    def get_all(self) -> List[Grade]:
        """Get all grades"""
        records = self._db_session.query(self._model_class).all()
        return [self._to_entity(record) for record in records]
    
    def get_by_uuid(self, uuid) -> Optional[Grade]:
        """Get grade by UUID"""
        record = self._db_session.query(self._model_class).filter(
            self._model_class.uuid == str(uuid)
        ).first()
        
        if not record:
            return None
            
        return self._to_entity(record)
    
    def get_by_student(self, student_uuid: str) -> List[Grade]:
        """Get grades for a student"""
        records = self._db_session.query(self._model_class).filter(
            self._model_class.student_uuid == student_uuid
        ).order_by(self._model_class.date.desc()).all()
        
        return [self._to_entity(record) for record in records]
    
    def get_by_subject(self, subject_uuid: str) -> List[Grade]:
        """Get grades for a subject"""
        records = self._db_session.query(self._model_class).filter(
            self._model_class.subject_uuid == subject_uuid
        ).order_by(self._model_class.date.desc()).all()
        
        return [self._to_entity(record) for record in records]
    
    def get_by_student_and_subject(self, student_uuid: str, subject_uuid: str) -> List[Grade]:
        """Get grades for a student in a specific subject"""
        records = self._db_session.query(self._model_class).filter(
            and_(
                self._model_class.student_uuid == student_uuid,
                self._model_class.subject_uuid == subject_uuid
            )
        ).order_by(self._model_class.date.desc()).all()
        
        return [self._to_entity(record) for record in records]
    
    def get_average_by_student_and_subject(self, student_uuid: str, subject_uuid: str) -> float:
        """Get average grade for a student in a specific subject"""
        result = self._db_session.query(
            func.sum(self._model_class.score * self._model_class.weight) / func.sum(self._model_class.weight)
        ).filter(
            and_(
                self._model_class.student_uuid == student_uuid,
                self._model_class.subject_uuid == subject_uuid
            )
        ).scalar()
        
        return float(result) if result is not None else 0.0
    
    def create(self, entity: Grade) -> Optional[Grade]:
        """Create a new grade"""
        if not entity.uuid:
            entity.uuid = str(Uuid.generate())
            
        record_model = self._to_model(entity)
        self._db_session.add(record_model)
        self._db_session.commit()
        self._db_session.refresh(record_model)
        
        return self._to_entity(record_model)
    
    def update(self, entity: Grade) -> Optional[Grade]:
        """Update an existing grade"""
        record_model = self._db_session.query(self._model_class).filter(
            self._model_class.uuid == str(entity.uuid)
        ).first()
        
        if not record_model:
            return None
        
        # Update model attributes
        record_model.student_uuid = entity.student_uuid
        record_model.subject_uuid = entity.subject_uuid
        record_model.evaluation_name = entity.evaluation_name
        record_model.score = entity.score
        record_model.weight = entity.weight
        record_model.date = entity.date
        record_model.comments = entity.comments
        
        self._db_session.commit()
        self._db_session.refresh(record_model)
        
        return self._to_entity(record_model)
    
    def delete(self, uuid) -> bool:
        """Delete a grade by UUID"""
        record = self._db_session.query(self._model_class).filter(
            self._model_class.uuid == str(uuid)
        ).first()
        
        if not record:
            return False
            
        self._db_session.delete(record)
        self._db_session.commit()
        
        return True
    
    def _to_entity(self, model: GradeModel) -> Grade:
        """Convert model to entity"""
        return Grade(
            uuid=model.uuid,
            student_uuid=model.student_uuid,
            subject_uuid=model.subject_uuid,
            evaluation_name=model.evaluation_name,
            score=model.score,
            weight=model.weight,
            date=model.date,
            comments=model.comments
        )
    
    def _to_model(self, entity: Grade) -> GradeModel:
        """Convert entity to model"""
        return GradeModel(
            uuid=entity.uuid,
            student_uuid=entity.student_uuid,
            subject_uuid=entity.subject_uuid,
            evaluation_name=entity.evaluation_name,
            score=entity.score,
            weight=entity.weight,
            date=entity.date,
            comments=entity.comments
        )