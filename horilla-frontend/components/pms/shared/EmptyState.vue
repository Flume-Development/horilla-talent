<template>
  <div class="card empty-state text-center py-12">
    <Icon v-if="icon" :name="icon" class="empty-state-icon mx-auto mb-4 w-16 h-16 text-gray-400" />
    <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ title }}</h3>
    <p class="text-gray-600 mb-6">{{ description }}</p>
    <slot />
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    default: '',
  },
  icon: {
    type: String,
    default: 'heroicons:inbox',
  },
})
</script>

<style scoped>
.empty-state {
  @apply border border-dashed border-gray-300 bg-gray-50;
}

.empty-state-icon {
  @apply text-gray-300;
}
</style>
