/** @type {import('next').NextConfig} */
const nextConfig = {
  basePath: process.env.NODE_ENV === 'production' ? '/ElevateU' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/ElevateU' : '',
  reactStrictMode: true,
}

module.exports = nextConfig
