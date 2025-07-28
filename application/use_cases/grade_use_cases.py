from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict

from domain.entities.grade import Grade
from domain.entities.enrollment import Enrollment
from domain.errors.entity_not_found_error import EntityNotFoundError
from domain.value_objects import Uuid
from domain.repositories.base_entity_repository import BaseEntityRepository


@dataclass
class AddGradeRequest:
    student_uuid: str
    subject_uuid: str
    evaluation_name: str
    score: float
    weight: float
    date: datetime
    comments: str = ""


@dataclass
class UpdateGradeRequest:
    uuid: str
    score: Optional[float] = None
    weight: Optional[float] = None
    comments: Optional[str] = None


@dataclass
class GetStudentGradesRequest:
    student_uuid: str
    subject_uuid: Optional[str] = None


@dataclass
class GetSubjectGradesRequest:
    subject_uuid: str


@dataclass
class StudentGradeSummary:
    student_uuid: str
    student_name: str
    grades: Dict[str, float]  # Mapping of evaluation_name to score
    final_grade: float


class GradeUseCases:
    def __init__(
        self, 
        grade_repository: BaseEntityRepository,
        enrollment_repository: Optional[BaseEntityRepository] = None
    ):
        self.__grade_repository = grade_repository
        self.__enrollment_repository = enrollment_repository
    
    def add_grade(self, request: AddGradeRequest) -> Grade:
        """Add a new grade for a student"""
        grade = Grade(
            uuid=Uuid.new(),
            student_uuid=request.student_uuid,
            subject_uuid=request.subject_uuid,
            evaluation_name=request.evaluation_name,
            score=request.score,
            weight=request.weight,
            date=request.date,
            comments=request.comments
        )
        return self.__grade_repository.create(grade)
    
    def update_grade(self, request: UpdateGradeRequest) -> Grade:
        """Update an existing grade"""
        existing = self.__grade_repository.get_by_uuid(request.uuid)
        if existing is None:
            raise EntityNotFoundError()
        
        updated = Grade(
            uuid=existing.uuid,
            student_uuid=existing.student_uuid,
            subject_uuid=existing.subject_uuid,
            evaluation_name=existing.evaluation_name,
            score=request.score if request.score is not None else existing.score,
            weight=request.weight if request.weight is not None else existing.weight,
            date=existing.date,
            comments=request.comments if request.comments is not None else existing.comments
        )
        
        return self.__grade_repository.update(updated)
    
    def delete_grade(self, uuid: str) -> bool:
        """Delete a grade"""
        existing = self.__grade_repository.get_by_uuid(uuid)
        if existing is None:
            raise EntityNotFoundError()
        
        return self.__grade_repository.delete(uuid)
    
    def get_student_grades(self, request: GetStudentGradesRequest) -> List[Grade]:
        """Get grades for a specific student"""
        # This requires a specific repository method implementation
        raise NotImplementedError("This method requires a specific repository implementation")
    
    def get_subject_grades(self, request: GetSubjectGradesRequest) -> List[Grade]:
        """Get all grades for a specific subject"""
        # This requires a specific repository method implementation
        raise NotImplementedError("This method requires a specific repository implementation")
    
    def calculate_final_grade(self, student_uuid: str, subject_uuid: str) -> float:
        """Calculate final grade for a student in a subject"""
        # This requires a specific repository method implementation
        raise NotImplementedError("This method requires a specific repository implementation")
    
    def update_enrollment_final_grade(self, student_uuid: str, subject_uuid: str) -> Optional[Enrollment]:
        """Update final grade in enrollment record"""
        if not self.__enrollment_repository:
            return None
            
        # Calculate final grade
        final_grade = self.calculate_final_grade(student_uuid, subject_uuid)
        
        # Find enrollment
        # This requires a specific repository method implementation
        raise NotImplementedError("This method requires a specific repository implementation")