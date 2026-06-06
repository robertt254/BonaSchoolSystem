<template>
  <div class="max-w-6xl mx-auto space-y-6">

    <div>
      <h1 class="text-2xl font-extrabold text-slate-800">Report Builder</h1>
      <p class="text-sm text-slate-400 mt-0.5">Generate and export standard school management reports.</p>
    </div>

    <!-- Report selector -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <button v-for="r in REPORTS" :key="r.id" @click="selectReport(r)"
        class="bg-white rounded-lg border p-4 text-left hover:border-school-purple/40 hover:shadow-sm transition"
        :class="selectedReport?.id === r.id ? 'border-school-purple shadow-sm' : 'border-slate-200'">
        <div class="w-8 h-8 rounded-lg mb-3 flex items-center justify-center" :class="r.iconBg">
          <svg class="w-4 h-4" :class="r.iconColor" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" v-html="r.icon"></svg>
        </div>
        <p class="font-bold text-slate-800 text-sm">{{ r.label }}</p>
        <p class="text-xs text-slate-400 mt-0.5">{{ r.desc }}</p>
      </button>
    </div>

    <!-- Filters for selected report -->
    <div v-if="selectedReport" class="bg-white rounded-lg border border-slate-200 p-6 flex flex-wrap gap-4 items-end">
      <template v-if="selectedReport.filters.includes('year')">
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Year</label>
          <select v-model="filters.year" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
            <option v-for="y in appStore.years" :key="y" :value="y">{{ y }}</option>
          </select>
        </div>
      </template>
      <template v-if="selectedReport.filters.includes('term')">
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Term</label>
          <select v-model="filters.term" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
            <option value="">All Terms</option>
            <option value="Term 1">Term 1</option>
            <option value="Term 2">Term 2</option>
            <option value="Term 3">Term 3</option>
          </select>
        </div>
      </template>
      <template v-if="selectedReport.filters.includes('grade')">
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Grade</label>
          <select v-model="filters.grade" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
            <option value="">All Grades</option>
            <option v-for="g in GRADES" :key="g" :value="g">{{ g }}</option>
          </select>
        </div>
      </template>
      <button @click="runReport" :disabled="loading"
        class="bg-school-purple text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition disabled:opacity-50">
        {{ loading ? 'Generating…' : 'Generate Report' }}
      </button>
      <button v-if="rows.length > 0" @click="exportReport"
        class="flex items-center gap-1.5 bg-white border border-slate-200 text-slate-600 px-4 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-50 transition">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        Export CSV
      </button>
      <button v-if="rows.length > 0" @click="printPage"
        class="bg-slate-100 text-slate-700 px-4 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-200 transition flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 01-2-2v-5a2 2 0 012-2h16a2 2 0 012 2v5a2 2 0 01-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
        Print
      </button>
    </div>

    <!-- Report output -->
    <div v-if="rows.length > 0" id="report-output" class="bg-white rounded-lg border border-slate-200 overflow-hidden">
      <div class="px-5 py-3.5 border-b border-slate-100 bg-slate-50 flex items-center justify-between print:border-b print:border-slate-300">
        <h3 class="font-bold text-slate-700 text-sm">{{ selectedReport.label }}</h3>
        <span class="text-xs text-slate-400">{{ rows.length }} record(s)</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-100 bg-slate-50">
              <th v-for="col in columns" :key="col.key" class="px-5 py-3" :class="col.align === 'right' ? 'text-right' : 'text-left'">
                {{ col.label }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, i) in rows" :key="i" class="border-b border-slate-50 hover:bg-slate-50">
              <td v-for="col in columns" :key="col.key" class="px-5 py-3"
                :class="[col.align === 'right' ? 'text-right font-mono text-xs' : '', col.bold ? 'font-semibold text-slate-800' : 'text-slate-600']">
                {{ row[col.key] }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else-if="ranReport" class="bg-white rounded-lg border border-slate-200 py-12 text-center text-slate-400 text-sm">
      No data found for this selection.
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { apiFetch } from '@/services/api'
import { useAppStore } from '@/stores/app'
import { downloadCsv } from '@/utils/csvExport'
import { useToast } from '@/composables/useToast'
const toast = useToast()

const appStore = useAppStore()
const GRADES = ['Play Group','PP1','PP2','Grade 1','Grade 2','Grade 3','Grade 4','Grade 5','Grade 6']

const REPORTS = [
  {
    id: 'enrollment',
    label: 'Enrollment by Grade',
    desc: 'Total students per grade',
    filters: ['year'],
    iconBg: 'bg-blue-50',
    iconColor: 'text-blue-600',
    icon: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
  },
  {
    id: 'fee_collection',
    label: 'Fee Collection',
    desc: 'Payments collected by term',
    filters: ['year', 'term'],
    iconBg: 'bg-emerald-50',
    iconColor: 'text-emerald-600',
    icon: '<rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>',
  },
  {
    id: 'attendance',
    label: 'Attendance Summary',
    desc: 'Present/absent rates by grade',
    filters: ['year', 'term', 'grade'],
    iconBg: 'bg-amber-50',
    iconColor: 'text-amber-600',
    icon: '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
  },
  {
    id: 'exam_performance',
    label: 'Exam Performance',
    desc: 'Average scores by grade/term',
    filters: ['year', 'term', 'grade'],
    iconBg: 'bg-purple-50',
    iconColor: 'text-purple-600',
    icon: '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
  },
]

const selectedReport = ref(null)
const filters = reactive({ year: appStore.currentYear, term: '', grade: '' })
const columns = ref([])
const rows = ref([])
const loading = ref(false)
const ranReport = ref(false)

const selectReport = (r) => {
  selectedReport.value = r
  rows.value = []
  ranReport.value = false
}

const runReport = async () => {
  loading.value = true
  ranReport.value = false
  rows.value = []
  try {
    const id = selectedReport.value.id
    if (id === 'enrollment') await runEnrollment()
    else if (id === 'fee_collection') await runFeeCollection()
    else if (id === 'attendance') await runAttendance()
    else if (id === 'exam_performance') await runExamPerformance()
    ranReport.value = true
  } catch (e) { toast.error('Report failed: ' + (e?.message || 'Unknown error')) }
  finally { loading.value = false }
}

const runEnrollment = async () => {
  const data = await apiFetch(`/api/students/enrollment-summary?academic_year=${filters.year}`)
  columns.value = [
    { key: 'grade_level', label: 'Grade', bold: true },
    { key: 'count', label: 'Students', align: 'right' },
  ]
  rows.value = data
}

const runFeeCollection = async () => {
  const qs = new URLSearchParams({ academic_year: filters.year })
  if (filters.term) qs.set('term', filters.term)
  const data = await apiFetch(`/api/fees/collection-summary?${qs}`)
  columns.value = [
    { key: 'term', label: 'Term', bold: true },
    { key: 'total_paid', label: 'Collected (KES)', align: 'right' },
    { key: 'num_payments', label: 'Payments', align: 'right' },
    { key: 'unique_students', label: 'Students', align: 'right' },
  ]
  rows.value = data
}

const runAttendance = async () => {
  const data = await apiFetch('/api/attendance/summary')
  columns.value = [
    { key: 'grade', label: 'Grade', bold: true },
    { key: 'total_records', label: 'Total Records', align: 'right' },
    { key: 'present', label: 'Present', align: 'right' },
    { key: 'absent', label: 'Absent', align: 'right' },
    { key: 'percentage', label: 'Rate %', align: 'right' },
  ]
  rows.value = (filters.grade
    ? data.filter(r => r.grade === filters.grade)
    : data
  ).map(r => ({
    ...r,
    absent: r.total_records - r.present,
    percentage: r.percentage !== null ? r.percentage + '%' : '—',
  }))
}

const runExamPerformance = async () => {
  const qs = new URLSearchParams({ academic_year: filters.year })
  if (filters.term) qs.set('term', filters.term)
  if (filters.grade) qs.set('grade_level', filters.grade)
  const data = await apiFetch(`/api/exams/performance-summary?${qs}`)
  columns.value = [
    { key: 'grade_level', label: 'Grade', bold: true },
    { key: 'subject', label: 'Subject' },
    { key: 'exam_type', label: 'Type' },
    { key: 'avg_score', label: 'Avg Score', align: 'right' },
    { key: 'highest', label: 'Highest', align: 'right' },
    { key: 'lowest', label: 'Lowest', align: 'right' },
    { key: 'num_students', label: 'Students', align: 'right' },
  ]
  rows.value = data
}

const exportReport = () => {
  if (!rows.value.length) return
  downloadCsv(`report-${selectedReport.value.id}-${filters.year}`, columns.value, rows.value)
}

const printPage = () => window.print()
</script>

<style>
@media print {
  .print\:hidden { display: none !important; }
}
</style>
