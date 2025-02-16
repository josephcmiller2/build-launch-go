import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../../../components/common/Layout';
import App from '../../_app';
import { Widget, ButtonWidget } from '../../../components/common/Widgets';

const AddView: React.FC = () => {
  const router = useRouter();
  const { dataObjectTypeSlug } = router.query;
  const [dataObject, setDataObject] = useState<any>(null);
  const [formData, setFormData] = useState<{ [key: string]: any }>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (dataObjectTypeSlug) {
      // validate that dataObjectTypeSlug is a valid slug
      if (!dataObjectTypeSlug.match(/^[a-z0-9_-]+$/)) {
        setError('Invalid data object type');
        return;
      }

      const fetchDataObject = async () => {
        try {
          const response = await fetch(`${App.config.backendUrl}/api/object/${dataObjectTypeSlug}`);
          if (!response.ok) {
            throw new Error('Failed to fetch data object');
          }
          const data = await response.json();
          setDataObject(data);
          
          // Initialize form data with default values
          const initialData: { [key: string]: any } = {};
          data.fields.forEach((field: any) => {
            initialData[field.name] = field.default || '';
          });
          setFormData(initialData);
        } catch (error) {
          setError('Failed to fetch data object');
        }
      };

      fetchDataObject();
    }
  }, [dataObjectTypeSlug]);

  const handleInputChange = (fieldName: string, value: any) => {
    // If value is an event, extract the value from it
    const newValue = value?.target?.value ?? value;
    setFormData(prev => ({
      ...prev,
      [fieldName]: newValue
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const response = await fetch(`${App.config.backendUrl}${dataObject.operations.create.endpoint}`, {
        method: dataObject.operations.create.method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to create record');
      }

      // Redirect to list view on success
      router.push(`/admin/${dataObjectTypeSlug}/list`);
    } catch (error) {
      setError('Failed to create record');
    }
  };

  if (error) {
    return <Layout><div className="text-red-500">{error}</div></Layout>;
  }

  if (!dataObject) {
    return <Layout><div>Loading...</div></Layout>;
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">
          Add New {dataObject.name}
        </h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          {dataObject.fields.map((field: any) => {
            // Only skip if display.visible is explicitly set to false
            const isVisible = field.display?.visible !== false;
            
            return isVisible && (
              <div key={field.name} className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">
                  {field.label}
                  {field.required && <span className="text-red-500">*</span>}
                </label>
                
                <Widget
                  type={field.type}
                  name={field.name}
                  field={field}
                  value={formData[field.name] || ''}
                  onChange={(value: any) => handleInputChange(field.name, value)}
                />
                
                {field.display?.help_text && (
                  <p className="text-sm text-gray-500">{field.display.help_text}</p>
                )}
              </div>
            );
          })}

          <div className="flex justify-end space-x-4">
            <ButtonWidget
              name="cancel-button"
              field={{
                name: "cancel-button",
                type: "button",
                label: "Cancel",
                required: false
              }}
              value={null}
              onChange={() => router.push(`/admin/${dataObjectTypeSlug}/list`)}
            />
            <ButtonWidget
              name="save-button"
              field={{
                name: "save-button",
                type: "button",
                label: "Save",
                required: false
              }}
              value={null}
              onChange={handleSubmit}
            />
          </div>
        </form>
      </div>
    </Layout>
  );
};

export default AddView;
