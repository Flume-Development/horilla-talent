<template>
  <div class="space-y-6 max-w-2xl mx-auto">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <NuxtLink
        to="/pms/bonus"
        class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <Icon name="heroicons:arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <h1 class="text-3xl font-bold text-gray-900">Award Bonus Points</h1>
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
      <!-- Employee -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Employee *</label>
        <input
          v-model.number="form.employee_id"
          type="number"
          required
          placeholder="Enter employee ID"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- Points -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Points *</label>
        <input
          v-model.number="form.points"
          type="number"
          min="1"
          required
          placeholder="Enter points to award"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- Reason -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Reason</label>
        <textarea
          v-model="form.reason"
          rows="4"
          placeholder="Enter reason for awarding bonus points"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
      </div>

      <!-- Date -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Award Date *</label>
        <input
          v-model="form.awarded_date"
          type="date"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
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
            Awarding...
          </span>
          <span v-else>Award Points</span>
        </button>
        <NuxtLink
          to="/pms/bonus"
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

const isLoading = ref(false)
const error = ref<string | null>(null)

const form = ref({
  employee_id: null,
  points: 1,
  reason: '',
  awarded_date: new Date().toISOString().split('T')[0],
})

const submitForm = async () => {
  if (!form.value.employee_id || !form.value.points) {
    error.value = 'Employee and points are required'
    return
  }

  isLoading.value = true
  error.value = null

  try {
    // TODO: Implement API call to award bonus points
    // const result = await awardBonusPoints(form.value)

    await router.push('/pms/bonus')
  } catch (err: any) {
    error.value = err.message || 'Failed to award bonus points'
  } finally {
    isLoading.value = false
  }
}
</script>
