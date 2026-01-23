export default defineNuxtConfig({
  modules: [
    '@nuxt/ui',
    '@pinia/nuxt',
  ],

  // Nuxt UI configuration
  ui: {
    icons: ['heroicons', 'mdi'],
  },

  // Pinia Store Configuration
  pinia: {
    storesDirs: ['./stores/**'],
  },

  // Environment variables
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
      apiTimeout: 30000,
    },
  },

  // Build configuration
  build: {
    transpile: ['@headlessui/vue'],
  },

  // CSS global imports
  css: [
    '~/assets/css/main.css',
  ],

  // App configuration
  app: {
    head: {
      title: 'Horilla HR Management',
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      meta: [
        {
          name: 'description',
          content: 'Comprehensive HR Management System',
        },
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      ],
    },
  },

  // Middleware configuration
  ssr: true,

  // TypeScript
  typescript: {
    strict: true,
    typeCheck: false,
  },

  // Development server
  devServer: {
    port: 3000,
  },

  // Nitro configuration for API routes
  nitro: {
    prerender: {
      crawlLinks: false,
      routes: [],
    },
  },
})
