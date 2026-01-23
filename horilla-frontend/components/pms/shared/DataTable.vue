<template>
  <div class="space-y-4">
    <!-- Filters -->
    <div v-if="showFilters" class="card">
      <div class="flex gap-4 flex-wrap items-end">
        <!-- Search -->
        <div class="flex-1 min-w-[200px]">
          <label class="block text-sm font-medium text-gray-700 mb-1">Search</label>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search..."
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- Column Filter -->
        <div v-if="columns.length > 0" class="flex-1 min-w-[200px]">
          <label class="block text-sm font-medium text-gray-700 mb-1">Filter By</label>
          <select
            v-model="filterColumn"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Columns</option>
            <option v-for="col in columns" :key="col.key" :value="col.key">
              {{ col.label }}
            </option>
          </select>
        </div>

        <!-- Reset -->
        <button
          @click="resetFilters"
          class="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
        >
          Reset
        </button>
      </div>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto card">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b">
            <th
              v-for="col in columns"
              :key="col.key"
              class="px-6 py-3 text-left font-semibold text-gray-700 cursor-pointer hover:bg-gray-50"
              @click="sortBy(col.key)"
            >
              <div class="flex items-center gap-2">
                {{ col.label }}
                <Icon
                  v-if="sortColumn === col.key"
                  :name="sortOrder === 'asc' ? 'heroicons:arrow-up' : 'heroicons:arrow-down'"
                  class="w-4 h-4"
                />
              </div>
            </th>
            <th class="px-6 py-3 text-left font-semibold text-gray-700">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, index) in filteredAndSortedData"
            :key="index"
            class="border-b hover:bg-gray-50 transition-colors"
          >
            <td v-for="col in columns" :key="col.key" class="px-6 py-4">
              {{ row[col.key] }}
            </td>
            <td class="px-6 py-4">
              <div class="flex gap-2">
                <button
                  @click="$emit('edit', row)"
                  class="text-blue-600 hover:text-blue-800"
                  title="Edit"
                >
                  <Icon name="heroicons:pencil" class="w-4 h-4" />
                </button>
                <button
                  @click="$emit('delete', row)"
                  class="text-red-600 hover:text-red-800"
                  title="Delete"
                >
                  <Icon name="heroicons:trash" class="w-4 h-4" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="filteredAndSortedData.length === 0" class="p-8 text-center">
        <p class="text-gray-500">No data available</p>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="showPagination && totalPages > 1" class="flex justify-between items-center">
      <p class="text-sm text-gray-600">
        Showing {{ startIndex + 1 }} to {{ endIndex }} of {{ data.length }} items
      </p>
      <div class="flex gap-2">
        <button
          @click="previousPage"
          :disabled="currentPage === 1"
          class="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
        >
          Previous
        </button>
        <div class="flex gap-1">
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="currentPage = page"
            :class="['px-3 py-2 rounded-lg', currentPage === page ? 'bg-blue-600 text-white' : 'border border-gray-300 hover:bg-gray-50']"
          >
            {{ page }}
          </button>
        </div>
        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '#components'

interface Column {
  key: string
  label: string
}

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
  columns: {
    type: Array as () => Column[],
    required: true,
  },
  showFilters: {
    type: Boolean,
    default: true,
  },
  showPagination: {
    type: Boolean,
    default: true,
  },
  itemsPerPage: {
    type: Number,
    default: 10,
  },
})

const emit = defineEmits(['edit', 'delete'])

const searchQuery = ref('')
const filterColumn = ref('')
const sortColumn = ref('')
const sortOrder = ref('asc')
const currentPage = ref(1)

const filteredData = computed(() => {
  return props.data.filter(row => {
    if (!searchQuery.value && !filterColumn.value) return true

    const searchStr = searchQuery.value.toLowerCase()

    if (filterColumn.value) {
      return String(row[filterColumn.value]).toLowerCase().includes(searchStr)
    }

    return Object.values(row).some(val =>
      String(val).toLowerCase().includes(searchStr)
    )
  })
})

const filteredAndSortedData = computed(() => {
  let result = [...filteredData.value]

  if (sortColumn.value) {
    result.sort((a, b) => {
      const aVal = a[sortColumn.value]
      const bVal = b[sortColumn.value]

      if (aVal < bVal) return sortOrder.value === 'asc' ? -1 : 1
      if (aVal > bVal) return sortOrder.value === 'asc' ? 1 : -1
      return 0
    })
  }

  if (props.showPagination) {
    const start = (currentPage.value - 1) * props.itemsPerPage
    const end = start + props.itemsPerPage
    return result.slice(start, end)
  }

  return result
})

const totalPages = computed(() =>
  Math.ceil(filteredData.value.length / props.itemsPerPage)
)

const startIndex = computed(() =>
  (currentPage.value - 1) * props.itemsPerPage
)

const endIndex = computed(() =>
  Math.min(startIndex.value + props.itemsPerPage, filteredData.value.length)
)

const visiblePages = computed(() => {
  const pages = []
  const maxPages = 5
  const half = Math.floor(maxPages / 2)

  let start = Math.max(1, currentPage.value - half)
  let end = Math.min(totalPages.value, start + maxPages - 1)

  if (end - start + 1 < maxPages) {
    start = Math.max(1, end - maxPages + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  return pages
})

const sortBy = (column: string) => {
  if (sortColumn.value === column) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortColumn.value = column
    sortOrder.value = 'asc'
  }
}

const resetFilters = () => {
  searchQuery.value = ''
  filterColumn.value = ''
  sortColumn.value = ''
  sortOrder.value = 'asc'
  currentPage.value = 1
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}
</script>
