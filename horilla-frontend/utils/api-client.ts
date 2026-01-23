import axios, { AxiosInstance, AxiosRequestConfig, AxiosError } from 'axios'
import { useAuthStore } from '~/stores/auth'

export interface ApiResponse<T = any> {
  data: T
  status: number
  message?: string
}

export interface ApiErrorResponse {
  detail?: string
  message?: string
  [key: string]: any
}

class APIClient {
  private client: AxiosInstance | null = null
  private config: { apiBaseUrl: string; apiTimeout: number } | null = null

  private initializeClient() {
    if (this.client) return

    try {
      const nuxtConfig = useRuntimeConfig()
      this.config = {
        apiBaseUrl: nuxtConfig.public.apiBaseUrl || 'http://localhost:8000',
        apiTimeout: nuxtConfig.public.apiTimeout || 30000,
      }

      this.client = axios.create({
        baseURL: `${this.config.apiBaseUrl}/api`,
        timeout: this.config.apiTimeout,
        headers: {
          'Content-Type': 'application/json',
        },
      })

      this.setupInterceptors()
    } catch (error) {
      // Fallback for build time or ssr context
      this.config = {
        apiBaseUrl: 'http://localhost:8000',
        apiTimeout: 30000,
      }
      this.client = axios.create({
        baseURL: `${this.config.apiBaseUrl}/api`,
        timeout: this.config.apiTimeout,
        headers: {
          'Content-Type': 'application/json',
        },
      })
      this.setupInterceptors()
    }
  }

  private setupInterceptors() {
    if (!this.client) return

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        const authStore = useAuthStore()
        const token = authStore.accessToken

        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }

        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        return response.data
      },
      async (error: AxiosError<ApiErrorResponse>) => {
        const authStore = useAuthStore()

        // Handle 401 Unauthorized
        if (error.response?.status === 401) {
          // Try to refresh token
          if (authStore.refreshToken) {
            try {
              await authStore.refreshAccessToken()
              // Retry the original request
              return this.client!.request(error.config!)
            } catch (refreshError) {
              authStore.logout()
              await navigateTo('/login')
            }
          } else {
            authStore.logout()
            await navigateTo('/login')
          }
        }

        // Handle 403 Forbidden
        if (error.response?.status === 403) {
          const message =
            error.response.data?.detail ||
            error.response.data?.message ||
            'Access Forbidden'
          throw new Error(message)
        }

        // Handle 404 Not Found
        if (error.response?.status === 404) {
          const message = 'Resource not found'
          throw new Error(message)
        }

        // Handle 500 Server Error
        if (error.response?.status === 500) {
          const message = 'Internal server error'
          throw new Error(message)
        }

        // Generic error handling
        const errorMessage =
          error.response?.data?.detail ||
          error.response?.data?.message ||
          error.message ||
          'An error occurred'

        throw new Error(errorMessage)
      }
    )
  }

  /**
   * GET request
   */
  async get<T = any>(
    url: string,
    config?: AxiosRequestConfig
  ): Promise<T> {
    this.initializeClient()
    return this.client!.get<any, T>(url, config)
  }

  /**
   * POST request
   */
  async post<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    this.initializeClient()
    return this.client!.post<any, T>(url, data, config)
  }

  /**
   * PUT request
   */
  async put<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    this.initializeClient()
    return this.client!.put<any, T>(url, data, config)
  }

  /**
   * PATCH request
   */
  async patch<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    this.initializeClient()
    return this.client!.patch<any, T>(url, data, config)
  }

  /**
   * DELETE request
   */
  async delete<T = any>(
    url: string,
    config?: AxiosRequestConfig
  ): Promise<T> {
    this.initializeClient()
    return this.client!.delete<any, T>(url, config)
  }

  /**
   * Get the axios instance directly
   */
  getInstance(): AxiosInstance {
    this.initializeClient()
    return this.client!
  }

  /**
   * Get the API base URL
   */
  getBaseUrl(): string {
    this.initializeClient()
    return this.config!.apiBaseUrl
  }
}

// Export singleton instance
export const apiClient = new APIClient()
