<template>
  <div class="space-y-6 max-w-4xl mx-auto">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <NuxtLink
        :to="`/pms/meetings/${meetingId}/answers`"
        class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <Icon name="heroicons:arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <h1 class="text-3xl font-bold text-gray-900">Edit Meeting Response</h1>
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
        @click="loadAnswer"
        class="ml-4 px-3 py-1 bg-red-200 hover:bg-red-300 rounded"
      >
        Retry
      </button>
    </div>

    <!-- Answer Edit Form -->
    <form v-else-if="answer" @submit.prevent="submitEdit" class="card space-y-6">
      <!-- Question Display -->
      <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
        <h3 class="font-semibold text-gray-900 mb-2">{{ answer.question }}</h3>
        <p class="text-xs text-gray-600">
          Type: <span class="font-medium">{{ answer.question_type }}</span>
        </p>
      </div>

      <!-- Answer Input -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Your Response</label>

        <!-- Text Answer -->
        <textarea
          v-if="answer.question_type === 'Text'"
          v-model="editedAnswer"
          rows="6"
          placeholder="Enter your response"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>

        <!-- Rating Answer -->
        <div v-else-if="answer.question_type === 'Rating'" class="flex gap-2">
          <button
            v-for="rating in 5"
            :key="rating"
            type="button"
            @click="editedAnswer = rating.toString()"
            :class="[
              'w-12 h-12 rounded-lg transition-colors font-semibold text-lg',
              editedAnswer === rating.toString()
                ? 'bg-yellow-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-yellow-300'
            ]"
          >
            {{ rating }}
          </button>
        </div>

        <!-- Boolean Answer -->
        <div v-else-if="answer.question_type === 'Boolean'" class="flex gap-4">
          <label class="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              :value="'true'"
              v-model="editedAnswer"
              class="w-4 h-4"
            />
            <span class="text-gray-700">Yes</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              :value="'false'"
              v-model="editedAnswer"
              class="w-4 h-4"
            />
            <span class="text-gray-700">No</span>
          </label>
        </div>

        <!-- Multi-choice Answer -->
        <div v-else-if="answer.question_type === 'Multi-choice'" class="space-y-2">
          <label
            v-for="option in getOptions(answer)"
            :key="option"
            class="flex items-center gap-2 cursor-pointer"
          >
            <input
              type="radio"
              :value="option"
              v-model="editedAnswer"
              class="w-4 h-4"
            />
            <span class="text-gray-700">{{ option }}</span>
          </label>
        </div>

        <!-- Likert Answer -->
        <div v-else-if="answer.question_type === 'Likert'" class="grid grid-cols-5 gap-2 text-center text-xs">
          <div v-for="i in 5" :key="i" class="mb-2">
            <button
              type="button"
              @click="editedAnswer = i.toString()"
              :class="[
                'w-full py-2 px-1 rounded border transition-colors font-semibold',
                editedAnswer === i.toString()
                  ? 'bg-blue-500 border-blue-500 text-white'
                  : 'bg-white border-gray-300 text-gray-700 hover:border-blue-500'
              ]"
            >
              {{ i }}
            </button>
            <p class="text-gray-600 text-xs mt-1">
              {{ likertLabels[i - 1] }}
            </p>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-4 pt-6 border-t">
        <button
          type="submit"
          class="flex-1 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          :disabled="isSubmitting"
        >
          <span v-if="isSubmitting" class="flex items-center justify-center gap-2">
            <Icon name="eos-icons:loading" class="w-5 h-5 animate-spin" />
            Updating...
          </span>
          <span v-else>Update Response</span>
        </button>
        <NuxtLink
          :to="`/pms/meetings/${meetingId}/answers`"
          class="flex-1 px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-center"
        >
          Cancel
        </NuxtLink>
      </div>

      <!-- Error Message -->
      <div v-if="submitError" class="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ submitError }}
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const route = useRoute()
const router = useRouter()

const isLoading = ref(false)
const isSubmitting = ref(false)
const error = ref<string | null>(null)
const submitError = ref<string | null>(null)

const meetingId = computed(() => parseInt(route.params.id as string))
const answerId = computed(() => parseInt(route.params.answerId as string))

const answer = ref(null)
const editedAnswer = ref('')

const likertLabels = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']

const getOptions = (answer: any) => {
  if (answer.options && typeof answer.options === 'string') {
    return answer.options.split(',').map((opt: string) => opt.trim())
  }
  if (Array.isArray(answer.options)) {
    return answer.options
  }
  return []
}

const loadAnswer = async () => {
  isLoading.value = true
  error.value = null
  try {
    // TODO: Implement fetching single answer
    // For now, placeholder
    answer.value = {
      id: answerId.value,
      question: 'Sample Meeting Question',
      question_type: 'Text',
      answer: 'Sample Response',
      created_at: new Date().toISOString(),
    }
    editedAnswer.value = answer.value.answer
  } catch (err: any) {
    error.value = err.message || 'Failed to load response'
  } finally {
    isLoading.value = false
  }
}

const submitEdit = async () => {
  if (!editedAnswer.value) {
    submitError.value = 'Please provide a response'
    return
  }

  isSubmitting.value = true
  submitError.value = null

  try {
    // TODO: Implement updating answer API call
    // const success = await updateMeetingAnswer(answerId.value, { answer: editedAnswer.value })
    // if (success) {
    await router.push(`/pms/meetings/${meetingId.value}/answers`)
    // } else {
    //   submitError.value = 'Failed to update response'
    // }
  } catch (err: any) {
    submitError.value = err.message || 'Failed to update response'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  loadAnswer()
})
</script>
