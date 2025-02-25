from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import logging

# Create a basic logger if utils.logger isn't available
logger = logging.getLogger(__name__)

Base = declarative_base()

class DataObject(Base):
    """
    Base class for all data objects in the system.
    Provides common fields and functionality.
    """
    __abstract__ = True  # Marks this as an abstract base class

    # static variable to store all registered classes
    _registered_classes = []

    # Common field definitions
    _common_field_attributes = {
        'id': {
            'label': 'ID',
            'display': {'visible': False}
        },
        'created_at': {
            'label': 'Created At',
            'display': {'visible': False}
        },
        'updated_at': {
            'label': 'Updated At',
            'display': {'visible': False}
        },
        'created_by': {
            'label': 'Created By',
            'display': {'visible': False}
        },
        'updated_by': {
            'label': 'Updated By',
            'display': {'visible': False}
        }
    }

    # Common identifier field
    id = Column(String(50), primary_key=True)
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

    # static method to regiser a class with the DataObject class
    @classmethod
    def register_class(cls):
        """
        Register a class with the DataObject class
        """
        # log that the class is being registered
        logger.info(f"Registering class {cls.__name__} with DataObject")
        if cls not in DataObject._registered_classes:
            DataObject._registered_classes.append(cls)

    @classmethod
    def get_object(cls, classname):
        """
        Get an object from the registered classes regardless of the case of the classname
        """
        for registered_class in DataObject._registered_classes:
            if registered_class.__name__.lower() == classname.lower():
                # instantiate an object of the class
                return registered_class()
        return None
    
    @classmethod
    def is_class_registered(cls, classname):
        """
        Check if a class is registered with the DataObject class
        """
        for cls in DataObject._registered_classes:
            # log the class name
            logger.info(f"Checking if {cls.__name__} is registered")
            if cls.__name__.lower() == classname.lower():
                return True
        
        return False
    
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

    def field_is_password(self, field):
        """
        Check if the field is a password.
        """
        return hasattr(field, 'field_format') and field.field_format == 'password'
    
    def field_is_enum(self, field):
        """
        Check if the field is an enum.
        """
        return self.get_field_type_name(field.type) == 'enum'
    
    def get_field_properties(self):
        """
        Get the field properties for the object.
        Override in child classes to add specific fields.
        """
        if hasattr(self, '_field_properties'):
            return self._field_properties
        return {}
    
    def get_field_validation(self, field):
        """
        Get the validation for the field.
        Override in child classes to add specific validation.
        """
        field_validation = {}

        # if the field is a format of password
        if self.field_is_password(field):
            field_validation['min_length'] = 8
            field_validation['max_length'] = 1024
        else:
            if 'length' in field.type.__dict__:
                    field_validation['max_length'] = field.type.__dict__['length']

        if hasattr(field, 'field_min_length'):
            field_validation['min_length'] = field.field_min_length

        if hasattr(field, 'field_regex'):
            field_validation['regex'] = field.field_regex

        return field_validation
    
    def get_field_desc(self, field, field_type, field_required):
        """
        Get the description for the field.
        Override in child classes to add specific description.
        """
        field_desc = {
            'name': field.name,
            'type': field_type,
            'required': field_required,
            'label': field.name,
            'description': field.description
        }
        
        # Apply common field attributes if they exist
        if field.name in self._common_field_attributes:
            common_attrs = self._common_field_attributes[field.name]
            for key, value in common_attrs.items():
                field_desc[key] = value

        if self.field_is_enum(field):
            if hasattr(field, 'field_enum_values'):
                field_desc['enum_values'] = field.field_enum_values
            else:
                # map field.type.enums to itself in a dictionary
                field_desc['enum_values'] = {enum: enum for enum in field.type.enums}
        
        # if field has a field_format attribute, add it to the field_desc
        if hasattr(field, 'field_format'):
            field_desc['format'] = field.field_format

        # if field has a field_label attribute, add it to the field_desc
        if hasattr(field, 'field_label'):
            field_desc['label'] = field.field_label

        # set default value if field has a field_default attribute
        if hasattr(field, 'field_default'):
            field_desc['default'] = field.field_default
        
        field_validation = self.get_field_validation(field)
        if field_validation:
            field_desc['validation'] = field_validation

        print(f"Field {field.name} checking display")
        if field.name == 'id':
            print(field.type)
        # if the field has a field_display attribute, add it to the field_desc
        if hasattr(field, 'field_display'):
            print(f"Field {field.name} has a field_display attribute: {field.field_display}")
            field_desc['display'] = field.field_display

        return field_desc

    def describe_object(self):
        """
        Describe the object.
        Override in child classes to add specific fields.
        """
        # iterate over all fields in the object
        fields = []
        for field in self.__table__.columns:
            if False:
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

            field_desc = self.get_field_desc(field, field_type, field_required)

            fields.append(field_desc)

        object_description = {
            'id': self.__class__.__name__.lower(),
            'name': self.__class__.__name__,
            'fields': fields
        }

        field_properties = self.get_field_properties()
        # if field_properties has a groups key, add it to the object_description
        if 'groups' in field_properties:
            object_description['groups'] = field_properties['groups']

        # if field_properties has an operations key, add it to the object_description
        if 'operations' in field_properties:
            object_description['operations'] = field_properties['operations']
        else:
            object_description['operations'] = {
                'create': {
                    'enabled': True
                },
                'read': {
                    'enabled': True
                },
                'update': {
                    'enabled': True
                },
                'delete': {
                    'enabled': True
                },
                'list': {
                    'enabled': True
                }
            }
        # if field_properties has a listFields key, add it to the object_description
        if 'listFields' in field_properties:
            object_description['listFields'] = field_properties['listFields']

        if 'searchFields' in field_properties:
            object_description['searchFields'] = field_properties['searchFields']

        if 'searchTextFields' in field_properties:
            object_description['searchTextFields'] = field_properties['searchTextFields']

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