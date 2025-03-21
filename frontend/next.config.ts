import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: process.env.NEXT_PUBLIC_BACKEND_URL?.split("//")[1].split(":")[0] ?? 'localhost',
        port: process.env.NEXT_PUBLIC_BACKEND_URL?.split(':')[2] ?? '8000',
        pathname: '/static/**',
        search: '',
      },
      {
        protocol: 'http',
        hostname: '127.0.0.1',
        port: '8000',
        pathname: '/static/**',
        search: '',
      },
    ],
  },
  output: 'export',
  /* config options here */
};

export default nextConfig;
