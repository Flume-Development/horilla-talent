<template>
  <div class="p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
    <div class="flex justify-between items-start">
      <div class="flex-1">
        <h3 class="font-semibold mb-2">{{ title }}</h3>
        <p class="text-sm">{{ message }}</p>
      </div>
      <button
        @click="$emit('close')"
        class="text-red-600 hover:text-red-800"
      >
        <Icon name="heroicons:x-mark" class="w-5 h-5" />
      </button>
    </div>
    <div v-if="showRetry" class="mt-3">
      <button
        @click="$emit('retry')"
        class="px-3 py-1 bg-red-200 hover:bg-red-300 rounded text-sm transition-colors"
      >
        Retry
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

defineProps({
  title: {
    type: String,
    default: 'Error',
  },
  message: {
    type: String,
    required: true,
  },
  showRetry: {
    type: Boolean,
    default: true,
  },
})

defineEmits(['close', 'retry'])
</script>
