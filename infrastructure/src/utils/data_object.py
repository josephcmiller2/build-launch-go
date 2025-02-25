from typing import Dict, Any, Optional, List
from datetime import datetime
# import data_object class
from models.data_object import DataObject
# import all models dynamically
from models import *  # This will import all models dynamically

class DataObjectManager:
    """
    Manages operations and descriptions for data objects in the system.
    Provides functionality for generating API endpoints and object metadata.
    """

    @staticmethod
    def build_endpoint_operations(object_slug: str, operations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build API endpoint configurations for the given operations.
        
        Args:
            object_slug (str): The slug identifier for the data object
            operations (Dict[str, Any]): Dictionary of operation configurations
            
        Returns:
            Dict[str, Any]: Updated operations with endpoint configurations
        """
        endpoint_configs = {
            'create': {'endpoint': f"/api/{object_slug}", 'method': "POST"},
            'read': {'endpoint': f"/api/{object_slug}/{{id}}", 'method': "GET"},
            'update': {'endpoint': f"/api/{object_slug}/{{id}}", 'method': "PUT"},
            'delete': {'endpoint': f"/api/{object_slug}/{{id}}", 'method': "DELETE"},
            'list': {'endpoint': f"/api/{object_slug}", 'method': "GET"}
        }

        for op_name, config in operations.items():
            if config.get('enabled'):
                operations[op_name].update(endpoint_configs.get(op_name, {}))
                
                # Add default list operation configurations
                if op_name == 'list':
                    if 'pagination' not in config:
                        operations[op_name]['pagination'] = True
                    if 'default_page_size' not in config:
                        operations[op_name]['default_page_size'] = 20

        return operations

    @staticmethod
    def get_object_description(object_slug: str) -> Optional[Dict[str, Any]]:
        """
        Generate a complete description of a data object including its operations and metadata.
        
        Args:
            object_slug (str): The slug identifier for the data object type
            
        Returns:
            Optional[Dict[str, Any]]: Complete object description or None if object not found
        """
        if not DataObject.is_class_registered(object_slug):
            return None

        # Get base object description
        data_object = DataObject.get_object(object_slug).describe_object()
        
        # Build and update operations
        if 'operations' in data_object:
            data_object['operations'] = DataObjectManager.build_endpoint_operations(
                object_slug, 
                data_object['operations']
            )

        # Ensure required fields exist
        data_object.setdefault('listFields', [])
        data_object.setdefault('searchFields', [])

        # Add version and metadata
        now = datetime.utcnow().isoformat()
        return {
            "version": "1.0.0",
            **data_object,
            "metadata": {
                "created_at": now,
                "updated_at": now,
                "created_by": "System",
                "updated_by": "System"
            }
        }

    @staticmethod
    def get_master_document() -> Dict[str, Any]:
        """
        Generate a master document containing information about all registered data objects.
        
        Returns:
            Dict[str, Any]: Master document with all data object descriptions
        """
        now = datetime.utcnow().isoformat()
        
        data_objects: List[Dict[str, Any]] = []
        
        for data_object_class in DataObject._registered_classes:
            if data_object_class.__name__ == "DataObject":
                continue
                
            object_slug = data_object_class.__name__.lower()
            description = data_object_class().describe_object()
            
            data_objects.append({
                "id": object_slug,
                "name": data_object_class.__name__,
                "description": description.get('description', 
                    f"{data_object_class.__name__} data object type"),
                "uri": f"/api/object/{object_slug}/",
                "operations": [
                    op for op, details in description.get('operations', {}).items() 
                    if details.get('enabled', False)
                ]
            })

        return {
            "version": "1.0.0",
            "name": "Master Document",
            "description": "Master document listing all available data object types",
            "data_objects": data_objects,
            "metadata": {
                "created_at": now,
                "updated_at": now,
                "created_by": "System",
                "updated_by": "System"
            }
        } 