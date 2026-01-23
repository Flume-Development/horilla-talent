<template>
  <header class="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
    <div>
      <h2 class="text-xl font-semibold text-gray-900">{{ pageTitle }}</h2>
    </div>
    <div class="flex items-center space-x-4">
      <!-- Notifications (Placeholder) -->
      <button class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <Icon name="heroicons:bell" class="w-5 h-5 text-gray-600" />
      </button>

      <!-- User Menu (Placeholder) -->
      <button class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <Icon name="heroicons:user-circle" class="w-6 h-6 text-gray-600" />
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const route = useRoute()

const pageTitle = computed(() => {
  const titles: { [key: string]: string } = {
    '/pms': 'Dashboard',
    '/pms/objectives': 'Objectives',
    '/pms/my-objectives': 'My Objectives',
    '/pms/feedback': 'Feedback',
    '/pms/meetings': 'Meetings',
    '/pms/bonus/settings': 'Bonus Points Settings',
    '/pms/bonus/employees': 'Employee Bonus Points',
  }

  return titles[route.path] || 'Performance Management System'
})
</script>
