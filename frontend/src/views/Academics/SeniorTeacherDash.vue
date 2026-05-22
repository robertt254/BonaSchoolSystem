<template>
  <div class="max-w-7xl mx-auto space-y-6">

    <!-- Grade tabs + mode toggle -->
    <div class="bg-white rounded-[12px] border border-[#E2E8F0] p-4 flex flex-col gap-4">
      <div class="flex flex-wrap gap-2">
        <button
          v-for="grade in cbcGrades"
          :key="grade"
          @click="selectGrade(grade)"
          :class="[
            'px-4 py-2.5 rounded-[10px] text-sm font-bold whitespace-nowrap transition-all',
            selectedGrade === grade
              ? 'bg-school-navy text-white shadow-sm'
              : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900',
          ]"
        >{{ grade }}</button>
      </div>

      <!-- Mode + subject -->
      <div class="flex flex-wrap items-end gap-4">
        <div>
          <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Learning Area</label>
          <select
            v-model="selectedArea"
            @change="loadBulkData"
            class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple"
          >
            <option v-for="a in learningAreas" :key="a" :value="a">{{ a }}</option>
          </select>
        </div>
        <div class="flex gap-2">
          <button
            @click="viewMode = 'bulk'"
            :class="viewMode === 'bulk' ? 'bg-school-purple text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'"
            class="px-4 py-2.5 rounded-lg text-sm font-bold transition"
          >Bulk Entry</button>
          <button
            @click="viewMode = 'list'"
            :class="viewMode === 'list' ? 'bg-school-purple text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'"
            class="px-4 py-2.5 rounded-lg text-sm font-bold transition"
          >Student List</button>
        </div>
        <div class="flex-1"></div>
        <div class="relative">
          <svg class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search student…"
            class="pl-9 pr-4 py-2.5 text-sm border border-[#E2E8F0] rounded-lg focus:outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple w-56"
          />
        </div>
      </div>
    </div>

    <!-- BULK ENTRY GRID -->
    <div v-if="viewMode === 'bulk'" class="bg-white rounded-[12px] border border-[#E2E8F0] overflow-hidden">
      <div class="border-b border-slate-100 px-6 py-4 bg-slate-50 flex items-center justify-between">
        <div>
          <h3 class="font-bold text-slate-800">{{ selectedGrade }} · {{ appStore.currentTerm }} · {{ selectedArea }}</h3>
          <p class="text-xs text-slate-400 mt-0.5">{{ filteredBulk.length }} students — click a cell or use the dropdown to enter scores</p>
        </div>
        <button
          @click="saveBulk"
          :disabled="bulkSaving || !hasPendingChanges"
          class="bg-school-purple text-white px-5 py-2 rounded-lg text-sm font-bold hover:bg-school-purple-l transition disabled:opacity-40 flex items-center gap-2"
        >
          <svg v-if="bulkSaving" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z" stroke-dasharray="50" stroke-dashoffset="50"/></svg>
          {{ bulkSaving ? 'Saving…' : 'Save All' }}
        </button>
      </div>

      <div v-if="loadingBulk" class="py-16 flex justify-center">
        <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
      </div>

      <div v-else-if="filteredBulk.length === 0" class="py-12 text-center text-slate-400 text-sm">
        No students in {{ selectedGrade }}.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200 text-[11px] font-bold uppercase tracking-wider text-slate-400">
              <th class="text-left px-6 py-3 w-8">#</th>
              <th class="text-left px-6 py-3">Student</th>
              <th class="text-left px-6 py-3 w-32">Adm No.</th>
              <th class="text-center px-4 py-3 w-36">Score</th>
              <th class="text-left px-4 py-3">Remarks</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr
              v-for="(row, i) in filteredBulk"
              :key="row.student_id"
              class="hover:bg-violet-50/20 transition-colors"
              :class="row._changed ? 'bg-amber-50/30' : ''"
            >
              <td class="px-6 py-3 text-slate-400 text-xs">{{ i + 1 }}</td>
              <td class="px-6 py-3 font-semibold text-slate-800">{{ row.student_name }}</td>
              <td class="px-6 py-3 font-mono text-xs text-slate-500">{{ row.admission_number }}</td>
              <td class="px-4 py-3">
                <select
                  v-model="row.score"
                  @change="row._changed = true"
                  class="w-full border rounded-lg px-2 py-2.5 text-sm font-bold outline-none transition"
                  :class="scoreClass(row.score)"
                >
                  <option value="">—</option>
                  <option value="EE">EE – Exceeding</option>
                  <option value="ME">ME – Meeting</option>
                  <option value="AE">AE – Approaching</option>
                  <option value="BE">BE – Below</option>
                </select>
              </td>
              <td class="px-4 py-3">
                <input
                  v-model="row.remarks"
                  @input="row._changed = true"
                  type="text"
                  placeholder="Optional remark…"
                  class="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="bulkSaveMsg" class="px-6 py-3 text-sm font-medium" :class="bulkSaveError ? 'text-school-red bg-red-50' : 'text-emerald-700 bg-emerald-50'">
        {{ bulkSaveMsg }}
      </div>
    </div>

    <!-- STUDENT LIST VIEW -->
    <div v-else class="bg-white rounded-[12px] border border-[#E2E8F0] overflow-hidden">
      <div class="border-b border-slate-100 px-6 py-4 bg-slate-50">
        <h3 class="font-bold text-slate-800">{{ selectedGrade }} Students</h3>
      </div>

      <div v-if="loadingBulk" class="py-16 flex justify-center">
        <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
      </div>

      <div v-else class="divide-y divide-slate-50">
        <div
          v-for="(s, i) in filteredBulk"
          :key="s.student_id"
          class="flex items-center justify-between px-6 py-4 hover:bg-slate-50 transition-colors"
        >
          <div class="flex items-center gap-4">
            <div class="w-8 h-8 rounded-full bg-violet-100 text-school-purple flex items-center justify-center font-bold text-xs">
              {{ s.student_name.charAt(0) }}
            </div>
            <div>
              <p class="font-semibold text-slate-800 text-sm">{{ s.student_name }}</p>
              <p class="text-xs text-slate-400 font-mono">{{ s.admission_number }}</p>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <span v-if="s.score" class="text-xs font-bold px-2.5 py-1 rounded-full" :class="scoreBadge(s.score)">{{ s.score }}</span>
            <router-link :to="`/students/${s.student_id}`" class="text-xs font-bold text-slate-500 hover:text-slate-800 border border-slate-200 px-3 py-1.5 rounded-lg hover:bg-slate-50 transition">Profile</router-link>
            <button @click="openModal(s)" class="text-xs font-bold text-school-purple border border-school-purple/30 bg-school-purple/5 hover:bg-school-purple hover:text-white px-3 py-1.5 rounded-lg transition">
              Grade
            </button>
          </div>
        </div>
        <div v-if="filteredBulk.length === 0" class="py-12 text-center text-slate-400 text-sm">
          No students in {{ selectedGrade }}.
        </div>
      </div>
    </div>

    <!-- Single-student grade modal -->
    <div v-if="showModal" class="fixed inset-0 bg-slate-900/40 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-[12px] shadow-2xl w-full max-w-lg overflow-hidden border border-[#E2E8F0]">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <div>
            <h2 class="text-lg font-bold text-[#0F172A]">Record Assessment</h2>
            <p class="text-xs text-slate-500 mt-0.5">{{ modalStudent?.student_name }} · {{ appStore.currentTerm }}</p>
          </div>
          <button @click="showModal = false" class="w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
        </div>

        <form @submit.prevent="submitSingle" class="p-6 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Learning Area</label>
              <select v-model="modalForm.learning_area" required class="w-full border border-slate-300 rounded-lg p-2.5 text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple">
                <option disabled value="">Select Area</option>
                <option v-for="a in learningAreas" :key="a" :value="a">{{ a }}</option>
              </select>
            </div>
            <div>
              <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Score (CBC)</label>
              <select v-model="modalForm.score" required class="w-full border border-slate-300 rounded-lg p-2.5 text-sm font-bold outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple">
                <option disabled value="">Select Score</option>
                <option value="EE">EE – Exceeding</option>
                <option value="ME">ME – Meeting</option>
                <option value="AE">AE – Approaching</option>
                <option value="BE">BE – Below</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Remarks (optional)</label>
            <textarea v-model="modalForm.remarks" rows="2" class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple resize-none" placeholder="Teacher's comments…"></textarea>
          </div>
          <button type="submit" class="w-full py-3 bg-school-purple text-white rounded-lg font-bold hover:bg-school-purple-l transition text-sm">
            Save Score
          </button>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useAppStore } from '@/stores/app'
