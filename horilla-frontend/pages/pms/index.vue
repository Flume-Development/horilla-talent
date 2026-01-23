<template>
  <div class="space-y-6">
    <!-- Header with Action Buttons -->
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold text-gray-900">Performance Dashboard</h1>
      <NuxtLink
        to="/pms/objectives/create"
        class="btn-primary flex items-center space-x-2"
      >
        <Icon name="heroicons:plus" class="w-5 h-5" />
        <span>New Objective</span>
      </NuxtLink>
    </div>

    <!-- Loading State -->
    <div v-if="pmsStore.isLoading" class="flex justify-center items-center py-12">
      <Icon name="eos-icons:loading" class="w-8 h-8 text-blue-600 animate-spin" />
    </div>

    <!-- Error State -->
    <div
      v-else-if="pmsStore.error"
      class="p-4 bg-red-100 border border-red-400 text-red-700 rounded"
    >
      {{ pmsStore.error }}
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <StatCard
          title="Total Objectives"
          :value="pmsStore.objectiveStats.total"
          color="blue"
        />
        <StatCard
          title="On Track"
          :value="pmsStore.objectiveStats.onTrack"
          color="green"
        />
        <StatCard
          title="Behind"
          :value="pmsStore.objectiveStats.behind"
          color="yellow"
        />
        <StatCard
          title="Avg Progress"
          :value="`${pmsStore.averageProgress}%`"
          color="purple"
        />
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Objectives Section -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Recent Objectives -->
          <div class="card">
            <div class="card-header flex justify-between items-center">
              <span>My Objectives</span>
              <NuxtLink
                to="/pms/my-objectives"
                class="text-sm text-blue-600 hover:text-blue-800"
              >
                View All
              </NuxtLink>
            </div>

            <div v-if="pmsStore.employeeObjectives.length === 0" class="empty-state">
              <Icon name="heroicons:briefcase" class="empty-state-icon" />
              <p class="empty-state-text">No objectives assigned yet</p>
            </div>

            <div v-else class="space-y-4">
              <div
                v-for="objective in pmsStore.employeeObjectives.slice(0, 3)"
                :key="objective.id"
                class="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
              >
                <div class="flex justify-between items-start mb-2">
                  <h3 class="font-semibold text-gray-900">
                    {{ objective.objective }}
                  </h3>
                  <span :class="`badge status-${objective.status.toLowerCase().replace(' ', '-')}`">
                    {{ objective.status }}
                  </span>
                </div>

                <!-- Progress Bar -->
                <div class="mb-3">
                  <div class="flex justify-between text-xs text-gray-600 mb-1">
                    <span>Progress</span>
                    <span>{{ objective.progress_percentage }}%</span>
                  </div>
                  <div class="progress-bar">
                    <div
                      class="progress-fill"
                      :style="{ width: `${objective.progress_percentage}%` }"
                    ></div>
                  </div>
                </div>

                <!-- Dates -->
                <div class="text-xs text-gray-500">
                  {{ formatDate(objective.start_date) }} - {{ formatDate(objective.end_date) }}
                </div>

                <!-- Action Links -->
                <div class="mt-3 flex space-x-2 text-xs">
                  <NuxtLink
                    :to="`/pms/objectives/${objective.objective_id.id}`"
                    class="text-blue-600 hover:text-blue-800"
                  >
                    View Details
                  </NuxtLink>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar Section -->
        <div class="space-y-6">
          <!-- Pending Feedback -->
          <div class="card">
            <div class="card-header flex justify-between items-center">
              <span>Feedback</span>
              <NuxtLink to="/pms/feedback" class="text-sm text-blue-600 hover:text-blue-800">
                View All
              </NuxtLink>
            </div>

            <div v-if="dashboardStats?.feedback.total === 0" class="empty-state text-sm">
              <p class="empty-state-text">No feedback cycles</p>
            </div>

            <div v-else class="space-y-2">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Total:</span>
                <span class="font-semibold">{{ dashboardStats?.feedback.total }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">On Track:</span>
                <span class="font-semibold text-green-600">
                  {{ dashboardStats?.feedback.on_track }}
                </span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Pending:</span>
                <span class="font-semibold text-yellow-600">
                  {{ dashboardStats?.feedback.not_started }}
                </span>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="card">
            <div class="card-header">Quick Actions</div>
            <div class="space-y-2">
              <NuxtLink
                to="/pms/feedback/create"
                class="block px-4 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded transition-colors"
              >
                Create Feedback Cycle
              </NuxtLink>
              <NuxtLink
                to="/pms/meetings/create"
                class="block px-4 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded transition-colors"
              >
                Schedule Meeting
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'
import StatCard from '~/components/pms/dashboard/StatCard.vue'

// Auth is handled in app.vue

const pmsStore = usePmsStore()
const { fetchDashboardStats, formatDate } = usePms()
const { fetchEmployeeObjectives } = useObjectives()

const dashboardStats = ref(pmsStore.dashboardStats)
const isLoading = ref(false)

onMounted(async () => {
  // Fetch initial data
  isLoading.value = true
  try {
    await Promise.all([
      fetchDashboardStats(),
      fetchEmployeeObjectives(),
    ])

    dashboardStats.value = pmsStore.dashboardStats
  } finally {
    isLoading.value = false
  }
})
</script>
