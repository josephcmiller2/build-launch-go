# Data Object Type Description Documentation

## Overview

A data object type description is a JSON file that defines the structure, fields, validation rules, and operations supported by a specific data object type. These descriptions are used by the platform to automatically generate the necessary CRUD (Create, Read, Update, Delete) interfaces. This document outlines the structure, required fields, and best practices for creating data object type descriptions.

## Structure of a Data Object Description

A data object description consists of the following main sections:

1. **Version**: Specifies the version of the data object type.
2. **Identifier and Metadata**: Basic information about the data object type.
3. **Fields**: Definition of all fields in the data object, including their types, validation rules, and display properties.
4. **Operations**: CRUD operations supported by the data object type.
5. **Styling and Grouping**: Optional settings for customizing the appearance and organization of fields in the UI.
6. **Versioning**: Tracks changes to the data object type over time.

## 1. Version

The `version` field specifies the version of the data object type description. This is used for version control and compatibility purposes.

**Example:**
```json
"version": "1.0.0"
```

## 2. Identifier and Metadata

### `id`
A unique identifier for the data object type. This is used in URLs and references.

**Example:**
```json
"id": "user"
```

### `name`
The human-readable name of the data object type.

**Example:**
```json
"name": "User"
```

### `description`
A brief description of the data object type.

**Example:**
```json
"description": "User data object type"
```

### `metadata`
Metadata tracks creation and modification details for auditing purposes.

**Properties:**
- `created_at`: Timestamp of when the data object type was created.
- `updated_at`: Timestamp of when the data object type was last updated.
- `created_by`: User or system that created the data object type.
- `updated_by`: User or system that last updated the data object type.

**Example:**
```json
"metadata": {
  "created_at": "2023-09-20T14:30:00Z",
  "updated_at": "2023-09-20T14:30:00Z",
  "created_by": "System",
  "updated_by": "System"
}
```

## 3. Fields

The `fields` array defines the structure of the data object type. Each field is an object with the following properties:

### Field Properties

#### `name`
The unique identifier for the field within the data object.

**Example:**
```json
"name": "first_name"
```

#### `type`
The data type of the field. Supported types include:
- `text`
- `integer`
- `float`
- `date`
- `boolean`
- `enum`
- `array`

**Example:**
```json
"type": "text"
```

#### `required`
A boolean indicating whether the field is mandatory.

**Example:**
```json
"required": true
```

#### `label`
The human-readable label for the field, used in forms and displays.

**Example:**
```json
"label": "First Name"
```

#### `validation`
Validation rules for the field. Can include:
- `min_length`: Minimum length of the input.
- `max_length`: Maximum length of the input.
- `regex`: Regular expression pattern for validation.
- `format`: Predefined formats (e.g., `email`, `phone`).

**Example:**
```json
"validation": {
  "min_length": 2,
  "max_length": 50,
  "regex": "^[a-zA-Z]+$"
}
```

#### `enum_values` (for `type`: `enum`)
A list of allowed values for an enum field.

**Example:**
```json
"enum_values": ["active", "inactive", "pending"]
```

#### `default` (optional)
The default value for the field.

**Example:**
```json
"default": "active"
```

### Example Field Definition:
```json
{
  "name": "email",
  "type": "email",
  "required": true,
  "label": "Email",
  "validation": {
    "format": "email"
  }
}
```


### Reference Field

A reference field allows you to link a field in one data object type to a field in another data object type. This is useful for creating relationships between different data entities. Below is the detailed documentation for the reference field.


### Field Properties - Reference

#### `type`
Set to `"reference"` to indicate that this field references another field in a different data object type.

**Example:**
```json
"type": "reference"
```

#### `reference_object_type_id`
The unique identifier (`id`) of the data object type that contains the referenced field.

**Example:**
```json
"reference_object_type_id": "user"
```

#### `reference_field_name`
The name of the field in the referenced data object type that this field references.

**Example:**
```json
"reference_field_name": "id"
```

#### `reference_field_definition` (optional)
A copy of the referenced field's definition from the referenced data object type. This allows the platform to have the field definition without needing to look it up elsewhere.

**Example:**
```json
"reference_field_definition": {
  "name": "id",
  "type": "integer",
  "required": true,
  "label": "User ID",
  "validation": {
    "min": 1
  }
}
```

