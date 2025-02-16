import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../../../components/common/Layout';
import App from '../../_app'; // Adjust the import path as necessary

const ListView: React.FC = () => {
  const router = useRouter();
  const { dataObjectTypeSlug } = router.query;
  const [dataObject, setDataObject] = useState<any>(null);
  const [error, setError] = useState<boolean>(false);

  useEffect(() => {
    if (dataObjectTypeSlug) {
      const fetchDataObject = async () => {
        try {
          const response = await fetch(`${App.config.backendUrl}/api/object/${dataObjectTypeSlug}`);
          if (!response.ok) {
            throw new Error('Failed to fetch data object');
          }
          const data = await response.json();
          setDataObject(data);
        } catch (error) {
          setError(true);
        }
      };

      fetchDataObject();
    }
  }, [dataObjectTypeSlug]);

  if (error) {
    return <Layout><h1 className="text-2xl font-bold">404 - Data Object Not Found</h1></Layout>;
  }

  if (!dataObject) {
    return <Layout><h1 className="text-2xl font-bold">Loading...</h1></Layout>;
  }

  const { listFields, fields } = dataObject;

  return (
    <Layout>
      <div className="text-center">
        <h1 className="text-2xl font-bold">
          List View for {dataObjectTypeSlug}
        </h1>
        <p>This is a list view of {dataObjectTypeSlug} data objects.</p>
        <table className="min-w-full border-collapse border border-gray-200">
          <thead>
            <tr>
              {listFields.map((field: string) => (
                <th key={field} className="border border-gray-300 px-4 py-2">
                  {fields.find((f: any) => f.name === field)?.label || field}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {/* Check if dataObject.data is an array before mapping */}
            {Array.isArray(dataObject.data) && dataObject.data.length > 0 ? (
              dataObject.data.map((record: any, index: number) => (
                <tr key={index}>
                  {listFields.map((field: string) => (
                    <td key={field} className="border border-gray-300 px-4 py-2">
                      {record[field]}
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={listFields.length} className="border border-gray-300 px-4 py-2 text-center">
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

export default ListView; 