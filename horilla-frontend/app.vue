<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
const authStore = useAuthStore()
const router = useRouter()

onMounted(async () => {
  // Initialize auth state from storage
  authStore.initializeAuth()

  // Redirect to login if not authenticated and not on login page
  if (!authStore.isAuthenticated && router.currentRoute.value.path !== '/login') {
    await router.push('/login')
  }
})
</script>

<style scoped>
:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgb(219, 234, 254), 0 0 0 5px rgb(59, 130, 246);
}
</style>
