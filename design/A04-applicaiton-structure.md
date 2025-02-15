# Application Structure Documentation

## Overview
This document outlines the structure and organization of the application, which is built using React for the frontend and PHP for the backend.

## Root Directory Structure


design/A05-applicaiton-structure.md
/
├── app/ # Frontend React application
├── backend/ # PHP backend
├── design/ # Design documentation
├── tools/ # Development tools and scripts
└── tests/ # Test suites

## Frontend Structure (`/app`)
app/
├── components/ # Reusable React components
│ ├── common/ # Common UI components
│ │ ├── Header.tsx
│ │ ├── Footer.tsx
│ │ ├── Breadcrumbs.tsx
│ │ └── Navigation.tsx
│ ├── forms/ # Form-related components
│ │ ├── DynamicForm.tsx
│ │ ├── FormField.tsx
│ │ └── ValidationMessage.tsx
│ └── crud/ # CRUD operation components
│ ├── ListView.tsx
│ ├── CreateView.tsx
│ ├── EditView.tsx
│ └── DeleteConfirmation.tsx
├── contexts/ # React Context providers
│ └── AppContext.tsx
├── hooks/ # Custom React hooks
│ ├── useDataObject.ts
│ └── useValidation.ts
├── services/ # API and utility services
│ ├── api.ts
│ └── validation.ts
├── types/ # TypeScript type definitions
│ ├── DataObject.ts
│ └── ValidationRules.ts
└── styles/ # CSS/styling files
└── tailwind.css

## Backend Structure (`/backend`)
backend/
├── src/
│ ├── Controllers/ # Request handlers
│ │ └── DataObjectController.php
│ ├── Services/ # Business logic
│ │ ├── ValidationService.php
│ │ └── DataObjectService.php
│ └── Utils/ # Utility functions
│ ├── JsonLoader.php
│ └── ResponseFormatter.php
├── config/ # Configuration files
│ └── app.php
└── public/ # Public entry point
└── index.php


## Main Components

### Frontend Components

1. **DynamicForm Component**
   - Purpose: Generates forms based on data object descriptions
   - Handles field validation and submission
   - Supports all field types defined in the data object specification

2. **ListView Component**
   - Displays paginated table of records
   - Includes filtering and sorting capabilities
   - Action buttons for CRUD operations

3. **Header/Navigation Components**
   - Consistent header across all pages
   - Dynamic navigation based on available data objects
   - Breadcrumb navigation

### Backend Components

1. **DataObjectController**
   - Handles CRUD operation requests
   - Manages request validation
   - Routes requests to appropriate services

2. **ValidationService**
   - Implements validation rules from field formats
   - Validates input data against schema definitions
   - Handles custom validation rules

3. **JsonLoader**
   - Loads and parses data object descriptions
   - Manages file and HTTP(S) URI resolution
   - Caches frequently accessed definitions

## Implementation Details

### Data Object Loading



## URL Structure
- `/` - Home Page
- `/DATA_OBJECT_TYPE_SLUG/list` - Paginated list view
- `/DATA_OBJECT_TYPE_SLUG/edit/ID` - GET: Edit form; POST: Save/Update
- `/DATA_OBJECT_TYPE_SLUG/add` - GET: Create form; POST: Submit new record
- `/DATA_OBJECT_TYPE_SLUG/delete/ID` - POST: Delete confirmation and execution

