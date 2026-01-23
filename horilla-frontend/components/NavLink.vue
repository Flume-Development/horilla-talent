<template>
  <NuxtLink
    :to="props.to"
    class="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
    :class="{ 'bg-gray-800 text-white': isActive }"
  >
    <Icon v-if="props.icon" :name="`heroicons:${props.icon}`" class="w-5 h-5" />
    <span class="text-sm font-medium">{{ props.label }}</span>
  </NuxtLink>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const props = withDefaults(
  defineProps<{
    to: string
    label: string
    icon?: string
  }>(),
  {
    icon: 'rectangle-group',
  }
)

const route = useRoute()

const isActive = computed(() => {
  return route.path === props.to
})
</script>
