<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          Leave Management
        </h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">
          Manage your leave and view your balance
        </p>
      </div>
      <NuxtLink
        to="/leave/request"
        class="btn-primary"
      >
        + Request Leave
      </NuxtLink>
    </div>

    <!-- Leave Balance -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card border-l-4 border-blue-500">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
          Annual Leave
        </p>
        <div class="flex items-end justify-between">
          <div>
            <p class="text-3xl font-bold text-gray-900 dark:text-white">
              12
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
              of 20 days
            </p>
          </div>
          <div class="text-4xl">🏖️</div>
        </div>
        <div class="mt-4 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div class="bg-blue-600 h-2 rounded-full" style="width: 60%"></div>
        </div>
      </div>

      <div class="card border-l-4 border-green-500">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
          Sick Leave
        </p>
        <div class="flex items-end justify-between">
          <div>
            <p class="text-3xl font-bold text-gray-900 dark:text-white">
              8
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
              of 10 days
            </p>
          </div>
          <div class="text-4xl">🏥</div>
        </div>
        <div class="mt-4 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div class="bg-green-600 h-2 rounded-full" style="width: 80%"></div>
        </div>
      </div>

      <div class="card border-l-4 border-amber-500">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
          Casual Leave
        </p>
        <div class="flex items-end justify-between">
          <div>
            <p class="text-3xl font-bold text-gray-900 dark:text-white">
              2
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
              of 5 days
            </p>
          </div>
          <div class="text-4xl">😴</div>
        </div>
        <div class="mt-4 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div class="bg-amber-600 h-2 rounded-full" style="width: 40%"></div>
        </div>
      </div>
    </div>

    <!-- Leave Requests -->
    <div class="card">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white">
          Recent Leave Requests
        </h2>
        <NuxtLink
          to="/leave/requests"
          class="text-blue-600 dark:text-blue-400 hover:underline text-sm"
        >
          View All
        </NuxtLink>
      </div>

      <div class="space-y-4">
        <div class="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
          <div>
            <p class="font-medium text-gray-900 dark:text-white">
              Annual Leave Request
            </p>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Jan 15 - Jan 20, 2026
            </p>
          </div>
          <span class="px-3 py-1 text-sm font-semibold rounded-full bg-amber-100 dark:bg-amber-900 text-amber-800 dark:text-amber-200">
            Pending
          </span>
        </div>

        <div class="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
          <div>
            <p class="font-medium text-gray-900 dark:text-white">
              Sick Leave Request
            </p>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Jan 10, 2026
            </p>
          </div>
          <span class="px-3 py-1 text-sm font-semibold rounded-full bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">
            Approved
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
  title: 'Leave Management',
})
</script>
