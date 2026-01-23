<template>
  <form @submit.prevent="$emit('submit', form)" class="space-y-6">
    <!-- Title -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">Title *</label>
      <input
        v-model="form.title"
        type="text"
        required
        placeholder="Enter objective title"
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Description -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
      <textarea
        v-model="form.description"
        rows="4"
        placeholder="Enter objective description"
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
        <option value="At Risk">At Risk</option>
        <option value="Closed">Closed</option>
      </select>
    </div>

    <!-- Duration -->
    <div class="grid grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Duration *</label>
        <input
          v-model.number="form.duration"
          type="number"
          min="1"
          required
          placeholder="Enter duration"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Unit *</label>
        <select
          v-model="form.duration_unit"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="days">Days</option>
          <option value="weeks">Weeks</option>
          <option value="months">Months</option>
          <option value="years">Years</option>
        </select>
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
      status: 'Not Started',
      duration: 1,
      duration_unit: 'months',
    }),
  },
})

const emit = defineEmits(['submit'])

const form = ref({ ...props.initialData })
</script>
