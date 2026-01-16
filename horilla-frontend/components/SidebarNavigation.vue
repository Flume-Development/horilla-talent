<template>
  <aside
    class="w-64 bg-white dark:bg-gray-900 shadow-lg flex flex-col h-screen border-r border-gray-200 dark:border-gray-800"
  >
    <!-- Logo Section -->
    <div class="px-6 py-8 border-b border-gray-200 dark:border-gray-800">
      <NuxtLink to="/dashboard" class="flex items-center gap-2">
        <div
          class="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center text-white font-bold"
        >
          H
        </div>
        <div>
          <h1 class="text-lg font-bold text-gray-900 dark:text-white">
            Horilla
          </h1>
          <p class="text-xs text-gray-500 dark:text-gray-400">HR System</p>
        </div>
      </NuxtLink>
    </div>

    <!-- Navigation Menu -->
    <nav class="flex-1 overflow-y-auto px-4 py-6">
      <div class="space-y-2">
        <NuxtLink
          v-for="item in navigationItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          :class="{
            'bg-blue-50 dark:bg-blue-900 text-blue-600 dark:text-blue-300':
              isActive(item.path),
          }"
        >
          <component :is="item.icon" class="w-5 h-5" />
          <span class="font-medium">{{ item.label }}</span>
        </NuxtLink>
      </div>
    </nav>

    <!-- User Profile Section -->
    <div class="px-4 py-4 border-t border-gray-200 dark:border-gray-800">
      <div
        class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer transition-colors"
        @click="showUserMenu = !showUserMenu"
      >
        <img
          v-if="authStore.employee?.profile_image"
          :src="authStore.employee.profile_image"
          :alt="authStore.employeeName"
          class="w-10 h-10 rounded-full object-cover"
        />
        <div v-else class="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold">
          {{ getInitials(authStore.employeeName) }}
        </div>
        <div class="flex-1">
          <p class="text-sm font-medium text-gray-900 dark:text-white">
            {{ authStore.employeeName }}
          </p>
          <p class="text-xs text-gray-500 dark:text-gray-400">
            {{ authStore.employee?.email }}
          </p>
        </div>
      </div>

      <!-- User Menu Dropdown -->
      <div v-if="showUserMenu" class="mt-2 space-y-1">
        <NuxtLink
          to="/profile"
          class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded transition-colors"
        >
          Profile
        </NuxtLink>
        <NuxtLink
          to="/settings"
          class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded transition-colors"
        >
          Settings
        </NuxtLink>
        <button
          @click="logout"
          class="w-full text-left px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900 rounded transition-colors"
        >
          Logout
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '~/stores/auth';
import { useRouter, useRoute } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const showUserMenu = ref(false);

const navigationItems = [
  {
    label: 'Dashboard',
    path: '/dashboard',
    icon: 'svg-icon-dashboard',
  },
  {
    label: 'Employees',
    path: '/employees',
    icon: 'svg-icon-users',
  },
  {
    label: 'Attendance',
    path: '/attendance',
    icon: 'svg-icon-calendar',
  },
  {
    label: 'Leave',
    path: '/leave',
    icon: 'svg-icon-briefcase',
  },
  {
    label: 'Payroll',
    path: '/payroll',
    icon: 'svg-icon-cash',
  },
  {
    label: 'Projects',
    path: '/projects',
    icon: 'svg-icon-folder',
  },
  {
    label: 'Reports',
    path: '/reports',
    icon: 'svg-icon-chart',
  },
];

const isActive = (path: string) => {
  return route.path === path || route.path.startsWith(path + '/');
};

const getInitials = (name: string) => {
  return name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
};

const logout = async () => {
  authStore.logout();
  await router.push('/login');
};
</script>
