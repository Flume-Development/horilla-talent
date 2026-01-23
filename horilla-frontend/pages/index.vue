<template>
  <div></div>
</template>

<script setup lang="ts">
const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  authStore.initializeAuth()

  if (authStore.isAuthenticated) {
    router.push('/pms')
  } else {
    router.push('/login')
  }
})
</script>
