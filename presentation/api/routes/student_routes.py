from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from domain.entities.student import Student
from infrastructure.database import get_db
from infrastructure.repositories.student_repository import StudentRepository

router = APIRouter()

@router.get("/students", response_model=list[Student])
def get_students(db: Session = Depends(get_db)):
    repo = StudentRepository(db)
    return repo.get_all()

@router.post("/students", response_model=Student)
def create_student(student: Student, db: Session = Depends(get_db)):
    repo = StudentRepository(db)
    return repo.create(student)

@router.put("/students", response_model=Student)
def update_student(student: Student, db: Session = Depends(get_db)):
    repo = StudentRepository(db)
    return repo.update(student)