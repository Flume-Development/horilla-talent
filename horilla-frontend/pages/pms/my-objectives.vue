<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold text-gray-900">My Objectives</h1>
      <NuxtLink
        to="/pms/objectives/create"
        class="btn-primary flex items-center space-x-2"
      >
        <Icon name="heroicons:plus" class="w-5 h-5" />
        <span>New Objective</span>
      </NuxtLink>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="card">
        <p class="text-xs text-gray-500 uppercase mb-1">Total</p>
        <p class="text-3xl font-bold text-gray-900">{{ pmsStore.objectiveStats.total }}</p>
      </div>
      <div class="card">
        <p class="text-xs text-gray-500 uppercase mb-1">On Track</p>
        <p class="text-3xl font-bold text-green-600">{{ pmsStore.objectiveStats.onTrack }}</p>
      </div>
      <div class="card">
        <p class="text-xs text-gray-500 uppercase mb-1">Behind</p>
        <p class="text-3xl font-bold text-yellow-600">{{ pmsStore.objectiveStats.behind }}</p>
      </div>
      <div class="card">
        <p class="text-xs text-gray-500 uppercase mb-1">Avg Progress</p>
        <p class="text-3xl font-bold text-purple-600">{{ pmsStore.averageProgress }}%</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="card">
      <div class="flex gap-4 flex-wrap">
        <div class="flex-1 min-w-[200px]">
          <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select
            :value="selectedStatus"
            @change="selectedStatus = $event.target.value"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Statuses</option>
            <option value="On Track">On Track</option>
            <option value="Behind">Behind</option>
            <option value="At Risk">At Risk</option>
            <option value="Closed">Closed</option>
            <option value="Not Started">Not Started</option>
          </select>
        </div>
        <div class="flex gap-2 items-end">
          <button
            @click="resetFilters"
            class="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Reset
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
        @click="loadObjectives"
        class="ml-4 px-3 py-1 bg-red-200 hover:bg-red-300 rounded"
      >
        Retry
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredObjectives.length === 0" class="card empty-state">
      <Icon name="heroicons:briefcase" class="empty-state-icon" />
      <p class="empty-state-text">No objectives assigned to you</p>
    </div>

    <!-- Objectives List -->
    <div v-else class="space-y-4">
      <div
        v-for="objective in filteredObjectives"
        :key="objective.id"
        class="card hover:shadow-lg transition-shadow cursor-pointer"
        @click="navigateTo(`/pms/objectives/${objective.objective_id.id}`)"
      >
        <div class="flex justify-between items-start mb-3">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900">{{ objective.objective }}</h3>
          </div>
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
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div
              class="bg-blue-600 h-2 rounded-full transition-all duration-300"
              :style="{ width: `${objective.progress_percentage}%` }"
            ></div>
          </div>
        </div>

        <!-- Dates -->
        <div class="text-xs text-gray-500 mb-3">
          {{ formatDate(objective.start_date) }} - {{ formatDate(objective.end_date) }}
        </div>

        <!-- Action -->
        <div class="flex gap-2 text-sm">
          <button
            @click.stop="updateStatus(objective.id, 'On Track')"
            class="px-3 py-1 bg-green-100 text-green-700 hover:bg-green-200 rounded transition-colors"
          >
            Mark On Track
          </button>
          <button
            @click.stop="updateStatus(objective.id, 'Behind')"
            class="px-3 py-1 bg-yellow-100 text-yellow-700 hover:bg-yellow-200 rounded transition-colors"
          >
            Mark Behind
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const pmsStore = usePmsStore()
const { fetchEmployeeObjectives, updateEmployeeObjectiveStatus } = useObjectives()
const { formatDate } = usePms()

const isLoading = ref(false)
const error = ref<string | null>(null)
const selectedStatus = ref('')

const filteredObjectives = computed(() => {
  if (!selectedStatus.value) {
    return pmsStore.employeeObjectives
  }
  return pmsStore.employeeObjectives.filter(obj => obj.status === selectedStatus.value)
})

const loadObjectives = async () => {
  isLoading.value = true
  error.value = null
  try {
    await fetchEmployeeObjectives()
  } catch (err: any) {
    error.value = err.message || 'Failed to load objectives'
  } finally {
    isLoading.value = false
  }
}

const updateStatus = async (id: number, status: string) => {
  isLoading.value = true
  try {
    await updateEmployeeObjectiveStatus(id, status)
    await loadObjectives()
  } catch (err: any) {
    error.value = err.message || 'Failed to update status'
  } finally {
    isLoading.value = false
  }
}

const resetFilters = () => {
  selectedStatus.value = ''
}

onMounted(() => {
  loadObjectives()
})
</script>
