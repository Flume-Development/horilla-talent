import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin(() => {
  const authStore = useAuthStore()

  // Initialize auth on app load
  if (process.client) {
    authStore.initializeAuth()
  }
})
