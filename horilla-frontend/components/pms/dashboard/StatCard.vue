<template>
  <div
    :class="`card border-t-4 ${colorClasses[props.color]}`"
    class="flex items-center justify-between"
  >
    <div>
      <p class="text-sm text-gray-600">{{ props.title }}</p>
      <p class="text-3xl font-bold text-gray-900 mt-1">{{ props.value }}</p>
    </div>
    <Icon :name="`heroicons:${iconName}`" class="w-12 h-12" :style="{ color: colorMap[props.color] }" />
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const props = withDefaults(
  defineProps<{
    title: string
    value: string | number
    color?: 'blue' | 'green' | 'yellow' | 'purple' | 'red'
  }>(),
  {
    color: 'blue',
  }
)

const colorClasses = {
  blue: 'border-t-blue-500',
  green: 'border-t-green-500',
  yellow: 'border-t-yellow-500',
  purple: 'border-t-purple-500',
  red: 'border-t-red-500',
}

const colorMap = {
  blue: 'rgb(219, 234, 254)',
  green: 'rgb(220, 252, 231)',
  yellow: 'rgb(254, 243, 199)',
  purple: 'rgb(243, 232, 255)',
  red: 'rgb(254, 226, 226)',
}

const iconName = computed(() => {
  const icons: { [key: string]: string } = {
    'Total Objectives': 'target',
    'On Track': 'check-circle',
    'Behind': 'exclamation-circle',
    'Avg Progress': 'chart-bar',
    'Total Feedback': 'message-square',
  }
  return icons[props.title] || 'chart-bar'
})
</script>
