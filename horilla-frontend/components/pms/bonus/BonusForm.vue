<template>
  <form @submit.prevent="$emit('submit', form)" class="space-y-6">
    <!-- Employee ID -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">Employee ID *</label>
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

    <!-- Award Date -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">Award Date *</label>
      <input
        v-model="form.awarded_date"
        type="date"
        required
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Slot for additional fields -->
    <slot />

    <!-- Submit Button -->
    <button
      type="submit"
      class="w-full px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
    >
      <slot name="submit-label">Award Points</slot>
    </button>
  </form>
</template>

<script setup lang="ts">
const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      employee_id: null,
      points: 1,
      reason: '',
      awarded_date: new Date().toISOString().split('T')[0],
    }),
  },
})

const emit = defineEmits(['submit'])

const form = ref({ ...props.initialData })
</script>
