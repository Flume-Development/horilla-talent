<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <NuxtLink
          :to="`/pms/feedback/${feedbackId}`"
          class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <Icon name="heroicons:arrow-left" class="w-6 h-6" />
        </NuxtLink>
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Feedback Answers</h1>
          <p class="text-gray-600 mt-1">{{ feedbackTitle }}</p>
        </div>
      </div>
      <NuxtLink
        :to="`/pms/feedback/${feedbackId}/answer`"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
      >
        <Icon name="heroicons:plus" class="w-4 h-4" />
        New Answer
      </NuxtLink>
    </div>

    <!-- Filters -->
    <div class="card">
      <div class="flex gap-4 flex-wrap">
        <div class="flex-1 min-w-[200px]">
          <label class="block text-sm font-medium text-gray-700 mb-1">Search Question</label>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search questions..."
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div class="flex gap-2 items-end">
          <button
            @click="resetFilters"
            class="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Reset
          </button>
        </div>
      </div>
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
        @click="loadAnswers"
        class="ml-4 px-3 py-1 bg-red-200 hover:bg-red-300 rounded"
      >
        Retry
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredAnswers.length === 0" class="card empty-state">
      <Icon name="heroicons:chat-bubble-left" class="empty-state-icon" />
      <p class="empty-state-text">No answers submitted yet</p>
      <NuxtLink
        :to="`/pms/feedback/${feedbackId}/answer`"
        class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors inline-block"
      >
        Submit Answers
      </NuxtLink>
    </div>

    <!-- Answers List -->
    <div v-else class="space-y-4">
      <div
        v-for="answer in filteredAnswers"
        :key="answer.id"
        class="card"
      >
        <div class="flex justify-between items-start mb-3">
          <div class="flex-1">
            <h3 class="font-semibold text-gray-900">{{ answer.question }}</h3>
            <p class="text-sm text-gray-600 mt-1">
              <span class="inline-block px-2 py-1 bg-gray-100 rounded text-xs mr-2">
                Type: {{ answer.question_type }}
              </span>
              <span class="inline-block px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                {{ answer.answer_by || 'Anonymous' }}
              </span>
            </p>
          </div>
          <div class="flex gap-2">
            <NuxtLink
              :to="`/pms/feedback/${feedbackId}/answers/${answer.id}/edit`"
              class="p-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
              title="Edit"
            >
              <Icon name="heroicons:pencil" class="w-5 h-5" />
            </NuxtLink>
            <button
              @click="deleteAnswer(answer.id)"
              class="p-2 text-red-600 hover:bg-red-50 rounded transition-colors"
              title="Delete"
            >
              <Icon name="heroicons:trash" class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Answer Content -->
        <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
          <div v-if="answer.question_type === 'Rating'">
            <div class="flex gap-1">
              <span
                v-for="i in 5"
                :key="i"
                :class="[
                  'w-8 h-8 flex items-center justify-center rounded',
                  parseInt(answer.answer) >= i
                    ? 'bg-yellow-500 text-white'
                    : 'bg-gray-300'
                ]"
              >
                ★
              </span>
            </div>
            <p class="text-sm text-gray-600 mt-2">Rating: {{ answer.answer }}/5</p>
          </div>

          <div v-else-if="answer.question_type === 'Likert'">
            <div class="flex gap-2">
              <span
                v-for="i in 5"
                :key="i"
                :class="[
                  'px-3 py-1 rounded text-sm',
                  parseInt(answer.answer) === i
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-300'
                ]"
              >
                {{ i }}
              </span>
            </div>
            <p class="text-sm text-gray-600 mt-2">
              {{ likertLabels[parseInt(answer.answer) - 1] }}
            </p>
          </div>

          <div v-else-if="answer.question_type === 'Boolean'">
            <span
              :class="[
                'inline-block px-3 py-1 rounded text-sm font-semibold',
                answer.answer === 'true'
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              ]"
            >
              {{ answer.answer === 'true' ? 'Yes' : 'No' }}
            </span>
          </div>

          <div v-else class="text-gray-900 whitespace-pre-wrap">
            {{ answer.answer }}
          </div>
        </div>

        <!-- Metadata -->
        <div class="mt-3 text-xs text-gray-500 flex gap-4">
          <span>📅 {{ formatDate(answer.created_at) }}</span>
          <span v-if="answer.updated_at && answer.updated_at !== answer.created_at">
            ✏️ Updated: {{ formatDate(answer.updated_at) }}
          </span>
        </div>
      </div>
    </div>

    <!-- Summary Stats -->
    <div v-if="answers.length > 0" class="card bg-blue-50 border border-blue-200">
      <h3 class="font-semibold text-blue-900 mb-3">Summary</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <div>
          <p class="text-blue-600 mb-1">Total Answers</p>
          <p class="text-2xl font-bold text-blue-900">{{ answers.length }}</p>
        </div>
        <div>
          <p class="text-blue-600 mb-1">Questions Answered</p>
          <p class="text-2xl font-bold text-blue-900">
            {{ new Set(answers.map(a => a.question_id)).size }} / {{ totalQuestions }}
          </p>
        </div>
        <div>
          <p class="text-blue-600 mb-1">Last Updated</p>
          <p class="text-sm text-blue-900">{{ formatDate(lastUpdated) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const route = useRoute()
const router = useRouter()
const { fetchFeedbackAnswers } = useFeedback()
const { formatDate } = usePms()

const isLoading = ref(false)
const error = ref<string | null>(null)
const searchQuery = ref('')

const feedbackId = computed(() => parseInt(route.params.id as string))
const feedbackTitle = ref('')
const answers = ref([])
const totalQuestions = ref(0)

const likertLabels = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']

const filteredAnswers = computed(() => {
  if (!searchQuery.value) return answers.value

  const query = searchQuery.value.toLowerCase()
  return answers.value.filter(answer =>
    answer.question.toLowerCase().includes(query) ||
    answer.answer.toString().toLowerCase().includes(query)
  )
})

const lastUpdated = computed(() => {
  if (answers.value.length === 0) return new Date().toISOString()
  const dates = answers.value.map(a => new Date(a.updated_at || a.created_at))
  return new Date(Math.max(...dates.map(d => d.getTime()))).toISOString()
})

const loadAnswers = async () => {
  isLoading.value = true
  error.value = null
  try {
    // TODO: Also fetch feedback title
    // Fetch answers for this feedback cycle
    const fetchedAnswers = await fetchFeedbackAnswers(feedbackId.value)
    answers.value = fetchedAnswers

    // Count unique questions
    totalQuestions.value = new Set(fetchedAnswers.map(a => a.question_id)).size
  } catch (err: any) {
    error.value = err.message || 'Failed to load answers'
  } finally {
    isLoading.value = false
  }
}

const deleteAnswer = async (answerId: number) => {
  if (confirm('Are you sure you want to delete this answer?')) {
    isLoading.value = true
    try {
      // TODO: Implement delete answer API call
      await loadAnswers()
    } catch (err: any) {
      error.value = err.message || 'Failed to delete answer'
    } finally {
      isLoading.value = false
    }
  }
}

const resetFilters = () => {
  searchQuery.value = ''
}

onMounted(() => {
  loadAnswers()
})
</script>
