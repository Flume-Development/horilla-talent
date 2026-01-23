<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold text-gray-900">Bonus Points</h1>
      <NuxtLink
        to="/pms/bonus/create"
        class="btn-primary flex items-center space-x-2"
      >
        <Icon name="heroicons:plus" class="w-5 h-5" />
        <span>Award Bonus</span>
      </NuxtLink>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="card">
        <p class="text-xs text-gray-500 uppercase mb-1">Total Awarded</p>
        <p class="text-3xl font-bold text-gray-900">{{ stats.totalAwarded }}</p>
      </div>
      <div class="card">
        <p class="text-xs text-gray-500 uppercase mb-1">Total Rules</p>
        <p class="text-3xl font-bold text-blue-600">{{ stats.totalRules }}</p>
      </div>
      <div class="card">
        <p class="text-xs text-gray-500 uppercase mb-1">Active Employees</p>
        <p class="text-3xl font-bold text-green-600">{{ stats.activeEmployees }}</p>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex gap-4 border-b">
      <button
        :class="['px-4 py-2 font-medium transition-colors', activeTab === 'points' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-gray-900']"
        @click="activeTab = 'points'"
      >
        Bonus Points
      </button>
      <button
        :class="['px-4 py-2 font-medium transition-colors', activeTab === 'rules' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-gray-900']"
        @click="activeTab = 'rules'"
      >
        Bonus Rules
      </button>
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
        @click="loadBonusData"
        class="ml-4 px-3 py-1 bg-red-200 hover:bg-red-300 rounded"
      >
        Retry
      </button>
    </div>

    <!-- Bonus Points Tab -->
    <div v-else-if="activeTab === 'points'">
      <!-- Empty State -->
      <div v-if="bonusPoints.length === 0" class="card empty-state">
        <Icon name="heroicons:gift" class="empty-state-icon" />
        <p class="empty-state-text">No bonus points awarded yet</p>
      </div>

      <!-- Points Grid -->
      <div v-else class="grid gap-4">
        <div
          v-for="point in bonusPoints"
          :key="point.id"
          class="card"
        >
          <div class="flex justify-between items-start mb-3">
            <div class="flex-1">
              <p class="font-semibold text-gray-900">Employee ID: {{ point.employee_id }}</p>
              <p class="text-sm text-gray-600">{{ point.reason || 'No reason specified' }}</p>
            </div>
            <div class="text-right">
              <p class="text-2xl font-bold text-green-600">{{ point.points }} pts</p>
              <p class="text-xs text-gray-500">{{ formatDate(point.awarded_date) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bonus Rules Tab -->
    <div v-else-if="activeTab === 'rules'">
      <!-- Empty State -->
      <div v-if="bonusRules.length === 0" class="card empty-state">
        <Icon name="heroicons:document" class="empty-state-icon" />
        <p class="empty-state-text">No bonus rules configured</p>
      </div>

      <!-- Rules Grid -->
      <div v-else class="grid gap-4">
        <div
          v-for="rule in bonusRules"
          :key="rule.id"
          class="card"
        >
          <div class="flex justify-between items-start mb-3">
            <div class="flex-1">
              <h3 class="font-semibold text-gray-900">{{ rule.title }}</h3>
              <p class="text-sm text-gray-600 mt-1">{{ rule.description }}</p>
            </div>
            <div class="text-right">
              <p class="text-xl font-bold text-blue-600">{{ rule.points }} pts</p>
              <p class="text-xs text-gray-500">Per: {{ rule.frequency }}</p>
            </div>
          </div>
          <div class="flex gap-2">
            <button
              class="flex-1 px-4 py-2 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors"
            >
              Edit Rule
            </button>
            <button
              class="flex-1 px-4 py-2 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const { formatDate } = usePms()

const isLoading = ref(false)
const error = ref<string | null>(null)
const activeTab = ref('points')

const bonusPoints = ref([])
const bonusRules = ref([])

const stats = computed(() => ({
  totalAwarded: bonusPoints.value.reduce((sum, p) => sum + (p.points || 0), 0),
  totalRules: bonusRules.value.length,
  activeEmployees: new Set(bonusPoints.value.map(p => p.employee_id)).size,
}))

const loadBonusData = async () => {
  isLoading.value = true
  error.value = null
  try {
    // TODO: Implement API calls for bonus points and rules
    // For now, using placeholder data
    bonusPoints.value = []
    bonusRules.value = []
  } catch (err: any) {
    error.value = err.message || 'Failed to load bonus data'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadBonusData()
})
</script>
