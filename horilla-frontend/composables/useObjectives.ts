import { apiClient } from '~/utils/api-client'
import { usePmsStore } from '~/stores/pms'
import {
  Objective,
  EmployeeObjective,
  EmployeeKeyResult,
  Period,
  KeyResult,
} from '~/types/pms'

/**
 * Composable for objectives management
 */
export const useObjectives = () => {
  const pmsStore = usePmsStore()

  /**
   * Fetch all periods
   */
  const fetchPeriods = async (): Promise<Period[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const periods = await apiClient.get<Period[]>('/pms/periods/')
      pmsStore.setPeriods(periods)
      return periods
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch periods')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Fetch all key results
   */
  const fetchKeyResults = async (): Promise<KeyResult[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const response = await apiClient.get<any>('/pms/key-results/')
      return response.results || response
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch key results')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Fetch all objectives
   */
  const fetchObjectives = async (filters?: any): Promise<Objective[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const config = filters ? { params: filters } : {}
      const response = await apiClient.get<any>('/pms/objectives/', config)
      const objectives = response.results || response
      pmsStore.setObjectives(objectives)
      return objectives
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch objectives')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Fetch single objective
   */
  const fetchObjective = async (id: number): Promise<Objective | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const objective = await apiClient.get<Objective>(`/pms/objectives/${id}/`)
      pmsStore.setSelectedObjective(objective)
      return objective
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch objective')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Create new objective
   */
  const createObjective = async (data: any): Promise<Objective | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const objective = await apiClient.post<Objective>('/pms/objectives/', data)
      pmsStore.addObjective(objective)
      return objective
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to create objective')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Update objective
   */
  const updateObjective = async (
    id: number,
    data: any
  ): Promise<Objective | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const objective = await apiClient.put<Objective>(
        `/pms/objectives/${id}/`,
        data
      )
      pmsStore.updateObjective(id, objective)
      return objective
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to update objective')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Delete objective
   */
  const deleteObjective = async (id: number): Promise<boolean> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      await apiClient.delete(`/pms/objectives/${id}/`)
      pmsStore.removeObjective(id)
      return true
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to delete objective')
      return false
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Archive objective
   */
  const archiveObjective = async (id: number): Promise<Objective | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const objective = await apiClient.post<Objective>(
        `/pms/objectives/${id}/archive/`,
        {}
      )
      pmsStore.updateObjective(id, objective)
      return objective
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to archive objective')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Fetch employee objectives
   */
  const fetchEmployeeObjectives = async (filters?: any): Promise<EmployeeObjective[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const config = filters ? { params: filters } : {}
      const response = await apiClient.get<any>('/pms/employee-objectives/', config)
      const empObjectives = response.results || response
      pmsStore.setEmployeeObjectives(empObjectives)
      return empObjectives
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch employee objectives')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Fetch single employee objective
   */
  const fetchEmployeeObjective = async (
    id: number
  ): Promise<EmployeeObjective | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const empObjective = await apiClient.get<EmployeeObjective>(
        `/pms/employee-objectives/${id}/`
      )
      return empObjective
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch employee objective')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Create employee objective
   */
  const createEmployeeObjective = async (data: any): Promise<EmployeeObjective | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const empObjective = await apiClient.post<EmployeeObjective>(
        '/pms/employee-objectives/',
        data
      )
      pmsStore.addEmployeeObjective(empObjective)
      return empObjective
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to create employee objective')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Update employee objective
   */
  const updateEmployeeObjective = async (
    id: number,
    data: any
  ): Promise<EmployeeObjective | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const empObjective = await apiClient.put<EmployeeObjective>(
        `/pms/employee-objectives/${id}/`,
        data
      )
      pmsStore.updateEmployeeObjective(id, empObjective)
      return empObjective
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to update employee objective')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Update employee objective status
   */
  const updateEmployeeObjectiveStatus = async (
    id: number,
    status: string
  ): Promise<EmployeeObjective | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const empObjective = await apiClient.post<EmployeeObjective>(
        `/pms/employee-objectives/${id}/status/`,
        { status }
      )
      pmsStore.updateEmployeeObjective(id, empObjective)
      return empObjective
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to update status')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Delete employee objective
   */
  const deleteEmployeeObjective = async (id: number): Promise<boolean> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      await apiClient.delete(`/pms/employee-objectives/${id}/`)
      pmsStore.removeEmployeeObjective(id)
      return true
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to delete employee objective')
      return false
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Fetch employee key results
   */
  const fetchEmployeeKeyResults = async (filters?: any): Promise<EmployeeKeyResult[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const config = filters ? { params: filters } : {}
      const response = await apiClient.get<any>('/pms/employee-key-results/', config)
      return response.results || response
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch key results')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Update employee key result progress
   */
  const updateKeyResultProgress = async (
    id: number,
    currentValue: number
  ): Promise<EmployeeKeyResult | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const kr = await apiClient.post<EmployeeKeyResult>(
        `/pms/employee-key-results/${id}/progress/`,
        { current_value: currentValue }
      )
      return kr
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to update progress')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  return {
    fetchPeriods,
    fetchKeyResults,
    fetchObjectives,
    fetchObjective,
    createObjective,
    updateObjective,
    deleteObjective,
    archiveObjective,
    fetchEmployeeObjectives,
    fetchEmployeeObjective,
    createEmployeeObjective,
    updateEmployeeObjective,
    updateEmployeeObjectiveStatus,
    deleteEmployeeObjective,
    fetchEmployeeKeyResults,
    updateKeyResultProgress,
  }
}
