<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <NuxtLink
        to="/pms/feedback"
        class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <Icon name="heroicons:arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <h1 class="text-3xl font-bold text-gray-900">Feedback Details</h1>
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

    <!-- Content -->
    <div v-else-if="feedback" class="space-y-6">
      <!-- Feedback Card -->
      <div class="card">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h2 class="text-2xl font-bold text-gray-900">{{ feedback.title }}</h2>
            <p class="text-gray-600 mt-2">{{ feedback.description }}</p>
          </div>
          <div class="flex gap-2">
            <button
              @click="archiveFeedback"
              class="p-2 text-orange-600 hover:bg-orange-50 rounded transition-colors"
              title="Archive"
            >
              <Icon name="heroicons:archive-box" class="w-5 h-5" />
            </button>
            <button
              @click="deleteFeedbackAndGoBack"
              class="p-2 text-red-600 hover:bg-red-50 rounded transition-colors"
              title="Delete"
            >
              <Icon name="heroicons:trash" class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Status and Meta Info -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 pb-6 border-b">
          <div>
            <p class="text-xs text-gray-500 uppercase">Status</p>
            <p :class="`badge status-${feedback.status.toLowerCase().replace(' ', '-')}`">
              {{ feedback.status }}
            </p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase">Start Date</p>
            <p class="text-sm text-gray-900">{{ formatDate(feedback.start_date) }}</p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase">End Date</p>
            <p class="text-sm text-gray-900">{{ formatDate(feedback.end_date) }}</p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase">Anonymous</p>
            <p class="text-sm text-gray-900">{{ feedback.allow_anonymous ? 'Yes' : 'No' }}</p>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex gap-4">
          <NuxtLink
            :to="`/pms/feedback/${feedbackId}/answer`"
            class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            Submit Answers
          </NuxtLink>
          <NuxtLink
            :to="`/pms/feedback/${feedbackId}/answers`"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            View Answers
          </NuxtLink>
          <NuxtLink
            to="/pms/feedback"
            class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Back to List
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const route = useRoute()
const router = useRouter()
const { fetchFeedback, deleteFeedback, archiveFeedback: archiveFb } = useFeedback()
const { formatDate } = usePms()

const isLoading = ref(false)
const error = ref<string | null>(null)
const feedback = ref(null)

const feedbackId = computed(() => parseInt(route.params.id as string))

const loadFeedback = async () => {
  isLoading.value = true
  error.value = null
  try {
    feedback.value = await fetchFeedback(feedbackId.value)
  } catch (err: any) {
    error.value = err.message || 'Failed to load feedback'
  } finally {
    isLoading.value = false
  }
}

const deleteFeedbackAndGoBack = async () => {
  if (confirm('Are you sure you want to delete this feedback cycle?')) {
    isLoading.value = true
    const success = await deleteFeedback(feedbackId.value)
    isLoading.value = false
    if (success) {
      await router.push('/pms/feedback')
    }
  }
}

const archiveFeedback = async () => {
  isLoading.value = true
  try {
    await archiveFb(feedbackId.value)
    await loadFeedback()
  } catch (err: any) {
    error.value = err.message || 'Failed to archive feedback'
  } finally {
    isLoading.value = false
  }
}


onMounted(() => {
  loadFeedback()
})
</script>
