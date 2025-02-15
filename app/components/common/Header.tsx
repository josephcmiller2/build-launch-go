import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import App from '../../pages/_app';

interface HeaderProps {
  title?: string;
}

const Header: React.FC<HeaderProps> = ({ title = 'Build Launch Go' }) => {
  const router = useRouter();
  const [dataObjects, setDataObjects] = useState<any[]>([]);
  const masterDocumentUri = App.config.backendUrl + '/api/master';

  useEffect(() => {
    const fetchMasterDocument = async () => {
      try {
        const response = await fetch(masterDocumentUri);
        if (!response.ok) {
          throw new Error('Failed to fetch master document');
        }
        const data = await response.json();
        setDataObjects(data.data_objects);
      } catch (error) {
        console.error('Error fetching master document:', error);
      }
    };

    fetchMasterDocument();
  }, [masterDocumentUri]);

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo/Home Link */}
          <div className="flex-shrink-0 flex items-center">
            <Link href="/" className="text-xl font-bold text-gray-800">
              {title}
            </Link>
          </div>

          {/* Navigation */}
          <nav className="flex space-x-4 items-center">
            <Link 
              href="/"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                router.pathname === '/' 
                  ? 'bg-gray-100 text-gray-900' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Home
            </Link>
            {dataObjects.map((dataObject) => (
              <Link 
                key={dataObject.id}
                href={`/${dataObject.id}/list`}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  router.pathname === `/${dataObject.id}/list` 
                    ? 'bg-gray-100 text-gray-900' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {dataObject.name}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
