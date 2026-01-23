<template>
  <div class="p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
    <div class="flex justify-between items-start">
      <div class="flex-1">
        <h3 class="font-semibold mb-2">{{ title }}</h3>
        <p class="text-sm">{{ message }}</p>
      </div>
      <button
        @click="$emit('close')"
        class="text-green-600 hover:text-green-800"
      >
        <Icon name="heroicons:x-mark" class="w-5 h-5" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

defineProps({
  title: {
    type: String,
    default: 'Success',
  },
  message: {
    type: String,
    required: true,
  },
})

defineEmits(['close'])
</script>
