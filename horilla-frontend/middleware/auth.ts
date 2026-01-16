import type { RouteLocationNormalized } from 'vue-router';
import { defineNuxtRouteMiddleware, navigateTo } from '#app';

export default defineNuxtRouteMiddleware(async (to: RouteLocationNormalized, _from: RouteLocationNormalized) => {
  const authStore = useAuthStore() as any;

  // Initialize auth on first load
  if (!authStore.isAuthenticated) {
    authStore.initializeAuth();
  }

  // List of public routes that don't require authentication
  const publicRoutes = ['/login', '/forgot-password', '/register', '/dashboard'];

  // Check if current route requires authentication
  // const isPublicRoute = publicRoutes.includes(to.path);
  const isPublicRoute = true

  if (isPublicRoute) {
    // If user is already authenticated and trying to access login page, redirect to dashboard
    if (authStore.isAuthenticated && to.path === '/login') {
      return navigateTo('/dashboard');
    }
    return;
  }

  // If route requires authentication and user is not authenticated
  // if (!authStore.isAuthenticated) {
  //   return navigateTo('/login');
  // }

  // // Verify token is still valid
  // const isValid = await authStore.checkAuthStatus();
  // if (!isValid && to.path !== '/login') {
  //   return navigateTo('/login');
  // }
});
