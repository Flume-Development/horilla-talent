<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold text-gray-900">Question Templates</h1>
      <NuxtLink
        to="/pms/question-templates/create"
        class="btn-primary flex items-center space-x-2"
      >
        <Icon name="heroicons:plus" class="w-5 h-5" />
        <span>New Template</span>
      </NuxtLink>
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
        @click="loadTemplates"
        class="ml-4 px-3 py-1 bg-red-200 hover:bg-red-300 rounded"
      >
        Retry
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="templates.length === 0" class="card empty-state">
      <Icon name="heroicons:document" class="empty-state-icon" />
      <p class="empty-state-text">No question templates found</p>
    </div>

    <!-- Templates Grid -->
    <div v-else class="grid gap-4">
      <div
        v-for="template in templates"
        :key="template.id"
        class="card hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start mb-3">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900">{{ template.title }}</h3>
            <p class="text-sm text-gray-600 mt-1">{{ template.description }}</p>
          </div>
          <div class="flex gap-2 ml-4">
            <NuxtLink
              :to="`/pms/question-templates/${template.id}/edit`"
              class="p-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
              title="Edit"
            >
              <Icon name="heroicons:pencil" class="w-5 h-5" />
            </NuxtLink>
            <button
              @click="deleteTemplate(template.id)"
              class="p-2 text-red-600 hover:bg-red-50 rounded transition-colors"
              title="Delete"
            >
              <Icon name="heroicons:trash" class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Template Info -->
        <div class="text-xs text-gray-500 mb-3">
          <span>Questions: {{ template.questions_count || 0 }}</span>
          <span class="mx-2">•</span>
          <span>Created: {{ formatDate(template.created_at) }}</span>
        </div>

        <!-- View Details Link -->
        <NuxtLink
          :to="`/pms/question-templates/${template.id}`"
          class="text-sm text-blue-600 hover:text-blue-800"
        >
          View Questions →
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const { fetchQuestionTemplates } = useFeedback()
const { formatDate } = usePms()

const isLoading = ref(false)
const error = ref<string | null>(null)
const templates = ref([])

const loadTemplates = async () => {
  isLoading.value = true
  error.value = null
  try {
    templates.value = await fetchQuestionTemplates()
  } catch (err: any) {
    error.value = err.message || 'Failed to load templates'
  } finally {
    isLoading.value = false
  }
}

const deleteTemplate = async (id: number) => {
  if (confirm('Are you sure you want to delete this template?')) {
    isLoading.value = true
    try {
      // TODO: Implement delete API call
      await loadTemplates()
    } catch (err: any) {
      error.value = err.message || 'Failed to delete template'
    } finally {
      isLoading.value = false
    }
  }
}

onMounted(() => {
  loadTemplates()
})
</script>
