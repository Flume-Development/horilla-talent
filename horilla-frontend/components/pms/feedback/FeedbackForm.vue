<template>
  <form @submit.prevent="$emit('submit', form)" class="space-y-6">
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
      status: 'Not Started',
      start_date: '',
      end_date: '',
      allow_anonymous: false,
    }),
  },
})

const emit = defineEmits(['submit'])

const form = ref({ ...props.initialData })
</script>
