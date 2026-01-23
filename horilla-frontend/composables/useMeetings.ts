import { apiClient } from '~/utils/api-client'
import { usePmsStore } from '~/stores/pms'
import { Meetings, MeetingsAnswer } from '~/types/pms'

/**
 * Composable for meetings management
 */
export const useMeetings = () => {
  const pmsStore = usePmsStore()

  /**
   * Fetch all meetings
   */
  const fetchMeetings = async (filters?: any): Promise<Meetings[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const config = filters ? { params: filters } : {}
      const response = await apiClient.get<any>('/pms/meetings/', config)
      const meetings = response.results || response
      pmsStore.setMeetings(meetings)
      return meetings
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch meetings')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Fetch single meeting
   */
  const fetchMeeting = async (id: number): Promise<Meetings | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const meeting = await apiClient.get<Meetings>(`/pms/meetings/${id}/`)
      pmsStore.setSelectedMeeting(meeting)
      return meeting
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch meeting')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Create meeting
   */
  const createMeeting = async (data: any): Promise<Meetings | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const meeting = await apiClient.post<Meetings>('/pms/meetings/', data)
      pmsStore.addMeeting(meeting)
      return meeting
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to create meeting')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Update meeting
   */
  const updateMeeting = async (id: number, data: any): Promise<Meetings | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const meeting = await apiClient.put<Meetings>(`/pms/meetings/${id}/`, data)
      pmsStore.updateMeeting(id, meeting)
      return meeting
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to update meeting')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Delete meeting
   */
  const deleteMeeting = async (id: number): Promise<boolean> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      await apiClient.delete(`/pms/meetings/${id}/`)
      pmsStore.removeMeeting(id)
      return true
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to delete meeting')
      return false
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Submit meeting answers
   */
  const submitMeetingAnswers = async (
    meetingId: number,
    answers: any[]
  ): Promise<boolean> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      await apiClient.post(`/pms/meetings/${meetingId}/submit-answers/`, {
        answers,
      })
      return true
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to submit answers')
      return false
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Fetch meeting answers
   */
  const fetchMeetingAnswers = async (meetingId: number): Promise<MeetingsAnswer[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const answers = await apiClient.get<MeetingsAnswer[]>(
        `/pms/meetings/${meetingId}/answers/`
      )
      return answers
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch answers')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  return {
    fetchMeetings,
    fetchMeeting,
    createMeeting,
    updateMeeting,
    deleteMeeting,
    submitMeetingAnswers,
    fetchMeetingAnswers,
  }
}
