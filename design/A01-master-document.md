# Master Document Structure

1. **Version**: Specifies the version of the master document format.
2. **Name and Description**: Provide a human-readable name and description of the master document.
3. **Data Objects Array**: Contains entries for each data object type, including:
   - **id**: Unique identifier for the data object type.
   - **name**: Human-readable name.
   - **description**: Brief description of the data object.
   - **uri**: URI pointing to the JSON description file for this data object.
   - **operations**: List of supported CRUD operations.
4. **Metadata**: Contains information about the creation and modification of the master document, including timestamps and responsible entities.

This structure is flexible and can be extended to include additional fields as needed, such as access control information or versioning details for each data object type.


```json
{
  "version": "1.0.0",
  "name": "Master Document",
  "description": "Master document listing all available data object types",
  "data_objects": [
    {
      "id": "user",
      "name": "User",
      "description": "User data object type",
      "uri": "/data_objects/user.json",
      "operations": ["create", "read", "update", "delete", "list"]
    },
    {
      "id": "product",
      "name": "Product",
      "description": "Product data object type",
      "uri": "/data_objects/product.json",
      "operations": ["create", "read", "update", "delete", "list"]
    }
  ],
  "metadata": {
    "created_at": "2023-09-20T14:30:00Z",
    "updated_at": "2023-09-20T14:30:00Z",
    "created_by": "System",
    "updated_by": "System"
  }
}
```

