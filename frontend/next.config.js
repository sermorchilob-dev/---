/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://sermorchilob-dev--1365.twc1.net/api/:path*',
      },
    ];
  },
  output: "standalone",
};

module.exports = nextConfig;