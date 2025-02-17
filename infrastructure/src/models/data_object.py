from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DataObject(Base):
    """
    Base class for all data objects in the system.
    Provides common fields and functionality.
    """
    __abstract__ = True  # Marks this as an abstract base class

    # Common identifier field
    id = Column(String(50), primary_key=True)

    # Common metadata fields
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(50), nullable=False, default='System')
    updated_by = Column(String(50), nullable=False, default='System')

    _field_type_map = {
        'varchar': 'text'
    }

    def __init__(self, **kwargs):
        """
        Initialize a new DataObject instance
        """
        super(DataObject, self).__init__(**kwargs)
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def to_dict(self):
        """
        Convert instance to dictionary.
        Override in child classes to add specific fields.
        """
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'created_by': self.created_by,
            'updated_by': self.updated_by
        }

    def describe_object(self):
        """
        Describe the object.
        Override in child classes to add specific fields.
        """
        # iterate over all fields in the object
        fields = []
        for field in self.__table__.columns:
            if True:
                # iterate over all parameters in the field
                print("")
                print("Name = ", field.name)
                for param in field.type.__dict__:
                        print(param, " = ", field.type.__dict__[param])
                print("")
            # get the field type name   
            field_type = self.get_field_type_name(field.type)

            # required is the opposite of nullable
            field_required = not field.nullable

            fields.append({
                'name': field.name,
                'type': field_type,
                'required': field_required,
                'label': field.name,
                'description': field.description
            })

        object_description = {
            'id': self.__class__.__name__.lower(),
            'name': self.__class__.__name__,
            'fields': fields
        }

        return object_description

    def get_field_type_name(self, field_type_obj):
        field_type = str(field_type_obj)
        # parse the field_type to get the name of the type from Type(parameters)
        field_type = field_type.split('(')[0]
        # set field type to lowercase
        field_type = field_type.lower()

        # if field_type_obj has a native_enum attribute
        if hasattr(field_type_obj, 'native_enum'):
            if field_type_obj.native_enum:
                return 'enum'

        # check if the field_type is in the _field_type_map
        if field_type in self._field_type_map:
            return self._field_type_map[field_type]



        return field_type

    def update(self, **kwargs):
        """
        Update object attributes
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()

    @classmethod
    def create_table(cls, engine):
        """
        Create the table in the database
        """
        Base.metadata.create_all(engine, tables=[cls.__table__])

    def __repr__(self):
        """
        String representation of the object.
        Override in child classes for more specific information.
        """
        return f"<{self.__class__.__name__}(id={self.id})>" 