from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, date, time

from domain.entities.subject import Subject
from infrastructure.database import get_db
from infrastructure.repositories.subject_repository import SubjectRepository
from infrastructure.repositories.enrollment_repository import EnrollmentRepository
from infrastructure.repositories.student_repository import StudentRepository
from infrastructure.repositories.teacher_repository import TeacherRepository
from presentation.api.dependencies import get_current_user

router = APIRouter()

# DTO model for schedule entries
class ScheduleEntry:
    subject_uuid: str
    subject_name: str
    teacher_name: str
    day_of_week: int  # 0=Monday, 1=Tuesday, etc.
    start_time: time
    end_time: time
    room: str

@router.get("/schedule/student/{student_uuid}")
def get_student_schedule(
    student_uuid: str,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get the weekly schedule for a student
    Returns a dictionary with days as keys and lists of subjects as values
    """
    # First, verify the student exists
    student_repo = StudentRepository(db)
    student = student_repo.get_by_id(student_uuid)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get the student's enrollments
    enrollment_repo = EnrollmentRepository(db)
    if semester:
        enrollments = enrollment_repo.get_by_student_and_semester(student_uuid, semester)
    else:
        enrollments = enrollment_repo.get_by_student(student_uuid)
    
    if not enrollments:
        # Return empty schedule if no enrollments
        return create_empty_schedule()
    
    # Get subject details for each enrollment
    subject_repo = SubjectRepository(db)
    teacher_repo = TeacherRepository(db)
    
    # Build the schedule
    schedule = create_empty_schedule()
    
    for enrollment in enrollments:
        subject = subject_repo.get_by_id(enrollment.subject_uuid)
        if not subject:
            continue
        
        # Get teacher info
        teacher = None
        if subject.teacher_uuid:
            teacher = teacher_repo.get_by_id(subject.teacher_uuid)
        
        # For each subject, add to the schedule based on its meeting times
        # In a real implementation, you would have subject schedules in the database
        # Here we'll create some sample data based on the subject code
        
        # Extract day of week from the first character of the subject code (1-5)
        # This is just a simple way to generate different schedules for testing
        day = (int(subject.code[-1]) % 5)  # 0=Monday, 1=Tuesday, etc.
        
        # Generate a start time based on subject code
        hour = (8 + int(subject.code[-2]) % 9)  # 8am to 5pm
        
        schedule_item = {
            "subject_uuid": str(subject.uuid),
            "subject_name": subject.name,
            "teacher_name": f"{teacher.first_name} {teacher.last_name}" if teacher else "Not assigned",
            "start_time": f"{hour:02d}:00",
            "end_time": f"{hour+2:02d}:00",
            "room": f"{subject.code[0]}{int(subject.code[-1]) * 100 + int(subject.code[-2]) * 10}"
        }
        
        day_name = ["monday", "tuesday", "wednesday", "thursday", "friday"][day]
        schedule[day_name].append(schedule_item)
    
    return schedule

@router.get("/schedule/teacher/{teacher_uuid}")
def get_teacher_schedule(
    teacher_uuid: str,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get the weekly schedule for a teacher
    Returns a dictionary with days as keys and lists of subjects as values
    """
    # First, verify the teacher exists
    teacher_repo = TeacherRepository(db)
    teacher = teacher_repo.get_by_id(teacher_uuid)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Get the teacher's subjects
    subject_repo = SubjectRepository(db)
    subjects = subject_repo.get_by_teacher(teacher_uuid)
    
    if not subjects:
        # Return empty schedule if no subjects
        return create_empty_schedule()
    
    # Build the schedule
    schedule = create_empty_schedule()
    
    for subject in subjects:
        # For each subject, add to the schedule based on its meeting times
        # In a real implementation, you would have subject schedules in the database
        # Here we'll create some sample data based on the subject code
        
        # Extract day of week from the first character of the subject code (1-5)
        # This is just a simple way to generate different schedules for testing
        day = (int(subject.code[-1]) % 5)  # 0=Monday, 1=Tuesday, etc.
        
        # Generate a start time based on subject code
        hour = (8 + int(subject.code[-2]) % 9)  # 8am to 5pm
        
        schedule_item = {
            "subject_uuid": str(subject.uuid),
            "subject_name": subject.name,
            "start_time": f"{hour:02d}:00",
            "end_time": f"{hour+2:02d}:00",
            "room": f"{subject.code[0]}{int(subject.code[-1]) * 100 + int(subject.code[-2]) * 10}",
            "students_count": get_subject_enrollment_count(subject.uuid, db)
        }
        
        day_name = ["monday", "tuesday", "wednesday", "thursday", "friday"][day]
        schedule[day_name].append(schedule_item)
    
    return schedule

@router.get("/schedule/subject/{subject_uuid}")
def get_subject_schedule(
    subject_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get the weekly schedule for a specific subject
    Returns a dictionary with days as keys and lists of time slots as values
    """
    # First, verify the subject exists
    subject_repo = SubjectRepository(db)
    subject = subject_repo.get_by_id(subject_uuid)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    # Get teacher info
    teacher_repo = TeacherRepository(db)
    teacher = None
    if subject.teacher_uuid:
        teacher = teacher_repo.get_by_id(subject.teacher_uuid)
    
    # Build the schedule
    schedule = create_empty_schedule()
    
    # For the subject, add to the schedule based on its meeting times
    # In a real implementation, you would have subject schedules in the database
    # Here we'll create some sample data based on the subject code
    
    # Extract day of week from the first character of the subject code (1-5)
    day = (int(subject.code[-1]) % 5)  # 0=Monday, 1=Tuesday, etc.
    
    # Generate a start time based on subject code
    hour = (8 + int(subject.code[-2]) % 9)  # 8am to 5pm
    
    schedule_item = {
        "subject_uuid": str(subject.uuid),
        "subject_name": subject.name,
        "teacher_name": f"{teacher.first_name} {teacher.last_name}" if teacher else "Not assigned",
        "start_time": f"{hour:02d}:00",
        "end_time": f"{hour+2:02d}:00",
        "room": f"{subject.code[0]}{int(subject.code[-1]) * 100 + int(subject.code[-2]) * 10}",
        "students_count": get_subject_enrollment_count(subject.uuid, db)
    }
    
    day_name = ["monday", "tuesday", "wednesday", "thursday", "friday"][day]
    schedule[day_name].append(schedule_item)
    
    return schedule

@router.get("/schedule/room/{room_id}")
def get_room_schedule(
    room_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get the weekly schedule for a specific classroom
    Returns a dictionary with days as keys and lists of time slots as values
    """
    # In a real implementation, you would query a rooms table and related schedules
    # For now, we'll create a sample schedule based on the room ID
    
    schedule = create_empty_schedule()
    
    # Mock data generation based on room ID to simulate different schedules
    subject_repo = SubjectRepository(db)
    teacher_repo = TeacherRepository(db)
    
    # Get some random subjects to assign to this room
    subjects = subject_repo.get_all()
    if not subjects:
        return schedule
    
    # Limit to 10 subjects to avoid overloading the schedule
    if len(subjects) > 10:
        subjects = subjects[:10]
    
    for subject in subjects:
        # Generate schedule based on subject code
        day = (int(subject.code[-1]) % 5)  # 0=Monday, 1=Tuesday, etc.
        hour = (8 + int(subject.code[-2]) % 9)  # 8am to 5pm
        
        # Only add to schedule if the generated room matches the requested room
        generated_room = f"{subject.code[0]}{int(subject.code[-1]) * 100 + int(subject.code[-2]) * 10}"
        if generated_room != room_id:
            continue
            
        # Get teacher info
        teacher = None
        if subject.teacher_uuid:
            teacher = teacher_repo.get_by_id(subject.teacher_uuid)
        
        schedule_item = {
            "subject_uuid": str(subject.uuid),
            "subject_name": subject.name,
            "teacher_name": f"{teacher.first_name} {teacher.last_name}" if teacher else "Not assigned",
            "start_time": f"{hour:02d}:00",
            "end_time": f"{hour+2:02d}:00"
        }
        
        day_name = ["monday", "tuesday", "wednesday", "thursday", "friday"][day]
        schedule[day_name].append(schedule_item)
    
    return schedule

def create_empty_schedule() -> Dict[str, List[Any]]:
    """Helper function to create an empty weekly schedule structure"""
    return {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": []
    }

def get_subject_enrollment_count(subject_uuid: str, db: Session) -> int:
    """Helper function to get the number of students enrolled in a subject"""
    enrollment_repo = EnrollmentRepository(db)
    enrollments = enrollment_repo.get_by_subject(subject_uuid)
    return len(enrollments) if enrollments else 0