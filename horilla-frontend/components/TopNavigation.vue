<template>
  <header class="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-800">
    <div class="px-6 py-4 flex items-center justify-between">
      <!-- Breadcrumb -->
      <div class="flex items-center gap-2 text-sm">
        <NuxtLink to="/dashboard" class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300">
          Home
        </NuxtLink>
        <span class="text-gray-400 dark:text-gray-600">/</span>
        <span class="text-gray-700 dark:text-gray-300 font-medium">
          {{ currentPageTitle }}
        </span>
      </div>

      <!-- Right Side Actions -->
      <div class="flex items-center gap-4">
        <!-- Search -->
        <div class="hidden md:block">
          <input
            type="text"
            placeholder="Search..."
            class="px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- Notifications -->
        <button class="relative p-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors">
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
            />
          </svg>
          <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>

        <!-- Theme Toggle -->
        <button
          @click="toggleDarkMode"
          class="p-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
        >
          <svg
            v-if="isDarkMode"
            class="w-6 h-6"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"
            />
          </svg>
          <svg v-else class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4.293 2.293a1 1 0 011.414 0l.707.707a1 1 0 11-1.414 1.414l-.707-.707a1 1 0 010-1.414zm2.828 2.828a1 1 0 011.414 0l.707.707a1 1 0 11-1.414 1.414l-.707-.707a1 1 0 010-1.414zM10 7a3 3 0 110 6 3 3 0 010-6zm-4.293-2.293a1 1 0 011.414 0l.707.707a1 1 0 11-1.414 1.414l-.707-.707a1 1 0 010-1.414zM3.464 9.172a1 1 0 011.414 0l.707.707a1 1 0 11-1.414 1.414l-.707-.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const isDarkMode = ref(false);

const currentPageTitle = computed(() => {
  const title = route.meta.title as string | undefined;
  if (title) return title;

  // Extract title from path
  const path = route.path.split('/')[1];
  return path.charAt(0).toUpperCase() + path.slice(1);
});

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
  if (process.client) {
    document.documentElement.classList.toggle('dark');
    localStorage.setItem('darkMode', JSON.stringify(isDarkMode.value));
  }
};

onMounted(() => {
  if (process.client) {
    const stored = localStorage.getItem('darkMode');
    isDarkMode.value = stored ? JSON.parse(stored) : false;
    if (isDarkMode.value) {
      document.documentElement.classList.add('dark');
    }
  }
});
</script>
