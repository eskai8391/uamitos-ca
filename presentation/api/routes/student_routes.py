from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from domain.entities.student import Student
from infrastructure.database import get_db
from infrastructure.repositories.student_repository import StudentRepository
from presentation.api.dependencies import get_current_user

router = APIRouter()

@router.get("/students", response_model=list[Student])
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
    repo = StudentRepository(db)
    return repo.update(student)