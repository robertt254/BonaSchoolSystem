<template>
  <div class="max-w-4xl mx-auto space-y-6">

    <!-- Mode toggle -->
    <div class="bg-white rounded-xl border border-slate-200 p-6 print:hidden">
      <div class="flex items-center justify-between mb-5">
        <div>
          <h2 class="font-bold text-slate-800 text-sm">CBC Report Cards</h2>
          <p class="text-xs text-slate-400 mt-0.5">Generate and print student report cards.</p>
        </div>
        <div class="flex gap-2">
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
          @click="printPage()"
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
          @click="printPage()"
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
import { useAppStore } from '@/stores/app'
import { useToast } from '@/composables/useToast'
const toast = useToast()


const appStore = useAppStore()

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
      h('div', { class: 'bg-school-navy text-white px-10 py-7 print:px-8 print:py-5' }, [
        h('div', { class: 'flex items-start justify-between' }, [
          h('div', {}, [
            h('h1', { class: 'text-2xl font-black uppercase tracking-wider' }, 'The Bona School'),
            h('p', { class: 'text-white/50 text-xs mt-1 font-medium' }, 'Competency-Based Curriculum (CBC) · Nairobi, Kenya'),
          ]),
          h('div', { class: 'text-right' }, [
            h('p', { class: 'text-white/40 text-xs uppercase tracking-widest font-bold' }, 'Official Report Card'),
            h('p', { class: 'text-white font-extrabold text-lg mt-0.5' }, props.data.term),
            h('p', { class: 'text-white/50 text-xs' }, `Academic Year ${props.data.academic_year || new Date().getFullYear()}`),
          ]),
        ]),
      ]),
      // Student info strip — 4 columns
      h('div', { class: 'grid grid-cols-2 sm:grid-cols-4 border-b border-slate-200 bg-slate-50 divide-x divide-slate-200' }, [
        h('div', { class: 'px-5 py-4' }, [
          h('p', { class: 'text-xs font-bold uppercase tracking-widest text-slate-400 mb-0.5' }, 'Student Name'),
          h('p', { class: 'font-bold text-slate-800 text-sm' }, props.data.student_name),
        ]),
        h('div', { class: 'px-5 py-4' }, [
          h('p', { class: 'text-xs font-bold uppercase tracking-widest text-slate-400 mb-0.5' }, 'Admission No.'),
          h('p', { class: 'font-bold text-slate-800 text-sm font-mono' }, props.data.admission_number),
        ]),
        h('div', { class: 'px-5 py-4' }, [
          h('p', { class: 'text-xs font-bold uppercase tracking-widest text-slate-400 mb-0.5' }, 'Grade Level'),
          h('p', { class: 'font-bold text-slate-800 text-sm' }, props.data.grade_level),
        ]),
        h('div', { class: 'px-5 py-4' }, [
          h('p', { class: 'text-xs font-bold uppercase tracking-widest text-slate-400 mb-0.5' }, 'Term / Year'),
          h('p', { class: 'font-bold text-slate-800 text-sm' }, `${props.data.term} · ${props.data.academic_year || new Date().getFullYear()}`),
        ]),
      ]),
      // Results table — supports strand-level CBC scores
      h('div', { class: 'px-8 py-6' }, [
        h('p', { class: 'text-xs font-bold uppercase tracking-widest text-slate-400 mb-4' }, 'CBC Assessment Results'),
        props.data.results.length
          ? h('table', { class: 'w-full border-collapse text-sm' }, [
              h('thead', {}, h('tr', { class: 'bg-slate-50 border-y border-slate-200' }, [
                h('th', { class: 'px-5 py-3 text-left font-bold text-slate-500 uppercase text-xs tracking-wider w-1/3' }, 'Learning Area / Strand'),
                h('th', { class: 'px-5 py-3 text-center font-bold text-slate-500 uppercase text-xs tracking-wider w-28' }, 'Score'),
                h('th', { class: 'px-5 py-3 text-left font-bold text-slate-500 uppercase text-xs tracking-wider' }, "Teacher's Remarks"),
              ])),
              h('tbody', {}, props.data.results.flatMap((r, i) => {
                const strandEntries = Object.entries(r.strands || {})
                // Single overall score (no strands or empty-string strand)
                if (strandEntries.length === 0 || (strandEntries.length === 1 && strandEntries[0][0] === '')) {
                  const score = strandEntries[0]?.[1] || ''
                  return [h('tr', {
                    key: r.learning_area,
                    class: i % 2 === 0 ? 'bg-white' : 'bg-slate-50/50',
                  }, [
                    h('td', { class: 'border-b border-slate-100 px-5 py-3 font-semibold text-slate-800' }, r.learning_area),
                    h('td', { class: 'border-b border-slate-100 px-5 py-3 text-center' },
                      score ? h('span', { class: `inline-block px-3 py-0.5 rounded-full text-xs font-black ${scoreClass(score)}` }, score) : h('span', { class: 'text-slate-300' }, '—')
                    ),
                    h('td', { class: 'border-b border-slate-100 px-5 py-3 text-slate-500 text-xs italic' }, r.remarks || '—'),
                  ])]
                }
                // Strand-level rows — area header + one row per strand
                return [
                  h('tr', { key: r.learning_area + '_header', class: 'bg-school-navy/5' }, [
                    h('td', { colspan: 3, class: 'px-5 py-2 font-extrabold text-slate-700 text-xs uppercase tracking-wider border-b border-slate-200' }, r.learning_area),
                  ]),
                  ...strandEntries.map(([strand, score], si) =>
                    h('tr', { key: r.learning_area + strand, class: si % 2 === 0 ? 'bg-white' : 'bg-slate-50/30' }, [
                      h('td', { class: 'border-b border-slate-100 pl-10 pr-5 py-2.5 text-slate-600 text-xs' }, strand),
                      h('td', { class: 'border-b border-slate-100 px-5 py-2.5 text-center' },
                        score ? h('span', { class: `inline-block px-2.5 py-0.5 rounded-full text-xs font-black ${scoreClass(score)}` }, score) : h('span', { class: 'text-slate-300' }, '—')
                      ),
                      h('td', { class: 'border-b border-slate-100 px-5 py-2.5 text-slate-400 text-xs italic' },
                        si === 0 ? (r.remarks || '') : ''
                      ),
                    ])
                  ),
                ]
              }))
            ])
          : h('div', { class: 'py-10 text-center text-slate-400 text-sm border border-slate-200 rounded-lg' }, 'No assessments recorded for this term.'),
      ]),
      // Grading key
      h('div', { class: 'mx-8 mb-5 bg-slate-50 border border-slate-200 rounded-lg p-4' }, [
        h('p', { class: 'text-xs font-bold uppercase tracking-widest text-slate-400 mb-2' }, 'CBC Grading Scale'),
        h('div', { class: 'grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs' }, [
          h('div', { class: 'flex items-center gap-2' }, [
            h('span', { class: 'inline-block w-7 text-center bg-emerald-100 text-emerald-700 rounded font-black text-xs py-0.5' }, 'EE'),
            h('span', { class: 'text-slate-500' }, 'Exceeding Expectations'),
          ]),
          h('div', { class: 'flex items-center gap-2' }, [
            h('span', { class: 'inline-block w-7 text-center bg-blue-100 text-blue-700 rounded font-black text-xs py-0.5' }, 'ME'),
            h('span', { class: 'text-slate-500' }, 'Meeting Expectations'),
          ]),
          h('div', { class: 'flex items-center gap-2' }, [
            h('span', { class: 'inline-block w-7 text-center bg-amber-100 text-amber-700 rounded font-black text-xs py-0.5' }, 'AE'),
            h('span', { class: 'text-slate-500' }, 'Approaching Expectations'),
          ]),
          h('div', { class: 'flex items-center gap-2' }, [
            h('span', { class: 'inline-block w-7 text-center bg-red-100 text-red-600 rounded font-black text-xs py-0.5' }, 'BE'),
            h('span', { class: 'text-slate-500' }, 'Below Expectations'),
          ]),
        ]),
      ]),
      // Signatures
      h('div', { class: 'mx-8 mb-8 flex justify-between items-end' }, [
        h('div', { class: 'text-center' }, [
          h('div', { class: 'w-48 border-t-2 border-slate-700 pt-2' }),
          h('p', { class: 'text-xs font-bold text-slate-600 mt-1' }, 'Class Teacher Signature'),
          h('p', { class: 'text-xs text-slate-400' }, 'Name & Date'),
        ]),
        h('div', { class: 'text-center text-xs text-slate-400 italic' }, [
          h('p', {}, 'This is an official document of'),
          h('p', { class: 'font-semibold text-slate-600 not-italic text-xs' }, 'The Bona School'),
        ]),
        h('div', { class: 'text-center' }, [
          h('div', { class: 'w-48 border-t-2 border-slate-700 pt-2' }),
          h('p', { class: 'text-xs font-bold text-slate-600 mt-1' }, "Principal's Signature"),
          h('p', { class: 'text-xs text-slate-400' }, 'Name & Date'),
        ]),
      ]),
    ])
  },
})

const printPage = () => window.print()

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
    reportData.value = await academicService.getReportCard(
      selectedStudent.value, selectedTerm.value, appStore.currentYear
    )
  } catch {
    toast.error('Failed to load report card.')
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
      gradeStudents.map(s => academicService.getReportCard(
        s.id, selectedTerm.value, appStore.currentYear
      ).catch(() => null))
    )
    bulkReports.value = reports.filter(Boolean)
  } catch (e) {
    toast.error('Failed to load reports.')
  } finally {
    generating.value = false
  }
}
</script>

<style>
@media print {
  .print\:page-break-after-always {
    page-break-after: always;
    break-after: page;
  }
  .print\:rounded-none { border-radius: 0 !important; }
  .print\:border-none { border: none !important; }
  .print\:mb-0 { margin-bottom: 0 !important; }
}
</style>
