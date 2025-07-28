from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from domain.entities.student import Student
from domain.entities.subject import Subject
from domain.entities.grade import Grade
from domain.entities.attendance import Attendance
from domain.repositories.base_entity_repository import BaseEntityRepository
from infrastructure.reports.pdf_generator import PDFReportGenerator


@dataclass
class GenerateStudentGradesReportRequest:
    student_uuid: str
    subject_uuid: Optional[str] = None  # If None, generate report for all subjects


@dataclass
class GenerateAttendanceReportRequest:
    student_uuid: str
    subject_uuid: str


@dataclass
class GenerateClassPerformanceReportRequest:
    subject_uuid: str


class ReportUseCases:
    def __init__(
        self,
        student_repository: BaseEntityRepository,
        subject_repository: BaseEntityRepository,
        grade_repository: BaseEntityRepository,
        attendance_repository: BaseEntityRepository,
        pdf_generator: PDFReportGenerator
    ):
        self.__student_repository = student_repository
        self.__subject_repository = subject_repository
        self.__grade_repository = grade_repository
        self.__attendance_repository = attendance_repository
        self.__pdf_generator = pdf_generator
    
    def generate_student_grades_report(self, request: GenerateStudentGradesReportRequest) -> Optional[str]:
        """
        Generate a PDF report of a student's grades
        
        :param request: Report request data
        :return: Path to the generated PDF file or None if error
        """
        try:
            # Get student
            student = self.__student_repository.get_by_uuid(request.student_uuid)
            if not student:
                return None
                
            # Get subjects
            if request.subject_uuid:
                subject = self.__subject_repository.get_by_uuid(request.subject_uuid)
                if not subject:
                    return None
                subjects = [subject]
            else:
                # Get all subjects for the student (this would require additional repository methods)
                subjects = []  # Placeholder, actual implementation depends on available repository methods
            
            # Get grades for each subject
            grades = {}
            for subject in subjects:
                # This requires specific repository methods
                subject_grades = []  # Placeholder, actual implementation depends on available repository methods
                grades[str(subject.uuid)] = subject_grades
            
            # Generate report
            return self.__pdf_generator.generate_student_grades_report(
                student=student,
                subjects=subjects,
                grades=grades
            )
        except Exception:
            return None
    
    def generate_attendance_report(self, request: GenerateAttendanceReportRequest) -> Optional[str]:
        """
        Generate a PDF report of a student's attendance
        
        :param request: Report request data
        :return: Path to the generated PDF file or None if error
        """
        try:
            # Get student
            student = self.__student_repository.get_by_uuid(request.student_uuid)
            if not student:
                return None
                
            # Get subject
            subject = self.__subject_repository.get_by_uuid(request.subject_uuid)
            if not subject:
                return None
            
            # Get attendance records
            # This requires specific repository methods
            attendance_records = []  # Placeholder, actual implementation depends on available repository methods
            
            # Generate report
            return self.__pdf_generator.generate_attendance_report(
                student=student,
                subject=subject,
                attendance_records=attendance_records
            )
        except Exception:
            return None
    
    def generate_class_performance_report(self, request: GenerateClassPerformanceReportRequest) -> Optional[str]:
        """
        Generate a PDF report of class performance
        
        :param request: Report request data
        :return: Path to the generated PDF file or None if error
        """
        try:
            # Get subject
            subject = self.__subject_repository.get_by_uuid(request.subject_uuid)
            if not subject:
                return None
            
            # Get teacher name
            teacher_name = "Profesor"  # Placeholder, actual implementation depends on available repository methods
            if subject.teacher_uuid:
                # Get teacher name from teacher_uuid
                pass
            
            # Get students in the subject
            # This requires specific repository methods
            students_data = []  # Placeholder, actual implementation depends on available repository methods
            
            # Generate report
            return self.__pdf_generator.generate_class_performance_report(
                subject=subject,
                teacher_name=teacher_name,
                students=students_data
            )
        except Exception:
            return None