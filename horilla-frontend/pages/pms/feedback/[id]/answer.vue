<template>
  <div class="space-y-6 max-w-4xl mx-auto">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <NuxtLink
        :to="`/pms/feedback/${feedbackId}`"
        class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <Icon name="heroicons:arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Answer Feedback</h1>
        <p class="text-gray-600 mt-1">{{ feedbackTitle }}</p>
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

    <!-- Feedback Info Card -->
    <div v-else class="card">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <p class="text-xs text-gray-500 uppercase mb-1">Feedback Cycle</p>
          <p class="text-sm text-gray-900">{{ feedbackTitle }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase mb-1">Duration</p>
          <p class="text-sm text-gray-900">
            {{ formatDate(feedbackStartDate) }} - {{ formatDate(feedbackEndDate) }}
          </p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase mb-1">Status</p>
          <p :class="`badge status-${feedbackStatus.toLowerCase().replace(' ', '-')}`">
            {{ feedbackStatus }}
          </p>
        </div>
      </div>
    </div>

    <!-- Answer Form -->
    <div v-if="questions.length > 0" class="card">
      <FeedbackAnswerForm
        :questions="questions"
        :initial-answers="answers"
        :submit-label="`Submit ${questions.length} Answers`"
        :is-loading="isSubmitting"
        :error="submitError"
        @submit="submitAnswers"
        @cancel="goBack"
      />
    </div>

    <!-- No Questions State -->
    <div v-else class="card empty-state">
      <Icon name="heroicons:document" class="empty-state-icon" />
      <p class="empty-state-text">No questions in this feedback cycle</p>
      <NuxtLink
        :to="`/pms/feedback/${feedbackId}`"
        class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors inline-block"
      >
        Back to Feedback
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'
import FeedbackAnswerForm from '~/components/pms/feedback/FeedbackAnswerForm.vue'

const route = useRoute()
const router = useRouter()
const { fetchFeedback, submitFeedbackAnswers } = useFeedback()
const { formatDate } = usePms()

const isLoading = ref(false)
const error = ref<string | null>(null)
const isSubmitting = ref(false)
const submitError = ref<string | null>(null)

const feedbackId = computed(() => parseInt(route.params.id as string))

const feedbackTitle = ref('')
const feedbackStatus = ref('')
const feedbackStartDate = ref('')
const feedbackEndDate = ref('')
const questions = ref([])
const answers = ref({})

const loadFeedback = async () => {
  isLoading.value = true
  error.value = null
  try {
    const feedback = await fetchFeedback(feedbackId.value)
    if (feedback) {
      feedbackTitle.value = feedback.title
      feedbackStatus.value = feedback.status
      feedbackStartDate.value = feedback.start_date
      feedbackEndDate.value = feedback.end_date

      // Load questions for this feedback
      // TODO: Implement fetching questions for this feedback cycle
      // For now, using placeholder
      questions.value = feedback.questions || []
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to load feedback'
  } finally {
    isLoading.value = false
  }
}

const submitAnswers = async (submittedAnswers: Record<number, any>) => {
  isSubmitting.value = true
  submitError.value = null

  try {
    // Format answers for API
    const formattedAnswers = Object.entries(submittedAnswers).map(([questionId, answer]) => ({
      question_id: parseInt(questionId),
      answer: answer,
    }))

    const success = await submitFeedbackAnswers(feedbackId.value, formattedAnswers)

    if (success) {
      // Show success message and redirect
      await router.push(`/pms/feedback/${feedbackId.value}/answers`)
    } else {
      submitError.value = 'Failed to submit answers'
    }
  } catch (err: any) {
    submitError.value = err.message || 'Failed to submit answers'
  } finally {
    isSubmitting.value = false
  }
}

const goBack = () => {
  router.push(`/pms/feedback/${feedbackId.value}`)
}

onMounted(() => {
  loadFeedback()
})
</script>
