<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          Employees
        </h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">
          Manage all employees in your organization
        </p>
      </div>
      <NuxtLink
        to="/employees/create"
        class="btn-primary"
      >
        + Add Employee
      </NuxtLink>
    </div>

    <!-- Filters and Search -->
    <div class="card">
      <div class="flex flex-col md:flex-row gap-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by name or email..."
          class="input-base flex-1"
        />
        <select v-model="departmentFilter" class="input-base">
          <option value="">All Departments</option>
          <option value="hr">Human Resources</option>
          <option value="it">IT</option>
          <option value="finance">Finance</option>
          <option value="sales">Sales</option>
        </select>
        <button
          @click="fetchEmployees"
          class="btn-primary px-6"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Loading...' : 'Search' }}
        </button>
      </div>
    </div>

    <!-- Employees Table -->
    <div class="card overflow-hidden">
      <div v-if="isLoading" class="text-center py-12">
        <p class="text-gray-600 dark:text-gray-400">Loading employees...</p>
      </div>

      <div v-else-if="employees.length === 0" class="text-center py-12">
        <p class="text-gray-600 dark:text-gray-400">No employees found</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Name
              </th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Email
              </th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Phone
              </th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Department
              </th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="employee in employees"
              :key="employee.id"
              class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <img
                    v-if="employee.profile_image"
                    :src="employee.profile_image"
                    :alt="employee.first_name"
                    class="w-10 h-10 rounded-full object-cover"
                  />
                  <div v-else class="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold text-sm">
                    {{ getInitials(`${employee.first_name} ${employee.last_name}`) }}
                  </div>
                  <div>
                    <p class="font-medium text-gray-900 dark:text-white">
                      {{ employee.first_name }} {{ employee.last_name }}
                    </p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">
                {{ employee.email }}
              </td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">
                {{ employee.phone || '--' }}
              </td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">
                {{ employee.department || '--' }}
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-2">
                  <NuxtLink
                    :to="`/employees/${employee.id}`"
                    class="px-3 py-1 text-sm bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300 rounded hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors"
                  >
                    View
                  </NuxtLink>
                  <button
                    @click="deleteEmployee(employee.id)"
                    class="px-3 py-1 text-sm bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-300 rounded hover:bg-red-200 dark:hover:bg-red-800 transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Pagination -->
    <div class="flex items-center justify-between card">
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Showing {{ employees.length }} employees
      </p>
      <div class="flex gap-2">
        <button
          class="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          Previous
        </button>
        <button
          class="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useEmployee, type EmployeeData } from '~/composables/useEmployee';

definePageMeta({
  middleware: 'auth',
  title: 'Employees',
});

const { getEmployees, deleteEmployee: deleteEmp, isLoading, error } = useEmployee();
const employees = ref<EmployeeData[]>([]);
const searchQuery = ref('');
const departmentFilter = ref('');

const getInitials = (name: string) => {
  return name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
};

const fetchEmployees = async () => {
  try {
    const response = await getEmployees(1, 20);
    employees.value = response.results;
  } catch (err) {
    console.error('Failed to fetch employees:', err);
  }
};

const deleteEmployee = async (id: number) => {
  if (confirm('Are you sure you want to delete this employee?')) {
    try {
      await deleteEmp(id);
      employees.value = employees.value.filter((emp) => emp.id !== id);
    } catch (err) {
      console.error('Failed to delete employee:', err);
    }
  }
};

onMounted(() => {
  fetchEmployees();
});
</script>
