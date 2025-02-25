import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../../../components/common/Layout';
import App from '../../_app'; // Adjust the import path as necessary
import { Widget, ButtonWidget } from '../../../components/common/Widgets'; // Import the Widget function

const ListView: React.FC = () => {
  const router = useRouter();
  const { dataObjectTypeSlug } = router.query;
  const [dataObject, setDataObject] = useState<any>(null);
  const [error, setError] = useState<boolean>(false);
  const [searchQueries, setSearchQueries] = useState<{ [key: string]: string }>({});
  const [filteredData, setFilteredData] = useState<any[]>([]);

  useEffect(() => {
    if (dataObjectTypeSlug) {
      // validate that dataObjectTypeSlug is a valid slug
      if (!dataObjectTypeSlug.match(/^[a-z0-9_-]+$/)) {
        setError(true);
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
          setFilteredData(data.data); // Initialize filtered data
        } catch (error) {
          setError(true);
        }
      };

      fetchDataObject();
    }
  }, [dataObjectTypeSlug]);

  useEffect(() => {
    if (dataObject) {
      filterData();
    }
  }, [searchQueries, dataObject]);

  const filterData = () => {
    if (!dataObject || !dataObject.data) return;

    const { searchFields } = dataObject;
    const filtered = dataObject.data.filter((record: any) => {
      // Check for general text search
      if (searchFields.includes("*TEXT*")) {
        return Object.values(record).some(value =>
          String(value).toLowerCase().includes(searchQueries["*TEXT*"]?.toLowerCase() || '')
        );
      }

      // Check specific fields
      return searchFields.some(field => {
        if (field === "*TEXT*") return false; // Skip the special field
        return String(record[field] || '').toLowerCase().includes(searchQueries[field]?.toLowerCase() || '');
      });
    });

    setFilteredData(filtered);
  };

  const handleSearch = () => {
    filterData();
  };

  const handleInputChange = (field: string, value: string) => {
    setSearchQueries(prev => ({ ...prev, [field]: value }));
  };

  if (error) {
    return <Layout><h1 className="text-2xl font-bold">404 - Data Object Not Found</h1></Layout>;
  }

  if (!dataObject) {
    return <Layout><h1 className="text-2xl font-bold">Loading...</h1></Layout>;
  }

  const { listFields, fields, searchFields } = dataObject;

  return (
    <Layout>
      <div className="text-left">
        <h1 className="text-2xl font-bold text-center">
          List View for {dataObjectTypeSlug}
        </h1>
        <p>This is a list view of {dataObjectTypeSlug} data objects.</p>

        {/* Add Button using ButtonWidget */}
        <div className="flex justify-between mb-4">
          <div></div> {/* Empty div for left alignment */}
          <ButtonWidget 
            name="add-button"
            field={{
              name: "add-button",
              type: "button",
              label: "Add",
              required: false
            }}
            value={null}
            onChange={() => router.push(`/admin/${dataObjectTypeSlug}/add`)}
          />
        </div>

        {/* Search Filters */}
        <div className="mb-4">
          {searchFields.map((field: string) => {
            const fieldInfo = fields.find((f: any) => f.name === field);
            if (field === "*TEXT*") {
              return (
                <Widget
                  key={field}
                  type="input"
                  name="global-search"
                  field={{
                    name: "global-search",
                    type: "text",
                    label: "Global Search",
                    required: false
                  }}
                  value={searchQueries["*TEXT*"] || ''}
                  onChange={(e) => handleInputChange("*TEXT*", e)}
                />
              );
            } else {
              return (
                <Widget
                  key={field}
                  type={fieldInfo.type}
                  name={`search-${field}`}
                  field={{
                    ...fieldInfo,
                    name: `search-${field}`,
                    required: false, // Search fields are never required
                    label: `Search ${fieldInfo.label || field}`
                  }}
                  value={searchQueries[field] || ''}
                  onChange={(e) => handleInputChange(field, e)}
                />
              );
            }
          })}
          <ButtonWidget
            name="search-button"
            field={{
              name: "search-button",
              type: "button",
              label: "Search",
              required: false
            }}
            value={null}
            onChange={handleSearch}
          />
        </div>

        <table className="min-w-full border-collapse border border-gray-200">
          <thead>
            <tr>
              {listFields.map((field: string) => (
                <th key={field} className="border border-gray-300 px-4 py-2">
                  {fields.find((f: any) => f.name === field)?.label || field}
                </th>
              ))}
              <th className="border border-gray-300 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(filteredData) && filteredData.length > 0 ? (
              filteredData.map((record: any, index: number) => (
                <tr key={index}>
                  {listFields.map((field: string) => (
                    <td key={field} className="border border-gray-300 px-4 py-2">
                      {record[field]}
                    </td>
                  ))}
                  <td className="border border-gray-300 px-4 py-2">
                    <button 
                      onClick={() => router.push(`/admin/${dataObjectTypeSlug}/edit/${record.id}`)} 
                      className="text-blue-500 hover:underline"
                    >
                      Edit
                    </button>
                    <button 
                      onClick={() => handleDelete(record.id)} 
                      className="text-red-500 hover:underline ml-2"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={listFields.length + 1} className="border border-gray-300 px-4 py-2 text-center">
                  No records found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </Layout>
  );
};

// Function to handle delete action
const handleDelete = async (id: string) => {
  if (confirm("Are you sure you want to delete this record?")) {
    try {
      const response = await fetch(`${App.config.backendUrl}/api/users/${id}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        // Optionally, refresh the data or redirect after deletion
        window.location.reload();
      } else {
        alert('Failed to delete the record.');
      }
    } catch (error) {
      alert('An error occurred while deleting the record.');
    }
  }
};

export default ListView; 