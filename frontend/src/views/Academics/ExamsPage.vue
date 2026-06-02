<template>
  <div class="max-w-7xl mx-auto space-y-6">

    <div>
      <h1 class="text-2xl font-extrabold text-slate-800">Exams & Marks</h1>
      <p class="text-sm text-slate-400 mt-0.5">Record numeric exam marks and view class rankings.</p>
    </div>

    <!-- Tab bar -->
    <div class="flex gap-1 bg-slate-100 p-1 rounded-xl w-fit">
      <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
        class="px-4 py-2 text-sm font-semibold rounded-lg transition-all"
        :class="activeTab === tab.id ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500 hover:text-slate-700'">
        {{ tab.label }}
      </button>
    </div>

    <!-- ── TAB: Enter Marks ─────────────────────────────────────── -->
    <template v-if="activeTab === 'entry'">
      <div class="bg-white rounded-xl border border-slate-200 p-6 flex flex-wrap gap-4 items-end">
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Grade</label>
          <select v-model="form.grade_level" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
            <option v-for="g in GRADES" :key="g" :value="g">{{ g }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Term</label>
          <select v-model="form.term" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
            <option value="Term 1">Term 1</option>
            <option value="Term 2">Term 2</option>
            <option value="Term 3">Term 3</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Exam Type</label>
          <select v-model="form.exam_type" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
            <option value="CAT1">CAT 1</option>
            <option value="CAT2">CAT 2</option>
            <option value="MidTerm">Mid-Term</option>
            <option value="EndTerm">End-Term</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Subject</label>
          <select v-model="form.subject" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none w-48">
            <option value="" disabled>— select subject —</option>
            <option v-for="s in subjectsForGrade" :key="s" :value="s">{{ s }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Max Marks</label>
          <input v-model.number="form.max_marks" type="number" min="1" max="300"
            class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none w-24" />
        </div>
        <button @click="loadStudents" :disabled="loadingStudents || !form.subject"
          class="bg-school-purple text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition disabled:opacity-50">
          {{ loadingStudents ? 'Loading…' : 'Load Class' }}
        </button>
      </div>

      <div v-if="marksList.length > 0" class="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div class="flex items-center justify-between px-5 py-3.5 border-b border-slate-100 bg-slate-50">
          <span class="font-semibold text-sm text-slate-700">
            {{ form.grade_level }} · {{ form.exam_type }} · {{ form.subject }} · {{ form.term }}
          </span>
          <span class="text-xs text-slate-400">{{ marksList.length }} students</span>
        </div>
        <table class="w-full text-sm">
          <thead>
            <tr class="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-100">
              <th class="px-5 py-4 text-left">Student</th>
              <th class="px-5 py-4 text-left">Adm No.</th>
              <th class="px-5 py-4 text-center w-36">Marks / {{ form.max_marks }}</th>
              <th class="px-5 py-4 text-center w-44">Grade</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in marksList" :key="s.student_id" class="border-b border-slate-50 hover:bg-slate-50">
              <td class="px-5 py-3 font-medium text-slate-800">{{ s.student_name }}</td>
              <td class="px-5 py-3 font-mono text-xs text-slate-500">{{ s.admission_number }}</td>
              <td class="px-5 py-3 text-center">
                <input v-model.number="s.marks" type="number" min="0" :max="form.max_marks" step="0.5"
                  class="border border-slate-200 rounded-lg px-3 py-1.5 text-sm text-center w-24 outline-none focus:border-school-purple" />
              </td>
              <td class="px-5 py-3 text-center">
                <span v-if="s.marks !== '' && s.marks !== null"
                  class="px-2.5 py-1 rounded-full text-xs font-bold"
                  :class="gradeLabel(s.marks, form.max_marks).cls">
                  {{ gradeLabel(s.marks, form.max_marks).label }}
                </span>
                <span v-else class="text-slate-300 text-xs">—</span>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="flex items-center justify-end px-5 py-4 bg-slate-50 border-t border-slate-100">
          <button @click="saveMarks" :disabled="saving"
            class="bg-emerald-600 text-white px-6 py-2.5 rounded-lg text-sm font-semibold hover:bg-emerald-700 transition disabled:opacity-60">
            {{ saving ? 'Saving…' : 'Save Marks' }}
          </button>
        </div>
      </div>
    </template>

    <!-- ── TAB: Rankings ─────────────────────────────────────────── -->
    <template v-if="activeTab === 'rankings'">
      <div class="bg-white rounded-xl border border-slate-200 p-6 flex flex-wrap gap-4 items-end">
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Grade</label>
          <select v-model="rankForm.grade_level" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
            <option v-for="g in GRADES" :key="g" :value="g">{{ g }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Term</label>
          <select v-model="rankForm.term" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
            <option value="Term 1">Term 1</option>
            <option value="Term 2">Term 2</option>
            <option value="Term 3">Term 3</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Exam Type</label>
          <select v-model="rankForm.exam_type" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
            <option value="">All Combined</option>
            <option value="CAT1">CAT 1</option>
            <option value="CAT2">CAT 2</option>
            <option value="MidTerm">Mid-Term</option>
            <option value="EndTerm">End-Term</option>
          </select>
        </div>
        <button @click="loadRankings" :disabled="loadingRankings"
          class="bg-school-navy text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-navy/90 transition disabled:opacity-50">
          {{ loadingRankings ? 'Loading…' : 'View Rankings' }}
        </button>
      </div>

      <div v-if="rankings.students.length > 0" class="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div class="border-b border-slate-100 px-5 py-3.5 bg-slate-50 flex items-center justify-between">
          <h3 class="font-semibold text-sm text-slate-700">{{ rankForm.grade_level }} · {{ rankForm.term }} Rankings</h3>
          <button @click="exportRankings"
            class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 bg-white border border-slate-200 px-3 py-1.5 rounded-lg hover:bg-slate-50 transition">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            Export CSV
          </button>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-100 bg-slate-50">
                <th class="px-4 py-3 text-center w-12">#</th>
                <th class="px-5 py-3 text-left">Student</th>
                <th v-for="subj in rankings.subjects" :key="subj" class="px-3 py-3 text-center">{{ subj }}</th>
                <th class="px-5 py-3 text-center">Total</th>
                <th class="px-5 py-3 text-center">%</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in rankings.students" :key="s.student_id"
                class="border-b border-slate-50 hover:bg-slate-50"
                :class="s.position <= 3 ? 'bg-amber-50/30' : ''">
                <td class="px-4 py-3.5 text-center">
                  <span class="inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-extrabold"
                    :class="s.position === 1 ? 'bg-amber-400 text-white' : s.position === 2 ? 'bg-slate-300 text-white' : s.position === 3 ? 'bg-amber-700 text-white' : 'text-slate-500'">
                    {{ s.position }}
                  </span>
                </td>
                <td class="px-5 py-3.5 font-semibold text-slate-800">{{ s.student_name }}</td>
                <td v-for="subj in rankings.subjects" :key="subj" class="px-3 py-3.5 text-center">
                  <span v-if="s.scores[subj]?.marks != null" class="font-medium text-slate-700">
                    {{ s.scores[subj].marks }}
                  </span>
                  <span v-if="s.scores[subj]?.marks != null"
                    class="ml-1 px-1.5 py-0.5 rounded text-xs font-bold"
                    :class="gradeLabel(s.scores[subj].marks, 100).cls">
                    {{ gradeLabel(s.scores[subj].marks, 100).abbr }}
                  </span>
                  <span v-else class="text-slate-300">—</span>
                </td>
                <td class="px-5 py-3.5 text-center font-bold text-slate-800">{{ s.total_marks }}</td>
                <td class="px-5 py-3.5 text-center">
                  <span v-if="s.percentage !== null" class="px-2 py-0.5 rounded-full text-xs font-bold"
                    :class="s.percentage >= 75 ? 'bg-emerald-50 text-emerald-700' : s.percentage >= 50 ? 'bg-amber-50 text-amber-700' : 'bg-red-50 text-red-600'">
                    {{ s.percentage }}%
                  </span>
                  <span v-else class="text-slate-300">—</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else-if="rankingsLoaded" class="bg-white rounded-xl border border-slate-200 py-12 text-center text-slate-400 text-sm">
        No exam results found for this selection.
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { apiFetch } from '@/services/api'
import { useAppStore } from '@/stores/app'
import { downloadCsv } from '@/utils/csvExport'
import { useToast } from '@/composables/useToast'
const toast = useToast()

const appStore = useAppStore()
const GRADES = ['Play Group','PP1','PP2','Grade 1','Grade 2','Grade 3','Grade 4','Grade 5','Grade 6']

// ── Grading scale (marks out of 100) ────────────────────────────────────────
function gradeLabel(marks, maxMarks = 100) {
  const pct = (Number(marks) / Number(maxMarks)) * 100
  if (pct >= 80) return { label: 'Exceeding Expectations', abbr: 'EE', cls: 'bg-emerald-50 text-emerald-700' }
  if (pct >= 70) return { label: 'Meeting Expectations',   abbr: 'ME', cls: 'bg-blue-50 text-blue-700' }
  if (pct >= 60) return { label: 'Approaching Expectations', abbr: 'AE', cls: 'bg-amber-50 text-amber-700' }
  return            { label: 'Below Expectations',          abbr: 'BE', cls: 'bg-red-50 text-red-600' }
}

// ── Subjects per grade ───────────────────────────────────────────────────────
const allSubjectsByGrade = ref({})  // { "Grade 1": ["Math", ...], ... }
const subjectsForGrade = computed(() =>
  allSubjectsByGrade.value[form.value.grade_level] ?? []
)

async function fetchSubjects() {
  try {
    const data = await apiFetch('/api/subjects/by-grade')
    // data = { "Grade 1": [{name, ...}], ... }
    const mapped = {}
    for (const [grade, subjects] of Object.entries(data)) {
      mapped[grade] = subjects.map(s => s.name)
    }
    allSubjectsByGrade.value = mapped
  } catch {
    // silent — subjects may not be configured yet
  }
}

fetchSubjects()

// Reset subject when grade changes
watch(() => form.value?.grade_level, () => {
  form.value.subject = subjectsForGrade.value[0] ?? ''
})

const tabs = [
  { id: 'entry', label: 'Enter Marks' },
  { id: 'rankings', label: 'Rankings' },
]
const activeTab = ref('entry')

// Entry form
const form = ref({ grade_level: 'Grade 1', term: 'Term 1', exam_type: 'EndTerm', subject: '', max_marks: 100 })
const marksList = ref([])
const loadingStudents = ref(false)
const saving = ref(false)

const loadStudents = async () => {
  if (!form.value.subject) return
  loadingStudents.value = true
  try {
    const data = await apiFetch(
      `/api/exams/grade/${encodeURIComponent(form.value.grade_level)}/${encodeURIComponent(form.value.term)}?academic_year=${appStore.currentYear}&exam_type=${form.value.exam_type}`
    )
    marksList.value = data.students.map(s => ({
      student_id: s.student_id,
      student_name: s.student_name,
      admission_number: s.admission_number,
      marks: s.scores[form.value.subject]?.marks ?? '',
    }))
  } catch {
    toast.error('Failed to load students.')
  } finally {
    loadingStudents.value = false
  }
}

const saveMarks = async () => {
  saving.value = true
  try {
    const results = marksList.value
      .filter(s => s.marks !== '' && s.marks !== null)
      .map(s => ({ student_id: s.student_id, marks: Number(s.marks), max_marks: form.value.max_marks }))
    await apiFetch('/api/exams/bulk', {
      method: 'POST',
      body: JSON.stringify({
        grade_level: form.value.grade_level,
        term: form.value.term,
        exam_type: form.value.exam_type,
        subject: form.value.subject,
        academic_year: appStore.currentYear,
        results,
      }),
    })
    toast.success('Marks saved successfully.')
  } catch {
    toast.error('Failed to save marks.')
  } finally {
    saving.value = false
  }
}

// Rankings
const rankForm = ref({ grade_level: 'Grade 1', term: 'Term 1', exam_type: '' })
const rankings = ref({ subjects: [], students: [] })
const loadingRankings = ref(false)
const rankingsLoaded = ref(false)

const exportRankings = () => {
  const headers = [
    { key: 'position', label: 'Position' },
    { key: 'student_name', label: 'Student Name' },
    ...rankings.value.subjects.map(s => ({ key: `score_${s}`, label: s })),
    { key: 'total_marks', label: 'Total Marks' },
    { key: 'percentage', label: 'Percentage (%)' },
  ]
  const rows = rankings.value.students.map(s => {
    const row = { position: s.position, student_name: s.student_name, total_marks: s.total_marks, percentage: s.percentage }
    for (const subj of rankings.value.subjects) row[`score_${subj}`] = s.scores[subj]?.marks ?? ''
    return row
  })
  downloadCsv(`rankings-${rankForm.value.grade_level}-${rankForm.value.term}`, headers, rows)
}

const loadRankings = async () => {
  loadingRankings.value = true
  rankingsLoaded.value = false
  try {
    const qs = new URLSearchParams({ academic_year: appStore.currentYear })
    if (rankForm.value.exam_type) qs.set('exam_type', rankForm.value.exam_type)
    const data = await apiFetch(
      `/api/exams/grade/${encodeURIComponent(rankForm.value.grade_level)}/${encodeURIComponent(rankForm.value.term)}?${qs}`
    )
    rankings.value = data
    rankingsLoaded.value = true
  } catch {
    toast.error('Failed to load rankings.')
  } finally {
    loadingRankings.value = false
  }
}
</script>
