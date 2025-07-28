from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from domain.entities.attendance import Attendance
from domain.errors.entity_not_found_error import EntityNotFoundError
from domain.value_objects import Uuid
from domain.repositories.base_entity_repository import BaseEntityRepository


@dataclass
class RegisterAttendanceRequest:
    student_uuid: str
    subject_uuid: str
    date: datetime
    status: str  # present, absent, late, excused
    notes: str = ""


@dataclass
class UpdateAttendanceRequest:
    uuid: str
    status: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class GetAttendanceBySubjectRequest:
    subject_uuid: str
    date: Optional[datetime] = None


@dataclass
class GetAttendanceByStudentRequest:
    student_uuid: str
    subject_uuid: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class AttendanceUseCases:
    def __init__(self, repository: BaseEntityRepository):
        self.__repository = repository
    
    def register_attendance(self, request: RegisterAttendanceRequest) -> Attendance:
        """Register attendance for a student"""
        attendance = Attendance(
            uuid=Uuid.new(),
            student_uuid=request.student_uuid,
            subject_uuid=request.subject_uuid,
            date=request.date,
            status=request.status,
            notes=request.notes
        )
        return self.__repository.create(attendance)
    
    def update_attendance(self, request: UpdateAttendanceRequest) -> Attendance:
        """Update attendance record"""
        existing = self.__repository.get_by_uuid(request.uuid)
        if existing is None:
            raise EntityNotFoundError()
        
        updated = Attendance(
            uuid=existing.uuid,
            student_uuid=existing.student_uuid,
            subject_uuid=existing.subject_uuid,
            date=existing.date,
            status=request.status or existing.status,
            notes=request.notes or existing.notes
        )
        
        return self.__repository.update(updated)
    
    def delete_attendance(self, uuid: str) -> bool:
        """Delete attendance record"""
        existing = self.__repository.get_by_uuid(uuid)
        if existing is None:
            raise EntityNotFoundError()
        
        return self.__repository.delete(uuid)
    
    def get_attendance_by_subject(self, request: GetAttendanceBySubjectRequest) -> List[Attendance]:
        """Get attendance records for a subject"""
        # This requires a specific repository method implementation
        raise NotImplementedError("This method requires a specific repository implementation")
    
    def get_attendance_by_student(self, request: GetAttendanceByStudentRequest) -> List[Attendance]:
        """Get attendance records for a student"""
        # This requires a specific repository method implementation
        raise NotImplementedError("This method requires a specific repository implementation")