import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const currentTerm = ref('Term 1')
  const terms = ref(['Term 1', 'Term 2', 'Term 3'])

  return { currentTerm, terms }
})
