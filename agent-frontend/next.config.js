/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Remove Next.js watermark
  devIndicators: {
    buildActivity: false,
    buildActivityPosition: 'bottom-right',
  },
}

module.exports = nextConfig 