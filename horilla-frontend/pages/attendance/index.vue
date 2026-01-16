<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          Attendance
        </h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">
          View and manage attendance records
        </p>
      </div>
      <NuxtLink
        to="/attendance/request"
        class="btn-primary"
      >
        + New Request
      </NuxtLink>
    </div>

    <!-- Filters -->
    <div class="card">
      <div class="flex flex-col md:flex-row gap-4">
        <input
          v-model="dateFrom"
          type="date"
          class="input-base"
        />
        <input
          v-model="dateTo"
          type="date"
          class="input-base"
        />
        <select v-model="statusFilter" class="input-base">
          <option value="">All Status</option>
          <option value="present">Present</option>
          <option value="absent">Absent</option>
          <option value="half_day">Half Day</option>
          <option value="late">Late</option>
        </select>
        <button
          @click="fetchAttendance"
          class="btn-primary px-6"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Loading...' : 'Filter' }}
        </button>
      </div>
    </div>

    <!-- Attendance Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="card border-l-4 border-green-500">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Present</p>
        <p class="text-3xl font-bold text-green-600 dark:text-green-400">22</p>
      </div>
      <div class="card border-l-4 border-red-500">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Absent</p>
        <p class="text-3xl font-bold text-red-600 dark:text-red-400">2</p>
      </div>
      <div class="card border-l-4 border-amber-500">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Half Day</p>
        <p class="text-3xl font-bold text-amber-600 dark:text-amber-400">1</p>
      </div>
      <div class="card border-l-4 border-orange-500">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Late</p>
        <p class="text-3xl font-bold text-orange-600 dark:text-orange-400">0</p>
      </div>
    </div>

    <!-- Attendance Table -->
    <div class="card overflow-hidden">
      <div v-if="isLoading" class="text-center py-12">
        <p class="text-gray-600 dark:text-gray-400">Loading attendance...</p>
      </div>

      <div v-else-if="attendance.length === 0" class="text-center py-12">
        <p class="text-gray-600 dark:text-gray-400">No attendance records found</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Date
              </th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Clock In
              </th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Clock Out
              </th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Duration
              </th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                Status
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="record in attendance"
              :key="record.id"
              class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              <td class="px-6 py-4 text-gray-900 dark:text-white">
                {{ formatDate(record.date) }}
              </td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">
                {{ record.clock_in_time || '--:--' }}
              </td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">
                {{ record.clock_out_time || '--:--' }}
              </td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">
                {{ calculateDuration(record.clock_in_time, record.clock_out_time) }}
              </td>
              <td class="px-6 py-4">
                <span
                  :class="getStatusBadgeClass(record.status)"
                  class="px-3 py-1 text-xs font-semibold rounded-full"
                >
                  {{ formatStatus(record.status) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAttendance, type AttendanceRecord } from '~/composables/useAttendance';

definePageMeta({
  middleware: 'auth',
  title: 'Attendance',
});

const { getMyAttendance, isLoading } = useAttendance();
const attendance = ref<AttendanceRecord[]>([]);
const dateFrom = ref('');
const dateTo = ref('');
const statusFilter = ref('');

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

const formatStatus = (status: string) => {
  return status.replace('_', ' ').toUpperCase();
};

const getStatusBadgeClass = (status: string) => {
  const statusClasses: Record<string, string> = {
    present: 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200',
    absent: 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200',
    half_day: 'bg-amber-100 dark:bg-amber-900 text-amber-800 dark:text-amber-200',
    late: 'bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-200',
  };
  return statusClasses[status] || 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200';
};

const calculateDuration = (clockIn: string | undefined, clockOut: string | undefined) => {
  if (!clockIn || !clockOut) return '--';

  const [inH, inM] = clockIn.split(':').map(Number);
  const [outH, outM] = clockOut.split(':').map(Number);

  const inMinutes = inH * 60 + inM;
  const outMinutes = outH * 60 + outM;
  const duration = outMinutes - inMinutes;

  const hours = Math.floor(duration / 60);
  const minutes = duration % 60;

  return `${hours}h ${minutes}m`;
};

const fetchAttendance = async () => {
  try {
    const response = await getMyAttendance();
    attendance.value = Array.isArray(response) ? response : [response];
  } catch (err) {
    console.error('Failed to fetch attendance:', err);
  }
};

onMounted(() => {
  fetchAttendance();
});
</script>
