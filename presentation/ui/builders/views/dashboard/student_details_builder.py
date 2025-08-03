from typing import Callable, Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QTableWidget, QTableWidgetItem

from presentation.ui.builders.builder_interface import Builder
from presentation.ui.factories import WidgetFactory, LayoutFactory
from presentation.ui.widgets import CircularImageWidget, get_initials
from domain.services.profile_image_service import ProfileImageService


class StudentDetailsBuilder(Builder):
    """
    Builder for student details view that shows detailed information about a student
    """
    def __init__(
        self,
        wf: WidgetFactory,
        lf: LayoutFactory,
        student_name: str,
        on_back: Callable[[], None] = None
    ):
        """
        Initialize the student details builder
        
        :param wf: Widget factory
        :param lf: Layout factory
        :param student_name: Student name to display
        :param on_back: Callback for back button
        """
        self._wf = wf
        self._lf = lf
        self._student_name = student_name
        self._on_back = on_back or (lambda: None)
        
        # Profile image service
        self._profile_image_service = ProfileImageService()
        
        # Create container
        self._container = QWidget()
        self._container.setObjectName("student-details-container")
        
        # Main layout using factory
        self._main_layout = self._lf.get("vbox").build()
        self._container.setLayout(self._main_layout)
        
        # Create components
        self._create_header()
        self._create_student_info()
        self._create_grades_section()
        self._create_attendance_section()
        
        # Apply styles
        self._apply_styles()
    
    def _create_header(self) -> None:
        """Create header with back button and title"""
        header = QFrame()
        header.setObjectName("details-header")
        
        # Use layout factory for header layout
        header_layout = self._lf.get("hbox").build()
        header.setLayout(header_layout)
        
        # Back button using widget factory
        self._back_button = self._wf.get("button").set_text("← Volver").build()
        self._back_button.setObjectName("back-button")
        self._back_button.clicked.connect(self._on_back)
        
        # Title using widget factory
        title = self._wf.get("label").set_text("Detalles del Estudiante").build()
        title.setObjectName("details-title")
        
        # Add to layout
        header_layout.addWidget(self._back_button)
        header_layout.addWidget(title, 1, Qt.AlignmentFlag.AlignCenter)
        header_layout.addStretch(1)
        
        self._main_layout.addWidget(header)
    
    def _create_student_info(self) -> None:
        """Create student information section with profile"""
        info_frame = QFrame()
        info_frame.setObjectName("student-info-frame")
        
        # Use layout factory
        info_layout = self._lf.get("hbox").build()
        info_frame.setLayout(info_layout)
        
        # Student profile image
        initials = get_initials(self._student_name)
        self._profile_image = CircularImageWidget(
            size=80,
            placeholder_bg_color="#8ecaef",
            placeholder_text=initials
        )
        
        # Try to load profile image
        student_id = self._student_name.lower().replace(" ", "_")
        image_path = self._profile_image_service.get_image_path(student_id, "student")
        self._profile_image.setImage(image_path)
        
        # Student details container
        details_frame = QFrame()
        
        # Use grid layout from factory
        details_layout = self._lf.get("grid").build()
        details_frame.setLayout(details_layout)
        
        # Add student details
        details = [
            ("Nombre:", self._student_name),
            ("ID:", f"EST-{hash(self._student_name) % 10000:04d}"),
            ("Grado:", "3°A"),  # Example data, would be dynamic in real app
            ("Edad:", "18"),    # Example data
            ("Email:", f"{student_id}@uamitos.edu.mx")
        ]
        
        for row, (label_text, value_text) in enumerate(details):
            # Create labels with widget factory
            label = self._wf.get("label").set_text(label_text).build()
            label.setObjectName("student-detail-label")
            
            value = self._wf.get("label").set_text(value_text).build()
            value.setObjectName("student-detail-value")
            
            details_layout.addWidget(label, row, 0)
            details_layout.addWidget(value, row, 1)
        
        # Add to main info layout
        info_layout.addWidget(self._profile_image)
        info_layout.addWidget(details_frame, 1)
        
        self._main_layout.addWidget(info_frame)
    
    def _create_grades_section(self) -> None:
        """Create student grades section"""
        grades_frame = QFrame()
        grades_frame.setObjectName("grades-section")
        
        # Use layout factory
        grades_layout = self._lf.get("vbox").build()
        grades_frame.setLayout(grades_layout)
        
        # Section title using widget factory
        title = self._wf.get("label").set_text("Calificaciones").build()
        title.setObjectName("section-title")
        grades_layout.addWidget(title)
        
        # Grades table
        self._grades_table = QTableWidget()
        self._grades_table.setObjectName("grades-table")
        self._grades_table.setColumnCount(5)
        self._grades_table.setHorizontalHeaderLabels(["Materia", "Parcial 1", "Parcial 2", "Parcial 3", "Final"])
        
        # Sample data
        subjects = [
            ("Matemáticas", 85, 90, 88, 88),
            ("Historia", 78, 82, 85, 82),
            ("Física", 92, 88, 95, 92),
            ("Literatura", 88, 90, 87, 88),
            ("Inglés", 95, 92, 97, 95)
        ]
        
        self._grades_table.setRowCount(len(subjects))
        
        for row, (subject, p1, p2, p3, final) in enumerate(subjects):
            self._grades_table.setItem(row, 0, QTableWidgetItem(subject))
            self._grades_table.setItem(row, 1, QTableWidgetItem(str(p1)))
            self._grades_table.setItem(row, 2, QTableWidgetItem(str(p2)))
            self._grades_table.setItem(row, 3, QTableWidgetItem(str(p3)))
            self._grades_table.setItem(row, 4, QTableWidgetItem(str(final)))
        
        grades_layout.addWidget(self._grades_table)
        self._main_layout.addWidget(grades_frame)
    
    def _create_attendance_section(self) -> None:
        """Create attendance record section"""
        attendance_frame = QFrame()
        attendance_frame.setObjectName("attendance-section")
        
        # Use layout factory
        attendance_layout = self._lf.get("vbox").build()
        attendance_frame.setLayout(attendance_layout)
        
        # Section title using widget factory
        title = self._wf.get("label").set_text("Registro de Asistencia").build()
        title.setObjectName("section-title")
        attendance_layout.addWidget(title)
        
        # Attendance table
        self._attendance_table = QTableWidget()
        self._attendance_table.setObjectName("attendance-table")
        self._attendance_table.setColumnCount(3)
        self._attendance_table.setHorizontalHeaderLabels(["Fecha", "Estado", "Comentario"])
        
        # Sample data
        attendance_data = [
            ("2025-07-01", "Presente", "-"),
            ("2025-06-30", "Presente", "-"),
            ("2025-06-29", "Ausente", "Justificada por enfermedad"),
            ("2025-06-28", "Presente", "-"),
            ("2025-06-27", "Presente", "-")
        ]
        
        self._attendance_table.setRowCount(len(attendance_data))
        
        for row, (date, status, comment) in enumerate(attendance_data):
            self._attendance_table.setItem(row, 0, QTableWidgetItem(date))
            self._attendance_table.setItem(row, 1, QTableWidgetItem(status))
            self._attendance_table.setItem(row, 2, QTableWidgetItem(comment))
        
        attendance_layout.addWidget(self._attendance_table)
        self._main_layout.addWidget(attendance_frame)
    
    def _apply_styles(self) -> None:
        """Apply styles to the components"""
        self._container.setStyleSheet("""
            #student-details-container {
                background-color: #f5f7fd;
                padding: 10px;
            }
            
            #details-header {
                border-bottom: 1px solid #ddd;
                padding-bottom: 10px;
                margin-bottom: 15px;
            }
            
            #back-button {
                background-color: transparent;
                border: none;
                color: #4a86e8;
                font-weight: bold;
            }
            
            #details-title {
                font-size: 18px;
                font-weight: bold;
                color: #333;
            }
            
            #student-info-frame {
                background-color: white;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
            }
            
            #student-detail-label {
                font-weight: bold;
                color: #555;
            }
            
            #student-detail-value {
                color: #333;
            }
            
            #section-title {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
            
            #grades-section, #attendance-section {
                background-color: white;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
            }
            
            QTableWidget {
                border: none;
                background-color: white;
            }
            
            QTableWidget::item {
                padding: 5px;
            }
            
            QTableWidget::item:selected {
                background-color: #e1f0ff;
            }
            
            QHeaderView::section {
                background-color: #d9d0c4;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)
    
    def build(self) -> QWidget:
        """Build and return the student details widget"""
        return self._container
        
    def create(self):
        """Create a new instance of this builder"""
        return type(self)(
            self._wf,
            self._lf,
            self._student_name,
            self._on_back
        )
    
    def clone(self):
        """Clone this builder instance"""
        import copy
        return copy.deepcopy(self)