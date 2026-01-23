<template>
  <div class="space-y-2">
    <div class="flex justify-between items-center">
      <label v-if="label" class="text-sm font-medium text-gray-700">{{ label }}</label>
      <span class="text-sm font-semibold text-gray-900">{{ percentage }}%</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2.5">
      <div
        class="h-2.5 rounded-full transition-all duration-300"
        :class="progressClass"
        :style="{ width: `${percentage}%` }"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  percentage: {
    type: Number,
    required: true,
    validator: (val: number) => val >= 0 && val <= 100,
  },
  label: {
    type: String,
    default: null,
  },
})

const progressClass = computed(() => {
  const pct = props.percentage

  if (pct >= 75) return 'bg-green-500'
  if (pct >= 50) return 'bg-blue-500'
  if (pct >= 25) return 'bg-yellow-500'
  return 'bg-red-500'
})
</script>
