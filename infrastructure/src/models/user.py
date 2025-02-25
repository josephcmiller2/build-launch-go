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

    # Personal Information
    first_name = Column(String(50), nullable=False)
    first_name.field_label = 'First Name'
    first_name.field_min_length = 2
    first_name.field_regex = '^[a-zA-Z]+$'

    last_name = Column(String(50), nullable=False)
    last_name.field_label = 'Last Name'
    last_name.field_min_length = 2
    last_name.field_regex = '^[a-zA-Z]+$'

    # Account Information
    email = Column(String(254), nullable=False, unique=True)
    email.field_label = 'Email Address'
    password = Column(String(128), nullable=False)  # Will store hashed password
    password.field_format = 'password'
    password.field_label = 'Password'
    password.field_min_length = 8
    password.field_regex = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$'

    status = Column(
        Enum('active', 'inactive', 'pending', name='user_status'),
        nullable=False,
        default='pending'
    )
    status.field_label = 'Account Status'
    status.field_enum_values = {
        'active': 'Active',
        'inactive': 'Inactive',
        'pending': 'Pending'
    }
    status.field_default = 'pending'

    _field_properties = {
        'groups': [
            {
                'name': 'Account Information',
                'fields': ['username', 'email', 'password']
            },
            {
                'name': 'Personal Information',
                'fields': ['first_name', 'last_name']
            },
            {
                'name': 'Status',
                'fields': ['status']
            }
        ],
        'listFields': ['email', 'first_name', 'last_name', 'status'],
        'searchFields': ['*TEXT*', 'status'],
        'searchTextFields': ['email', 'first_name', 'last_name']
    }

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