from typing import Dict, Any, Optional
from models.user import User

# Make list of valid data object types
VALID_DATA_OBJECT_TYPES = [
    'user'
]

def get_data_object_description(object_slug: str) -> Optional[Dict[str, Any]]:
    """
    Get the description of a data object based on its slug.
    
    Args:
        object_slug (str): The slug identifier for the data object type
        
    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the data object description,
                                 or None if the object type is not found
    """
    if object_slug not in VALID_DATA_OBJECT_TYPES:
        return None

    # Basic template for data object description
    data_object_base = {
        "version": "1.0.0"
    }

    if object_slug == 'user':
        # get a User object
        user = User()
        data_object = user.describe_object()

    # merge data_object_base with data_object
    data_object = {**data_object_base, **data_object}

    
    return data_object 