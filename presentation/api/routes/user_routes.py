from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Union, Dict, Any
import json

from domain.entities.user import User, UserRole
from domain.entities.admin import Admin
from domain.entities.teacher import Teacher
from domain.entities.student import Student
from infrastructure.database import get_db
from infrastructure.repositories.admin_repository import AdminRepository
from infrastructure.repositories.teacher_repository import TeacherRepository
from infrastructure.repositories.student_repository import StudentRepository
from presentation.api.dependencies import get_current_user

router = APIRouter()

@router.get("/users", response_model=List[Dict[str, Any]])
def get_all_users(
    role: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get all users, optionally filtered by role and search term.
    Returns a list of user objects with common fields.
    """
    # Initialize repositories
    admin_repo = AdminRepository(db)
    teacher_repo = TeacherRepository(db)
    student_repo = StudentRepository(db)
    
    all_users = []
    
    # Filter by role if specified
    if role and role.lower() == "admin":
        admins = admin_repo.get_all()
        all_users.extend([
            {
                "uuid": str(admin.uuid),
                "email": admin.email.value if hasattr(admin.email, "value") else str(admin.email),
                "first_name": admin.first_name,
                "last_name": admin.last_name,
                "role": "Administrador",
                "active": admin.is_active,
                "last_login": admin.last_login.isoformat() if admin.last_login else None,
                "access_level": admin.access_level
            } 
            for admin in admins
        ])
    elif role and role.lower() == "teacher":
        teachers = teacher_repo.get_all()
        all_users.extend([
            {
                "uuid": str(teacher.uuid),
                "email": teacher.email.value if hasattr(teacher.email, "value") else str(teacher.email),
                "first_name": teacher.first_name,
                "last_name": teacher.last_name,
                "role": "Profesor",
                "active": teacher.is_active,
                "last_login": teacher.last_login.isoformat() if teacher.last_login else None,
                "department": teacher.department,
                "specialization": teacher.specialization
            } 
            for teacher in teachers
        ])
    elif role and role.lower() == "student":
        students = student_repo.get_all()
        all_users.extend([
            {
                "uuid": str(student.uuid),
                "email": student.email.value if hasattr(student.email, "value") else str(student.email),
                "first_name": student.first_name,
                "last_name": student.last_name,
                "role": "Estudiante",
                "active": student.is_active,
                "last_login": student.last_login.isoformat() if student.last_login else None,
                "age": student.age,
                "city": student.city
            } 
            for student in students
        ])
    else:
        # Get all users from all repositories
        admins = admin_repo.get_all()
        teachers = teacher_repo.get_all()
        students = student_repo.get_all()
        
        # Combine users with appropriate role labels
        all_users.extend([
            {
                "uuid": str(admin.uuid),
                "email": admin.email.value if hasattr(admin.email, "value") else str(admin.email),
                "first_name": admin.first_name,
                "last_name": admin.last_name,
                "role": "Administrador",
                "active": admin.is_active,
                "last_login": admin.last_login.isoformat() if admin.last_login else None,
                "access_level": admin.access_level
            } 
            for admin in admins
        ])
        
        all_users.extend([
            {
                "uuid": str(teacher.uuid),
                "email": teacher.email.value if hasattr(teacher.email, "value") else str(teacher.email),
                "first_name": teacher.first_name,
                "last_name": teacher.last_name,
                "role": "Profesor",
                "active": teacher.is_active,
                "last_login": teacher.last_login.isoformat() if teacher.last_login else None,
                "department": teacher.department,
                "specialization": teacher.specialization
            } 
            for teacher in teachers
        ])
        
        all_users.extend([
            {
                "uuid": str(student.uuid),
                "email": student.email.value if hasattr(student.email, "value") else str(student.email),
                "first_name": student.first_name,
                "last_name": student.last_name,
                "role": "Estudiante",
                "active": student.is_active,
                "last_login": student.last_login.isoformat() if student.last_login else None,
                "age": student.age,
                "city": student.city
            } 
            for student in students
        ])
    
    # Filter by search term if specified
    if search:
        search_lower = search.lower()
        filtered_users = []
        for user in all_users:
            # Search in name, email, or role
            if (search_lower in user["first_name"].lower() or 
                search_lower in user["last_name"].lower() or
                search_lower in user["email"].lower() or
                search_lower in user["role"].lower()):
                filtered_users.append(user)
        all_users = filtered_users
    
    # Add 'name' field for convenience (combining first_name and last_name)
    for user in all_users:
        user["name"] = f"{user['first_name']} {user['last_name']}"
    
    return all_users

@router.get("/users/{user_uuid}")
def get_user(
    user_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get a specific user by UUID
    Returns the user details from the appropriate repository based on the user's role
    """
    # Try each repository to find the user
    admin_repo = AdminRepository(db)
    teacher_repo = TeacherRepository(db)
    student_repo = StudentRepository(db)
    
    # Check admin repository
    admin = admin_repo.get_by_id(user_uuid)
    if admin:
        return {
            "uuid": str(admin.uuid),
            "email": admin.email.value if hasattr(admin.email, "value") else str(admin.email),
            "first_name": admin.first_name,
            "last_name": admin.last_name,
            "name": f"{admin.first_name} {admin.last_name}",
            "role": "Administrador",
            "role_id": UserRole.ADMIN.value,
            "active": admin.is_active,
            "last_login": admin.last_login.isoformat() if admin.last_login else None,
            "access_level": admin.access_level
        }
    
    # Check teacher repository
    teacher = teacher_repo.get_by_id(user_uuid)
    if teacher:
        return {
            "uuid": str(teacher.uuid),
            "email": teacher.email.value if hasattr(teacher.email, "value") else str(teacher.email),
            "first_name": teacher.first_name,
            "last_name": teacher.last_name,
            "name": f"{teacher.first_name} {teacher.last_name}",
            "role": "Profesor",
            "role_id": UserRole.TEACHER.value,
            "active": teacher.is_active,
            "last_login": teacher.last_login.isoformat() if teacher.last_login else None,
            "phone": teacher.phone.value if hasattr(teacher.phone, "value") else str(teacher.phone),
            "department": teacher.department,
            "specialization": teacher.specialization
        }
    
    # Check student repository
    student = student_repo.get_by_id(user_uuid)
    if student:
        return {
            "uuid": str(student.uuid),
            "email": student.email.value if hasattr(student.email, "value") else str(student.email),
            "first_name": student.first_name,
            "last_name": student.last_name,
            "name": f"{student.first_name} {student.last_name}",
            "role": "Estudiante",
            "role_id": UserRole.STUDENT.value,
            "active": student.is_active,
            "last_login": student.last_login.isoformat() if student.last_login else None,
            "phone": student.phone.value if hasattr(student.phone, "value") else str(student.phone),
            "address": student.address,
            "city": student.city,
            "state": student.state,
            "zip_code": student.zip_code.value if hasattr(student.zip_code, "value") else str(student.zip_code),
            "age": student.age
        }
    
    # If not found in any repository
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/users/statistics/overview")
def get_user_statistics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get user statistics overview"""
    admin_repo = AdminRepository(db)
    teacher_repo = TeacherRepository(db)
    student_repo = StudentRepository(db)
    
    # Count users by type
    admin_count = len(admin_repo.get_all())
    teacher_count = len(teacher_repo.get_all())
    student_count = len(student_repo.get_all())
    
    # Count active vs inactive users
    active_admins = len([a for a in admin_repo.get_all() if a.is_active])
    active_teachers = len([t for t in teacher_repo.get_all() if t.is_active])
    active_students = len([s for s in student_repo.get_all() if s.is_active])
    
    total_users = admin_count + teacher_count + student_count
    active_users = active_admins + active_teachers + active_students
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": total_users - active_users,
        "user_types": {
            "admin": admin_count,
            "teacher": teacher_count,
            "student": student_count
        },
        "active_by_type": {
            "admin": active_admins,
            "teacher": active_teachers,
            "student": active_students
        },
        "inactive_by_type": {
            "admin": admin_count - active_admins,
            "teacher": teacher_count - active_teachers,
            "student": student_count - active_students
        }
    }