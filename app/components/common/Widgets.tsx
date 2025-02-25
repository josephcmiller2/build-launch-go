import React, { useState } from 'react';

interface Field {
  name: string;
  type: string;
  format?: string;
  label: string;
  required?: boolean;
  validation?: {
    min_length?: number;
    max_length?: number;
    regex?: string;
  };
  enum_values?: string[];
  display?: {
    visible?: boolean;
    help_text?: string;
  };
  [key: string]: any;
}

interface WidgetProps {
  type: string;
  name: string;
  field: Field;
  value: any;
  onChange: (value: any) => void;
}

// Update ButtonWidget
export const ButtonWidget: React.FC<WidgetProps> = ({ 
  name, 
  field, 
  onChange 
}) => (
  <button 
    name={name}
    onClick={() => onChange(null)}
    className="bg-blue-500 text-white px-4 py-2"
  >
    {field.label}
  </button>
);

// Update InputWidget
export const InputWidget: React.FC<WidgetProps> = ({
  name,
  field,
  value,
  onChange
}) => {
  const validationAttrs = {
    minLength: field.validation?.min_length,
    maxLength: field.validation?.max_length,
    pattern: field.validation?.regex,
    required: field.required,
  };

  return (
    <div className="space-y-1">
      <input
        id={name}
        name={name}
        type={field.format || "text"}
        placeholder={`Enter ${field.label}...`}
        value={value}
        onChange={(e) => onChange(e)}
        {...validationAttrs}
        className="border border-gray-300 px-4 py-2 mr-2 rounded-md w-full"
      />
    </div>
  );
};

// Update SelectWidget
export const SelectWidget: React.FC<WidgetProps> = ({
  name,
  field,
  value,
  onChange
}) => (
  <select
    id={name}
    name={name}
    value={value}
    onChange={(e) => onChange(e)}
    required={field.required}
    className="border border-gray-300 px-4 py-2 mr-2"
  >
    <option value="">Select {field.label}...</option>
    {field.enum_values && Object.entries(field.enum_values).map(([value, label]) => (
      <option key={value} value={value}>
        {label}
      </option>
    ))}
  </select>
);

// Update PasswordWidget
export const PasswordWidget: React.FC<WidgetProps> = ({
  name,
  field,
  value,
  onChange
}) => {
  const [password, setPassword] = useState(value);
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [validationMessage, setValidationMessage] = useState<string | null>(null);

  const validatePassword = (pass: string) => {
    if (field.validation?.regex) {
      const regex = new RegExp(field.validation.regex);
      if (!regex.test(pass)) {
        setValidationMessage('Password does not meet requirements');
        return false;
      }
    }
    if (field.validation?.min_length && pass.length < field.validation.min_length) {
      setValidationMessage(`Password must be at least ${field.validation.min_length} characters`);
      return false;
    }
    if (field.validation?.max_length && pass.length > field.validation.max_length) {
      setValidationMessage(`Password must be no more than ${field.validation.max_length} characters`);
      return false;
    }
    setValidationMessage(null);
    return true;
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newPassword = e.target.value;
    setPassword(newPassword);
    validatePassword(newPassword);
    
    if (newPassword === confirmPassword) {
      setError(null);
      if (validatePassword(newPassword)) {
        onChange(newPassword);
      }
    } else if (confirmPassword) {
      setError('Passwords do not match');
    }
  };

  const handleConfirmChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setConfirmPassword(e.target.value);
    if (e.target.value === password) {
      setError(null);
      onChange(password);
    } else {
      setError('Passwords do not match');
    }
  };

  return (
    <div className="space-y-2">
      <input
        id={name}
        name={name}
        type="password"
        value={password}
        onChange={handlePasswordChange}
        placeholder={`Enter ${field.label}...`}
        required={field.required}
        minLength={field.validation?.min_length}
        maxLength={field.validation?.max_length}
        pattern={field.validation?.regex}
        className="border border-gray-300 px-4 py-2 rounded-md w-full"
      />
      {validationMessage && (
        <p className="text-yellow-600 text-sm">{validationMessage}</p>
      )}
      <input
        id={`${name}-confirm`}
        name={`${name}-confirm`}
        type="password"
        value={confirmPassword}
        onChange={handleConfirmChange}
        placeholder="Re-enter password"
        required={field.required}
        className="border border-gray-300 px-4 py-2 rounded-md w-full"
        aria-describedby={error ? `${name}-error` : undefined}
      />
      {error && (
        <p id={`${name}-error`} className="text-red-500 text-sm">{error}</p>
      )}
    </div>
  );
};

// Update main Widget component
export const Widget: React.FC<WidgetProps> = (props) => {
  const { type, field } = props;

  // Ensure field is defined
  if (!field) {
    console.error('Field is required for Widget');
    return null;
  }

  // Check for format
  if (field?.format) {
    switch (field.format) {
      case 'password':
        return <PasswordWidget {...props} />;
      case 'email':
      case 'date':
      case 'datetime':
      case 'phone':
      case 'url':
      case 'currency':
      case 'percentage':
        return <InputWidget {...props} />;
    }
  }

  // Fall back to type-based rendering
  switch (type) {
    case 'button':
      return <ButtonWidget {...props} />;
    case 'input':
    case 'text':
      return <InputWidget {...props} />;
    case 'enum':
    case 'select':
      return <SelectWidget {...props} />;
    default:
      return null;
  }
};

export default {
  ButtonWidget,
  InputWidget,
  SelectWidget,
  PasswordWidget,
  Widget,
}; 