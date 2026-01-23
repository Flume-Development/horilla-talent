<template>
  <form @submit.prevent="submitAnswers" class="space-y-6">
    <!-- Instructions -->
    <div v-if="instructions" class="p-4 bg-blue-50 border border-blue-200 text-blue-900 rounded-lg">
      <p class="text-sm">{{ instructions }}</p>
    </div>

    <!-- Questions List -->
    <div v-if="questions.length === 0" class="text-center py-8">
      <p class="text-gray-500">No questions available</p>
    </div>

    <div v-else class="space-y-6">
      <div
        v-for="(question, index) in questions"
        :key="question.id"
        class="p-6 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
      >
        <!-- Question Number and Text -->
        <div class="mb-4">
          <label class="block font-semibold text-gray-900 mb-2">
            {{ index + 1 }}. {{ question.question }}
            <span v-if="question.required" class="text-red-500">*</span>
          </label>
          <p v-if="question.description" class="text-sm text-gray-600">
            {{ question.description }}
          </p>
        </div>

        <!-- Text Question -->
        <div v-if="question.question_type === 'Text'">
          <textarea
            v-model="answers[question.id]"
            :required="question.required"
            rows="4"
            placeholder="Enter your answer"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          ></textarea>
        </div>

        <!-- Rating Question -->
        <div v-else-if="question.question_type === 'Rating'">
          <div class="flex gap-2">
            <button
              v-for="rating in 5"
              :key="rating"
              type="button"
              @click="answers[question.id] = rating.toString()"
              :class="[
                'w-10 h-10 rounded-lg transition-colors font-semibold',
                answers[question.id] === rating.toString()
                  ? 'bg-yellow-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-yellow-300'
              ]"
            >
              {{ rating }}
            </button>
          </div>
          <p class="text-xs text-gray-500 mt-2">1 = Poor, 5 = Excellent</p>
        </div>

        <!-- Boolean Question -->
        <div v-else-if="question.question_type === 'Boolean'">
          <div class="flex gap-4">
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                :value="'true'"
                :name="`question_${question.id}`"
                v-model="answers[question.id]"
                :required="question.required"
                class="w-4 h-4"
              />
              <span class="text-gray-700">Yes</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                :value="'false'"
                :name="`question_${question.id}`"
                v-model="answers[question.id]"
                :required="question.required"
                class="w-4 h-4"
              />
              <span class="text-gray-700">No</span>
            </label>
          </div>
        </div>

        <!-- Multi-choice Question -->
        <div v-else-if="question.question_type === 'Multi-choice'">
          <div class="space-y-2">
            <label
              v-for="option in getOptions(question)"
              :key="option"
              class="flex items-center gap-2 cursor-pointer"
            >
              <input
                type="radio"
                :value="option"
                :name="`question_${question.id}`"
                v-model="answers[question.id]"
                :required="question.required"
                class="w-4 h-4"
              />
              <span class="text-gray-700">{{ option }}</span>
            </label>
          </div>
        </div>

        <!-- Likert Scale Question -->
        <div v-else-if="question.question_type === 'Likert'">
          <div class="grid grid-cols-5 gap-2 text-center text-xs">
            <div v-for="i in 5" :key="i" class="mb-2">
              <button
                type="button"
                @click="answers[question.id] = i.toString()"
                :class="[
                  'w-full py-2 px-1 rounded border transition-colors font-semibold',
                  answers[question.id] === i.toString()
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

        <!-- Unknown Type -->
        <div v-else>
          <p class="text-sm text-red-600">Unknown question type: {{ question.question_type }}</p>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-4 pt-6 border-t">
      <button
        type="submit"
        class="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium flex items-center justify-center gap-2"
        :disabled="isLoading"
      >
        <Icon v-if="isLoading" name="eos-icons:loading" class="w-5 h-5 animate-spin" />
        <span v-if="isLoading">Submitting...</span>
        <span v-else>{{ submitLabel }}</span>
      </button>
      <button
        type="button"
        @click="$emit('cancel')"
        class="flex-1 px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium"
      >
        Cancel
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
      {{ error }}
    </div>
  </form>
</template>

<script setup lang="ts">
import { Icon } from '#components'

const props = defineProps({
  questions: {
    type: Array,
    required: true,
  },
  initialAnswers: {
    type: Object,
    default: () => ({}),
  },
  instructions: {
    type: String,
    default: '',
  },
  submitLabel: {
    type: String,
    default: 'Submit Answers',
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: null,
  },
})

const emit = defineEmits(['submit', 'cancel'])

const answers = ref({ ...props.initialAnswers })

const likertLabels = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']

const getOptions = (question: any) => {
  if (question.options && typeof question.options === 'string') {
    return question.options.split(',').map((opt: string) => opt.trim())
  }
  if (Array.isArray(question.options)) {
    return question.options
  }
  return []
}

const submitAnswers = () => {
  // Validate required fields
  const unansweredRequired = props.questions.filter(
    q => q.required && !answers.value[q.id]
  )

  if (unansweredRequired.length > 0) {
    alert(`Please answer all required questions: ${unansweredRequired.map(q => q.question).join(', ')}`)
    return
  }

  emit('submit', answers.value)
}

watch(
  () => props.initialAnswers,
  (newAnswers) => {
    answers.value = { ...newAnswers }
  }
)
</script>
