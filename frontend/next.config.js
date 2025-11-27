/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  basePath: process.env.NODE_ENV === 'production' ? '/ElevateU' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/ElevateU' : '',
  output: 'export',
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
