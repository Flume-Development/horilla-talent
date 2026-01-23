<template>
  <form @submit.prevent="$emit('submit', form)" class="space-y-6">
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

    <!-- Slot for additional fields -->
    <slot />

    <!-- Submit Button -->
    <button
      type="submit"
      class="w-full px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
    >
      <slot name="submit-label">Submit</slot>
    </button>
  </form>
</template>

<script setup lang="ts">
const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      title: '',
      description: '',
      status: 'Scheduled',
      meeting_date: '',
      meeting_time: '',
    }),
  },
})

const emit = defineEmits(['submit'])

const form = ref({ ...props.initialData })
</script>
