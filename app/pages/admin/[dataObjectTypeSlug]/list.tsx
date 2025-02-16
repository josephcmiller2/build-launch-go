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

  return (
    <Layout>
      <div className="text-center">
        <h1 className="text-2xl font-bold">
          List View for {dataObjectTypeSlug}
        </h1>
        <p>This is a stub page for the list view of {dataObjectTypeSlug} data objects.</p>
        {/* Render the data object details here if needed */}
      </div>
    </Layout>
  );
};

export default ListView; 