<template>
  <div class="space-y-6 max-w-2xl mx-auto">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <NuxtLink
        to="/pms/meetings"
        class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <Icon name="heroicons:arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <h1 class="text-3xl font-bold text-gray-900">Schedule Meeting</h1>
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
    </div>

    <!-- Form -->
    <form v-else @submit.prevent="submitForm" class="card space-y-6">
      <!-- Title -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Title *</label>
        <input
          v-model="form.title"
          type="text"
          required
          placeholder="Enter meeting title"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- Description -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
        <textarea
          v-model="form.description"
          rows="4"
          placeholder="Enter meeting description"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
      </div>

      <!-- Status -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
        <select
          v-model="form.status"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="Scheduled">Scheduled</option>
          <option value="Completed">Completed</option>
          <option value="Cancelled">Cancelled</option>
        </select>
      </div>

      <!-- Date and Time -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Meeting Date *</label>
          <input
            v-model="form.meeting_date"
            type="date"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Meeting Time *</label>
          <input
            v-model="form.meeting_time"
            type="time"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <!-- Attendees -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Attendees</label>
        <input
          v-model="form.attendees_input"
          type="text"
          placeholder="Enter attendee IDs separated by commas (e.g., 1,2,3)"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <p class="text-xs text-gray-500 mt-1">Enter comma-separated employee IDs</p>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-4">
        <button
          type="submit"
          class="flex-1 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="flex items-center justify-center gap-2">
            <Icon name="eos-icons:loading" class="w-5 h-5 animate-spin" />
            Creating...
          </span>
          <span v-else>Schedule Meeting</span>
        </button>
        <NuxtLink
          to="/pms/meetings"
          class="flex-1 px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-center"
        >
          Cancel
        </NuxtLink>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const router = useRouter()
const { createMeeting } = useMeetings()

const isLoading = ref(false)
const error = ref<string | null>(null)

const form = ref({
  title: '',
  description: '',
  status: 'Scheduled',
  meeting_date: '',
  meeting_time: '',
  attendees_input: '',
})

const submitForm = async () => {
  if (!form.value.title || !form.value.meeting_date || !form.value.meeting_time) {
    error.value = 'Title, date, and time are required'
    return
  }

  isLoading.value = true
  error.value = null

  try {
    const attendeeIds = form.value.attendees_input
      .split(',')
      .map(id => parseInt(id.trim()))
      .filter(id => !isNaN(id))

    const meeting = await createMeeting({
      title: form.value.title,
      description: form.value.description,
      status: form.value.status,
      meeting_date: form.value.meeting_date,
      meeting_time: form.value.meeting_time,
      attendees: attendeeIds,
    })

    if (meeting) {
      await router.push('/pms/meetings')
    } else {
      error.value = 'Failed to schedule meeting'
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to schedule meeting'
  } finally {
    isLoading.value = false
  }
}
</script>
