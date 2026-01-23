export default defineRouteMiddleware(async (to, from) => {
  if (typeof window === 'undefined') {
    // Skip middleware on server-side
    return
  }

  const authStore = useAuthStore()

  // Initialize auth from storage
  if (!authStore.isAuthenticated) {
    authStore.initializeAuth()
  }

  // List of routes that don't require authentication
  const publicRoutes = ['/login']

  // Check if current route requires authentication
  const isPublicRoute = publicRoutes.includes(to.path)

  if (!authStore.isAuthenticated && !isPublicRoute) {
    // Redirect to login if not authenticated
    return navigateTo('/login')
  }

  if (authStore.isAuthenticated && to.path === '/login') {
    // Redirect to dashboard if already authenticated
    return navigateTo('/pms')
  }
})
