<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
        Payroll
      </h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        View your salary slips and payroll information
      </p>
    </div>

    <!-- Current Salary Info -->
    <div class="card">
      <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">
        Current Month Salary
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
          <p class="text-sm text-blue-600 dark:text-blue-300 font-medium mb-1">
            Gross Salary
          </p>
          <p class="text-2xl font-bold text-blue-900 dark:text-blue-100">
            $5,000
          </p>
        </div>
        <div class="p-4 bg-amber-50 dark:bg-amber-900 rounded-lg">
          <p class="text-sm text-amber-600 dark:text-amber-300 font-medium mb-1">
            Deductions
          </p>
          <p class="text-2xl font-bold text-amber-900 dark:text-amber-100">
            $500
          </p>
        </div>
        <div class="p-4 bg-green-50 dark:bg-green-900 rounded-lg">
          <p class="text-sm text-green-600 dark:text-green-300 font-medium mb-1">
            Net Salary
          </p>
          <p class="text-2xl font-bold text-green-900 dark:text-green-100">
            $4,500
          </p>
        </div>
      </div>
    </div>

    <!-- Salary Components -->
    <div class="card">
      <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">
        Salary Breakdown
      </h2>

      <!-- Earnings -->
      <div class="mb-8">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Earnings
        </h3>
        <div class="space-y-3">
          <div class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded">
            <span class="text-gray-600 dark:text-gray-300">Basic Salary</span>
            <span class="font-semibold text-gray-900 dark:text-white">
              $4,000
            </span>
          </div>
          <div class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded">
            <span class="text-gray-600 dark:text-gray-300">House Allowance</span>
            <span class="font-semibold text-gray-900 dark:text-white">
              $500
            </span>
          </div>
          <div class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded">
            <span class="text-gray-600 dark:text-gray-300">Conveyance</span>
            <span class="font-semibold text-gray-900 dark:text-white">
              $500
            </span>
          </div>
        </div>
      </div>

      <!-- Deductions -->
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Deductions
        </h3>
        <div class="space-y-3">
          <div class="flex items-center justify-between p-3 bg-red-50 dark:bg-red-900 rounded">
            <span class="text-red-600 dark:text-red-300">Income Tax</span>
            <span class="font-semibold text-red-900 dark:text-red-100">
              $300
            </span>
          </div>
          <div class="flex items-center justify-between p-3 bg-red-50 dark:bg-red-900 rounded">
            <span class="text-red-600 dark:text-red-300">
              Provident Fund
            </span>
            <span class="font-semibold text-red-900 dark:text-red-100">
              $200
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Payslips -->
    <div class="card">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white">
          Recent Payslips
        </h2>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Month
              </th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Gross
              </th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Deductions
              </th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Net
              </th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
              <td class="px-6 py-4 text-gray-900 dark:text-white font-medium">
                December 2025
              </td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">
                $5,000
              </td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">
                $500
              </td>
              <td class="px-6 py-4 text-gray-900 dark:text-white font-semibold">
                $4,500
              </td>
              <td class="px-6 py-4">
                <button class="text-blue-600 dark:text-blue-400 hover:underline">
                  Download
                </button>
              </td>
            </tr>
            <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
              <td class="px-6 py-4 text-gray-900 dark:text-white font-medium">
                November 2025
              </td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">
                $5,000
              </td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">
                $500
              </td>
              <td class="px-6 py-4 text-gray-900 dark:text-white font-semibold">
                $4,500
              </td>
              <td class="px-6 py-4">
                <button class="text-blue-600 dark:text-blue-400 hover:underline">
                  Download
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
  title: 'Payroll',
})
</script>
