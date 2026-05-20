<template>
  <div class="max-w-4xl mx-auto space-y-5">

    <!-- Mode toggle -->
    <div class="bg-white rounded-xl border border-slate-200 p-5 print:hidden">
      <div class="flex gap-2 mb-5">
        <button
          @click="mode = 'single'"
          :class="mode === 'single' ? 'bg-school-purple text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'"
          class="px-4 py-2 rounded-lg text-sm font-bold transition"
        >Single Student</button>
        <button
          @click="mode = 'bulk'"
          :class="mode === 'bulk' ? 'bg-school-purple text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'"
          class="px-4 py-2 rounded-lg text-sm font-bold transition"
        >Bulk Grade Export</button>
      </div>

      <!-- Single mode controls -->
      <div v-if="mode === 'single'" class="flex flex-col sm:flex-row gap-4 items-end">
        <div class="flex-1">
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Student</label>
          <select
            v-model="selectedStudent"
            class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none"
          >
            <option disabled value="">— Choose a student —</option>
            <option v-for="s in students" :key="s.id" :value="s.id">
              {{ s.first_name }} {{ s.last_name }} · {{ s.admission_number }}
            </option>
          </select>
        </div>
        <div class="w-40">
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Term</label>
          <select v-model="selectedTerm" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none">
            <option value="Term 1">Term 1</option>
            <option value="Term 2">Term 2</option>
            <option value="Term 3">Term 3</option>
          </select>
        </div>
        <button
          @click="loadReport"
          :disabled="!selectedStudent || generating"
          class="bg-school-purple text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition disabled:opacity-50"
        >{{ generating ? 'Loading…' : 'Generate' }}</button>
      </div>

      <!-- Bulk mode controls -->
      <div v-else class="flex flex-col sm:flex-row gap-4 items-end">
        <div class="flex-1">
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Grade</label>
          <select v-model="bulkGrade" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none">
            <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
          </select>
        </div>
        <div class="w-40">
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Term</label>
          <select v-model="selectedTerm" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none">
            <option value="Term 1">Term 1</option>
            <option value="Term 2">Term 2</option>
            <option value="Term 3">Term 3</option>
          </select>
        </div>
        <button
          @click="loadBulk"
          :disabled="generating"
          class="bg-school-purple text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition disabled:opacity-50"
        >{{ generating ? 'Loading…' : 'Load All' }}</button>
        <button
          v-if="bulkReports.length"
          @click="window.print()"
          class="inline-flex items-center gap-2 bg-slate-800 text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-black transition"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
            <rect x="6" y="14" width="12" height="8"/>
          </svg>
          Print All ({{ bulkReports.length }})
        </button>
      </div>
    </div>

    <!-- Single report card -->
    <div
      v-if="mode === 'single' && reportData"
      id="report-card"
      class="bg-white rounded-xl border border-slate-200 overflow-hidden print:rounded-none print:border-none print:shadow-none"
    >
      <ReportCardDoc :data="reportData" />
      <div class="border-t border-slate-100 px-8 py-4 flex justify-end print:hidden">
        <button
          @click="window.print()"
          class="inline-flex items-center gap-2 bg-slate-800 text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-black transition"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1-2 2h-2"/>
            <rect x="6" y="14" width="12" height="8"/>
          </svg>
          Print Report Card
        </button>
      </div>
    </div>

    <!-- Bulk report cards -->
    <div v-if="mode === 'bulk' && bulkReports.length" id="bulk-report">
      <div
        v-for="(rpt, idx) in bulkReports"
        :key="rpt.student_id || idx"
        class="bg-white rounded-xl border border-slate-200 overflow-hidden mb-5 print:rounded-none print:border-none print:page-break-after-always print:mb-0"
      >
        <ReportCardDoc :data="rpt" />
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, defineComponent, h, onMounted } from 'vue'
import studentService from '@/services/studentService'
import academicService from '@/services/academicService'
import { apiFetch } from '@/services/api'

// Inline report card document component
const scoreClass = (s) => ({
  EE: 'bg-emerald-100 text-emerald-700',
  ME: 'bg-blue-100 text-blue-700',
  AE: 'bg-amber-100 text-amber-700',
  BE: 'bg-red-100 text-red-600',
}[s] || 'bg-slate-100 text-slate-600')

