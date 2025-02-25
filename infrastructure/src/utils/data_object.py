from typing import Dict, Any, Optional
from datetime import datetime
# import data_object class
from models.data_object import DataObject
# import all models dynamically
from models import *  # This will import all models dynamically

def object_operations(object_slug: str, operations: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Get the operations for a data object based on its slug.
    """
    if not DataObject.is_class_registered(object_slug):
        return None
        
    # if create is defined and enabled is true, add the create operation
    if 'create' in operations and operations['create']['enabled']:
        operations['create']['endpoint'] = f"/api/{object_slug}"
        operations['create']['method'] = "POST"

    # if read is defined and enabled is true, add the read operation
    if 'read' in operations and operations['read']['enabled']:
        operations['read']['endpoint'] = f"/api/{object_slug}/"+"{id}"
        operations['read']['method'] = "GET"

    if 'update' in operations and operations['update']['enabled']:
        operations['update']['endpoint'] = f"/api/{object_slug}/"+"{id}"
        operations['update']['method'] = "PUT"

    if 'delete' in operations and operations['delete']['enabled']:
        operations['delete']['endpoint'] = f"/api/{object_slug}/"+"{id}"
        operations['delete']['method'] = "DELETE"

    if 'list' in operations and operations['list']['enabled']:
        operations['list']['endpoint'] = f"/api/{object_slug}"
        operations['list']['method'] = "GET"
        if 'pagination' not in operations['list']:
            operations['list']['pagination'] = True

        if 'default_page_size' not in operations['list']:
            operations['list']['default_page_size'] = 20

    return operations


def get_data_object_description(object_slug: str) -> Optional[Dict[str, Any]]:
    """
    Get the description of a data object based on its slug.
    
    Args:
        object_slug (str): The slug identifier for the data object type
        
    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the data object description,
                                 or None if the object type is not found
    """
    if not DataObject.is_class_registered(object_slug):
        return None

    # Basic template for data object description
    data_object_base = {
        "version": "1.0.0"
    }

    # get the object class
    data_object = DataObject.get_object(object_slug).describe_object()


    data_object['operations'] = object_operations(object_slug, data_object['operations'])

    if 'listFields' not in data_object:
        data_object['listFields'] = []

    if 'searchFields' not in data_object:
        data_object['searchFields'] = []

    # merge data_object_base with data_object
    data_object = {**data_object_base, **data_object}

    now_time = datetime.utcnow().isoformat()

    data_object['metadata'] = {
        "created_at": now_time,
        "updated_at": now_time,
        "created_by": "System",
        "updated_by": "System"
    }

    
    return data_object 

def get_master() -> Dict[str, Any]:
    """
    Generate a master document listing all available data object types.
    """
    generated_datetime = datetime.utcnow().isoformat()
    master_doc = {
        "version": "1.0.0",
        "name": "Master Document",
        "description": "Master document listing all available data object types",
        "data_objects": [],
        "metadata": {
            "created_at": generated_datetime,
            "updated_at": generated_datetime,
            "created_by": "System",
            "updated_by": "System"
        }
    }

    # Get all registered data objects
    for data_object_class in DataObject._registered_classes:
        if data_object_class.__name__ != "DataObject":
            object_slug = data_object_class.__name__.lower()
            data_object = data_object_class()
            description = data_object.describe_object()
            
            object_info = {
                "id": object_slug,
                "name": data_object_class.__name__,
                "description": description.get('description', f"{data_object_class.__name__} data object type"),
                "uri": f"/api/object/{object_slug}/",
                "operations": [op for op, details in description.get('operations', {}).items() 
                             if details.get('enabled', False)]
            }
            master_doc["data_objects"].append(object_info)

    return master_doc 