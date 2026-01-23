import { apiClient } from '~/utils/api-client'
import { usePmsStore } from '~/stores/pms'

/**
 * Composable for bonus management
 */
export const useBonus = () => {
  const pmsStore = usePmsStore()

  /**
   * Fetch bonus settings
   */
  const fetchBonusSettings = async (filters?: any): Promise<any[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const config = filters ? { params: filters } : {}
      const response = await apiClient.get<any>('/pms/bonus-settings/', config)
      return response.results || response
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch bonus settings')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Create bonus setting
   */
  const createBonusSetting = async (data: any): Promise<any | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const setting = await apiClient.post<any>('/pms/bonus-settings/', data)
      return setting
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to create bonus setting')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Fetch employee bonus points
   */
  const fetchEmployeeBonusPoints = async (filters?: any): Promise<any[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const config = filters ? { params: filters } : {}
      const response = await apiClient.get<any>('/pms/employee-bonus-points/', config)
      return response.results || response
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch bonus points')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Award bonus points
   */
  const awardBonusPoints = async (data: any): Promise<any | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const points = await apiClient.post<any>(
        '/pms/employee-bonus-points/',
        data
      )
      return points
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to award bonus points')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Update bonus points
   */
  const updateBonusPoints = async (
    id: number,
    data: any
  ): Promise<any | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const points = await apiClient.put<any>(
        `/pms/employee-bonus-points/${id}/`,
        data
      )
      return points
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to update bonus points')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Delete bonus points
   */
  const deleteBonusPoints = async (id: number): Promise<boolean> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      await apiClient.delete(`/pms/employee-bonus-points/${id}/`)
      return true
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to delete bonus points')
      return false
    } finally {
      pmsStore.setLoading(false)
    }
  }

  return {
    fetchBonusSettings,
    createBonusSetting,
    fetchEmployeeBonusPoints,
    awardBonusPoints,
    updateBonusPoints,
    deleteBonusPoints,
  }
}
