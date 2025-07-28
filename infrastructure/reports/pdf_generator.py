import os
from datetime import datetime
from typing import List, Dict, Any, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from domain.entities.student import Student
from domain.entities.subject import Subject
from domain.entities.grade import Grade
from domain.entities.attendance import Attendance


class PDFReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        """
        Initialize the PDF report generator
        
        :param output_dir: Directory to store generated reports
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Get reportlab styles
        self.styles = getSampleStyleSheet()
        
        # Add custom styles
        self.styles.add(
            ParagraphStyle(
                name='Title',
                parent=self.styles['Heading1'],
                fontSize=16,
                alignment=1,
                spaceAfter=12
            )
        )
        
        self.styles.add(
            ParagraphStyle(
                name='Subtitle',
                parent=self.styles['Heading2'],
                fontSize=14,
                spaceBefore=6,
                spaceAfter=6
            )
        )
        
        self.styles.add(
            ParagraphStyle(
                name='Normal',
                parent=self.styles['Normal'],
                fontSize=10,
                spaceBefore=3,
                spaceAfter=3
            )
        )
    
    def generate_student_grades_report(
        self,
        student: Student,
        subjects: List[Subject],
        grades: Dict[str, List[Grade]],  # Subject UUID to list of grades
        filename: Optional[str] = None
    ) -> str:
        """
        Generate a PDF report of a student's grades
        
        :param student: Student entity
        :param subjects: List of subject entities
        :param grades: Dictionary mapping subject UUID to list of grades
        :param filename: Optional filename for the report
        :return: Path to the generated PDF file
        """
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"student_grades_{student.uuid}_{timestamp}.pdf"
        
        # Create full path
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Add title
        title = Paragraph("Reporte de Calificaciones", self.styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.25 * inch))
        
        # Add student info
        student_info = [
            Paragraph(f"Estudiante: {student.name} {student.last_name}", self.styles['Normal']),
            Paragraph(f"Email: {student.email.value}", self.styles['Normal']),
            Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", self.styles['Normal'])
        ]
        
        for info in student_info:
            story.append(info)
        
        story.append(Spacer(1, 0.25 * inch))
        
        # Add grades for each subject
        for subject in subjects:
            # Add subject header
            subject_header = Paragraph(f"Materia: {subject.name} ({subject.code})", self.styles['Subtitle'])
            story.append(subject_header)
            
            # Get grades for this subject
            subject_grades = grades.get(str(subject.uuid), [])
            
            if subject_grades:
                # Create table data
                table_data = [["Evaluación", "Calificación", "Peso", "Fecha"]]
                
                for grade in subject_grades:
                    table_data.append([
                        grade.evaluation_name,
                        f"{grade.score:.1f}",
                        f"{grade.weight:.0f}%",
                        grade.date.strftime("%d/%m/%Y")
                    ])
                
                # Calculate weighted average
                weighted_sum = sum(g.score * g.weight / 100 for g in subject_grades)
                total_weight = sum(g.weight for g in subject_grades)
                
                if total_weight > 0:
                    average = weighted_sum / (total_weight / 100)
                    table_data.append(["Promedio Final", f"{average:.1f}", "", ""])
                
                # Create table
                table = Table(table_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1.5*inch])
                
                # Style the table
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(table)
            else:
                story.append(Paragraph("No hay calificaciones registradas para esta materia", self.styles['Normal']))
            
            story.append(Spacer(1, 0.25 * inch))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def generate_attendance_report(
        self,
        student: Student,
        subject: Subject,
        attendance_records: List[Attendance],
        filename: Optional[str] = None
    ) -> str:
        """
        Generate a PDF report of a student's attendance for a subject
        
        :param student: Student entity
        :param subject: Subject entity
        :param attendance_records: List of attendance records
        :param filename: Optional filename for the report
        :return: Path to the generated PDF file
        """
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"attendance_{student.uuid}_{subject.uuid}_{timestamp}.pdf"
        
        # Create full path
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Add title
        title = Paragraph("Reporte de Asistencia", self.styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.25 * inch))
        
        # Add info
        info = [
            Paragraph(f"Estudiante: {student.name} {student.last_name}", self.styles['Normal']),
            Paragraph(f"Materia: {subject.name} ({subject.code})", self.styles['Normal']),
            Paragraph(f"Fecha del reporte: {datetime.now().strftime('%d/%m/%Y')}", self.styles['Normal'])
        ]
        
        for item in info:
            story.append(item)
        
        story.append(Spacer(1, 0.25 * inch))
        
        if attendance_records:
            # Count status types
            status_counts = {
                "present": 0,
                "absent": 0,
                "late": 0,
                "excused": 0
            }
            
            for record in attendance_records:
                status_counts[record.status] = status_counts.get(record.status, 0) + 1
            
            total = len(attendance_records)
            
            # Create summary table
            summary_data = [
                ["Estado", "Cantidad", "Porcentaje"],
                ["Presente", status_counts["present"], f"{status_counts['present'] * 100 / total:.1f}%"],
                ["Ausente", status_counts["absent"], f"{status_counts['absent'] * 100 / total:.1f}%"],
                ["Retardo", status_counts["late"], f"{status_counts['late'] * 100 / total:.1f}%"],
                ["Justificado", status_counts["excused"], f"{status_counts['excused'] * 100 / total:.1f}%"],
                ["Total", total, "100%"]
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            
            # Style the table
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(Paragraph("Resumen de Asistencia", self.styles['Subtitle']))
            story.append(summary_table)
            story.append(Spacer(1, 0.25 * inch))
            
            # Create detailed table
            detail_data = [["Fecha", "Estado", "Notas"]]
            
            # Sort records by date
            sorted_records = sorted(attendance_records, key=lambda x: x.date)
            
            for record in sorted_records:
                detail_data.append([
                    record.date.strftime("%d/%m/%Y"),
                    record.status,
                    record.notes or ""
                ])
            
            detail_table = Table(detail_data, colWidths=[1.5*inch, 1.5*inch, 3*inch])
            
            # Style the table
            detail_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (2, 1), (2, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(Paragraph("Detalle de Asistencia", self.styles['Subtitle']))
            story.append(detail_table)
        else:
            story.append(Paragraph("No hay registros de asistencia para este estudiante en esta materia", self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def generate_class_performance_report(
        self,
        subject: Subject,
        teacher_name: str,
        students: List[Dict[str, Any]],
        filename: Optional[str] = None
    ) -> str:
        """
        Generate a PDF report of class performance
        
        :param subject: Subject entity
        :param teacher_name: Name of the teacher
        :param students: List of student performance data
        :param filename: Optional filename for the report
        :return: Path to the generated PDF file
        """
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"class_performance_{subject.uuid}_{timestamp}.pdf"
        
        # Create full path
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Add title
        title = Paragraph("Reporte de Rendimiento del Grupo", self.styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.25 * inch))
        
        # Add info
        info = [
            Paragraph(f"Materia: {subject.name} ({subject.code})", self.styles['Normal']),
            Paragraph(f"Profesor: {teacher_name}", self.styles['Normal']),
            Paragraph(f"Fecha del reporte: {datetime.now().strftime('%d/%m/%Y')}", self.styles['Normal'])
        ]
        
        for item in info:
            story.append(item)
        
        story.append(Spacer(1, 0.25 * inch))
        
        if students:
            # Create table
            table_data = [["Estudiante", "Promedio", "Asistencia", "Estado"]]
            
            for student in students:
                table_data.append([
                    f"{student['name']} {student['last_name']}",
                    f"{student['average']:.1f}",
                    f"{student['attendance_percentage']:.1f}%",
                    student['status']
                ])
            
            # Calculate averages
            avg_grade = sum(s['average'] for s in students) / len(students)
            avg_attendance = sum(s['attendance_percentage'] for s in students) / len(students)
            
            table_data.append([
                "Promedio del Grupo",
                f"{avg_grade:.1f}",
                f"{avg_attendance:.1f}%",
                ""
            ])
            
            # Create table
            table = Table(table_data, colWidths=[3*inch, 1.25*inch, 1.25*inch, 1.25*inch])
            
            # Style the table
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 1), (0, -2), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            
            # Add performance statistics
            story.append(Spacer(1, 0.5 * inch))
            story.append(Paragraph("Estadísticas de Rendimiento", self.styles['Subtitle']))
            
            # Count status types
            status_counts = {}
            for student in students:
                status = student['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            stats_data = [["Estado", "Cantidad", "Porcentaje"]]
            
            for status, count in status_counts.items():
                stats_data.append([
                    status,
                    count,
                    f"{count * 100 / len(students):.1f}%"
                ])
            
            stats_data.append(["Total", len(students), "100%"])
            
            # Create stats table
            stats_table = Table(stats_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            
            # Style the table
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(stats_table)
        else:
            story.append(Paragraph("No hay estudiantes registrados para esta materia", self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        return filepath