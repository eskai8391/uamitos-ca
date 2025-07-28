from typing import Generator, Optional
from threading import Lock
import logging

from sqlalchemy import create_engine, Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.pool import QueuePool


class DatabaseSingleton:
    """Singleton class to manage database connections and sessions"""
    
    _instance = None
    _lock = Lock()
    _initialized = False
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseSingleton, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    # Configure database connection
                    self.DATABASE_URL = {
                        "database": "uamitosca-database",
                        "drivername": "postgresql+psycopg2",
                        "username": "postgres",
                        "password": "root",
                        "host": "localhost",
                        "port": "5432",
                        "query": {"client_encoding": "utf8"}
                    }
                    
                    # Create engine with connection pooling settings
                    self._engine = create_engine(
                        URL(**self.DATABASE_URL),
                        poolclass=QueuePool,
                        pool_size=5,
                        max_overflow=10,
                        pool_timeout=30,
                        pool_recycle=1800,  # Recycle connections every 30 minutes
                        pool_pre_ping=True  # Check connections before use
                    )
                    
                    # Create session factory
                    self._session_factory = sessionmaker(
                        autocommit=False,
                        autoflush=False,
                        bind=self._engine
                    )
                    
                    # Create base for models
                    self._base = declarative_base()
                    
                    # Mark as initialized
                    self._initialized = True
                    logging.info("Database singleton initialized")
    
    @property
    def engine(self) -> Engine:
        """Get the SQLAlchemy engine"""
        return self._engine
    
    @property
    def base(self):
        """Get the SQLAlchemy base for models"""
        return self._base
    
    def create_session(self) -> Session:
        """Create a new database session"""
        return self._session_factory()
    
    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session with automatic cleanup"""
        session = self._session_factory()
        try:
            yield session
        finally:
            session.close()
    
    def create_all(self):
        """Create all tables defined in the models"""
        self._base.metadata.create_all(self._engine)
    
    def drop_all(self):
        """Drop all tables defined in the models"""
        self._base.metadata.drop_all(self._engine)


# Create the singleton instance
db = DatabaseSingleton()

# Export convenience references
Base = db.base
SessionLocal = db.create_session
get_db = db.get_session
create_all = db.create_all
drop_all = db.drop_all

# Export engine for direct access if needed
engine = db.engine