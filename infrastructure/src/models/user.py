from datetime import datetime
from sqlalchemy import Column, String, Enum, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from .data_object import DataObject

Base = declarative_base()

class User(DataObject):
    """
    User model class based on users.json schema
    """
    __tablename__ = 'users'

    # Override id to use auto-incrementing integer
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Personal Information
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    # Account Information
    email = Column(String(254), nullable=False, unique=True)
    password = Column(String(128), nullable=False)  # Will store hashed password
    status = Column(
        Enum('active', 'inactive', 'pending', name='user_status'),
        nullable=False,
        default='pending'
    )

    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(50), nullable=False, default='System')
    updated_by = Column(String(50), nullable=False, default='System')

    def __init__(self, **kwargs):
        """
        Initialize a new User instance
        """
        super(User, self).__init__(**kwargs)

    def to_dict(self):
        """
        Convert User instance to dictionary
        """
        base_dict = super().to_dict()
        user_dict = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'status': self.status
        }
        return {**base_dict, **user_dict}

    def update(self, **kwargs):
        """
        Update user attributes
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, status={self.status})>"

    @classmethod
    def create_table(cls, engine):
        """
        Create the users table in the database
        """
        Base.metadata.create_all(engine, tables=[cls.__table__]) 