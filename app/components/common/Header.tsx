import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

interface HeaderProps {
  title?: string;
}

const Header: React.FC<HeaderProps> = ({ title = 'Build Launch Go' }) => {
  const router = useRouter();

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
            {/* Additional navigation items will be dynamically generated based on the master document */}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
