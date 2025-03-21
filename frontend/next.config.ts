import type { NextConfig } from "next";

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: backendUrl?.split("//")[1].split(":")[0] ?? 'localhost',
        port: backendUrl?.split(':')[2].split('/')[0] ?? '8000',
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
  }  /* config options here */
};

export default nextConfig;