#### `display_field` (optional)
The name of a field in the referenced data object type whose value will be displayed to the user. This is useful for showing meaningful information instead of just the referenced field's value.

**Example:**
```json
"display_field": "username"
```

#### `required`
A boolean indicating whether the reference is mandatory.

**Example:**
```json
"required": true
```

### Example Reference Field Definition:
```json
{
  "name": "user_id",
  "type": "reference",
  "reference_object_type_id": "user",
  "reference_field_name": "id",
  "reference_field_definition": {
    "name": "id",
    "type": "integer",
    "required": true,
    "label": "User ID",
    "validation": {
      "min": 1
    }
  },
  "display_field": "username",
  "required": true,
  "label": "User"
}
```

### Operations with References

When defining operations for a data object type that includes reference fields, the platform will automatically handle the resolution of referenced fields, ensuring that the referenced data is properly fetched and displayed. For example, when retrieving a record, the platform will include the referenced field's value and, if `display_field` is specified, the corresponding display value.

### Example Operations with References:
```json
"operations": {
  "create": {
    "enabled": true,
    "endpoint": "/api/orders",
    "method": "POST"
  },
  "read": {
    "enabled": true,
    "endpoint": "/api/orders/{id}",
    "method": "GET"
  },
  "update": {
    "enabled": true,
    "endpoint": "/api/orders/{id}",
    "method": "PUT"
  },
  "delete": {
    "enabled": true,
    "endpoint": "/api/orders/{id}",
    "method": "DELETE"
  },
  "list": {
    "enabled": true,
    "endpoint": "/api/orders",
    "method": "GET",
    "pagination": true,
    "default_page_size": 10
  }
}
```

### Example Data Object Description with References

Here's an updated example that includes a reference field with the revised properties:

```json
{
  "version": "1.0.0",
  "id": "order",
  "name": "Order",
  "description": "Order data object type",
  "stylesheet": "styles/order.css",
  "groups": [
    {
      "name": "Order Information",
      "fields": ["order_id", "user_id", "order_date"]
    }
  ],
  "fields": [
    {
      "name": "order_id",
      "type": "integer",
      "required": true,
      "label": "Order ID",
      "validation": {
        "min": 1
      }
    },
    {
      "name": "user_id",
      "type": "reference",
      "reference_object_type_id": "user",
      "reference_field_name": "id",
      "reference_field_definition": {
        "name": "id",
        "type": "integer",
        "required": true,
        "label": "User ID",
        "validation": {
          "min": 1
        }
      },
      "display_field": "username",
      "required": true,
      "label": "User"
    },
    {
      "name": "order_date",
      "type": "date",
      "required": true,
      "label": "Order Date",
      "validation": {
        "format": "YYYY-MM-DD"
      }
    }
  ],
  "operations": {
    "create": {
      "enabled": true,
      "endpoint": "/api/orders",
      "method": "POST"
    },
    "read": {
      "enabled": true,
      "endpoint": "/api/orders/{id}",
      "method": "GET"
    },
    "update": {
      "enabled": true,
      "endpoint": "/api/orders/{id}",
      "method": "PUT"
    },
    "delete": {
      "enabled": true,
      "endpoint": "/api/orders/{id}",
      "method": "DELETE"
    },
    "list": {
      "enabled": true,
      "endpoint": "/api/orders",
      "method": "GET",
      "pagination": true,
      "default_page_size": 10
    }
  },
  "metadata": {
    "created_at": "2023-09-20T14:30:00Z",
    "updated_at": "2023-09-20T14:30:00Z",
    "created_by": "System",
    "updated_by": "System"
  }
}
```

## 4. Operations

The `operations` object defines the CRUD operations supported by the data object type. Each operation specifies the endpoint, HTTP method, and additional settings.

### Operation Properties

#### `enabled`
A boolean indicating whether the operation is enabled.

#### `endpoint`
The API endpoint for the operation.

#### `method`
The HTTP method for the operation (e.g., `GET`, `POST`, `PUT`, `DELETE`).

#### `pagination` (for `list` operation)
A boolean indicating whether pagination is enabled for the list operation.

#### `default_page_size` (for `list` operation)
The default number of records per page for pagination.

