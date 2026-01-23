<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900">PMS Analytics</h1>
      <p class="text-gray-600 mt-1">Performance metrics and insights</p>
    </div>

    <!-- Filters -->
    <div class="card">
      <div class="flex gap-4 flex-wrap">
        <div class="flex-1 min-w-[200px]">
          <label class="block text-sm font-medium text-gray-700 mb-1">Period</label>
          <select
            v-model="selectedPeriod"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="week">This Week</option>
            <option value="month">This Month</option>
            <option value="quarter">This Quarter</option>
            <option value="year">This Year</option>
          </select>
        </div>
        <div class="flex gap-2 items-end">
          <button
            @click="loadAnalytics"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Refresh
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <Icon name="eos-icons:loading" class="w-8 h-8 text-blue-600 animate-spin" />
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="p-4 bg-red-100 border border-red-400 text-red-700 rounded"
    >
      {{ error }}
      <button
        @click="loadAnalytics"
        class="ml-4 px-3 py-1 bg-red-200 hover:bg-red-300 rounded"
      >
        Retry
      </button>
    </div>

    <!-- Content -->
    <div v-else class="space-y-6">
      <!-- Key Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="card">
          <p class="text-xs text-gray-500 uppercase mb-2">Objectives Completion</p>
          <p class="text-3xl font-bold text-blue-600">{{ metrics.completionRate }}%</p>
        </div>
        <div class="card">
          <p class="text-xs text-gray-500 uppercase mb-2">Avg Progress</p>
          <p class="text-3xl font-bold text-green-600">{{ metrics.avgProgress }}%</p>
        </div>
        <div class="card">
          <p class="text-xs text-gray-500 uppercase mb-2">On Track</p>
          <p class="text-3xl font-bold text-purple-600">{{ metrics.onTrack }}%</p>
        </div>
        <div class="card">
          <p class="text-xs text-gray-500 uppercase mb-2">At Risk</p>
          <p class="text-3xl font-bold text-red-600">{{ metrics.atRisk }}%</p>
        </div>
      </div>

      <!-- Objective Status Distribution -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Objective Status Distribution</h3>
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div class="text-center p-4 bg-green-50 rounded-lg">
            <p class="text-2xl font-bold text-green-600">{{ distribution.onTrack }}</p>
            <p class="text-sm text-gray-600 mt-1">On Track</p>
          </div>
          <div class="text-center p-4 bg-yellow-50 rounded-lg">
            <p class="text-2xl font-bold text-yellow-600">{{ distribution.behind }}</p>
            <p class="text-sm text-gray-600 mt-1">Behind</p>
          </div>
          <div class="text-center p-4 bg-orange-50 rounded-lg">
            <p class="text-2xl font-bold text-orange-600">{{ distribution.atRisk }}</p>
            <p class="text-sm text-gray-600 mt-1">At Risk</p>
          </div>
          <div class="text-center p-4 bg-blue-50 rounded-lg">
            <p class="text-2xl font-bold text-blue-600">{{ distribution.notStarted }}</p>
            <p class="text-sm text-gray-600 mt-1">Not Started</p>
          </div>
          <div class="text-center p-4 bg-gray-50 rounded-lg">
            <p class="text-2xl font-bold text-gray-600">{{ distribution.closed }}</p>
            <p class="text-sm text-gray-600 mt-1">Closed</p>
          </div>
        </div>
      </div>

      <!-- Feedback Summary -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Feedback Summary</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <p class="text-sm text-gray-600 mb-2">Total Cycles</p>
            <p class="text-2xl font-bold text-gray-900">{{ feedbackMetrics.totalCycles }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-600 mb-2">Completed</p>
            <p class="text-2xl font-bold text-green-600">{{ feedbackMetrics.completed }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-600 mb-2">In Progress</p>
            <p class="text-2xl font-bold text-blue-600">{{ feedbackMetrics.inProgress }}</p>
          </div>
        </div>
      </div>

      <!-- Meeting Summary -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Meeting Summary</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <p class="text-sm text-gray-600 mb-2">Scheduled</p>
            <p class="text-2xl font-bold text-blue-600">{{ meetingMetrics.scheduled }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-600 mb-2">Completed</p>
            <p class="text-2xl font-bold text-green-600">{{ meetingMetrics.completed }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-600 mb-2">Cancelled</p>
            <p class="text-2xl font-bold text-red-600">{{ meetingMetrics.cancelled }}</p>
          </div>
        </div>
      </div>

      <!-- Insights -->
      <div class="card bg-blue-50 border border-blue-200">
        <h3 class="text-lg font-semibold text-blue-900 mb-3">Insights & Recommendations</h3>
        <ul class="space-y-2 text-sm text-blue-800">
          <li class="flex gap-2">
            <span>📊</span>
            <span>{{ metrics.atRisk }}% of objectives are at risk - consider prioritization and support</span>
          </li>
          <li class="flex gap-2">
            <span>📈</span>
            <span>Average progress is {{ metrics.avgProgress }}% - maintain current pace for on-time completion</span>
          </li>
          <li class="flex gap-2">
            <span>💬</span>
            <span>{{ feedbackMetrics.inProgress }} feedback cycles are in progress - track completion</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const pmsStore = usePmsStore()
const { fetchDashboardStats } = usePms()

const isLoading = ref(false)
const error = ref<string | null>(null)
const selectedPeriod = ref('month')

const metrics = ref({
  completionRate: 0,
  avgProgress: 0,
  onTrack: 0,
  atRisk: 0,
})

const distribution = ref({
  onTrack: 0,
  behind: 0,
  atRisk: 0,
  notStarted: 0,
  closed: 0,
})

const feedbackMetrics = ref({
  totalCycles: 0,
  completed: 0,
  inProgress: 0,
})

const meetingMetrics = ref({
  scheduled: 0,
  completed: 0,
  cancelled: 0,
})

const loadAnalytics = async () => {
  isLoading.value = true
  error.value = null
  try {
    await fetchDashboardStats()

    const stats = pmsStore.objectiveStats
    const objectives = pmsStore.employeeObjectives

    // Calculate metrics
    metrics.value = {
      completionRate: stats.closed,
      avgProgress: pmsStore.averageProgress,
      onTrack: stats.onTrack > 0 ? Math.round((stats.onTrack / stats.total) * 100) : 0,
      atRisk: stats.atRisk > 0 ? Math.round((stats.atRisk / stats.total) * 100) : 0,
    }

    // Distribution
    distribution.value = {
      onTrack: stats.onTrack,
      behind: stats.behind,
      atRisk: stats.atRisk,
      notStarted: stats.notStarted,
      closed: stats.closed,
    }

    // Feedback metrics (from store)
    feedbackMetrics.value = {
      totalCycles: pmsStore.feedbackList.length,
      completed: pmsStore.feedbackList.filter(f => f.status === 'Completed').length,
      inProgress: pmsStore.feedbackList.filter(f => f.status !== 'Completed').length,
    }

    // Meeting metrics
    meetingMetrics.value = {
      scheduled: pmsStore.meetingsList.filter(m => m.status === 'Scheduled').length,
      completed: pmsStore.meetingsList.filter(m => m.status === 'Completed').length,
      cancelled: pmsStore.meetingsList.filter(m => m.status === 'Cancelled').length,
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to load analytics'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadAnalytics()
})
</script>