const ReportCardDoc = defineComponent({
  props: { data: Object },
  setup(props) {
    return () => h('div', {}, [
      // Header
      h('div', { class: 'bg-school-navy text-white px-10 py-8 print:px-8 print:py-6' }, [
        h('div', { class: 'flex items-start justify-between' }, [
          h('div', {}, [
            h('h1', { class: 'text-2xl font-black uppercase tracking-wider' }, 'The Bona School'),
            h('p', { class: 'text-white/60 text-sm mt-1' }, 'Competency-Based Curriculum (CBC) · Nairobi, Kenya'),
          ]),
          h('div', { class: 'text-right' }, [
            h('p', { class: 'text-white/40 text-xs uppercase tracking-widest font-bold' }, 'Report Card'),
            h('p', { class: 'text-white font-bold mt-0.5' }, `${props.data.term} · ${new Date().getFullYear()}`),
          ]),
        ]),
      ]),
      // Student info strip
      h('div', { class: 'grid grid-cols-3 gap-0 border-b border-slate-200 bg-slate-50 divide-x divide-slate-200' }, [
        h('div', { class: 'px-6 py-4' }, [
          h('p', { class: 'text-[10px] font-bold uppercase tracking-widest text-slate-400' }, 'Student Name'),
          h('p', { class: 'font-bold text-slate-800 mt-0.5' }, props.data.student_name),
        ]),
        h('div', { class: 'px-6 py-4' }, [
          h('p', { class: 'text-[10px] font-bold uppercase tracking-widest text-slate-400' }, 'Admission No.'),
          h('p', { class: 'font-bold text-slate-800 mt-0.5 font-mono' }, props.data.admission_number),
        ]),
        h('div', { class: 'px-6 py-4' }, [
          h('p', { class: 'text-[10px] font-bold uppercase tracking-widest text-slate-400' }, 'Grade / Term'),
          h('p', { class: 'font-bold text-slate-800 mt-0.5' }, `${props.data.grade_level} · ${props.data.term}`),
        ]),
      ]),
      // Results table
      h('div', { class: 'px-8 py-6' }, [
        h('h3', { class: 'text-xs font-bold uppercase tracking-widest text-slate-400 mb-4' }, 'CBC Assessment Results'),
        h('table', { class: 'w-full border-collapse border border-slate-200 text-sm' }, [
          h('thead', {}, h('tr', { class: 'bg-slate-50' }, [
            h('th', { class: 'border border-slate-200 px-5 py-3 text-left font-bold text-slate-600 uppercase text-xs tracking-wider' }, 'Learning Area'),
            h('th', { class: 'border border-slate-200 px-5 py-3 text-center font-bold text-slate-600 uppercase text-xs tracking-wider w-24' }, 'Score'),
            h('th', { class: 'border border-slate-200 px-5 py-3 text-left font-bold text-slate-600 uppercase text-xs tracking-wider' }, 'Remarks'),
          ])),
          h('tbody', {}, props.data.results.length
            ? props.data.results.map(r => h('tr', { key: r.learning_area }, [
                h('td', { class: 'border border-slate-200 px-5 py-3 font-medium text-slate-800' }, r.learning_area),
                h('td', { class: 'border border-slate-200 px-5 py-3 text-center' },
                  h('span', { class: `inline-block px-3 py-0.5 rounded-full text-xs font-black ${scoreClass(r.score)}` }, r.score)
                ),
                h('td', { class: 'border border-slate-200 px-5 py-3 text-slate-500 italic text-xs' }, r.remarks || '—'),
              ]))
            : [h('tr', {}, h('td', { colspan: 3, class: 'border border-slate-200 px-5 py-8 text-center text-slate-400' }, 'No assessments recorded for this term.'))]
          ),
        ]),
      ]),
      // Grading key
      h('div', { class: 'mx-8 mb-6 bg-slate-50 border border-slate-200 rounded-lg p-4' }, [
        h('p', { class: 'text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-2' }, 'CBC Grading Key'),
        h('div', { class: 'grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs' }, [
          h('span', {}, [h('strong', { class: 'text-emerald-700' }, 'EE (4)'), ' — Exceeding Expectations']),
          h('span', {}, [h('strong', { class: 'text-blue-700' }, 'ME (3)'), ' — Meeting Expectations']),
          h('span', {}, [h('strong', { class: 'text-amber-600' }, 'AE (2)'), ' — Approaching Expectations']),
          h('span', {}, [h('strong', { class: 'text-red-600' }, 'BE (1)'), ' — Below Expectations']),
        ]),
      ]),
      // Signatures
      h('div', { class: 'mx-8 mb-8 flex justify-between' }, [
        h('div', { class: 'w-52 border-t-2 border-slate-800 pt-2 text-center' }, h('p', { class: 'text-xs font-bold text-slate-600' }, 'Class Teacher')),
        h('div', { class: 'w-52 border-t-2 border-slate-800 pt-2 text-center' }, h('p', { class: 'text-xs font-bold text-slate-600' }, 'Principal')),
      ]),
    ])
  },
})

const grades = ['Play Group', 'PP1', 'PP2', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6']

const mode = ref('single')
const students = ref([])
const selectedStudent = ref('')
const selectedTerm = ref('Term 1')
const reportData = ref(null)
const generating = ref(false)
const bulkGrade = ref('Grade 1')
const bulkReports = ref([])

onMounted(async () => {
  try { students.value = await studentService.getAllStudents() }
  catch (e) { console.error(e) }
})

const loadReport = async () => {
  generating.value = true
  reportData.value = null
  try {
    reportData.value = await academicService.getReportCard(selectedStudent.value, selectedTerm.value)
  } catch {
    alert('Failed to load report card.')
  } finally {
    generating.value = false
  }
}

const loadBulk = async () => {
  generating.value = true
  bulkReports.value = []
  try {
    const gradeStudents = students.value.filter(s => s.grade_level === bulkGrade.value)
    const reports = await Promise.all(
      gradeStudents.map(s => academicService.getReportCard(s.id, selectedTerm.value).catch(() => null))
    )
    bulkReports.value = reports.filter(Boolean)
  } catch (e) {
    alert('Failed to load reports.')
  } finally {
    generating.value = false
  }
}
</script>

<style>
@media print {
  body * { visibility: hidden; }
  #report-card, #report-card *,
  #bulk-report, #bulk-report * { visibility: visible; }
  #report-card { position: fixed; top: 0; left: 0; width: 100%; }
  #bulk-report { position: fixed; top: 0; left: 0; width: 100%; }
  .print\:page-break-after-always { page-break-after: always; }
}
</style>
