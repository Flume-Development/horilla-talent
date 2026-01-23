import { apiClient } from '~/utils/api-client'
import { usePmsStore } from '~/stores/pms'
import { DashboardStats } from '~/types/pms'

/**
 * Core PMS composable for dashboard and general operations
 */
export const usePms = () => {
  const pmsStore = usePmsStore()

  /**
   * Fetch dashboard statistics
   */
  const fetchDashboardStats = async (): Promise<DashboardStats | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const stats = await apiClient.get<DashboardStats>('/pms/dashboard/stats/')
      pmsStore.setDashboardStats(stats)
      return stats
    } catch (error: any) {
      const message = error.message || 'Failed to fetch dashboard statistics'
      pmsStore.setError(message)
      console.error('Error fetching dashboard stats:', error)
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Get status color based on status value
   */
  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'On Track':
        return 'green'
      case 'Behind':
        return 'yellow'
      case 'At Risk':
        return 'red'
      case 'Closed':
        return 'gray'
      case 'Not Started':
        return 'blue'
      default:
        return 'gray'
    }
  }

  /**
   * Calculate progress percentage
   */
  const calculateProgress = (current: number, target: number): number => {
    if (target === 0) return 0
    return Math.round((current / target) * 100)
  }

  /**
   * Format date to readable format
   */
  const formatDate = (dateString: string): string => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  /**
   * Check if date range is active
   */
  const isDateRangeActive = (startDate: string, endDate: string): boolean => {
    const now = new Date()
    const start = new Date(startDate)
    const end = new Date(endDate)
    return now >= start && now <= end
  }

  /**
   * Get days remaining
   */
  const getDaysRemaining = (endDate: string): number => {
    const now = new Date()
    const end = new Date(endDate)
    const diffTime = end.getTime() - now.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    return Math.max(0, diffDays)
  }

  return {
    fetchDashboardStats,
    getStatusColor,
    calculateProgress,
    formatDate,
    isDateRangeActive,
    getDaysRemaining,
  }
}
