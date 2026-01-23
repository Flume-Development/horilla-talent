<template>
  <div class="card hover:shadow-lg transition-shadow cursor-pointer" @click="$emit('click')">
    <div class="flex justify-between items-start mb-4">
      <div class="flex-1">
        <h3 class="text-lg font-semibold text-gray-900">{{ objective.title }}</h3>
        <p class="text-sm text-gray-600 mt-1">{{ objective.description }}</p>
      </div>
      <div class="flex gap-2 ml-4">
        <slot name="actions" />
      </div>
    </div>

    <!-- Status Badge -->
    <div class="mb-3">
      <StatusBadge :status="objective.status" />
    </div>

    <!-- Progress Bar -->
    <div v-if="showProgress" class="mb-3">
      <ProgressBar :percentage="objective.progress_percentage || 0" label="Progress" />
    </div>

    <!-- Meta Information -->
    <div class="grid grid-cols-2 gap-2 text-xs text-gray-500">
      <div v-if="objective.start_date">
        <span class="text-gray-600">Start:</span> {{ formatDate(objective.start_date) }}
      </div>
      <div v-if="objective.end_date">
        <span class="text-gray-600">End:</span> {{ formatDate(objective.end_date) }}
      </div>
      <div v-if="objective.duration">
        <span class="text-gray-600">Duration:</span> {{ objective.duration }} {{ objective.duration_unit }}
      </div>
      <div v-if="objective.id">
        <span class="text-gray-600">ID:</span> {{ objective.id }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import StatusBadge from './StatusBadge.vue'
import ProgressBar from './ProgressBar.vue'

const props = defineProps({
  objective: {
    type: Object,
    required: true,
  },
  showProgress: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['click'])

const { formatDate } = usePms()
</script>
