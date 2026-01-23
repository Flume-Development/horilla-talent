<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <NuxtLink
        to="/pms/meetings"
        class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <Icon name="heroicons:arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <h1 class="text-3xl font-bold text-gray-900">Meeting Details</h1>
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

    <!-- Content -->
    <div v-else-if="meeting" class="space-y-6">
      <!-- Meeting Card -->
      <div class="card">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h2 class="text-2xl font-bold text-gray-900">{{ meeting.title }}</h2>
            <p class="text-gray-600 mt-2">{{ meeting.description }}</p>
          </div>
          <div class="flex gap-2">
            <NuxtLink
              :to="`/pms/meetings/${meeting.id}/edit`"
              class="p-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
              title="Edit"
            >
              <Icon name="heroicons:pencil" class="w-5 h-5" />
            </NuxtLink>
            <button
              @click="deleteMeetingAndGoBack"
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
            <p :class="`badge status-${meeting.status.toLowerCase().replace(' ', '-')}`">
              {{ meeting.status }}
            </p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase">Date</p>
            <p class="text-sm text-gray-900">{{ formatDate(meeting.meeting_date) }}</p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase">Time</p>
            <p class="text-sm text-gray-900">{{ meeting.meeting_time }}</p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase">ID</p>
            <p class="text-sm text-gray-900">{{ meeting.id }}</p>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex gap-4">
          <NuxtLink
            :to="`/pms/meetings/${meetingId}/answer`"
            class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            Submit Response
          </NuxtLink>
          <NuxtLink
            :to="`/pms/meetings/${meetingId}/answers`"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            View Responses
          </NuxtLink>
          <NuxtLink
            to="/pms/meetings"
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
const { fetchMeeting, deleteMeeting } = useMeetings()
const { formatDate } = usePms()

const isLoading = ref(false)
const error = ref<string | null>(null)
const meeting = ref(null)

const meetingId = computed(() => parseInt(route.params.id as string))

const loadMeeting = async () => {
  isLoading.value = true
  error.value = null
  try {
    meeting.value = await fetchMeeting(meetingId.value)
  } catch (err: any) {
    error.value = err.message || 'Failed to load meeting'
  } finally {
    isLoading.value = false
  }
}

const deleteMeetingAndGoBack = async () => {
  if (confirm('Are you sure you want to delete this meeting?')) {
    isLoading.value = true
    const success = await deleteMeeting(meetingId.value)
    isLoading.value = false
    if (success) {
      await router.push('/pms/meetings')
    }
  }
}


onMounted(() => {
  loadMeeting()
})
</script>
