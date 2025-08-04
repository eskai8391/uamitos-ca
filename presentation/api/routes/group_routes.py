from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, time
from pydantic import BaseModel
import uuid

from domain.entities.group import Group
from domain.value_objects import Uuid
from infrastructure.database import get_db
from infrastructure.repositories.group_repository import GroupRepository
from infrastructure.repositories.subject_repository import SubjectRepository
from infrastructure.repositories.teacher_repository import TeacherRepository
from infrastructure.repositories.student_repository import StudentRepository
from presentation.api.dependencies import get_current_user


router = APIRouter()


# DTOs for Group operations
class GroupCreate(BaseModel):
    name: str
    subject_uuid: str
    teacher_uuid: str
    day_of_week: int
    start_time: str  # Format: "HH:MM"
    end_time: str    # Format: "HH:MM"
    room: str
    max_students: int = 30
    semester: str = "current"
    students_uuids: List[str] = []
    
    class Config:
        orm_mode = True


class GroupResponse(BaseModel):
    uuid: str
    name: str
    subject_uuid: str
    subject_name: str
    teacher_uuid: str
    teacher_name: str
    day_of_week: int
    start_time: str
    end_time: str
    room: str
    max_students: int
    semester: str
    student_count: int
    students: List[Dict[str, Any]] = []
    
    class Config:
        orm_mode = True


class StudentAdd(BaseModel):
    student_uuid: str


@router.post("/groups", response_model=GroupResponse)
def create_group(
    group_data: GroupCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a new group"""
    # Check if the subject and teacher exist
    subject_repo = SubjectRepository(db)
    teacher_repo = TeacherRepository(db)
    
    # Get by ID is used for SubjectRepository since it might not have been updated to use BaseEntityRepository yet
    subject = subject_repo.get_by_id(group_data.subject_uuid)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
        
    # Get by ID is used for TeacherRepository since it might not have been updated to use BaseEntityRepository yet
    teacher = teacher_repo.get_by_id(group_data.teacher_uuid)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Convert time strings to time objects
    try:
        start_time = datetime.strptime(group_data.start_time, "%H:%M").time()
        end_time = datetime.strptime(group_data.end_time, "%H:%M").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format. Use HH:MM")
    
    # Create new Group entity
    group = Group(
        uuid=Uuid(str(uuid.uuid4())),
        name=group_data.name,
        subject_uuid=group_data.subject_uuid,
        teacher_uuid=group_data.teacher_uuid,
        day_of_week=group_data.day_of_week,
        start_time=start_time,
        end_time=end_time,
        room=group_data.room,
        max_students=group_data.max_students,
        semester=group_data.semester,
        students_uuids=group_data.students_uuids
    )
    
    # Save to database
    group_repo = GroupRepository(db)
    created_group = group_repo.create(group)
    
    if not created_group:
        raise HTTPException(status_code=500, detail="Failed to create group")
    
    # Return full group details
    return get_group_response(str(created_group.uuid), db)


@router.get("/groups", response_model=List[GroupResponse])
def get_all_groups(
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get all groups, optionally filtered by semester"""
    group_repo = GroupRepository(db)
    
    groups = group_repo.get_all()
    
    if semester:
        groups = [group for group in groups if group.semester == semester]
        
    # Convert to response format
    return [get_group_response(str(group.uuid), db) for group in groups]


@router.get("/groups/{group_id}", response_model=GroupResponse)
def get_group(
    group_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get a specific group by ID"""
    return get_group_response(group_id, db)


@router.get("/teachers/{teacher_id}/groups", response_model=List[GroupResponse])
def get_teacher_groups(
    teacher_id: str,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get all groups taught by a specific teacher"""
    group_repo = GroupRepository(db)
    
    groups = group_repo.get_by_teacher(teacher_id)
    
    if semester:
        groups = [group for group in groups if group.semester == semester]
        
    # Convert to response format
    return [get_group_response(str(group.uuid), db) for group in groups]


@router.get("/students/{student_id}/groups", response_model=List[GroupResponse])
def get_student_groups(
    student_id: str,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get all groups that a student is enrolled in"""
    group_repo = GroupRepository(db)
    
    groups = group_repo.get_by_student(student_id)
    
    if semester:
        groups = [group for group in groups if group.semester == semester]
        
    # Convert to response format
    return [get_group_response(str(group.uuid), db) for group in groups]


@router.post("/groups/{group_id}/students")
def add_student_to_group(
    group_id: str,
    student_data: StudentAdd,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Add a student to a group"""
    # Check if the student exists
    student_repo = StudentRepository(db)
    # Get by ID is used for StudentRepository since it might not have been updated to use BaseEntityRepository yet
    student = student_repo.get_by_id(student_data.student_uuid)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Add student to group
    group_repo = GroupRepository(db)
    success = group_repo.add_student_to_group(group_id, student_data.student_uuid)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add student to group. Group may be full.")
    
    return {"message": "Student added to group successfully"}


@router.delete("/groups/{group_id}/students/{student_id}")
def remove_student_from_group(
    group_id: str,
    student_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Remove a student from a group"""
    group_repo = GroupRepository(db)
    success = group_repo.remove_student_from_group(group_id, student_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Student not found in group")
    
    return {"message": "Student removed from group successfully"}


@router.delete("/groups/{group_id}")
def delete_group(
    group_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Delete a group"""
    group_repo = GroupRepository(db)
    success = group_repo.delete(group_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Group not found")
    
    return {"message": "Group deleted successfully"}


def get_group_response(group_id: str, db: Session) -> GroupResponse:
    """Helper function to generate a group response with all details"""
    group_repo = GroupRepository(db)
    subject_repo = SubjectRepository(db)
    teacher_repo = TeacherRepository(db)
    student_repo = StudentRepository(db)
    
    group = group_repo.get_by_uuid(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Get subject and teacher details
    # Get by ID is used for these repositories since they might not have been updated to use BaseEntityRepository yet
    subject = subject_repo.get_by_id(group.subject_uuid)
    teacher = teacher_repo.get_by_id(group.teacher_uuid)
    
    if not subject:
        subject_name = "Unknown Subject"
    else:
        subject_name = subject.name
        
    if not teacher:
        teacher_name = "Unknown Teacher"
    else:
        teacher_name = f"{teacher.first_name} {teacher.last_name}"
    
    # Get student details
    students = []
    for student_id in group.students_uuids:
        # Get by ID is used for StudentRepository since it might not have been updated to use BaseEntityRepository yet
        student = student_repo.get_by_id(student_id)
        if student:
            students.append({
                "uuid": str(student.uuid),
                "name": f"{student.first_name} {student.last_name}",
                "email": str(student.email)
            })
    
    # Format times as strings
    start_time_str = group.start_time.strftime("%H:%M")
    end_time_str = group.end_time.strftime("%H:%M")
    
    return GroupResponse(
        uuid=str(group.uuid),
        name=group.name,
        subject_uuid=group.subject_uuid,
        subject_name=subject_name,
        teacher_uuid=group.teacher_uuid,
        teacher_name=teacher_name,
        day_of_week=group.day_of_week,
        start_time=start_time_str,
        end_time=end_time_str,
        room=group.room,
        max_students=group.max_students,
        semester=group.semester,
        student_count=len(group.students_uuids),
        students=students
    )