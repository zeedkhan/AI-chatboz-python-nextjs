/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ["lh3.googleusercontent.com", "vercel.com"],
  },
  webpack: (config, context) => {
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300
    }
    return config
  },
  experimental: {
    serverActions: true,
  },
  async redirects() {
    return [
      {
        source: '/api-v2/refresh-token/',
        destination: 'http://localhost:8000/refresh-token/',
        permanent: true,
        basePath: false
      },
    ]
  },

};

module.exports = nextConfig;