<template>
  <div class="flex justify-center items-center py-12">
    <div class="text-center">
      <Icon name="eos-icons:loading" class="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
      <p class="text-gray-600">{{ message }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

defineProps({
  message: {
    type: String,
    default: 'Loading...',
  },
})
</script>
