/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Remove all development indicators/watermarks
  devIndicators: {
    buildActivity: false,
    buildActivityPosition: false,
  },
  // Disable powered by header
  poweredByHeader: false,
}

module.exports = nextConfig 