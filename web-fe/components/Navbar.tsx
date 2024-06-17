// components/Navbar.tsx

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const Navbar: React.FC = () => {
  const pathname = usePathname();

  return (
    <nav className="bg-gray-800 p-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex space-x-4">
          <Link href="/">
            <p className={`text-white ${pathname === '/' ? 'underline' : ''}`}>
              Home
            </p>
          </Link>
          <Link href="/scan">
            <p className={`text-white ${pathname === '/scan' ? 'underline' : ''}`}>
              Scan
            </p>
          </Link>
          <Link href="/scan-results">
            <p className={`text-white ${pathname === '/scan-results' ? 'underline' : ''}`}>
              Scan Result
            </p>
          </Link>
          {/* Add more links as needed */}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
