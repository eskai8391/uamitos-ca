import sys
import os
import logging
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.database import db, create_all, drop_all
from infrastructure.repositories.admin_repository import AdminRepository
from infrastructure.repositories.teacher_repository import TeacherRepository
from infrastructure.repositories.student_repository import StudentRepository
from infrastructure.repositories.subject_repository import SubjectRepository
from infrastructure.repositories.attendance_repository import AttendanceRepository
from infrastructure.repositories.enrollment_repository import EnrollmentRepository
from infrastructure.repositories.grade_repository import GradeRepository
from infrastructure.repositories.event_repository import EventRepository

from domain.entities.admin import Admin
from domain.entities.teacher import Teacher
from domain.entities.student import Student
from domain.entities.subject import Subject
from domain.entities.attendance import Attendance
from domain.entities.enrollment import Enrollment
from domain.entities.grade import Grade
from domain.entities.event import Event
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
        attendance_repo = AttendanceRepository(session)
        enrollment_repo = EnrollmentRepository(session)
        grade_repo = GradeRepository(session)
        event_repo = EventRepository(session)
        
        # Create admins - expanded to include 3 admins
        admins = [
            Admin(
                uuid=Uuid.new(),
                email=Email("admin@uamitos.edu.mx"),
                password=Password.create("Admin123!", hasher),
                first_name="Admin",
                last_name="User",
                role=UserRole.ADMIN,
                access_level=3,  # Highest level
                is_active=True,
                last_login=datetime.now()
            ),
            Admin(
                uuid=Uuid.new(),
                email=Email("director@uamitos.edu.mx"),
                password=Password.create("Admin123!", hasher),
                first_name="Carlos",
                last_name="Ramirez",
                role=UserRole.ADMIN,
                access_level=3,
                is_active=True,
                last_login=datetime.now()
            ),
            Admin(
                uuid=Uuid.new(),
                email=Email("registrar@uamitos.edu.mx"),
                password=Password.create("Admin123!", hasher),
                first_name="Lucia",
                last_name="Valdez",
                role=UserRole.ADMIN,
                access_level=2,
                is_active=True,
                last_login=datetime.now()
            ),
            Admin(
                uuid=Uuid.new(),
                email=Email("coordinator@uamitos.edu.mx"),
                password=Password.create("Admin123!", hasher),
                first_name="Eduardo",
                last_name="Mendoza",
                role=UserRole.ADMIN,
                access_level=2,
                is_active=True,
                last_login=datetime.now()
            ),
            Admin(
                uuid=Uuid.new(),
                email=Email("sysadmin@uamitos.edu.mx"),
                password=Password.create("Admin123!", hasher),
                first_name="Fernando",
                last_name="Torres",
                role=UserRole.ADMIN,
                access_level=1,
                is_active=True,
                last_login=datetime.now()
            )
        ]
        
        for admin in admins:
            admin_repo.create(admin)
            logger.info(f"Admin created: {admin.email.value}")
        
        # Create teachers - expanded to include 10 teachers
        departments = ["Computer Science", "Mathematics", "Physics", "Chemistry", "Biology", 
                      "Literature", "History", "Engineering", "Art", "Physical Education"]
        specializations = ["Software Engineering", "Calculus", "Quantum Physics", "Organic Chemistry", 
                          "Microbiology", "Contemporary Literature", "World History", "Mechanical Engineering",
                          "Digital Arts", "Sports Science"]
        
        teachers = [
            # Original teachers
            Teacher(
                uuid=str(Uuid.new()),
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
                uuid=str(Uuid.new()),
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
            ),
            # Additional teachers
            Teacher(
                uuid=str(Uuid.new()),
                email=Email("pedro.gonzalez@uamitos.edu.mx"),
                password=Password.create("Teacher123!", hasher),
                first_name="Pedro",
                last_name="Gonzalez",
                role=UserRole.TEACHER,
                phone=Phone("5552223333"),
                department="Physics",
                specialization="Quantum Physics",
                is_active=True,
                last_login=datetime.now()
            ),
            Teacher(
                uuid=str(Uuid.new()),
                email=Email("maria.rodriguez@uamitos.edu.mx"),
                password=Password.create("Teacher123!", hasher),
                first_name="Maria",
                last_name="Rodriguez",
                role=UserRole.TEACHER,
                phone=Phone("5553334444"),
                department="Chemistry",
                specialization="Organic Chemistry",
                is_active=True,
                last_login=datetime.now()
            ),
            Teacher(
                uuid=str(Uuid.new()),
                email=Email("luis.hernandez@uamitos.edu.mx"),
                password=Password.create("Teacher123!", hasher),
                first_name="Luis",
                last_name="Hernandez",
                role=UserRole.TEACHER,
                phone=Phone("5554445555"),
                department="Biology",
                specialization="Microbiology",
                is_active=True,
                last_login=datetime.now()
            ),
            Teacher(
                uuid=str(Uuid.new()),
                email=Email("carmen.perez@uamitos.edu.mx"),
                password=Password.create("Teacher123!", hasher),
                first_name="Carmen",
                last_name="Perez",
                role=UserRole.TEACHER,
                phone=Phone("5555556666"),
                department="Literature",
                specialization="Contemporary Literature",
                is_active=True,
                last_login=datetime.now()
            ),
            Teacher(
                uuid=str(Uuid.new()),
                email=Email("roberto.sanchez@uamitos.edu.mx"),
                password=Password.create("Teacher123!", hasher),
                first_name="Roberto",
                last_name="Sanchez",
                role=UserRole.TEACHER,
                phone=Phone("5556667777"),
                department="History",
                specialization="World History",
                is_active=True,
                last_login=datetime.now()
            ),
            Teacher(
                uuid=str(Uuid.new()),
                email=Email("ana.martinez@uamitos.edu.mx"),
                password=Password.create("Teacher123!", hasher),
                first_name="Ana",
                last_name="Martinez",
                role=UserRole.TEACHER,
                phone=Phone("5557778888"),
                department="Engineering",
                specialization="Mechanical Engineering",
                is_active=True,
                last_login=datetime.now()
            ),
            Teacher(
                uuid=str(Uuid.new()),
                email=Email("miguel.lopez@uamitos.edu.mx"),
                password=Password.create("Teacher123!", hasher),
                first_name="Miguel",
                last_name="Lopez",
                role=UserRole.TEACHER,
                phone=Phone("5558889999"),
                department="Art",
                specialization="Digital Arts",
                is_active=True,
                last_login=datetime.now()
            ),
            Teacher(
                uuid=str(Uuid.new()),
                email=Email("laura.gomez@uamitos.edu.mx"),
                password=Password.create("Teacher123!", hasher),
                first_name="Laura",
                last_name="Gomez",
                role=UserRole.TEACHER,
                phone=Phone("5559990000"),
                department="Physical Education",
                specialization="Sports Science",
                is_active=True,
                last_login=datetime.now()
            )
        ]
        
        for teacher in teachers:
            teacher_repo.create(teacher)
            logger.info(f"Teacher created: {teacher.email.value}")
        
        # Create students - expanded to 20 students
        student_details = [
            # Original students
            {
                "email": "alex.johnson@uamitos.edu.mx",
                "first_name": "Alex",
                "last_name": "Johnson",
                "phone": "5551112222",
                "address": "123 Main St",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "04500",
                "age": 20
            },
            {
                "email": "maria.garcia@uamitos.edu.mx",
                "first_name": "Maria",
                "last_name": "Garcia",
                "phone": "5553334444",
                "address": "456 Oak Ave",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "04600",
                "age": 22
            },
            {
                "email": "david.martinez@uamitos.edu.mx",
                "first_name": "David",
                "last_name": "Martinez",
                "phone": "5555556666",
                "address": "789 Pine St",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "04700",
                "age": 21
            },
            # Additional students
            {
                "email": "sofia.lopez@uamitos.edu.mx",
                "first_name": "Sofia",
                "last_name": "Lopez",
                "phone": "5551234567",
                "address": "101 Reforma Ave",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "04800",
                "age": 19
            },
            {
                "email": "jose.rodriguez@uamitos.edu.mx",
                "first_name": "Jose",
                "last_name": "Rodriguez",
                "phone": "5552345678",
                "address": "202 Juarez St",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "04900",
                "age": 23
            },
            {
                "email": "isabella.hernandez@uamitos.edu.mx",
                "first_name": "Isabella",
                "last_name": "Hernandez",
                "phone": "5553456789",
                "address": "303 Polanco Blvd",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "05000",
                "age": 20
            },
            {
                "email": "miguel.torres@uamitos.edu.mx",
                "first_name": "Miguel",
                "last_name": "Torres",
                "phone": "5554567890",
                "address": "404 Roma North",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "05100",
                "age": 22
            },
            {
                "email": "valentina.diaz@uamitos.edu.mx",
                "first_name": "Valentina",
                "last_name": "Diaz",
                "phone": "5555678901",
                "address": "505 Condesa Ave",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "05200",
                "age": 21
            },
            {
                "email": "alejandro.perez@uamitos.edu.mx",
                "first_name": "Alejandro",
                "last_name": "Perez",
                "phone": "5556789012",
                "address": "606 Chapultepec",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "05300",
                "age": 24
            },
            {
                "email": "camila.sanchez@uamitos.edu.mx",
                "first_name": "Camila",
                "last_name": "Sanchez",
                "phone": "5557890123",
                "address": "707 Coyoacan",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "05400",
                "age": 20
            },
            {
                "email": "sebastian.ramirez@uamitos.edu.mx",
                "first_name": "Sebastian",
                "last_name": "Ramirez",
                "phone": "5558901234",
                "address": "808 San Angel",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "05500",
                "age": 22
            },
            {
                "email": "victoria.flores@uamitos.edu.mx",
                "first_name": "Victoria",
                "last_name": "Flores",
                "phone": "5559012345",
                "address": "909 Tlalpan",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "05600",
                "age": 21
            },
            {
                "email": "mateo.gonzalez@uamitos.edu.mx",
                "first_name": "Mateo",
                "last_name": "Gonzalez",
                "phone": "5550123456",
                "address": "1010 Xochimilco",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "05700",
                "age": 19
            },
            {
                "email": "valeria.reyes@uamitos.edu.mx",
                "first_name": "Valeria",
                "last_name": "Reyes",
                "phone": "5551234567",
                "address": "1111 Iztapalapa",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "05800",
                "age": 23
            },
            {
                "email": "santiago.cruz@uamitos.edu.mx",
                "first_name": "Santiago",
                "last_name": "Cruz",
                "phone": "5552345678",
                "address": "1212 Cuauhtemoc",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "05900",
                "age": 20
            },
            {
                "email": "daniela.gomez@uamitos.edu.mx",
                "first_name": "Daniela",
                "last_name": "Gomez",
                "phone": "5553456789",
                "address": "1313 Benito Juarez",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "06000",
                "age": 22
            },
            {
                "email": "leonardo.vargas@uamitos.edu.mx",
                "first_name": "Leonardo",
                "last_name": "Vargas",
                "phone": "5554567890",
                "address": "1414 Miguel Hidalgo",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "06100",
                "age": 21
            },
            {
                "email": "regina.castro@uamitos.edu.mx",
                "first_name": "Regina",
                "last_name": "Castro",
                "phone": "5555678901",
                "address": "1515 Alvaro Obregon",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "06200",
                "age": 20
            },
            {
                "email": "emilio.jimenez@uamitos.edu.mx",
                "first_name": "Emilio",
                "last_name": "Jimenez",
                "phone": "5556789012",
                "address": "1616 Venustiano Carranza",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "06300",
                "age": 23
            },
            {
                "email": "renata.morales@uamitos.edu.mx",
                "first_name": "Renata",
                "last_name": "Morales",
                "phone": "5557890123",
                "address": "1717 Azcapotzalco",
                "city": "Mexico City",
                "state": "CDMX",
                "zip_code": "06400",
                "age": 21
            }
        ]
        
        students = []
        for student_detail in student_details:
            student = Student(
                uuid=str(Uuid.new()),
                email=Email(student_detail["email"]),
                password=Password.create("Student123!", hasher),
                first_name=student_detail["first_name"],
                last_name=student_detail["last_name"],
                role=UserRole.STUDENT,
                phone=Phone(student_detail["phone"]),
                address=student_detail["address"],
                city=student_detail["city"],
                state=student_detail["state"],
                zip_code=ZipCode(student_detail["zip_code"]),
                age=student_detail["age"],
                is_active=True,
                last_login=datetime.now()
            )
            students.append(student)
            student_repo.create(student)
            logger.info(f"Student created: {student.email.value}")
            
        # Create more subjects - expanded to 15 subjects
        subject_details = [
            # Original subjects
            {
                "name": "Introduction to Programming", 
                "code": "CS101", 
                "description": "Basic programming concepts and algorithms", 
                "credits": 4, 
                "semester": 1, 
                "teacher_uuid": str(teachers[0].uuid)
            },
            {
                "name": "Calculus I", 
                "code": "MATH201", 
                "description": "Limits, derivatives, and integrals", 
                "credits": 4, 
                "semester": 1, 
                "teacher_uuid": str(teachers[1].uuid)
            },
            {
                "name": "Software Engineering", 
                "code": "CS301", 
                "description": "Software development methodologies and practices", 
                "credits": 4, 
                "semester": 3, 
                "teacher_uuid": str(teachers[0].uuid)
            },
            # Additional subjects
            {
                "name": "Quantum Mechanics", 
                "code": "PHYS301", 
                "description": "Principles of quantum mechanics and applications", 
                "credits": 4, 
                "semester": 3, 
                "teacher_uuid": str(teachers[2].uuid)
            },
            {
                "name": "Organic Chemistry", 
                "code": "CHEM201", 
                "description": "Structure and reactions of organic compounds", 
                "credits": 4, 
                "semester": 2, 
                "teacher_uuid": str(teachers[3].uuid)
            },
            {
                "name": "Microbiology", 
                "code": "BIO301", 
                "description": "Study of microorganisms and their applications", 
                "credits": 3, 
                "semester": 3, 
                "teacher_uuid": str(teachers[4].uuid)
            },
            {
                "name": "World Literature", 
                "code": "LIT201", 
                "description": "Study of literary works from around the world", 
                "credits": 3, 
                "semester": 2, 
                "teacher_uuid": str(teachers[5].uuid)
            },
            {
                "name": "Modern History", 
                "code": "HIST301", 
                "description": "History from the Industrial Revolution to present day", 
                "credits": 3, 
                "semester": 3, 
                "teacher_uuid": str(teachers[6].uuid)
            },
            {
                "name": "Machine Design", 
                "code": "ENG401", 
                "description": "Principles of mechanical design and analysis", 
                "credits": 4, 
                "semester": 4, 
                "teacher_uuid": str(teachers[7].uuid)
            },
            {
                "name": "Digital Media", 
                "code": "ART301", 
                "description": "Creation and analysis of digital art forms", 
                "credits": 3, 
                "semester": 3, 
                "teacher_uuid": str(teachers[8].uuid)
            },
            {
                "name": "Sports Physiology", 
                "code": "PE201", 
                "description": "Study of body function during physical activity", 
                "credits": 3, 
                "semester": 2, 
                "teacher_uuid": str(teachers[9].uuid)
            },
            {
                "name": "Advanced Programming", 
                "code": "CS202", 
                "description": "Advanced concepts in programming and algorithms", 
                "credits": 4, 
                "semester": 2, 
                "teacher_uuid": str(teachers[0].uuid)
            },
            {
                "name": "Calculus II", 
                "code": "MATH202", 
                "description": "Multivariable calculus and applications", 
                "credits": 4, 
                "semester": 2, 
                "teacher_uuid": str(teachers[1].uuid)
            },
            {
                "name": "Database Systems", 
                "code": "CS303", 
                "description": "Design and implementation of database systems", 
                "credits": 4, 
                "semester": 3, 
                "teacher_uuid": str(teachers[0].uuid)
            },
            {
                "name": "Linear Algebra", 
                "code": "MATH301", 
                "description": "Vector spaces, matrices, and linear transformations", 
                "credits": 4, 
                "semester": 3, 
                "teacher_uuid": str(teachers[1].uuid)
            }
        ]
        
        subjects = []
        for subject_detail in subject_details:
            subject = Subject(
                uuid=str(Uuid.new()),
                name=subject_detail["name"],
                code=subject_detail["code"],
                description=subject_detail["description"],
                credits=subject_detail["credits"],
                semester=subject_detail["semester"],
                teacher_uuid=subject_detail["teacher_uuid"]
            )
            subjects.append(subject)
            subject_repo.create(subject)
            logger.info(f"Subject created: {subject.name} ({subject.code})")
        
        # Create more enrollments - approximately 60 enrollments
        # Each student will be enrolled in 3 subjects on average
        enrollments = []
        
        # Current semester
        current_semester = "2025-1"
        
        import random
        for student in students:
            # Randomly select 2-4 subjects for each student
            num_subjects = random.randint(2, 4)
            selected_subjects = random.sample(subjects, num_subjects)
            
            for subject in selected_subjects:
                enrollment = Enrollment(
                    uuid=str(Uuid.new()),
                    student_uuid=str(student.uuid),
                    subject_uuid=str(subject.uuid),
                    enrollment_date=datetime.now() - timedelta(days=random.randint(1, 90)),
                    semester=current_semester,
                    status="active",
                    final_grade=None
                )
                enrollments.append(enrollment)
                enrollment_repo.create(enrollment)
                logger.info(f"Enrollment created: Student {student.first_name} {student.last_name} in {subject.name}")
        
        # Create more attendance records - approximately 300 records
        # For each enrollment, create attendance records for the past 2 weeks
        attendances = []
        today = datetime.now()
        
        # Status options for attendance
        status_options = ["present", "late", "absent", "excused"]
        status_weights = [0.7, 0.15, 0.1, 0.05]  # Probability weights
        
        # Notes options for different statuses
        notes_for_present = ["On time", "Participated in class", "Good engagement", "", "Asked questions", "Helped others"]
        notes_for_late = ["5 minutes late", "10 minutes late", "15 minutes late", "Late due to traffic", "Late but notified"]
        notes_for_absent = ["No notification", "No show", "Will need to make up", "", "Unexcused"]
        notes_for_excused = ["Medical appointment", "Family emergency", "Doctor's note provided", "Approved absence", "Official university event"]
        
        for enrollment in enrollments:
            # Create attendance for the last 10 class days (2 weeks)
            for days_ago in range(10):
                # Skip weekends
                class_date = today - timedelta(days=days_ago)
                if class_date.weekday() >= 5:  # Saturday or Sunday
                    continue
                    
                # Randomly determine attendance status based on weights
                status = random.choices(status_options, weights=status_weights, k=1)[0]
                
                # Select appropriate note based on status
                if status == "present":
                    note = random.choice(notes_for_present)
                elif status == "late":
                    note = random.choice(notes_for_late)
                elif status == "absent":
                    note = random.choice(notes_for_absent)
                else:  # excused
                    note = random.choice(notes_for_excused)
                
                attendance = Attendance(
                    uuid=str(Uuid.new()),
                    student_uuid=enrollment.student_uuid,
                    subject_uuid=enrollment.subject_uuid,
                    date=class_date,
                    status=status,
                    notes=note
                )
                attendances.append(attendance)
                attendance_repo.create(attendance)
                
        logger.info(f"Created {len(attendances)} attendance records")
        
        # Create more grades - approximately 150 records
        # For each enrollment, create various types of evaluations
        grades = []
        
        # Types of evaluations
        evaluation_types = [
            {"name": "Midterm", "weight": 30.0},
            {"name": "Final", "weight": 40.0},
            {"name": "Quiz 1", "weight": 5.0},
            {"name": "Quiz 2", "weight": 5.0},
            {"name": "Project 1", "weight": 10.0},
            {"name": "Project 2", "weight": 10.0}
        ]
        
        # Comments based on score ranges
        def get_comment_for_score(score):
            if score >= 90:
                return random.choice(["Excellent work", "Outstanding performance", "Exceptional understanding", "Very well done", "Top-notch work"])
            elif score >= 80:
                return random.choice(["Good work", "Solid performance", "Strong understanding", "Well done", "Good job"])
            elif score >= 70:
                return random.choice(["Satisfactory work", "Adequate understanding", "Average performance", "Meets expectations", "Room for improvement"])
            elif score >= 60:
                return random.choice(["Needs improvement", "Basic understanding", "Passing but weak", "Barely meets requirements", "Significant improvement needed"])
            else:
                return random.choice(["Poor performance", "Inadequate work", "Fails to meet requirements", "Major improvement needed", "Please seek tutoring"])
        
        # Dates for different evaluation types
        midterm_date = today - timedelta(days=30)
        final_date = today - timedelta(days=7)
        quiz1_date = today - timedelta(days=45)
        quiz2_date = today - timedelta(days=15)
        project1_date = today - timedelta(days=40)
        project2_date = today - timedelta(days=10)
        
        for enrollment in enrollments:
            # Not all enrollments will have all evaluation types yet
            # Determine which evaluations are available for this enrollment
            
            available_evaluations = []
            
            # Always include quizzes and first project
            available_evaluations.extend([evaluation_types[2], evaluation_types[3], evaluation_types[4]])
            
            # 90% have midterm
            if random.random() < 0.9:
                available_evaluations.append(evaluation_types[0])
                
            # 40% have final
            if random.random() < 0.4:
                available_evaluations.append(evaluation_types[1])
                
            # 60% have second project
            if random.random() < 0.6:
                available_evaluations.append(evaluation_types[5])
            
            for eval_type in available_evaluations:
                # Generate a realistic score distribution
                if eval_type["name"] == "Midterm":
                    score = round(random.normalvariate(78, 12), 1)  # Mean of 78, stddev of 12
                    date = midterm_date
                elif eval_type["name"] == "Final":
                    score = round(random.normalvariate(80, 10), 1)  # Mean of 80, stddev of 10
                    date = final_date
                elif eval_type["name"] == "Quiz 1":
                    score = round(random.normalvariate(75, 15), 1)  # Mean of 75, stddev of 15
                    date = quiz1_date
                elif eval_type["name"] == "Quiz 2":
                    score = round(random.normalvariate(77, 14), 1)  # Mean of 77, stddev of 14
                    date = quiz2_date
                elif eval_type["name"] == "Project 1":
                    score = round(random.normalvariate(82, 8), 1)  # Mean of 82, stddev of 8
                    date = project1_date
                else:  # Project 2
                    score = round(random.normalvariate(85, 7), 1)  # Mean of 85, stddev of 7
                    date = project2_date
                
                # Ensure score is within 0-100 range
                score = max(0, min(100, score))
                
                # Get appropriate comment
                comment = get_comment_for_score(score)
                
                # Create the grade
                grade = Grade(
                    uuid=str(Uuid.new()),
                    student_uuid=enrollment.student_uuid,
                    subject_uuid=enrollment.subject_uuid,
                    evaluation_name=eval_type["name"],
                    score=score,
                    weight=eval_type["weight"],
                    date=date,
                    comments=comment
                )
                grades.append(grade)
                grade_repo.create(grade)
        
        logger.info(f"Created {len(grades)} grade records")
        
        # Create more events - approximately 30 events
        events = []
        now = datetime.now()
        
        # Event types
        event_types = ["meeting", "workshop", "competition", "presentation", "field_trip", "lecture", "seminar", "conference", "ceremony", "social"]
        
        # Locations
        locations = [
            "Conference Room A", "Conference Room B", "Main Auditorium", "Computer Lab 3", 
            "Classroom 101", "Classroom 203", "Science Museum", "University Stadium",
            "Library Main Hall", "Arts Center", "Engineering Building Lobby", "Campus Garden",
            "University Theater", "Student Center", "Faculty Lounge"
        ]
        
        # Create events spread across the next 3 months
        for i in range(30):
            # Determine event date - spread across next 90 days
            days_ahead = random.randint(1, 90)
            event_date = now + timedelta(days=days_ahead)
            
            # Determine duration - 1 to 6 hours
            duration_hours = random.randint(1, 6)
            
            # Determine if all-day event (10% chance)
            all_day = random.random() < 0.1
            
            # If all day, set times accordingly
            if all_day:
                start_date = event_date.replace(hour=9, minute=0, second=0)
                end_date = event_date.replace(hour=17, minute=0, second=0)
            else:
                # Random start time between 8AM and 6PM
                start_hour = random.randint(8, 18)
                start_date = event_date.replace(hour=start_hour, minute=0, second=0)
                end_date = start_date + timedelta(hours=duration_hours)
            
            # Select random event type and location
            event_type = random.choice(event_types)
            location = random.choice(locations)
            
            # Determine max participants (for certain event types)
            max_participants = None
            if event_type in ["workshop", "competition", "field_trip", "seminar"]:
                max_participants = random.randint(20, 150)
            
            # Select random organizer from teachers
            organizer = random.choice(teachers)
            
            # Generate title and description based on event type
            titles_by_type = {
                "meeting": [f"Department {departments[i % len(departments)]} Meeting", "Faculty Meeting", "Staff Meeting", "Student Council Meeting", "Program Committee Meeting"],
                "workshop": [f"{specializations[i % len(specializations)]} Workshop", "Career Skills Workshop", "Research Methods Workshop", "Leadership Workshop", "Communication Skills Workshop"],
                "competition": ["Academic Olympiad", "Programming Contest", "Research Poster Competition", "Debate Tournament", "Science Fair"],
                "presentation": ["Guest Speaker Series", "Research Presentation", "Thesis Defense", "Student Project Showcase", "Industry Expert Talk"],
                "field_trip": ["Museum Visit", "Industry Tour", "Archaeological Site Visit", "Research Facility Tour", "Cultural Excursion"],
                "lecture": [f"Special Lecture: {specializations[i % len(specializations)]}", "Guest Lecture Series", "Distinguished Professor Talk", "Industry Insights Lecture", "Research Frontiers Lecture"],
                "seminar": [f"Seminar on {specializations[i % len(specializations)]}", "Professional Development Seminar", "Research Methods Seminar", "Graduate Studies Seminar", "Career Preparation Seminar"],
                "conference": ["Annual Department Conference", "Student Research Conference", "Academic Symposium", "Industry-Academia Conference", "Interdisciplinary Studies Conference"],
                "ceremony": ["Awards Ceremony", "Graduation Ceremony", "Honor Society Induction", "Recognition Event", "Opening Ceremony"],
                "social": ["Student Mixer", "Faculty Reception", "Department Celebration", "Cultural Festival", "End of Term Party"]
            }
            
            title = random.choice(titles_by_type.get(event_type, ["University Event"]))
            
            descriptions_by_type = {
                "meeting": ["Regular meeting to discuss departmental matters and updates", "Monthly coordination meeting for faculty and staff", "Planning session for upcoming activities and initiatives"],
                "workshop": ["Hands-on session to develop practical skills and knowledge", "Interactive workshop with expert guidance and practical exercises", "Skill-building session with collaborative activities"],
                "competition": ["Annual competition to showcase student talents and abilities", "Competitive event with prizes for top performers", "Challenge designed to test skills and knowledge in the field"],
                "presentation": ["Presentation of recent research findings and developments", "Showcase of student projects and achievements", "Informative session on current topics in the field"],
                "field_trip": ["Educational visit to relevant external location", "Guided tour with hands-on learning opportunities", "Off-campus experience to enhance classroom learning"],
                "lecture": ["In-depth presentation on specialized topic", "Expert insights on current developments in the field", "Comprehensive overview of advanced concepts"],
                "seminar": ["Interactive session focused on specific topic or skill", "Discussion-based learning experience with expert guidance", "Specialized training session with practical applications"],
                "conference": ["Large-scale event featuring multiple speakers and sessions", "Academic gathering to present and discuss research", "Professional development opportunity with networking"],
                "ceremony": ["Formal event to recognize achievements and milestones", "Celebratory gathering with presentations and awards", "Official university function with distinguished guests"],
                "social": ["Informal gathering for networking and community building", "Social event to foster connections between students and faculty", "Recreational activity to promote university community"]
            }
            
            description = random.choice(descriptions_by_type.get(event_type, ["University event for students and faculty"]))
            
            # Create the event
            event = Event(
                uuid=str(Uuid.new()),
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                location=location,
                organizer_uuid=str(organizer.uuid),
                event_type=event_type,
                all_day=all_day,
                max_participants=max_participants
            )
            events.append(event)
            event_repo.create(event)
        
        logger.info(f"Created {len(events)} event records")
        
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