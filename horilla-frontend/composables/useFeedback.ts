import { apiClient } from '~/utils/api-client'
import { usePmsStore } from '~/stores/pms'
import {
  Feedback,
  QuestionTemplate,
  Question,
  Answer,
  AnonymousFeedback,
} from '~/types/pms'

/**
 * Composable for feedback management
 */
export const useFeedback = () => {
  const pmsStore = usePmsStore()

  /**
   * Fetch question templates
   */
  const fetchQuestionTemplates = async (): Promise<QuestionTemplate[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const response = await apiClient.get<any>('/pms/question-templates/')
      return response.results || response
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch question templates')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Create question template
   */
  const createQuestionTemplate = async (data: any): Promise<QuestionTemplate | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const template = await apiClient.post<QuestionTemplate>(
        '/pms/question-templates/',
        data
      )
      return template
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to create template')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Fetch questions for template
   */
  const fetchQuestions = async (templateId: number): Promise<Question[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const questions = await apiClient.get<Question[]>('/pms/questions/', {
        params: { template_id: templateId },
      })
      return questions
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch questions')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Create question
   */
  const createQuestion = async (data: any): Promise<Question | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const question = await apiClient.post<Question>('/pms/questions/', data)
      return question
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to create question')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Fetch all feedback cycles
   */
  const fetchFeedbackList = async (filters?: any): Promise<Feedback[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const config = filters ? { params: filters } : {}
      const response = await apiClient.get<any>('/pms/feedback/', config)
      const feedbacks = response.results || response
      pmsStore.setFeedback(feedbacks)
      return feedbacks
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch feedback')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Fetch single feedback
   */
  const fetchFeedback = async (id: number): Promise<Feedback | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const feedback = await apiClient.get<Feedback>(`/pms/feedback/${id}/`)
      pmsStore.setSelectedFeedback(feedback)
      return feedback
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch feedback')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Create feedback
   */
  const createFeedback = async (data: any): Promise<Feedback | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const feedback = await apiClient.post<Feedback>('/pms/feedback/', data)
      pmsStore.addFeedback(feedback)
      return feedback
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to create feedback')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Update feedback
   */
  const updateFeedback = async (id: number, data: any): Promise<Feedback | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const feedback = await apiClient.put<Feedback>(`/pms/feedback/${id}/`, data)
      pmsStore.updateFeedback(id, feedback)
      return feedback
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to update feedback')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Delete feedback
   */
  const deleteFeedback = async (id: number): Promise<boolean> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      await apiClient.delete(`/pms/feedback/${id}/`)
      pmsStore.removeFeedback(id)
      return true
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to delete feedback')
      return false
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Archive feedback
   */
  const archiveFeedback = async (id: number): Promise<Feedback | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const feedback = await apiClient.post<Feedback>(
        `/pms/feedback/${id}/archive/`,
        {}
      )
      pmsStore.updateFeedback(id, feedback)
      return feedback
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to archive feedback')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Submit feedback answers
   */
  const submitFeedbackAnswers = async (
    feedbackId: number,
    answers: any[]
  ): Promise<boolean> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      await apiClient.post(`/pms/feedback/${feedbackId}/submit-answers/`, {
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
   * Fetch feedback answers
   */
  const fetchFeedbackAnswers = async (feedbackId: number): Promise<Answer[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const answers = await apiClient.get<Answer[]>(
        `/pms/feedback/${feedbackId}/answers/`
      )
      return answers
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch answers')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Fetch anonymous feedback
   */
  const fetchAnonymousFeedback = async (filters?: any): Promise<AnonymousFeedback[]> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const config = filters ? { params: filters } : {}
      const response = await apiClient.get<any>('/pms/anonymous-feedback/', config)
      return response.results || response
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to fetch anonymous feedback')
      return []
    } finally {
      pmsStore.setLoading(false)
    }
  }

  /**
   * Create anonymous feedback
   */
  const createAnonymousFeedback = async (data: any): Promise<AnonymousFeedback | null> => {
    try {
      pmsStore.setLoading(true)
      pmsStore.clearError()

      const feedback = await apiClient.post<AnonymousFeedback>(
        '/pms/anonymous-feedback/',
        data
      )
      return feedback
    } catch (error: any) {
      pmsStore.setError(error.message || 'Failed to create feedback')
      return null
    } finally {
      pmsStore.setLoading(false)
    }
  }

  return {
    fetchQuestionTemplates,
    createQuestionTemplate,
    fetchQuestions,
    createQuestion,
    fetchFeedbackList,
    fetchFeedback,
    createFeedback,
    updateFeedback,
    deleteFeedback,
    archiveFeedback,
    submitFeedbackAnswers,
    fetchFeedbackAnswers,
    fetchAnonymousFeedback,
    createAnonymousFeedback,
  }
}
