from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from domain.entities.student import Student
from domain.entities.subject import Subject
from domain.entities.enrollment import Enrollment
from infrastructure.database import get_db
from infrastructure.repositories.student_repository import StudentRepository
from infrastructure.repositories.subject_repository import SubjectRepository
from infrastructure.repositories.enrollment_repository import EnrollmentRepository
from presentation.api.dependencies import get_current_user

router = APIRouter()

@router.get("/students", response_model=List[Student])
def get_students(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = StudentRepository(db)
    return repo.get_all()

@router.post("/students", response_model=Student)
def create_student(
    student: Student,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = StudentRepository(db)
    return repo.create(student)

@router.put("/students", response_model=Student)
def update_student(
    student: Student,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Update an existing student"""
    repo = StudentRepository(db)
    return repo.update(student)

@router.get("/students/{student_uuid}", response_model=Student)
def get_student(
    student_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get a specific student by UUID"""
    repo = StudentRepository(db)
    student = repo.get_by_id(student_uuid)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
    
@router.get("/students/{student_uuid}/subjects", response_model=List[Subject])
def get_student_subjects(
    student_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get all subjects a student is enrolled in"""
    # First get all enrollments for the student
    enrollment_repo = EnrollmentRepository(db)
    enrollments = enrollment_repo.get_by_student(student_uuid)
    
    if not enrollments:
        return []
    
    # Extract subject UUIDs from enrollments
    subject_uuids = [enrollment.subject_uuid for enrollment in enrollments]
    
    # Get subjects by their UUIDs
    subject_repo = SubjectRepository(db)
    subjects = [subject_repo.get_by_id(subject_uuid) for subject_uuid in subject_uuids]
    
    # Filter out any None values (in case a subject was deleted)
    return [subject for subject in subjects if subject]

@router.get("/students/{student_uuid}/enrollments", response_model=List[Enrollment])
def get_student_enrollments(
    student_uuid: str,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get all enrollments for a student, optionally filtered by semester"""
    enrollment_repo = EnrollmentRepository(db)
    
    if semester:
        return enrollment_repo.get_by_student_and_semester(student_uuid, semester)
    else:
        return enrollment_repo.get_by_student(student_uuid)

@router.delete("/students/{student_uuid}")
def delete_student(
    student_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete a student"""
    repo = StudentRepository(db)
    success = repo.delete(student_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}