### Example Operations Definition:
```json
"operations": {
  "create": {
    "enabled": true,
    "endpoint": "/api/users",
    "method": "POST"
  },
  "read": {
    "enabled": true,
    "endpoint": "/api/users/{id}",
    "method": "GET"
  },
  "update": {
    "enabled": true,
    "endpoint": "/api/users/{id}",
    "method": "PUT"
  },
  "delete": {
    "enabled": true,
    "endpoint": "/api/users/{id}",
    "method": "DELETE"
  },
  "list": {
    "enabled": true,
    "endpoint": "/api/users",
    "method": "GET",
    "pagination": true,
    "default_page_size": 10
  }
}
```


## 5. Styling and Grouping

### Stylesheet Reference
You can reference a stylesheet to customize the appearance of the generated interface.

**Example:**
```json
"stylesheet": "styles/user.css"
```

### Field Grouping
Fields can be grouped logically for better organization in the UI.

**Example:**
```json
"groups": [
  {
    "name": "Personal Information",
    "fields": ["first_name", "last_name", "email"]
  },
  {
    "name": "Contact Information",
    "fields": ["phone"]
  }
]
```

### Conditional Display
Fields can be shown or hidden based on other field values.

**Example:**
```json
"fields": [
  {
    "name": "phone",
    "type": "text",
    "display_conditions": {
      "show_if": {
        "field": "phone_type",
        "value": "mobile"
      }
    }
  }
]
```

## 6. Versioning

The `version` field is used to track changes to the data object type. This ensures compatibility when new versions are introduced.

**Example:**
```json
"version": "1.0.0"
```

## 7. Best Practices

- **Keep it Simple**: Start with basic fields and operations, then add complexity as needed.
- **Validation**: Define thorough validation rules to ensure data integrity.
- **Grouping**: Organize fields into logical groups for better usability.
- **Consistency**: Use consistent naming conventions and styles across data object types.

## 8. Example Data Object Description

```json
{
  "version": "1.0.0",
  "id": "user",
  "name": "User",
  "description": "User data object type",
  "stylesheet": "styles/user.css",
  "groups": [
    {
      "name": "Personal Information",
      "fields": ["first_name", "last_name", "email"]
    },
    {
      "name": "Contact Information",
      "fields": ["phone"]
    }
  ],
  "fields": [
    {
      "name": "first_name",
      "type": "text",
      "required": true,
      "label": "First Name",
      "validation": {
        "min_length": 2,
        "max_length": 50,
        "regex": "^[a-zA-Z]+$"
      }
    },
    {
      "name": "last_name",
      "type": "text",
      "required": true,
      "label": "Last Name",
      "validation": {
        "min_length": 2,
        "max_length": 50,
        "regex": "^[a-zA-Z]+$"
      }
    },
    {
      "name": "email",
      "type": "email",
      "required": true,
      "label": "Email",
      "validation": {
        "format": "email"
      }
    },
    {
      "name": "phone",
      "type": "text",
      "required": false,
      "label": "Phone",
      "validation": {
        "format": "phone",
        "regex": "^\\+?\\d{1,3}?[- .]?\\(?(\\d{3})\\)?[- .]?\\d{3}[- .]?\\d{4}$"
      }
    },
    {
      "name": "status",
      "type": "enum",
      "required": true,
      "label": "Status",
      "enum_values": ["active", "inactive", "pending"],
      "default": "active"
    }
  ],
  "operations": {
    "create": {
      "enabled": true,
      "endpoint": "/api/users",
      "method": "POST"
    },
    "read": {
      "enabled": true,
      "endpoint": "/api/users/{id}",
      "method": "GET"
    },
    "update": {
      "enabled": true,
      "endpoint": "/api/users/{id}",
      "method": "PUT"
    },
    "delete": {
      "enabled": true,
      "endpoint": "/api/users/{id}",
      "method": "DELETE"
    },
    "list": {
      "enabled": true,
      "endpoint": "/api/users",
      "method": "GET",
      "pagination": true,
      "default_page_size": 10
    }
  },
  "metadata": {
    "created_at": "2023-09-20T14:30:00Z",
    "updated_at": "2023-09-20T14:30:00Z",
    "created_by": "System",
    "updated_by": "System"
  }
}
```

## Conclusion

This documentation provides a comprehensive guide to creating and structuring data object type descriptions. By following these guidelines, developers can define data models that enable the platform to automatically generate user-friendly CRUD interfaces while maintaining data integrity and consistency.