import logging
import os
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtGui import QIcon
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application.container import AppContainer
from infrastructure.database import create_all
from presentation.api.routes import student_routes, auth_routes, teacher_routes, event_routes, grade_routes, schedule_routes, user_routes, report_routes


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for development
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", mode="a")  # Add file handler to keep logs
    ]
)

# Set specific logging levels for modules
logging.getLogger("infrastructure.security").setLevel(logging.DEBUG)
logging.getLogger("application.use_cases").setLevel(logging.DEBUG)
logging.getLogger("presentation.api").setLevel(logging.DEBUG)
logging.getLogger("infrastructure.repositories").setLevel(logging.INFO)
logging.getLogger("uvicorn").setLevel(logging.INFO)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

# Root logger
logger = logging.getLogger(__name__)


def init_database():
    """Initialize database and create tables if they don't exist"""
    logger.info("Initializing database...")
    create_all()
    logger.info("Database initialization complete")


def create_api():
    """Create and configure the FastAPI application"""
    app = FastAPI(title="Uamitos-CA API")
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth_routes.router, tags=["authentication"])
    app.include_router(student_routes.router, tags=["students"])
    app.include_router(teacher_routes.router, tags=["teachers"])
    app.include_router(event_routes.router, tags=["events"])
    app.include_router(grade_routes.router, tags=["grades"])
    app.include_router(schedule_routes.router, tags=["schedules"])
    app.include_router(user_routes.router, tags=["users"])
    app.include_router(report_routes.router, tags=["reports"])
    
    return app


def main():
    """Main application entry point"""
    try:
        # Initialize database
        init_database()
        
        # Initialize GUI
        qt_app = QApplication(sys.argv)
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "window", "logoUamitos.png")
        if os.path.exists(icon_path):
            qt_app.setWindowIcon(QIcon(icon_path))
        else:
            logger.warning(f"Window icon not found at: {icon_path}")
            
        # Create dependency container
        container = AppContainer()
        
        # Force initialization of login_builder singleton
        login_builder = container.login_builder()
        
        # Build main window
        window = container.main_window_builder().build()
        
        # Get stacked widget
        stacked_widget = window.centralWidget()
        if not isinstance(stacked_widget, QStackedWidget):
            logger.error("Central widget is not a QStackedWidget")
            return
            
        # Initialize coordinator
        coordinator = container.coordinator(
            main_window=window,
            stacked_widget=stacked_widget
        )
        
        # Now update the login success callback with the correct coordinator reference
        login_builder.set_on_login_success(lambda uuid, role, name: coordinator.handle_login_success(uuid, role, name))
        
        # Register pages
        coordinator.register_page("login", 0)
        
        # Show window
        window.show()
        
        # Run application
        sys.exit(qt_app.exec())
        
    except Exception as e:
        logger.error(f"Application failed to start: {e}", exc_info=True)
        raise


# Create FastAPI app for uvicorn
api = create_api()

if __name__ == '__main__':
    main()