import { apiFetch } from '@/services/api'
import academicService from '@/services/academicService'

const appStore = useAppStore()

const cbcGrades = ['Play Group', 'PP1', 'PP2', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6']

const AREAS_BY_GRADE = {
  'Play Group': ['Psychomotor & Creative Activities', 'Language Activities', 'Mathematical Activities', 'Environmental Activities', 'Religious & Moral Education'],
  'PP1': ['Psychomotor & Creative Activities', 'Language Activities', 'Mathematical Activities', 'Environmental Activities', 'Religious & Moral Education'],
  'PP2': ['Psychomotor & Creative Activities', 'Language Activities', 'Mathematical Activities', 'Environmental Activities', 'Religious & Moral Education'],
  default: ['English', 'Kiswahili', 'Mathematics', 'Integrated Science', 'Social Studies', 'Creative Arts', 'Religious Education', 'Physical & Health Education'],
}

const selectedGrade = ref('Grade 1')
const selectedArea = ref('Mathematics')
const viewMode = ref('bulk')
const searchQuery = ref('')
const bulkRows = ref([])
const loadingBulk = ref(false)
const bulkSaving = ref(false)
const bulkSaveMsg = ref('')
const bulkSaveError = ref(false)

const showModal = ref(false)
const modalStudent = ref(null)
const modalForm = reactive({ learning_area: '', score: '', remarks: '' })

const learningAreas = computed(() => AREAS_BY_GRADE[selectedGrade.value] || AREAS_BY_GRADE.default)

const hasPendingChanges = computed(() => bulkRows.value.some(r => r._changed))

const filteredBulk = computed(() => {
  const q = searchQuery.value.toLowerCase()
  if (!q) return bulkRows.value
  return bulkRows.value.filter(r =>
    r.student_name.toLowerCase().includes(q) ||
    r.admission_number.toLowerCase().includes(q)
  )
})

const scoreClass = (score) => ({
  EE: 'border-emerald-300 bg-emerald-50 text-emerald-700',
  ME: 'border-blue-300 bg-blue-50 text-blue-700',
  AE: 'border-amber-300 bg-amber-50 text-amber-700',
  BE: 'border-red-300 bg-red-50 text-red-700',
  '': 'border-slate-200 text-slate-600',
}[score] || 'border-slate-200 text-slate-600')

const scoreBadge = (score) => ({
  EE: 'bg-emerald-50 text-emerald-700',
  ME: 'bg-blue-50 text-blue-700',
  AE: 'bg-amber-50 text-amber-700',
  BE: 'bg-red-50 text-red-700',
}[score] || 'bg-slate-100 text-slate-500')

const loadBulkData = async () => {
  loadingBulk.value = true
  try {
    const data = await apiFetch(
      `/api/academics/grade/${encodeURIComponent(selectedGrade.value)}/${encodeURIComponent(appStore.currentTerm)}`
    )
    bulkRows.value = data.map(s => ({
      student_id: s.student_id,
      student_name: s.student_name,
      admission_number: s.admission_number,
      score: s.scores[selectedArea.value]?.score || '',
      remarks: s.scores[selectedArea.value]?.remarks || '',
      _changed: false,
    }))
  } catch (e) {
    console.error(e)
  } finally {
    loadingBulk.value = false
  }
}

const selectGrade = (grade) => {
  selectedGrade.value = grade
  const areas = AREAS_BY_GRADE[grade] || AREAS_BY_GRADE.default
  selectedArea.value = areas[0]
  loadBulkData()
}

const saveBulk = async () => {
  bulkSaveMsg.value = ''
  bulkSaveError.value = false
  const changed = bulkRows.value.filter(r => r._changed && r.score)
  if (!changed.length) return

  bulkSaving.value = true
  try {
    const payload = changed.map(r => ({
      student_id: r.student_id,
      term: appStore.currentTerm,
      learning_area: selectedArea.value,
      score: r.score,
      remarks: r.remarks || null,
    }))
    await academicService.saveScores(payload)
    bulkRows.value.forEach(r => { r._changed = false })
    bulkSaveMsg.value = `${changed.length} score${changed.length !== 1 ? 's' : ''} saved successfully.`
    setTimeout(() => { bulkSaveMsg.value = '' }, 4000)
  } catch (e) {
    bulkSaveMsg.value = 'Save failed: ' + (e?.message || '')
    bulkSaveError.value = true
  } finally {
    bulkSaving.value = false
  }
}

const openModal = (s) => {
  modalStudent.value = s
  modalForm.learning_area = selectedArea.value
  modalForm.score = s.score || ''
  modalForm.remarks = s.remarks || ''
  showModal.value = true
}

const submitSingle = async () => {
  if (!modalStudent.value) return
  try {
    await academicService.saveScores([{
      student_id: modalStudent.value.student_id,
      term: appStore.currentTerm,
      learning_area: modalForm.learning_area,
      score: modalForm.score,
      remarks: modalForm.remarks,
    }])
    showModal.value = false
    await loadBulkData()
  } catch (e) {
    alert('Save failed: ' + (e?.message || ''))
  }
}

watch(() => appStore.currentTerm, loadBulkData)

onMounted(() => {
  selectedArea.value = learningAreas.value[0]
  loadBulkData()
})
</script>
