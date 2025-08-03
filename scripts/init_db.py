import sys
import os
import logging
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.database import db, create_all, drop_all
from infrastructure.repositories.admin_repository import AdminRepository
from infrastructure.repositories.teacher_repository import TeacherRepository
from infrastructure.repositories.student_repository import StudentRepository
from infrastructure.repositories.subject_repository import SubjectRepository

from domain.entities.admin import Admin
from domain.entities.teacher import Teacher
from domain.entities.student import Student
from domain.entities.subject import Subject
from domain.entities.user import UserRole
from domain.value_objects import Uuid, Email, Password, Phone, ZipCode
from infrastructure.security.bcrypt_hasher import BcryptHasher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def create_tables():
    """Create all database tables"""
    try:
        logger.info("Creating database tables...")
        create_all()
        logger.info("Tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}", exc_info=True)
        raise


def drop_tables():
    """Drop all database tables"""
    try:
        logger.info("Dropping database tables...")
        drop_all()
        logger.info("Tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping tables: {e}", exc_info=True)
        raise


def create_test_data():
    """Create test data for the application"""
    try:
        logger.info("Creating test data...")
        
        # Create database session
        session = db.create_session()
        hasher = BcryptHasher()
        
        # Create repositories
        admin_repo = AdminRepository(session)
        teacher_repo = TeacherRepository(session)
        student_repo = StudentRepository(session)
        subject_repo = SubjectRepository(session)
        
        # Create admin
        admin = Admin(
            uuid=Uuid.new(),
            email=Email("admin@uamitos.edu.mx"),
            password=Password.create("Admin123!", hasher),
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
            access_level=2,
            is_active=True,
            last_login=datetime.now()
        )
        admin_repo.create(admin)
        logger.info(f"Admin created: {admin.email.value}")
        
        # Create teachers
        teachers = [
            Teacher(
                uuid=Uuid.new(),
                email=Email("john.doe@uamitos.edu.mx"),
                password=Password.create("Teacher123!", hasher),
                first_name="John",
                last_name="Doe",
                role=UserRole.TEACHER,
                phone=Phone("5551234567"),
                department="Computer Science",
                specialization="Software Engineering",
                is_active=True,
                last_login=datetime.now()
            ),
            Teacher(
                uuid=Uuid.new(),
                email=Email("jane.smith@uamitos.edu.mx"),
                password=Password.create("Teacher123!", hasher),
                first_name="Jane",
                last_name="Smith",
                role=UserRole.TEACHER,
                phone=Phone("5559876543"),
                department="Mathematics",
                specialization="Calculus",
                is_active=True,
                last_login=datetime.now()
            )
        ]
        
        for teacher in teachers:
            teacher_repo.create(teacher)
            logger.info(f"Teacher created: {teacher.email.value}")
        
        # Create students
        students = [
            Student(
                uuid=Uuid.new(),
                email=Email("alex.johnson@uamitos.edu.mx"),
                password=Password.create("Student123!", hasher),
                first_name="Alex",
                last_name="Johnson",
                role=UserRole.STUDENT,
                phone=Phone("5551112222"),
                address="123 Main St",
                city="Mexico City",
                state="CDMX",
                zip_code=ZipCode("04500"),
                age=20,
                is_active=True,
                last_login=datetime.now()
            ),
            Student(
                uuid=Uuid.new(),
                email=Email("maria.garcia@uamitos.edu.mx"),
                password=Password.create("Student123!", hasher),
                first_name="Maria",
                last_name="Garcia",
                role=UserRole.STUDENT,
                phone=Phone("5553334444"),
                address="456 Oak Ave",
                city="Mexico City",
                state="CDMX",
                zip_code=ZipCode("04600"),
                age=22,
                is_active=True,
                last_login=datetime.now()
            ),
            Student(
                uuid=Uuid.new(),
                email=Email("david.martinez@uamitos.edu.mx"),
                password=Password.create("Student123!", hasher),
                first_name="David",
                last_name="Martinez",
                role=UserRole.STUDENT,
                phone=Phone("5555556666"),
                address="789 Pine St",
                city="Mexico City",
                state="CDMX",
                zip_code=ZipCode("04700"),
                age=21,
                is_active=True,
                last_login=datetime.now()
            )
        ]
        
        for student in students:
            student_repo.create(student)
            logger.info(f"Student created: {student.email.value}")
        
        # Create subjects
        subjects = [
            Subject(
                uuid=Uuid.new(),
                name="Introduction to Programming",
                code="CS101",
                description="Basic programming concepts and algorithms",
                credits=4,
                semester=1,
                teacher_uuid=str(teachers[0].uuid),
            ),
            Subject(
                uuid=Uuid.new(),
                name="Calculus I",
                code="MATH201",
                description="Limits, derivatives, and integrals",
                credits=4,
                semester=1,
                teacher_uuid=str(teachers[1].uuid)
            ),
            Subject(
                uuid=Uuid.new(),
                name="Software Engineering",
                code="CS301",
                description="Software development methodologies and practices",
                credits=4,
                semester=3,
                teacher_uuid=str(teachers[0].uuid)
            )
        ]
        
        for subject in subjects:
            subject_repo.create(subject)
            logger.info(f"Subject created: {subject.name} ({subject.code})")
        
        logger.info("Test data created successfully")
        
    except Exception as e:
        logger.error(f"Error creating test data: {e}", exc_info=True)
        raise
    finally:
        session.close()


def reset_database():
    """Reset the database and create test data"""
    try:
        drop_tables()
        create_tables()
        create_test_data()
        logger.info("Database reset complete")
    except Exception as e:
        logger.error(f"Database reset failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database management script")
    parser.add_argument('--reset', action='store_true', help='Reset database and create test data')
    parser.add_argument('--create-tables', action='store_true', help='Create database tables')
    parser.add_argument('--drop-tables', action='store_true', help='Drop database tables')
    parser.add_argument('--create-test-data', action='store_true', help='Create test data')
    
    args = parser.parse_args()
    
    if args.reset:
        reset_database()
    elif args.create_tables:
        create_tables()
    elif args.drop_tables:
        drop_tables()
    elif args.create_test_data:
        create_test_data()
    else:
        parser.print_help()