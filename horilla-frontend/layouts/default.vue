<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <SidebarNavigation />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Top Navigation -->
      <TopNavigation />

      <!-- Page Content -->
      <main class="flex-1 overflow-auto">
        <div class="p-6">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import SidebarNavigation from '~/components/SidebarNavigation.vue'
import TopNavigation from '~/components/TopNavigation.vue'

const authStore = useAuthStore()

onMounted(async () => {
  // Initialize auth on app load
  authStore.initializeAuth()
})
</script>
