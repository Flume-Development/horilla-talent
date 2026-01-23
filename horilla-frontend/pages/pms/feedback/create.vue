<template>
  <div class="space-y-6 max-w-2xl mx-auto">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <NuxtLink
        to="/pms/feedback"
        class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <Icon name="heroicons:arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <h1 class="text-3xl font-bold text-gray-900">Create Feedback Cycle</h1>
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
          placeholder="Enter feedback cycle title"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- Description -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
        <textarea
          v-model="form.description"
          rows="4"
          placeholder="Enter feedback cycle description"
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
          <option value="Not Started">Not Started</option>
          <option value="On Track">On Track</option>
          <option value="Behind">Behind</option>
          <option value="Completed">Completed</option>
        </select>
      </div>

      <!-- Dates -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Start Date *</label>
          <input
            v-model="form.start_date"
            type="date"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">End Date *</label>
          <input
            v-model="form.end_date"
            type="date"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <!-- Allow Anonymous -->
      <div>
        <label class="flex items-center gap-2">
          <input
            v-model="form.allow_anonymous"
            type="checkbox"
            class="w-4 h-4 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
          />
          <span class="text-sm font-medium text-gray-700">Allow Anonymous Feedback</span>
        </label>
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
          <span v-else>Create Feedback Cycle</span>
        </button>
        <NuxtLink
          to="/pms/feedback"
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
const { createFeedback } = useFeedback()

const isLoading = ref(false)
const error = ref<string | null>(null)

const form = ref({
  title: '',
  description: '',
  status: 'Not Started',
  start_date: '',
  end_date: '',
  allow_anonymous: false,
})

const submitForm = async () => {
  if (!form.value.title || !form.value.start_date || !form.value.end_date) {
    error.value = 'Title and dates are required'
    return
  }

  isLoading.value = true
  error.value = null

  try {
    const feedback = await createFeedback({
      title: form.value.title,
      description: form.value.description,
      status: form.value.status,
      start_date: form.value.start_date,
      end_date: form.value.end_date,
      allow_anonymous: form.value.allow_anonymous,
    })

    if (feedback) {
      await router.push('/pms/feedback')
    } else {
      error.value = 'Failed to create feedback cycle'
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to create feedback cycle'
  } finally {
    isLoading.value = false
  }
}
</script>
