import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const currentTerm = ref('Term 1')
  const terms = ref(['Term 1', 'Term 2', 'Term 3'])
  const currentYear = ref(new Date().getFullYear())
  const years = ref([new Date().getFullYear() - 1, new Date().getFullYear(), new Date().getFullYear() + 1])

  return { currentTerm, terms, currentYear, years }
})
