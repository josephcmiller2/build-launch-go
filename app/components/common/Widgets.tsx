import React from 'react';

// Example Widget: Button
export const ButtonWidget: React.FC<{ label: string; onClick: () => void }> = ({ label, onClick }) => (
  <button onClick={onClick} className="bg-blue-500 text-white px-4 py-2">
    {label}
  </button>
);

// Example Widget: Input
export const InputWidget: React.FC<{ placeholder: string; value: string; onChange: (e: React.ChangeEvent<HTMLInputElement>) => void }> = ({
  placeholder,
  value,
  onChange,
}) => (
  <input
    type="text"
    placeholder={placeholder}
    value={value}
    onChange={onChange}
    className="border border-gray-300 px-4 py-2 mr-2"
  />
);

// New Widget: Select
export const SelectWidget: React.FC<{
  options: { value: string; label: string }[];
  value: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  placeholder?: string;
}> = ({ options, value, onChange, placeholder }) => (
  <select
    value={value}
    onChange={onChange}
    className="border border-gray-300 px-4 py-2 mr-2"
  >
    {placeholder && <option value="">{placeholder}</option>}
    {options.map(option => (
      <option key={option.value} value={option.value}>
        {option.label}
      </option>
    ))}
  </select>
);

// Widget function to choose the correct widget based on type
export const Widget: React.FC<{
  type: 'button' | 'input' | 'select';
  props: any; // Use a more specific type if possible
}> = ({ type, props }) => {
  switch (type) {
    case 'button':
      return <ButtonWidget {...props} />;
    case 'text':
    case 'input':
      return <InputWidget {...props} />;
    case 'enum':
    case 'select':
      return <SelectWidget {...props} />;
    default:
      return null; // or throw an error
  }
};

// Export all widgets
export default {
  ButtonWidget,
  InputWidget,
  SelectWidget,
  Widget, // Export the new Widget function
  // Export other widgets here...
}; 