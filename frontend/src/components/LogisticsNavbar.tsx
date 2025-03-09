"use client";

import Link from "next/link";

export default function LogisticsNavbar() {
  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="text-2xl font-bold text-black">
            Bookworm
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center space-x-12">
            <Link
              href="/logistics/upload"
              className="text-base font-medium text-black hover:text-gray-600"
            >
              Upload
            </Link>
            <Link
              href="/logistics/orders"
              className="text-base font-medium text-black hover:text-gray-600"
            >
              Orders
            </Link>
          </div>

          {/* Right side */}
          <div className="flex items-center space-x-6">
            <Link
              href="/logistics/notifications"
              className="text-black hover:text-gray-600 relative"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="w-6 h-6"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"
                />
              </svg>
            </Link>
            <button className="bg-black text-white px-4 py-2 rounded-lg hover:bg-gray-800">
              Admin
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
