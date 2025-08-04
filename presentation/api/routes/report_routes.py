from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
import json
import random

from domain.entities.student import Student
from domain.entities.teacher import Teacher
from domain.entities.subject import Subject
from domain.entities.enrollment import Enrollment
from domain.entities.attendance import Attendance
from domain.entities.grade import Grade
from infrastructure.database import get_db
from infrastructure.repositories.student_repository import StudentRepository
from infrastructure.repositories.teacher_repository import TeacherRepository
from infrastructure.repositories.subject_repository import SubjectRepository
from infrastructure.repositories.enrollment_repository import EnrollmentRepository
from infrastructure.repositories.attendance_repository import AttendanceRepository
from infrastructure.repositories.grade_repository import GradeRepository
from presentation.api.dependencies import get_current_user

router = APIRouter()

@router.get("/reports")
def get_all_reports(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get list of available reports
    """
    # In a production system, reports would be stored in a database
    # Here we're returning a static list of available report types
    
    now = datetime.now()
    
    # Generate some sample reports with recent dates
    reports = [
        {
            "uuid": "report-001",
            "name": "Reporte de Asistencia - Agosto 2025",
            "type": "attendance",
            "date": (now - timedelta(days=2)).isoformat(),
            "created_by": "admin@uamitos.edu.mx",
            "status": "Completado"
        },
        {
            "uuid": "report-002",
            "name": "Reporte de Calificaciones - Semestre 2025-1",
            "type": "grades",
            "date": (now - timedelta(days=5)).isoformat(),
            "created_by": "admin@uamitos.edu.mx",
            "status": "Completado"
        },
        {
            "uuid": "report-003",
            "name": "Reporte de Usuarios Nuevos",
            "type": "users",
            "date": (now - timedelta(days=7)).isoformat(),
            "created_by": "admin@uamitos.edu.mx",
            "status": "Completado"
        },
        {
            "uuid": "report-004",
            "name": "Reporte de Rendimiento Académico",
            "type": "performance",
            "date": (now - timedelta(days=10)).isoformat(),
            "created_by": "admin@uamitos.edu.mx",
            "status": "Completado"
        },
        {
            "uuid": "report-005",
            "name": "Reporte de Horarios - Agosto 2025",
            "type": "schedule",
            "date": (now - timedelta(days=3)).isoformat(),
            "created_by": "admin@uamitos.edu.mx", 
            "status": "Completado"
        }
    ]
    
    return reports

@router.get("/reports/{report_uuid}")
def get_report(
    report_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get a specific report by UUID
    """
    # In a production system, this would fetch the report from a database
    # Here we'll generate some mock data based on the report UUID
    
    now = datetime.now()
    
    # Sample report types
    reports = {
        "report-001": {
            "uuid": "report-001",
            "name": "Reporte de Asistencia - Agosto 2025",
            "type": "attendance",
            "date": (now - timedelta(days=2)).isoformat(),
            "created_by": "admin@uamitos.edu.mx",
            "status": "Completado",
            "data": _generate_attendance_report_data(db)
        },
        "report-002": {
            "uuid": "report-002",
            "name": "Reporte de Calificaciones - Semestre 2025-1",
            "type": "grades",
            "date": (now - timedelta(days=5)).isoformat(),
            "created_by": "admin@uamitos.edu.mx",
            "status": "Completado",
            "data": _generate_grades_report_data(db)
        },
        "report-003": {
            "uuid": "report-003",
            "name": "Reporte de Usuarios Nuevos",
            "type": "users",
            "date": (now - timedelta(days=7)).isoformat(),
            "created_by": "admin@uamitos.edu.mx",
            "status": "Completado",
            "data": _generate_users_report_data(db)
        },
        "report-004": {
            "uuid": "report-004",
            "name": "Reporte de Rendimiento Académico",
            "type": "performance",
            "date": (now - timedelta(days=10)).isoformat(),
            "created_by": "admin@uamitos.edu.mx",
            "status": "Completado",
            "data": _generate_performance_report_data(db)
        },
        "report-005": {
            "uuid": "report-005",
            "name": "Reporte de Horarios - Agosto 2025",
            "type": "schedule",
            "date": (now - timedelta(days=3)).isoformat(),
            "created_by": "admin@uamitos.edu.mx",
            "status": "Completado",
            "data": _generate_schedule_report_data(db)
        }
    }
    
    if report_uuid not in reports:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return reports[report_uuid]

@router.post("/reports/generate")
def generate_report(
    report_type: str,
    parameters: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Generate a new report
    
    :param report_type: Type of report to generate
    :param parameters: Optional parameters for the report generation
    :return: Generated report data
    """
    now = datetime.now()
    
    # In a real system, this would generate a report and store it
    # Here we'll generate mock data based on the report type
    if report_type == "attendance":
        data = _generate_attendance_report_data(db)
        name = f"Reporte de Asistencia - {now.strftime('%B %Y')}"
    elif report_type == "grades":
        data = _generate_grades_report_data(db)
        name = f"Reporte de Calificaciones - Semestre {now.year}-{1 if now.month < 7 else 2}"
    elif report_type == "users":
        data = _generate_users_report_data(db)
        name = "Reporte de Usuarios Nuevos"
    elif report_type == "performance":
        data = _generate_performance_report_data(db)
        name = "Reporte de Rendimiento Académico"
    elif report_type == "schedule":
        data = _generate_schedule_report_data(db)
        name = f"Reporte de Horarios - {now.strftime('%B %Y')}"
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported report type: {report_type}")
    
    # Generate a new report object
    report = {
        "uuid": f"report-{now.strftime('%Y%m%d%H%M%S')}",
        "name": name,
        "type": report_type,
        "date": now.isoformat(),
        "created_by": current_user["email"] if isinstance(current_user, dict) else "system",
        "status": "Completado",
        "data": data
    }
    
    # In a real system, you would save this report to a database
    # For now, we'll just return it
    return report

# Helper functions to generate report data

def _generate_attendance_report_data(db: Session) -> Dict[str, Any]:
    """Generate attendance report data"""
    # In a real system, this would query the database for actual attendance data
    # For now, we'll generate some mock data
    
    # Get real subjects and students from the database if available
    subject_repo = SubjectRepository(db)
    student_repo = StudentRepository(db)
    
    subjects = subject_repo.get_all()
    students = student_repo.get_all()
    
    if not subjects or not students:
        # Fallback to mock data if no real data is available
        subject_names = ["Matemáticas", "Física", "Química", "Historia", "Literatura"]
        student_names = ["Alex Johnson", "Maria Garcia", "David Martinez", "Sarah Wilson", "Carlos Rodriguez"]
    else:
        # Use real data
        subject_names = [subject.name for subject in subjects[:5]]
        student_names = [f"{student.first_name} {student.last_name}" for student in students[:5]]
    
    # Generate attendance data for each subject and student
    attendance_data = []
    
    for subject_name in subject_names:
        subject_attendance = {
            "subject": subject_name,
            "total_classes": random.randint(10, 20),
            "students": []
        }
        
        for student_name in student_names:
            # Generate random attendance
            total_classes = subject_attendance["total_classes"]
            present = random.randint(int(total_classes * 0.6), total_classes)
            absent = total_classes - present
            attendance_rate = round(present / total_classes * 100, 1)
            
            student_attendance = {
                "name": student_name,
                "present": present,
                "absent": absent,
                "attendance_rate": attendance_rate,
                "status": "Good" if attendance_rate >= 80 else "Warning" if attendance_rate >= 60 else "Critical"
            }
            
            subject_attendance["students"].append(student_attendance)
        
        attendance_data.append(subject_attendance)
    
    # Calculate overall statistics
    total_classes = sum(subject["total_classes"] for subject in attendance_data)
    total_present = sum(sum(student["present"] for student in subject["students"]) for subject in attendance_data)
    total_absent = sum(sum(student["absent"] for student in subject["students"]) for subject in attendance_data)
    
    overall_attendance_rate = round(total_present / (total_present + total_absent) * 100, 1) if (total_present + total_absent) > 0 else 0
    
    return {
        "overall_attendance_rate": overall_attendance_rate,
        "total_classes": total_classes,
        "subjects": attendance_data
    }

def _generate_grades_report_data(db: Session) -> Dict[str, Any]:
    """Generate grades report data"""
    # In a real system, this would query the database for actual grade data
    # For now, we'll generate some mock data
    
    # Get real subjects and students from the database if available
    subject_repo = SubjectRepository(db)
    student_repo = StudentRepository(db)
    
    subjects = subject_repo.get_all()
    students = student_repo.get_all()
    
    if not subjects or not students:
        # Fallback to mock data if no real data is available
        subject_names = ["Matemáticas", "Física", "Química", "Historia", "Literatura"]
        student_names = ["Alex Johnson", "Maria Garcia", "David Martinez", "Sarah Wilson", "Carlos Rodriguez"]
    else:
        # Use real data
        subject_names = [subject.name for subject in subjects[:5]]
        student_names = [f"{student.first_name} {student.last_name}" for student in students[:5]]
    
    # Generate grade data for each subject and student
    grades_data = []
    
    for subject_name in subject_names:
        subject_grades = {
            "subject": subject_name,
            "students": []
        }
        
        subject_total = 0
        
        for student_name in student_names:
            # Generate random grades
            midterm = round(random.uniform(60, 100), 1)
            final = round(random.uniform(60, 100), 1)
            assignments = round(random.uniform(60, 100), 1)
            
            # Calculate final grade
            final_grade = round(midterm * 0.3 + final * 0.4 + assignments * 0.3, 1)
            subject_total += final_grade
            
            student_grade = {
                "name": student_name,
                "midterm": midterm,
                "final": final,
                "assignments": assignments,
                "final_grade": final_grade,
                "status": "Aprobado" if final_grade >= 60 else "Reprobado"
            }
            
            subject_grades["students"].append(student_grade)
        
        # Add average grade for the subject
        subject_grades["average"] = round(subject_total / len(student_names), 1)
        grades_data.append(subject_grades)
    
    # Calculate overall statistics
    overall_average = sum(subject["average"] for subject in grades_data) / len(grades_data)
    
    return {
        "overall_average": round(overall_average, 1),
        "subjects": grades_data
    }

def _generate_users_report_data(db: Session) -> Dict[str, Any]:
    """Generate users report data"""
    # Get actual user counts from repositories
    student_repo = StudentRepository(db)
    teacher_repo = TeacherRepository(db)
    
    students = student_repo.get_all()
    teachers = teacher_repo.get_all()
    
    student_count = len(students) if students else 0
    teacher_count = len(teachers) if teachers else 0
    
    # If no real data, use random counts
    if student_count == 0 and teacher_count == 0:
        student_count = random.randint(50, 200)
        teacher_count = random.randint(10, 30)
    
    # Generate active and inactive counts
    active_students = len([s for s in students if s.is_active]) if students else int(student_count * 0.9)
    active_teachers = len([t for t in teachers if t.is_active]) if teachers else int(teacher_count * 0.95)
    
    inactive_students = student_count - active_students
    inactive_teachers = teacher_count - active_teachers
    
    # Generate month-by-month new user counts for the last 6 months
    now = datetime.now()
    months = []
    
    for i in range(5, -1, -1):
        month_date = now - timedelta(days=i * 30)
        month_name = month_date.strftime("%b")
        
        # Generate random new user counts
        new_students = random.randint(5, 15)
        new_teachers = random.randint(1, 3)
        
        months.append({
            "month": month_name,
            "new_students": new_students,
            "new_teachers": new_teachers
        })
    
    return {
        "total_users": student_count + teacher_count,
        "student_count": student_count,
        "teacher_count": teacher_count,
        "active_students": active_students,
        "active_teachers": active_teachers,
        "inactive_students": inactive_students,
        "inactive_teachers": inactive_teachers,
        "monthly_growth": months
    }

def _generate_performance_report_data(db: Session) -> Dict[str, Any]:
    """Generate academic performance report data"""
    # In a real system, this would query the database for actual performance data
    # For now, we'll generate some mock data
    
    # Performance metrics for the current semester
    current_semester = {
        "overall_gpa": round(random.uniform(7.0, 9.0), 1),
        "pass_rate": round(random.uniform(0.8, 0.95) * 100, 1),
        "attendance_rate": round(random.uniform(0.85, 0.98) * 100, 1),
        "subject_performance": []
    }
    
    # Get real subjects from the database if available
    subject_repo = SubjectRepository(db)
    subjects = subject_repo.get_all()
    
    if not subjects:
        # Fallback to mock data if no real subjects available
        subject_names = ["Matemáticas", "Física", "Química", "Historia", "Literatura", 
                        "Inglés", "Computación", "Biología", "Educación Física", "Arte"]
    else:
        # Use real data
        subject_names = [subject.name for subject in subjects[:10]]
    
    # Generate performance data for each subject
    for subject_name in subject_names:
        avg_grade = round(random.uniform(60, 95), 1)
        pass_rate = round(random.uniform(0.7, 1.0) * 100, 1)
        
        subject_performance = {
            "name": subject_name,
            "average_grade": avg_grade,
            "pass_rate": pass_rate,
            "performance_level": "Excelente" if avg_grade >= 90 else 
                              "Bueno" if avg_grade >= 80 else 
                              "Satisfactorio" if avg_grade >= 70 else 
                              "Necesita mejorar"
        }
        
        current_semester["subject_performance"].append(subject_performance)
    
    # Historical semester data (last 5 semesters)
    historical_data = []
    
    for i in range(5):
        semester_name = f"{2023 + i//2}-{2 if i % 2 else 1}"
        
        semester_data = {
            "name": semester_name,
            "overall_gpa": round(random.uniform(7.0, 9.0), 1),
            "pass_rate": round(random.uniform(0.8, 0.95) * 100, 1),
            "attendance_rate": round(random.uniform(0.85, 0.98) * 100, 1)
        }
        
        historical_data.append(semester_data)
    
    return {
        "current_semester": current_semester,
        "historical_data": historical_data
    }

def _generate_schedule_report_data(db: Session) -> Dict[str, Any]:
    """Generate schedule report data"""
    # In a real system, this would query the database for actual schedule data
    # For now, we'll generate some mock data
    
    # Get real teachers and subjects from the database if available
    teacher_repo = TeacherRepository(db)
    subject_repo = SubjectRepository(db)
    
    teachers = teacher_repo.get_all()
    subjects = subject_repo.get_all()
    
    if not teachers or not subjects:
        # Fallback to mock data if no real data available
        teacher_names = ["John Doe", "Jane Smith", "Pedro Gonzalez", "Maria Rodriguez", "Luis Hernandez"]
        subject_names = ["Matemáticas", "Física", "Química", "Historia", "Literatura"]
        room_ids = ["A101", "A102", "B201", "B202", "C301"]
    else:
        # Use real data
        teacher_names = [f"{teacher.first_name} {teacher.last_name}" for teacher in teachers[:5]]
        subject_names = [subject.name for subject in subjects[:5]]
        # Generate room IDs
        room_ids = [f"{chr(65 + i//3)}{100 + i%3 + 1}" for i in range(5)]
    
    # Days of the week
    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    
    # Time slots
    time_slots = ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]
    
    # Generate schedule data
    schedule_data = []
    
    # Teacher schedules
    teacher_schedules = []
    
    for i, teacher_name in enumerate(teacher_names):
        teacher_schedule = {
            "name": teacher_name,
            "total_hours": 0,
            "schedule": {}
        }
        
        # Initialize schedule for each day
        for day in days:
            teacher_schedule["schedule"][day] = []
        
        # Assign 2-3 time slots for each teacher
        num_slots = random.randint(2, 3)
        assigned_slots = []
        
        for _ in range(num_slots):
            # Pick a random day and time slot
            day = random.choice(days)
            time_slot = random.choice(time_slots)
            
            # Avoid duplicate assignments
            if (day, time_slot) in assigned_slots:
                continue
                
            assigned_slots.append((day, time_slot))
            
            # Pick a random subject and room
            subject = random.choice(subject_names)
            room = random.choice(room_ids)
            
            # Calculate hours (each slot is 2 hours)
            teacher_schedule["total_hours"] += 2
            
            # Add to schedule
            teacher_schedule["schedule"][day].append({
                "time": time_slot,
                "subject": subject,
                "room": room
            })
        
        teacher_schedules.append(teacher_schedule)
    
    # Room utilization
    room_utilization = []
    
    for room_id in room_ids:
        # Count how many times this room is used
        usage_count = 0
        for teacher_schedule in teacher_schedules:
            for day_schedule in teacher_schedule["schedule"].values():
                for slot in day_schedule:
                    if slot["room"] == room_id:
                        usage_count += 1
        
        # Calculate utilization rate (out of 25 possible slots - 5 days * 5 time slots)
        utilization_rate = round(usage_count / 25 * 100, 1)
        
        room_utilization.append({
            "room_id": room_id,
            "usage_count": usage_count,
            "utilization_rate": utilization_rate
        })
    
    return {
        "teacher_schedules": teacher_schedules,
        "room_utilization": room_utilization
    }