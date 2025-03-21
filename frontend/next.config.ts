import type { NextConfig } from "next";

console.log(process.env.NEXT_PUBLIC_BACKEND_URL?.split("//")[1].split(":")[0]);

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      // {
      //   protocol: 'http',
      //   hostname: process.env.NEXT_PUBLIC_BACKEND_URL?.split("//")[1].split(":")[0].split("/")[0] ?? 'localhost',
      //   port: process.env.NEXT_PUBLIC_BACKEND_PORT,
      //   pathname: '/static/**',
      //   search: '',
      // },
      {
        protocol: 'https',
        hostname: 'genies-9ibi.onrender.com',
        port: '',
        pathname: '/api/static/**',
      },
      // {
      //   protocol: 'http',
      //   hostname: '127.0.0.1',
      //   port: '8000',
      //   pathname: '/static/**',
      //   search: '',
      // },
    ],
  }  /* config options here */
};

export default nextConfig;
