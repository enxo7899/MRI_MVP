/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  
  // Environment variables
  env: {
    NEXT_PUBLIC_PACS_URL: process.env.NEXT_PUBLIC_PACS_URL || '/pacs',
    NEXT_PUBLIC_VIEWER_URL: process.env.NEXT_PUBLIC_VIEWER_URL || '/viewer',
    NEXT_PUBLIC_MONAI_URL: process.env.NEXT_PUBLIC_MONAI_URL || '/monai',
  },

  // Rewrites for development
  async rewrites() {
    return [
      {
        source: '/pacs/:path*',
        destination: 'http://localhost:8042/:path*',
      },
      {
        source: '/monai/:path*',
        destination: 'http://localhost:8000/:path*',
      },
    ];
  },

  // Headers for CORS
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Cross-Origin-Opener-Policy',
            value: 'same-origin',
          },
          {
            key: 'Cross-Origin-Embedder-Policy',
            value: 'require-corp',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
