from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from domain.entities.grade import Grade
from infrastructure.database import get_db
from infrastructure.repositories.grade_repository import GradeRepository
from presentation.api.dependencies import get_current_user

router = APIRouter()

@router.get("/grades", response_model=List[Grade])
def get_grades(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get all grades"""
    repo = GradeRepository(db)
    return repo.get_all()

@router.get("/grades/{grade_uuid}", response_model=Grade)
def get_grade(
    grade_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get a specific grade by UUID"""
    repo = GradeRepository(db)
    grade = repo.get_by_id(grade_uuid)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade

@router.get("/grades/student/{student_uuid}", response_model=List[Grade])
def get_student_grades(
    student_uuid: str,
    subject_uuid: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get all grades for a specific student, optionally filtered by subject"""
    repo = GradeRepository(db)
    if subject_uuid:
        return repo.get_by_student_and_subject(student_uuid, subject_uuid)
    else:
        return repo.get_by_student(student_uuid)

@router.get("/grades/subject/{subject_uuid}", response_model=List[Grade])
def get_subject_grades(
    subject_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get all grades for a specific subject"""
    repo = GradeRepository(db)
    return repo.get_by_subject(subject_uuid)

@router.post("/grades", response_model=Grade)
def create_grade(
    grade: Grade,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Create a new grade"""
    repo = GradeRepository(db)
    return repo.create(grade)

@router.put("/grades", response_model=Grade)
def update_grade(
    grade: Grade,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Update an existing grade"""
    repo = GradeRepository(db)
    return repo.update(grade)

@router.delete("/grades/{grade_uuid}")
def delete_grade(
    grade_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete a grade"""
    repo = GradeRepository(db)
    success = repo.delete(grade_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Grade not found")
    return {"message": "Grade deleted successfully"}

@router.get("/grades/statistics/student/{student_uuid}")
def get_student_grade_statistics(
    student_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get grade statistics for a student (average, highest, lowest)"""
    repo = GradeRepository(db)
    grades = repo.get_by_student(student_uuid)
    
    if not grades:
        return {
            "average": 0.0,
            "highest": 0.0,
            "lowest": 0.0,
            "count": 0
        }
    
    scores = [grade.score for grade in grades if grade.score is not None]
    
    if not scores:
        return {
            "average": 0.0,
            "highest": 0.0,
            "lowest": 0.0,
            "count": 0
        }
    
    return {
        "average": sum(scores) / len(scores),
        "highest": max(scores),
        "lowest": min(scores),
        "count": len(scores)
    }

@router.get("/grades/statistics/subject/{subject_uuid}")
def get_subject_grade_statistics(
    subject_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get grade statistics for a subject (average, highest, lowest, distribution)"""
    repo = GradeRepository(db)
    grades = repo.get_by_subject(subject_uuid)
    
    if not grades:
        return {
            "average": 0.0,
            "highest": 0.0,
            "lowest": 0.0,
            "count": 0,
            "distribution": {}
        }
    
    scores = [grade.score for grade in grades if grade.score is not None]
    
    if not scores:
        return {
            "average": 0.0,
            "highest": 0.0,
            "lowest": 0.0,
            "count": 0,
            "distribution": {}
        }
    
    # Calculate grade distribution (ranges: 0-59, 60-69, 70-79, 80-89, 90-100)
    distribution = {
        "0-59": 0,
        "60-69": 0,
        "70-79": 0,
        "80-89": 0,
        "90-100": 0
    }
    
    for score in scores:
        if score < 60:
            distribution["0-59"] += 1
        elif score < 70:
            distribution["60-69"] += 1
        elif score < 80:
            distribution["70-79"] += 1
        elif score < 90:
            distribution["80-89"] += 1
        else:
            distribution["90-100"] += 1
    
    return {
        "average": sum(scores) / len(scores),
        "highest": max(scores),
        "lowest": min(scores),
        "count": len(scores),
        "distribution": distribution
    }