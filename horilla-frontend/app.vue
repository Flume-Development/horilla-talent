<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()

// Check if user is already authenticated on app load
onMounted(() => {
  authStore.checkAuthStatus()
})
</script>
