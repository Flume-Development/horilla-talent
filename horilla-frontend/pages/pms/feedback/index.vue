<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold text-gray-900">Feedback Cycles</h1>
      <NuxtLink
        to="/pms/feedback/create"
        class="btn-primary flex items-center space-x-2"
      >
        <Icon name="heroicons:plus" class="w-5 h-5" />
        <span>New Feedback Cycle</span>
      </NuxtLink>
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
            <option value="Completed">Completed</option>
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
        @click="loadFeedback"
        class="ml-4 px-3 py-1 bg-red-200 hover:bg-red-300 rounded"
      >
        Retry
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredFeedback.length === 0" class="card empty-state">
      <Icon name="heroicons:chat-bubble-left" class="empty-state-icon" />
      <p class="empty-state-text">No feedback cycles found</p>
    </div>

    <!-- Feedback Grid -->
    <div v-else class="grid gap-4">
      <div
        v-for="feedback in filteredFeedback"
        :key="feedback.id"
        class="card hover:shadow-lg transition-shadow cursor-pointer"
        @click="navigateTo(`/pms/feedback/${feedback.id}`)"
      >
        <div class="flex justify-between items-start mb-3">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900">{{ feedback.title }}</h3>
            <p class="text-sm text-gray-600 mt-1">{{ feedback.description }}</p>
          </div>
          <div class="flex gap-2 ml-4">
            <NuxtLink
              :to="`/pms/feedback/${feedback.id}/edit`"
              @click.stop
              class="p-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
              title="Edit"
            >
              <Icon name="heroicons:pencil" class="w-5 h-5" />
            </NuxtLink>
            <button
              @click.stop="deleteFeedback(feedback.id)"
              class="p-2 text-red-600 hover:bg-red-50 rounded transition-colors"
              title="Delete"
            >
              <Icon name="heroicons:trash" class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Status Badge -->
        <div class="flex items-center gap-4 mb-3">
          <span :class="`badge status-${feedback.status.toLowerCase().replace(' ', '-')}`">
            {{ feedback.status }}
          </span>
          <span class="text-xs text-gray-500">
            ID: {{ feedback.id }}
          </span>
        </div>

        <!-- Dates -->
        <div class="text-xs text-gray-500 mb-3">
          Start: {{ formatDate(feedback.start_date) }} | End: {{ formatDate(feedback.end_date) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const pmsStore = usePmsStore()
const { fetchFeedbackList, deleteFeedback: deleteFb } = useFeedback()
const { formatDate } = usePms()

const isLoading = ref(false)
const error = ref<string | null>(null)
const selectedStatus = ref('')

const filteredFeedback = computed(() => {
  if (!selectedStatus.value) {
    return pmsStore.feedbackList
  }
  return pmsStore.feedbackList.filter(fb => fb.status === selectedStatus.value)
})

const loadFeedback = async () => {
  isLoading.value = true
  error.value = null
  try {
    await fetchFeedbackList()
  } catch (err: any) {
    error.value = err.message || 'Failed to load feedback cycles'
  } finally {
    isLoading.value = false
  }
}

const deleteFeedback = async (id: number) => {
  if (confirm('Are you sure you want to delete this feedback cycle?')) {
    isLoading.value = true
    const success = await deleteFb(id)
    isLoading.value = false
    if (success) {
      await loadFeedback()
    }
  }
}

const resetFilters = () => {
  selectedStatus.value = ''
}

onMounted(() => {
  loadFeedback()
})
</script>
