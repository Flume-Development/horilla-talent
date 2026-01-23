import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  Objective,
  EmployeeObjective,
  Feedback,
  Meetings,
  Period,
  DashboardStats,
} from '~/types/pms'

export const usePmsStore = defineStore('pms', () => {
  // State
  const currentPeriodId = ref<number | null>(null)
  const objectives = ref<Objective[]>([])
  const employeeObjectives = ref<EmployeeObjective[]>([])
  const feedbackList = ref<Feedback[]>([])
  const meetingsList = ref<Meetings[]>([])
  const periods = ref<Period[]>([])
  const dashboardStats = ref<DashboardStats | null>(null)

  const selectedObjective = ref<Objective | null>(null)
  const selectedFeedback = ref<Feedback | null>(null)
  const selectedMeeting = ref<Meetings | null>(null)

  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Filters
  const objectiveStatusFilter = ref<string | null>(null)
  const objectivePeriodFilter = ref<number | null>(null)
  const feedbackStatusFilter = ref<string | null>(null)

  // Computed
  const filteredObjectives = computed(() => {
    let result = objectives.value

    if (objectiveStatusFilter.value) {
      result = result.filter(obj => {
        const empObjective = employeeObjectives.value.find(eo => eo.objective_id.id === obj.id)
        return empObjective?.status === objectiveStatusFilter.value
      })
    }

    if (objectivePeriodFilter.value) {
      result = result.filter(obj => obj.company_id === objectivePeriodFilter.value)
    }

    return result
  })

  const filteredFeedback = computed(() => {
    let result = feedbackList.value

    if (feedbackStatusFilter.value) {
      result = result.filter(fb => fb.status === feedbackStatusFilter.value)
    }

    return result
  })

  const objectiveStats = computed(() => {
    const all = employeeObjectives.value
    return {
      total: all.length,
      onTrack: all.filter(o => o.status === 'On Track').length,
      behind: all.filter(o => o.status === 'Behind').length,
      atRisk: all.filter(o => o.status === 'At Risk').length,
      closed: all.filter(o => o.status === 'Closed').length,
      notStarted: all.filter(o => o.status === 'Not Started').length,
    }
  })

  const averageProgress = computed(() => {
    if (employeeObjectives.value.length === 0) return 0
    const total = employeeObjectives.value.reduce(
      (sum, obj) => sum + obj.progress_percentage,
      0
    )
    return Math.round(total / employeeObjectives.value.length)
  })

  // Methods
  const setCurrentPeriod = (periodId: number | null) => {
    currentPeriodId.value = periodId
  }

  const setPeriods = (data: Period[]) => {
    periods.value = data
  }

  const setObjectives = (data: Objective[]) => {
    objectives.value = data
  }

  const setEmployeeObjectives = (data: EmployeeObjective[]) => {
    employeeObjectives.value = data
  }

  const setFeedback = (data: Feedback[]) => {
    feedbackList.value = data
  }

  const setMeetings = (data: Meetings[]) => {
    meetingsList.value = data
  }

  const setDashboardStats = (data: DashboardStats) => {
    dashboardStats.value = data
  }

  const setSelectedObjective = (objective: Objective | null) => {
    selectedObjective.value = objective
  }

  const setSelectedFeedback = (feedback: Feedback | null) => {
    selectedFeedback.value = feedback
  }

  const setSelectedMeeting = (meeting: Meetings | null) => {
    selectedMeeting.value = meeting
  }

  const setLoading = (value: boolean) => {
    isLoading.value = value
  }

  const setError = (message: string | null) => {
    error.value = message
  }

  const clearError = () => {
    error.value = null
  }

  const addObjective = (objective: Objective) => {
    objectives.value.push(objective)
  }

  const updateObjective = (id: number, objective: Partial<Objective>) => {
    const index = objectives.value.findIndex(o => o.id === id)
    if (index !== -1) {
      objectives.value[index] = { ...objectives.value[index], ...objective }
    }
  }

  const removeObjective = (id: number) => {
    objectives.value = objectives.value.filter(o => o.id !== id)
  }

  const addEmployeeObjective = (empObjective: EmployeeObjective) => {
    employeeObjectives.value.push(empObjective)
  }

  const updateEmployeeObjective = (id: number, empObjective: Partial<EmployeeObjective>) => {
    const index = employeeObjectives.value.findIndex(eo => eo.id === id)
    if (index !== -1) {
      employeeObjectives.value[index] = {
        ...employeeObjectives.value[index],
        ...empObjective,
      }
    }
  }

  const removeEmployeeObjective = (id: number) => {
    employeeObjectives.value = employeeObjectives.value.filter(eo => eo.id !== id)
  }

  const addFeedback = (feedback: Feedback) => {
    feedbackList.value.push(feedback)
  }

  const updateFeedback = (id: number, feedback: Partial<Feedback>) => {
    const index = feedbackList.value.findIndex(f => f.id === id)
    if (index !== -1) {
      feedbackList.value[index] = { ...feedbackList.value[index], ...feedback }
    }
  }

  const removeFeedback = (id: number) => {
    feedbackList.value = feedbackList.value.filter(f => f.id !== id)
  }

  const addMeeting = (meeting: Meetings) => {
    meetingsList.value.push(meeting)
  }

  const updateMeeting = (id: number, meeting: Partial<Meetings>) => {
    const index = meetingsList.value.findIndex(m => m.id === id)
    if (index !== -1) {
      meetingsList.value[index] = { ...meetingsList.value[index], ...meeting }
    }
  }

  const removeMeeting = (id: number) => {
    meetingsList.value = meetingsList.value.filter(m => m.id !== id)
  }

  const setObjectiveStatusFilter = (status: string | null) => {
    objectiveStatusFilter.value = status
  }

  const setObjectivePeriodFilter = (periodId: number | null) => {
    objectivePeriodFilter.value = periodId
  }

  const setFeedbackStatusFilter = (status: string | null) => {
    feedbackStatusFilter.value = status
  }

  const resetFilters = () => {
    objectiveStatusFilter.value = null
    objectivePeriodFilter.value = null
    feedbackStatusFilter.value = null
  }

  return {
    // State
    currentPeriodId,
    objectives,
    employeeObjectives,
    feedbackList,
    meetingsList,
    periods,
    dashboardStats,
    selectedObjective,
    selectedFeedback,
    selectedMeeting,
    isLoading,
    error,
    objectiveStatusFilter,
    objectivePeriodFilter,
    feedbackStatusFilter,

    // Computed
    filteredObjectives,
    filteredFeedback,
    objectiveStats,
    averageProgress,

    // Methods
    setCurrentPeriod,
    setPeriods,
    setObjectives,
    setEmployeeObjectives,
    setFeedback,
    setMeetings,
    setDashboardStats,
    setSelectedObjective,
    setSelectedFeedback,
    setSelectedMeeting,
    setLoading,
    setError,
    clearError,
    addObjective,
    updateObjective,
    removeObjective,
    addEmployeeObjective,
    updateEmployeeObjective,
    removeEmployeeObjective,
    addFeedback,
    updateFeedback,
    removeFeedback,
    addMeeting,
    updateMeeting,
    removeMeeting,
    setObjectiveStatusFilter,
    setObjectivePeriodFilter,
    setFeedbackStatusFilter,
    resetFilters,
  }
})
