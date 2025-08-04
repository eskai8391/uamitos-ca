from typing import Callable, Dict, Optional, List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QTableWidget, QTableWidgetItem, QHeaderView

from presentation.ui.builders.builder_interface import Builder
from presentation.ui.factories import WidgetFactory, LayoutFactory
from presentation.ui.widgets import CircularImageWidget, get_initials
from domain.services.profile_image_service import ProfileImageService


class TeacherDetailsBuilder(Builder):
    """
    Builder for teacher details view that shows detailed information about a teacher
    """
    def __init__(
        self,
        wf: WidgetFactory,
        lf: LayoutFactory,
        teacher_name: str,
        on_back: Callable[[], None] = None
    ):
        """
        Initialize the teacher details builder
        
        :param wf: Widget factory
        :param lf: Layout factory
        :param teacher_name: Teacher name to display
        :param on_back: Callback for back button
        """
        self._wf = wf
        self._lf = lf
        self._teacher_name = teacher_name
        self._on_back = on_back or (lambda: None)
        
        # Profile image service
        self._profile_image_service = ProfileImageService()
        
        # Create container
        self._container = QWidget()
        self._container.setObjectName("teacher-details-container")
        
        # Main layout using factory
        self._main_layout = self._lf.get("vbox").build()
        self._container.setLayout(self._main_layout)
        
        # Create components
        self._create_header()
        self._create_teacher_info()
        self._create_subjects_section()
        self._create_schedule_section()
        
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
        title = self._wf.get("label").set_text("Detalles del Profesor").build()
        title.setObjectName("details-title")
        
        # Add to layout
        header_layout.addWidget(self._back_button)
        header_layout.addWidget(title, 1, Qt.AlignmentFlag.AlignCenter)
        header_layout.addStretch(1)
        
        self._main_layout.addWidget(header)
    
    def _create_teacher_info(self) -> None:
        """Create teacher information section with profile"""
        info_frame = QFrame()
        info_frame.setObjectName("teacher-info-frame")
        
        # Use layout factory
        info_layout = self._lf.get("hbox").build()
        info_frame.setLayout(info_layout)
        
        # Teacher profile image
        initials = get_initials(self._teacher_name)
        self._profile_image = CircularImageWidget(
            size=80,
            placeholder_bg_color="#5a7a95",
            placeholder_text=initials
        )
        
        # Try to load profile image
        teacher_id = self._teacher_name.lower().replace(" ", "_")
        image_path = self._profile_image_service.get_image_path(teacher_id, "teacher")
        self._profile_image.setImage(image_path)
        
        # Teacher details container
        details_frame = QFrame()
        
        # Use grid layout from factory
        details_layout = self._lf.get("grid").build()
        details_frame.setLayout(details_layout)
        
        # Map teacher name to subject specialization
        subject_map = {
            "Laura Gómez": "Matemáticas",
            "Pedro Ruiz": "Física",
            "Ana Torres": "Química", 
            "María López": "Biología",
            "Juan Pérez": "Historia"
        }
        
        specialization = subject_map.get(self._teacher_name, "General")
        
        # Add teacher details
        details = [
            ("Nombre:", self._teacher_name),
            ("ID:", f"TCH-{hash(self._teacher_name) % 10000:04d}"),
            ("Especialidad:", specialization),
            ("Años de Servicio:", "5"),  # Example data
            ("Email:", f"{teacher_id}@uamitos.edu.mx")
        ]
        
        for row, (label_text, value_text) in enumerate(details):
            # Create labels using widget factory
            label = self._wf.get("label").set_text(label_text).build()
            label.setObjectName("teacher-detail-label")
            
            value = self._wf.get("label").set_text(value_text).build()
            value.setObjectName("teacher-detail-value")
            
            details_layout.addWidget(label, row, 0)
            details_layout.addWidget(value, row, 1)
        
        # Add to main info layout
        info_layout.addWidget(self._profile_image)
        info_layout.addWidget(details_frame, 1)
        
        self._main_layout.addWidget(info_frame)
    
    def _create_subjects_section(self) -> None:
        """Create subjects and classes section"""
        subjects_frame = QFrame()
        subjects_frame.setObjectName("subjects-section")
        
        # Use layout factory
        subjects_layout = self._lf.get("vbox").build()
        subjects_frame.setLayout(subjects_layout)
        
        # Section title using widget factory
        title = self._wf.get("label").set_text("Clases Asignadas").build()
        title.setObjectName("section-title")
        subjects_layout.addWidget(title)
        
        # Subjects table
        self._subjects_table = QTableWidget()
        self._subjects_table.setObjectName("subjects-table")
        self._subjects_table.setColumnCount(4)
        self._subjects_table.setHorizontalHeaderLabels(["Materia", "Grupo", "Horario", "No. Estudiantes"])
        
        # Configure table appearance to match teacher dashboard
        self._subjects_table.horizontalHeader().setStyleSheet("background-color: #3a7bd5; color: white; font-weight: bold;")
        self._subjects_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._subjects_table.setAlternatingRowColors(True)
        self._subjects_table.setShowGrid(True)
        self._subjects_table.setGridStyle(Qt.PenStyle.SolidLine)
        self._subjects_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Sample data - match teacher name to subjects
        if "Laura Gómez" == self._teacher_name:
            subjects = [
                ("Matemáticas I", "1°A", "Lu-Mi-Vi 8:00-9:30", 28),
                ("Matemáticas II", "2°B", "Ma-Ju 10:00-11:30", 25),
                ("Álgebra", "3°A", "Lu-Mi 12:00-13:30", 22)
            ]
        elif "Pedro Ruiz" == self._teacher_name:
            subjects = [
                ("Física I", "2°A", "Lu-Mi 8:00-9:30", 26),
                ("Física II", "3°B", "Ma-Ju 10:00-11:30", 24)
            ]
        else:
            # Generic data for other teachers
            subjects = [
                (f"{self._get_subject_for_teacher()} I", "1°C", "Lu-Mi 8:00-9:30", 27),
                (f"{self._get_subject_for_teacher()} II", "2°A", "Ma-Ju 10:00-11:30", 25)
            ]
        
        self._subjects_table.setRowCount(len(subjects))
        
        for row, (subject, group, schedule, students) in enumerate(subjects):
            self._subjects_table.setItem(row, 0, QTableWidgetItem(subject))
            self._subjects_table.setItem(row, 1, QTableWidgetItem(group))
            self._subjects_table.setItem(row, 2, QTableWidgetItem(schedule))
            self._subjects_table.setItem(row, 3, QTableWidgetItem(str(students)))
        
        subjects_layout.addWidget(self._subjects_table)
        self._main_layout.addWidget(subjects_frame)
    
    def _get_subject_for_teacher(self) -> str:
        """Map teacher name to their subject"""
        subject_map = {
            "Laura Gómez": "Matemáticas",
            "Pedro Ruiz": "Física",
            "Ana Torres": "Química", 
            "María López": "Biología",
            "Juan Pérez": "Historia"
        }
        return subject_map.get(self._teacher_name, "Estudios Generales")
    
    def _create_schedule_section(self) -> None:
        """Create weekly schedule section"""
        schedule_frame = QFrame()
        schedule_frame.setObjectName("schedule-section")
        
        # Use layout factory
        schedule_layout = self._lf.get("vbox").build()
        schedule_frame.setLayout(schedule_layout)
        
        # Section title using widget factory
        title = self._wf.get("label").set_text("Horario Semanal").build()
        title.setObjectName("section-title")
        schedule_layout.addWidget(title)
        
        # Schedule table
        self._schedule_table = QTableWidget()
        self._schedule_table.setObjectName("schedule-table")
        self._schedule_table.setColumnCount(6)
        self._schedule_table.setHorizontalHeaderLabels(["Hora", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
        
        # Configure table appearance to match teacher dashboard
        self._schedule_table.horizontalHeader().setStyleSheet("background-color: #3a7bd5; color: white; font-weight: bold;")
        self._schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._schedule_table.setAlternatingRowColors(True)
        self._schedule_table.setShowGrid(True)
        self._schedule_table.setGridStyle(Qt.PenStyle.SolidLine)
        self._schedule_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Sample schedule data
        time_slots = ["8:00-9:30", "9:30-11:00", "11:00-12:30", "12:30-14:00", "14:00-15:30"]
        
        self._schedule_table.setRowCount(len(time_slots))
        
        # Fill time column
        for row, time in enumerate(time_slots):
            self._schedule_table.setItem(row, 0, QTableWidgetItem(time))
        
        # Fill schedule data - create a simple pattern based on teacher name
        teacher_hash = hash(self._teacher_name) % 100
        subject = self._get_subject_for_teacher()
        
        for row in range(len(time_slots)):
            for col in range(1, 6):  # Skip time column
                # Create a pattern of classes based on hash
                if (row + col + teacher_hash) % 3 == 0:
                    group = f"{(row % 3) + 1}°{chr(65 + (col % 3))}"
                    self._schedule_table.setItem(row, col, QTableWidgetItem(f"{subject} {group}"))
                else:
                    self._schedule_table.setItem(row, col, QTableWidgetItem("-"))
        
        schedule_layout.addWidget(self._schedule_table)
        self._main_layout.addWidget(schedule_frame)
    
    def _apply_styles(self) -> None:
        """Apply styles to the components"""
        self._container.setStyleSheet("""
            #teacher-details-container {
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
            
            #teacher-info-frame {
                background-color: white;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
            }
            
            #teacher-detail-label {
                font-weight: bold;
                color: #555;
            }
            
            #teacher-detail-value {
                color: #333;
            }
            
            #section-title {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
            
            #subjects-section, #schedule-section {
                background-color: white;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
            }
            
            QTableWidget {
                border: none;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            QTableWidget::item {
                padding: 8px;
                font-size: 14px;
                font-family: "Segoe UI", Arial, sans-serif;
                color: #000000;
            }
            
            QTableWidget::item:selected {
                background-color: #4facfe;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #3a7bd5;
                color: white;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
                font-family: "Segoe UI", Arial, sans-serif;
                border: none;
            }
            
            /* Specific styling for subjects table */
            #subjects-table {
                border: none;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            #subjects-table::item {
                padding: 8px;
                font-size: 14px;
                font-family: "Segoe UI", Arial, sans-serif;
                color: #000000;
            }
            
            #subjects-table::item:selected {
                background-color: #4facfe;
                color: white;
            }
            
            #subjects-table QHeaderView::section {
                background-color: #3a7bd5;
                color: white;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
                font-family: "Segoe UI", Arial, sans-serif;
                border: none;
            }
            
            /* Specific styling for schedule table */
            #schedule-table {
                border: none;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            #schedule-table::item {
                padding: 8px;
                font-size: 14px;
                font-family: "Segoe UI", Arial, sans-serif;
                color: #000000;
            }
            
            #schedule-table::item:selected {
                background-color: #4facfe;
                color: white;
            }
            
            #schedule-table QHeaderView::section {
                background-color: #3a7bd5;
                color: white;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
                font-family: "Segoe UI", Arial, sans-serif;
                border: none;
            }
        """)
    
    def build(self) -> QWidget:
        """Build and return the teacher details widget"""
        return self._container
        
    def create(self):
        """Create a new instance of this builder"""
        return type(self)(
            self._wf,
            self._lf,
            self._teacher_name,
            self._on_back
        )
    
    def clone(self):
        """Clone this builder instance"""
        import copy
        return copy.deepcopy(self)