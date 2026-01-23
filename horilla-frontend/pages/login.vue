<template>
  <div
    class="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center px-4"
  >
    <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Horilla PMS</h1>
        <p class="text-gray-600 mt-2">Performance Management System</p>
      </div>

      <!-- Error Message -->
      <div
        v-if="authStore.error"
        class="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded"
      >
        {{ authStore.error }}
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="space-y-4">
        <!-- Username -->
        <div>
          <label for="username" class="form-label">Username</label>
          <input
            id="username"
            v-model="username"
            type="text"
            class="form-input"
            placeholder="Enter your username"
            required
          />
        </div>

        <!-- Password -->
        <div>
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            class="form-input"
            placeholder="Enter your password"
            required
          />
        </div>

        <!-- Remember Me -->
        <div class="flex items-center">
          <input
            id="remember"
            type="checkbox"
            class="rounded border-gray-300"
          />
          <label for="remember" class="ml-2 text-sm text-gray-600">
            Remember me
          </label>
        </div>

        <!-- Login Button -->
        <button
          type="submit"
          :disabled="authStore.isLoading"
          class="w-full form-button flex items-center justify-center space-x-2 disabled:opacity-50"
        >
          <Icon
            v-if="authStore.isLoading"
            name="eos-icons:loading"
            class="w-5 h-5"
          />
          <span>{{ authStore.isLoading ? 'Logging in...' : 'Login' }}</span>
        </button>
      </form>

      <!-- Footer -->
      <p class="text-center text-sm text-gray-600 mt-4">
        © 2024 Horilla. All rights reserved.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

definePageMeta({
  layout: 'blank',
})

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')

const handleLogin = async () => {
  const success = await authStore.login(username.value, password.value)

  if (success) {
    // Clear form
    username.value = ''
    password.value = ''
    // Redirect to dashboard
    await router.push('/pms')
  }
}
</script>
