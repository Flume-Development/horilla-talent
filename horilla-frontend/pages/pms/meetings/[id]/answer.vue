<template>
  <div class="space-y-6 max-w-4xl mx-auto">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <NuxtLink
        :to="`/pms/meetings/${meetingId}`"
        class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <Icon name="heroicons:arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Meeting Response</h1>
        <p class="text-gray-600 mt-1">{{ meetingTitle }}</p>
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
        @click="loadMeeting"
        class="ml-4 px-3 py-1 bg-red-200 hover:bg-red-300 rounded"
      >
        Retry
      </button>
    </div>

    <!-- Meeting Info Card -->
    <div v-else class="card">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <p class="text-xs text-gray-500 uppercase mb-1">Meeting</p>
          <p class="text-sm text-gray-900">{{ meetingTitle }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase mb-1">Date & Time</p>
          <p class="text-sm text-gray-900">
            {{ formatDate(meetingDate) }} at {{ meetingTime }}
          </p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase mb-1">Status</p>
          <p :class="`badge status-${meetingStatus.toLowerCase().replace(' ', '-')}`">
            {{ meetingStatus }}
          </p>
        </div>
      </div>
    </div>

    <!-- Answer Form -->
    <div v-if="questions.length > 0" class="card">
      <MeetingAnswerForm
        :questions="questions"
        :initial-answers="answers"
        :submit-label="`Submit ${questions.length} Responses`"
        :is-loading="isSubmitting"
        :error="submitError"
        @submit="submitAnswers"
        @cancel="goBack"
      />
    </div>

    <!-- No Questions State -->
    <div v-else class="card empty-state">
      <Icon name="heroicons:document" class="empty-state-icon" />
      <p class="empty-state-text">No questions for this meeting</p>
      <NuxtLink
        :to="`/pms/meetings/${meetingId}`"
        class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors inline-block"
      >
        Back to Meeting
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'
import MeetingAnswerForm from '~/components/pms/meetings/MeetingAnswerForm.vue'

const route = useRoute()
const router = useRouter()
const { fetchMeeting, submitMeetingAnswers } = useMeetings()
const { formatDate } = usePms()

const isLoading = ref(false)
const error = ref<string | null>(null)
const isSubmitting = ref(false)
const submitError = ref<string | null>(null)

const meetingId = computed(() => parseInt(route.params.id as string))

const meetingTitle = ref('')
const meetingStatus = ref('')
const meetingDate = ref('')
const meetingTime = ref('')
const questions = ref([])
const answers = ref({})

const loadMeeting = async () => {
  isLoading.value = true
  error.value = null
  try {
    const meeting = await fetchMeeting(meetingId.value)
    if (meeting) {
      meetingTitle.value = meeting.title
      meetingStatus.value = meeting.status
      meetingDate.value = meeting.meeting_date
      meetingTime.value = meeting.meeting_time

      // Load questions for this meeting
      // TODO: Implement fetching questions for this meeting
      questions.value = meeting.questions || []
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to load meeting'
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

    const success = await submitMeetingAnswers(meetingId.value, formattedAnswers)

    if (success) {
      // Redirect to answers view
      await router.push(`/pms/meetings/${meetingId.value}/answers`)
    } else {
      submitError.value = 'Failed to submit responses'
    }
  } catch (err: any) {
    submitError.value = err.message || 'Failed to submit responses'
  } finally {
    isSubmitting.value = false
  }
}

const goBack = () => {
  router.push(`/pms/meetings/${meetingId.value}`)
}

onMounted(() => {
  loadMeeting()
})
</script>
