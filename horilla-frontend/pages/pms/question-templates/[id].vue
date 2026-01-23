<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <NuxtLink
        to="/pms/question-templates"
        class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <Icon name="heroicons:arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <h1 class="text-3xl font-bold text-gray-900">Question Template</h1>
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
        @click="loadTemplate"
        class="ml-4 px-3 py-1 bg-red-200 hover:bg-red-300 rounded"
      >
        Retry
      </button>
    </div>

    <!-- Content -->
    <div v-else-if="template" class="space-y-6">
      <!-- Template Info Card -->
      <div class="card">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h2 class="text-2xl font-bold text-gray-900">{{ template.title }}</h2>
            <p class="text-gray-600 mt-2">{{ template.description }}</p>
          </div>
          <div class="flex gap-2">
            <NuxtLink
              :to="`/pms/question-templates/${template.id}/edit`"
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

        <!-- Template Meta -->
        <div class="grid grid-cols-2 gap-4 pt-4 border-t">
          <div>
            <p class="text-xs text-gray-500 uppercase mb-1">Created</p>
            <p class="text-sm text-gray-900">{{ formatDate(template.created_at) }}</p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase mb-1">ID</p>
            <p class="text-sm text-gray-900">{{ template.id }}</p>
          </div>
        </div>
      </div>

      <!-- Questions Section -->
      <div class="card">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Questions ({{ questions.length }})</h3>
          <NuxtLink
            :to="`/pms/question-templates/${template.id}/add-question`"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm flex items-center gap-2"
          >
            <Icon name="heroicons:plus" class="w-4 h-4" />
            Add Question
          </NuxtLink>
        </div>

        <div v-if="questions.length === 0" class="text-center py-8">
          <p class="text-gray-500">No questions in this template yet</p>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="(question, index) in questions"
            :key="question.id"
            class="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <p class="font-semibold text-gray-900">{{ index + 1 }}. {{ question.question }}</p>
                <p class="text-sm text-gray-600 mt-1">Type: <span class="font-medium">{{ question.question_type }}</span></p>
              </div>
              <button
                @click="deleteQuestion(question.id)"
                class="p-2 text-red-600 hover:bg-red-50 rounded transition-colors"
                title="Delete"
              >
                <Icon name="heroicons:trash" class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-4">
        <NuxtLink
          to="/pms/question-templates"
          class="flex-1 px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-center"
        >
          Back to Templates
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const route = useRoute()
const router = useRouter()
const { fetchQuestionTemplates, fetchQuestions } = useFeedback()
const { formatDate } = usePms()

const isLoading = ref(false)
const error = ref<string | null>(null)
const template = ref(null)
const questions = ref([])

const templateId = computed(() => parseInt(route.params.id as string))

const loadTemplate = async () => {
  isLoading.value = true
  error.value = null
  try {
    const templates = await fetchQuestionTemplates()
    template.value = templates.find(t => t.id === templateId.value) || null

    if (template.value) {
      questions.value = await fetchQuestions(templateId.value)
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to load template'
  } finally {
    isLoading.value = false
  }
}

const deleteQuestion = async (questionId: number) => {
  if (confirm('Are you sure you want to delete this question?')) {
    try {
      // TODO: Implement delete question API call
      await loadTemplate()
    } catch (err: any) {
      error.value = err.message || 'Failed to delete question'
    }
  }
}

const deleteAndGoBack = async () => {
  if (confirm('Are you sure you want to delete this template?')) {
    try {
      // TODO: Implement delete template API call
      await router.push('/pms/question-templates')
    } catch (err: any) {
      error.value = err.message || 'Failed to delete template'
    }
  }
}

onMounted(() => {
  loadTemplate()
})
</script>
