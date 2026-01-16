<template>
  <div class="w-full max-w-md">
    <div class="bg-white dark:bg-gray-900 rounded-lg shadow-lg p-8">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div
          class="w-16 h-16 rounded-lg bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center text-white font-bold text-2xl mx-auto mb-4"
        >
          H
        </div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          Horilla HR
        </h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">
          Sign in to your account
        </p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleLogin" class="space-y-6">
        <!-- Username -->
        <div>
          <label
            for="username"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Username
          </label>
          <input
            v-model="form.username"
            id="username"
            type="text"
            placeholder="Enter your username"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
            required
          />
        </div>

        <!-- Password -->
        <div>
          <label
            for="password"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Password
          </label>
          <input
            v-model="form.password"
            id="password"
            type="password"
            placeholder="Enter your password"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
            required
          />
        </div>

        <!-- Remember Me -->
        <div class="flex items-center gap-2">
          <input
            v-model="form.rememberMe"
            id="remember"
            type="checkbox"
            class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <label
            for="remember"
            class="text-sm text-gray-600 dark:text-gray-400 cursor-pointer"
          >
            Remember me
          </label>
        </div>

        <!-- Error Message -->
        <div
          v-if="authStore.error"
          class="p-3 rounded-lg bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-800"
        >
          <p class="text-sm text-red-600 dark:text-red-300">
            {{ authStore.error }}
          </p>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="authStore.isLoading"
          class="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          <span v-if="authStore.isLoading" class="inline-block animate-spin">
            ⏳
          </span>
          {{ authStore.isLoading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <!-- Footer -->
      <div class="mt-6 text-center text-sm text-gray-600 dark:text-gray-400">
        <p>
          <NuxtLink
            to="/forgot-password"
            class="text-blue-600 dark:text-blue-400 hover:underline"
          >
            Forgot password?
          </NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '~/stores/auth';
import { useRouter } from 'vue-router';

definePageMeta({
  layout: 'blank',
});

const authStore = useAuthStore();
const router = useRouter();

const form = ref({
  username: '',
  password: '',
  rememberMe: false,
});

const handleLogin = async () => {
  authStore.clearError();

  if (!form.value.username || !form.value.password) {
    authStore.error = 'Username and password are required';
    return;
  }

  const success = await authStore.login(
    form.value.username,
    form.value.password
  );

  if (success) {
    await router.push('/dashboard');
  }
};

// Redirect to dashboard if already authenticated
onMounted(() => {
  if (authStore.isAuthenticated) {
    router.push('/dashboard');
  }
});
</script>
