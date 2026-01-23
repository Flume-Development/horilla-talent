<template>
  <span :class="['px-3 py-1 rounded-full text-sm font-medium', statusClass]">
    {{ status }}
  </span>
</template>

<script setup lang="ts">
const props = defineProps({
  status: {
    type: String,
    required: true,
  },
})

const statusClass = computed(() => {
  const status = props.status.toLowerCase()

  const statusMap: Record<string, string> = {
    'on track': 'bg-green-100 text-green-800',
    'behind': 'bg-yellow-100 text-yellow-800',
    'at risk': 'bg-orange-100 text-orange-800',
    'closed': 'bg-gray-100 text-gray-800',
    'completed': 'bg-blue-100 text-blue-800',
    'not started': 'bg-gray-100 text-gray-600',
    'scheduled': 'bg-blue-100 text-blue-800',
    'cancelled': 'bg-red-100 text-red-800',
  }

  return statusMap[status] || 'bg-gray-100 text-gray-600'
})
</script>
