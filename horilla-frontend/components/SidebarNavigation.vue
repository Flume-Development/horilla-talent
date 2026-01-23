<template>
  <aside class="w-64 bg-gray-900 text-white hidden md:flex flex-col">
    <!-- Logo -->
    <div class="p-6 border-b border-gray-800">
      <h1 class="text-2xl font-bold">Horilla PMS</h1>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
      <NavLink to="/pms" icon="home" label="Dashboard" />
      <NavLink to="/pms/objectives" icon="target" label="Objectives" />
      <NavLink to="/pms/my-objectives" icon="list" label="My Objectives" />
      <NavLink to="/pms/feedback" icon="message" label="Feedback" />
      <NavLink to="/pms/meetings" icon="calendar" label="Meetings" />
      <NavLink to="/pms/bonus" icon="gift" label="Bonus Points" />
      <NavLink to="/pms/analytics" icon="chart-bar" label="Analytics" />

      <!-- Divider -->
      <div class="my-4 border-t border-gray-800"></div>

      <!-- Admin Section -->
      <div v-if="authStore.employee?.is_superuser || authStore.employee?.is_staff" class="mt-6">
        <p class="px-4 py-2 text-xs font-semibold text-gray-400 uppercase">Administration</p>
        <NavLink to="/pms/question-templates" icon="document-duplicate" label="Question Templates" />
      </div>
    </nav>

    <!-- User Profile -->
    <div class="border-t border-gray-800 p-4">
      <div class="flex items-center space-x-3">
        <div class="flex-1">
          <p class="text-sm font-semibold">{{ authStore.employeeName }}</p>
          <p class="text-xs text-gray-400">{{ authStore.employee?.email }}</p>
        </div>
        <button
          @click="handleLogout"
          class="p-2 hover:bg-gray-800 rounded-lg transition-colors"
          title="Logout"
        >
          <Icon name="heroicons:arrow-left-on-rectangle" class="w-5 h-5" />
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = async () => {
  authStore.logout()
  await router.push('/login')
}
</script>

<style scoped>
aside {
  @apply flex-col;
}
</style>
