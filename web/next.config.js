/** @type {import('next').NextConfig} */
const nextConfig = {
  rewrites: async () => {
    // In production, something else (nginx in the one box setup) should take
    // care of this rewrite. TODO: better support setups where
    // web_server and api_server are on different machines.
    return [
      {
        source: "/:path*",
        destination:
          process.env.NODE_ENV === "development" && !process.env.BACK_URL
            ? "http://127.0.0.1:8000/:path*"
            : `${process.env.BACK_URL}/:path*`,
      },
      {
        source: "/docs",
        destination:
          process.env.NODE_ENV === "development" && !process.env.BACK_URL
            ? "http://127.0.0.1:8000/docs"
            : `${process.env.BACK_URL}/docs`,
      },
      {
        source: "/openapi.json",
        destination:
          process.env.NODE_ENV === "development" && !process.env.BACK_URL
            ? "http://127.0.0.1:8000/openapi.json"
            : `${process.env.BACK_URL}/openapi.json`,
      },
    ];
  },
};

module.exports = nextConfig;
