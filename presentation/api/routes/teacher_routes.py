from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from domain.entities.teacher import Teacher
from domain.entities.subject import Subject
from infrastructure.database import get_db
from infrastructure.repositories.teacher_repository import TeacherRepository
from infrastructure.repositories.subject_repository import SubjectRepository
from presentation.api.dependencies import get_current_user

router = APIRouter()

@router.get("/teachers", response_model=List[Teacher])
def get_teachers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get all teachers"""
    repo = TeacherRepository(db)
    return repo.get_all()

@router.get("/teachers/{teacher_uuid}", response_model=Teacher)
def get_teacher(
    teacher_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get a specific teacher by UUID"""
    repo = TeacherRepository(db)
    teacher = repo.get_by_id(teacher_uuid)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@router.post("/teachers", response_model=Teacher)
def create_teacher(
    teacher: Teacher,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Create a new teacher"""
    repo = TeacherRepository(db)
    return repo.create(teacher)

@router.put("/teachers", response_model=Teacher)
def update_teacher(
    teacher: Teacher,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Update an existing teacher"""
    repo = TeacherRepository(db)
    return repo.update(teacher)

@router.get("/teachers/{teacher_uuid}/subjects", response_model=List[Subject])
def get_teacher_subjects(
    teacher_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get all subjects taught by a specific teacher"""
    subject_repo = SubjectRepository(db)
    return subject_repo.get_by_teacher(teacher_uuid)

@router.get("/teachers/by-subject/{subject_uuid}", response_model=Teacher)
def get_teacher_by_subject(
    subject_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get the teacher assigned to a specific subject"""
    subject_repo = SubjectRepository(db)
    subject = subject_repo.get_by_id(subject_uuid)
    if not subject or not subject.teacher_uuid:
        raise HTTPException(status_code=404, detail="Teacher not found for this subject")
    
    teacher_repo = TeacherRepository(db)
    teacher = teacher_repo.get_by_id(subject.teacher_uuid)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    return teacher