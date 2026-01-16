<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
        Dashboard
      </h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        Welcome back, {{ authStore.employeeName }}
      </p>
    </div>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <DashboardCard
        title="Total Employees"
        :value="'500'"
        icon="👥"
        color="blue"
      />
      <DashboardCard
        title="Present Today"
        :value="'480'"
        icon="✅"
        color="green"
      />
      <DashboardCard
        title="On Leave"
        :value="'15'"
        icon="🏖️"
        color="amber"
      />
      <DashboardCard
        title="Pending Requests"
        :value="'8'"
        icon="⏳"
        color="red"
      />
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Attendance Status -->
      <div class="lg:col-span-2 card">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">
            My Attendance
          </h2>
          <NuxtLink
            to="/attendance"
            class="text-blue-600 dark:text-blue-400 hover:underline text-sm"
          >
            View All
          </NuxtLink>
        </div>

        <div class="space-y-4">
          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Status</p>
              <p class="text-lg font-bold text-gray-900 dark:text-white">
                {{ attendanceStatus }}
              </p>
            </div>
            <div class="text-4xl">{{ attendanceEmoji }}</div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">
                Clock In Time
              </p>
              <p class="text-lg font-bold text-gray-900 dark:text-white">
                {{ clockInTime || '--:--' }}
              </p>
            </div>
            <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">
                Clock Out Time
              </p>
              <p class="text-lg font-bold text-gray-900 dark:text-white">
                {{ clockOutTime || '--:--' }}
              </p>
            </div>
          </div>

          <button
            v-if="!isClocked"
            @click="clockIn"
            :disabled="isLoading"
            class="w-full px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white font-medium rounded-lg transition-colors"
          >
            {{ isLoading ? 'Loading...' : 'Clock In' }}
          </button>
          <button
            v-else
            @click="clockOut"
            :disabled="isLoading"
            class="w-full px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white font-medium rounded-lg transition-colors"
          >
            {{ isLoading ? 'Loading...' : 'Clock Out' }}
          </button>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">
          Quick Actions
        </h2>
        <div class="space-y-3">
          <NuxtLink
            to="/attendance/request"
            class="block p-3 rounded-lg bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors text-gray-900 dark:text-white font-medium"
          >
            📝 Request Leave
          </NuxtLink>
          <NuxtLink
            to="/attendance/request"
            class="block p-3 rounded-lg bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors text-gray-900 dark:text-white font-medium"
          >
            ⏰ Attendance Request
          </NuxtLink>
          <NuxtLink
            to="/payroll"
            class="block p-3 rounded-lg bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors text-gray-900 dark:text-white font-medium"
          >
            💰 View Payslip
          </NuxtLink>
          <NuxtLink
            to="/profile"
            class="block p-3 rounded-lg bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors text-gray-900 dark:text-white font-medium"
          >
            👤 My Profile
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- Recent Activities -->
    <div class="card">
      <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">
        Recent Activities
      </h2>
      <div class="space-y-4">
        <div class="flex items-center gap-4 pb-4 border-b border-gray-200 dark:border-gray-700 last:border-b-0 last:pb-0">
          <div class="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center text-blue-600 dark:text-blue-300">
            ✓
          </div>
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-900 dark:text-white">
              Clock In
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              Today at 09:00 AM
            </p>
          </div>
        </div>

        <div class="flex items-center gap-4 pb-4 border-b border-gray-200 dark:border-gray-700 last:border-b-0 last:pb-0">
          <div class="w-10 h-10 rounded-full bg-amber-100 dark:bg-amber-900 flex items-center justify-center text-amber-600 dark:text-amber-300">
            ⏳
          </div>
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-900 dark:text-white">
              Leave Request Submitted
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              Yesterday at 03:30 PM
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '~/stores/auth';
import { useAttendance } from '~/composables/useAttendance';

definePageMeta({
  middleware: 'auth',
  title: 'Dashboard',
});

const authStore = useAuthStore();
const { clockIn: clockInAPI, clockOut: clockOutAPI, isLoading } = useAttendance();

const isClocked = ref(false);
const clockInTime = ref<string | null>(null);
const clockOutTime = ref<string | null>(null);

const attendanceStatus = computed(() => {
  if (isClocked.value) return 'Clocked In';
  if (clockOutTime.value) return 'Clocked Out';
  return 'Not Clocked';
});

const attendanceEmoji = computed(() => {
  if (isClocked.value) return '✅';
  if (clockOutTime.value) return '🏁';
  return '⭕';
});

const clockIn = async () => {
  try {
    await clockInAPI();
    isClocked.value = true;
    clockInTime.value = new Date().toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch (error) {
    console.error('Clock in failed:', error);
  }
};

const clockOut = async () => {
  try {
    await clockOutAPI();
    isClocked.value = false;
    clockOutTime.value = new Date().toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch (error) {
    console.error('Clock out failed:', error);
  }
};

onMounted(() => {
  // Initialize with current time
  const now = new Date();
  clockInTime.value = now.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  });
});
</script>
