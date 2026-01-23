import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient } from '~/utils/api-client'
// @ts-ignore - js-cookie doesn't have full type definitions
import Cookie from 'js-cookie'

export interface Employee {
  id: number
  employee_first_name: string
  employee_last_name: string
  email: string
  phone?: string
  profile_image?: string
  company?: number
  [key: string]: any
}

export interface LoginResponse {
  access: string
  refresh: string
  employee: Employee
  face_detection?: boolean
  geo_fencing?: boolean
}

const STORAGE_KEYS = {
  ACCESS_TOKEN: 'auth:access_token',
  REFRESH_TOKEN: 'auth:refresh_token',
  EMPLOYEE: 'auth:employee',
}

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const employee = ref<Employee | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Computed properties
  const isAuthenticated = computed(() => !!accessToken.value)
  const employeeName = computed(
    () => `${employee.value?.employee_first_name} ${employee.value?.employee_last_name}` || 'User'
  )

  /**
   * Initialize auth state from localStorage
   */
  const initializeAuth = () => {
    if (typeof window !== 'undefined') {
      const storedAccessToken = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN)
      const storedRefreshToken = localStorage.getItem(
        STORAGE_KEYS.REFRESH_TOKEN
      )
      const storedEmployee = localStorage.getItem(STORAGE_KEYS.EMPLOYEE)

      if (storedAccessToken) {
        accessToken.value = storedAccessToken
      }
      if (storedRefreshToken) {
        refreshToken.value = storedRefreshToken
      }
      if (storedEmployee) {
        try {
          employee.value = JSON.parse(storedEmployee)
        } catch (e) {
          console.error('Failed to parse stored employee data')
        }
      }
    }
  }

  /**
   * Login with username and password
   */
  const login = async (
    username: string,
    password: string
  ): Promise<boolean> => {
    isLoading.value = true
    error.value = null

    try {
      const response = await apiClient.post<LoginResponse>('/auth/login/', {
        username,
        password,
      })

      // Store tokens and employee data
      accessToken.value = response.access
      refreshToken.value = response.refresh
      employee.value = response.employee

      // Persist to localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.access)
        localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, response.refresh)
        localStorage.setItem(
          STORAGE_KEYS.EMPLOYEE,
          JSON.stringify(response.employee)
        )
        // Also set cookie for SSR
        Cookie.set(STORAGE_KEYS.ACCESS_TOKEN, response.access, {
          expires: 7,
          secure: true,
          sameSite: 'lax',
        })
      }

      return true
    } catch (err: any) {
      error.value = err.message || 'Login failed'
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Refresh access token using refresh token
   */
  const refreshAccessToken = async (): Promise<boolean> => {
    if (!refreshToken.value) {
      return false
    }

    try {
      const response = await apiClient.post<{ access: string }>(
        '/auth/token/refresh/',
        {
          refresh: refreshToken.value,
        }
      )

      accessToken.value = response.access

      if (typeof window !== 'undefined') {
        localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.access)
        Cookie.set(STORAGE_KEYS.ACCESS_TOKEN, response.access, {
          expires: 7,
          secure: true,
          sameSite: 'lax',
        })
      }

      return true
    } catch (err) {
      console.error('Token refresh failed:', err)
      logout()
      return false
    }
  }

  /**
   * Check if user is still authenticated
   */
  const checkAuthStatus = async (): Promise<boolean> => {
    if (!accessToken.value) {
      return false
    }

    try {
      // Try to fetch current user info to verify token
      const response = await apiClient.get<{ employee: Employee }>(
        '/employee/employees/me/'
      )
      employee.value = response.employee
      return true
    } catch (err) {
      // Token might be expired, try to refresh
      if (refreshToken.value) {
        return await refreshAccessToken()
      }
      logout()
      return false
    }
  }

  /**
   * Logout and clear all auth data
   */
  const logout = () => {
    accessToken.value = null
    refreshToken.value = null
    employee.value = null
    error.value = null

    if (typeof window !== 'undefined') {
      localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN)
      localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN)
      localStorage.removeItem(STORAGE_KEYS.EMPLOYEE)
      Cookie.remove(STORAGE_KEYS.ACCESS_TOKEN)
    }
  }

  /**
   * Clear error state
   */
  const clearError = () => {
    error.value = null
  }

  return {
    // State
    accessToken,
    refreshToken,
    employee,
    isLoading,
    error,

    // Computed
    isAuthenticated,
    employeeName,

    // Methods
    initializeAuth,
    login,
    refreshAccessToken,
    checkAuthStatus,
    logout,
    clearError,
  }
})
