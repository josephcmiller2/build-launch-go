# src/database/db.py
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# Initialize a logger for this module.
logger = logging.getLogger(__name__)

class DatabaseManager:
    # Retrieve connection parameters from environment variables.
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "ai_agent")
    
    # Build the connection URL.
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    logger.info(f"Database URL constructed: postgresql://{DB_USER}:********@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    # Static members for the engine, session factory, and Base.
    engine = create_engine(DATABASE_URL)
    logger.info("Database engine created successfully.")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = scoped_session(SessionLocal)
    Base = declarative_base()
    
    @classmethod
    def init_db(cls):
        """
        Initialize the database by importing the models and creating all tables.
        """
        logger.info("Initializing the database...")
        try:
            # Import all modules that define models to ensure they are registered with the Base.
            import models  # Ensure models/__init__.py imports your model classes (e.g., Trigger)
            cls.Base.metadata.create_all(bind=cls.engine)
            logger.info("Database tables created successfully.")
        except Exception as e:
            logger.error("Error initializing the database: %s", e)
            raise
    
    @classmethod
    def get_session(cls):
        """
        Returns a new session instance.
        """
        logger.debug("Creating new database session.")
        return cls.db_session()

# Example usage:
# from database.db import DatabaseManager
# session = DatabaseManager.get_session()
# ... use session to interact with the database ...
