import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiFetch } from '@/services/api'

export const useAppStore = defineStore('app', () => {
  const currentTerm = ref('Term 1')
  const terms = ref(['Term 1', 'Term 2', 'Term 3'])
  const currentYear = ref(new Date().getFullYear())
  const years = ref([new Date().getFullYear() - 1, new Date().getFullYear(), new Date().getFullYear() + 1])
  const termSource = ref(null)   // 'configured' | 'default'

  // Auto-detect the active term/year from the academic calendar (Kenyan term
  // dates by default, or whatever has been configured on the Calendar page).
  async function loadCurrentTerm() {
    try {
      const data = await apiFetch('/api/calendar/current-term')
      if (data?.term) currentTerm.value = data.term
      if (data?.academic_year) currentYear.value = data.academic_year
      termSource.value = data?.source ?? null
    } catch {
      /* keep defaults if the call fails */
    }
  }

  return { currentTerm, terms, currentYear, years, termSource, loadCurrentTerm }
})
