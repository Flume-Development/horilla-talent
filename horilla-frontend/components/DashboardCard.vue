<template>
  <div class="card border-l-4" :class="borderColorClass">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
          {{ title }}
        </p>
        <p class="text-3xl font-bold text-gray-900 dark:text-white">
          {{ value }}
        </p>
      </div>
      <div class="text-5xl opacity-20">
        {{ icon }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  title: string;
  value: string | number;
  icon: string;
  color?: 'blue' | 'green' | 'amber' | 'red';
}

const props = withDefaults(defineProps<Props>(), {
  color: 'blue',
});

const borderColorClass = computed(() => {
  const colors = {
    blue: 'border-blue-500',
    green: 'border-green-500',
    amber: 'border-amber-500',
    red: 'border-red-500',
  };
  return colors[props.color];
});
</script>
