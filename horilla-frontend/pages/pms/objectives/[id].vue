<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <NuxtLink
        to="/pms/objectives"
        class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <Icon name="heroicons:arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <h1 class="text-3xl font-bold text-gray-900">Objective Details</h1>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <Icon name="eos-icons:loading" class="w-8 h-8 text-blue-600 animate-spin" />
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="p-4 bg-red-100 border border-red-400 text-red-700 rounded"
    >
      {{ error }}
      <button
        @click="loadObjective"
        class="ml-4 px-3 py-1 bg-red-200 hover:bg-red-300 rounded"
      >
        Retry
      </button>
    </div>

    <!-- Content -->
    <div v-else-if="objective" class="space-y-6">
      <!-- Objective Card -->
      <div class="card">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h2 class="text-2xl font-bold text-gray-900">{{ objective.title }}</h2>
            <p class="text-gray-600 mt-2">{{ objective.description }}</p>
          </div>
          <div class="flex gap-2">
            <NuxtLink
              :to="`/pms/objectives/${objective.id}/edit`"
              class="p-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
              title="Edit"
            >
              <Icon name="heroicons:pencil" class="w-5 h-5" />
            </NuxtLink>
            <button
              @click="deleteAndGoBack"
              class="p-2 text-red-600 hover:bg-red-50 rounded transition-colors"
              title="Delete"
            >
              <Icon name="heroicons:trash" class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Status and Meta Info -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 pb-6 border-b">
          <div>
            <p class="text-xs text-gray-500 uppercase">Status</p>
            <p :class="`badge status-${objective.status.toLowerCase().replace(' ', '-')}`">
              {{ objective.status }}
            </p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase">Duration</p>
            <p class="font-semibold text-gray-900">{{ objective.duration }} {{ objective.duration_unit }}</p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase">Created</p>
            <p class="text-sm text-gray-900">{{ formatDate(objective.created_at) }}</p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase">Updated</p>
            <p class="text-sm text-gray-900">{{ formatDate(objective.updated_at) }}</p>
          </div>
        </div>

        <!-- Key Information -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-xs text-gray-500 uppercase mb-1">ID</p>
            <p class="text-gray-900">{{ objective.id }}</p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase mb-1">Status</p>
            <p class="text-gray-900">{{ objective.status }}</p>
          </div>
        </div>
      </div>

      <!-- Key Results Section -->
      <div v-if="keyResults.length > 0" class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Key Results</h3>
        <div class="space-y-3">
          <div
            v-for="kr in keyResults"
            :key="kr.id"
            class="p-4 border border-gray-200 rounded-lg"
          >
            <div class="flex justify-between items-start mb-2">
              <p class="font-medium text-gray-900">{{ kr.key_result_name }}</p>
              <span class="text-xs text-gray-500">Target: {{ kr.target_value }}</span>
            </div>
            <p class="text-sm text-gray-600">{{ kr.description }}</p>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-4">
        <NuxtLink
          to="/pms/objectives"
          class="flex-1 px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-center"
        >
          Back to List
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const route = useRoute()
const router = useRouter()
const { fetchObjective, deleteObjective, fetchEmployeeKeyResults } = useObjectives()
const { formatDate } = usePms()

const isLoading = ref(false)
const error = ref<string | null>(null)
const objective = ref(null)
const keyResults = ref([])

const objectiveId = computed(() => parseInt(route.params.id as string))

const loadObjective = async () => {
  isLoading.value = true
  error.value = null
  try {
    objective.value = await fetchObjective(objectiveId.value)
    if (objective.value) {
      // Load key results for this objective
      const results = await fetchEmployeeKeyResults({
        objective_id: objectiveId.value,
      })
      keyResults.value = results
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to load objective'
  } finally {
    isLoading.value = false
  }
}

const deleteAndGoBack = async () => {
  if (confirm('Are you sure you want to delete this objective?')) {
    isLoading.value = true
    const success = await deleteObjective(objectiveId.value)
    isLoading.value = false
    if (success) {
      await router.push('/pms/objectives')
    }
  }
}

onMounted(() => {
  loadObjective()
})
</script>
