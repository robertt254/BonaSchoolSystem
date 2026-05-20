<template>
  <div class="max-w-4xl mx-auto space-y-5">

    <!-- Controls (hidden when printing) -->
    <div class="bg-white rounded-xl border border-slate-200 p-5 print:hidden">
      <h2 class="text-base font-bold text-slate-800 mb-4">Generate CBC Report Card</h2>
      <div class="flex flex-col sm:flex-row gap-4 items-end">
        <div class="flex-1">
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Student</label>
          <select
            v-model="selectedStudent"
            class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none"
          >
            <option disabled value="">— Choose a student —</option>
            <option v-for="s in students" :key="s.id" :value="s.id">
              {{ s.first_name }} {{ s.last_name }} · {{ s.admission_number }}
            </option>
          </select>
        </div>
        <div class="w-40">
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Term</label>
          <select
            v-model="selectedTerm"
            class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none"
          >
            <option value="Term 1">Term 1</option>
            <option value="Term 2">Term 2</option>
            <option value="Term 3">Term 3</option>
          </select>
        </div>
        <button
          @click="loadReport"
          :disabled="!selectedStudent || generating"
          class="bg-school-navy text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-navy/90 transition disabled:opacity-50"
        >
          {{ generating ? 'Loading…' : 'Generate' }}
        </button>
      </div>
    </div>

    <!-- Report card document -->
    <div
      v-if="reportData"
      id="report-card"
      class="bg-white rounded-xl border border-slate-200 overflow-hidden print:rounded-none print:border-none print:shadow-none"
    >
      <!-- Header band -->
      <div class="bg-school-navy text-white px-10 py-8 print:px-8 print:py-6">
        <div class="flex items-start justify-between">
          <div>
            <h1 class="text-2xl font-black uppercase tracking-wider">The Bona School</h1>
            <p class="text-white/60 text-sm mt-1">Competency-Based Curriculum (CBC) · Nairobi, Kenya</p>
          </div>
          <div class="text-right">
            <p class="text-white/40 text-xs uppercase tracking-widest font-bold">Report Card</p>
            <p class="text-white font-bold mt-0.5">{{ reportData.term }} · {{ new Date().getFullYear() }}</p>
          </div>
        </div>
      </div>

      <!-- Student info strip -->
      <div class="grid grid-cols-3 gap-0 border-b border-slate-200 bg-slate-50 divide-x divide-slate-200">
        <div class="px-6 py-4">
          <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Student Name</p>
          <p class="font-bold text-slate-800 mt-0.5">{{ reportData.student_name }}</p>
        </div>
        <div class="px-6 py-4">
          <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Admission No.</p>
          <p class="font-bold text-slate-800 mt-0.5 font-mono">{{ reportData.admission_number }}</p>
        </div>
        <div class="px-6 py-4">
          <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Grade / Term</p>
          <p class="font-bold text-slate-800 mt-0.5">{{ reportData.grade_level }} · {{ reportData.term }}</p>
        </div>
      </div>

      <!-- Assessment table -->
      <div class="px-8 py-6 print:px-8">
        <h3 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4">CBC Assessment Results</h3>
        <table class="w-full border-collapse border border-slate-200 text-sm">
          <thead>
            <tr class="bg-slate-50">
              <th class="border border-slate-200 px-5 py-3 text-left font-bold text-slate-600 uppercase text-xs tracking-wider">Learning Area</th>
              <th class="border border-slate-200 px-5 py-3 text-center font-bold text-slate-600 uppercase text-xs tracking-wider w-24">Score</th>
              <th class="border border-slate-200 px-5 py-3 text-left font-bold text-slate-600 uppercase text-xs tracking-wider">Remarks</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in reportData.results" :key="r.learning_area" class="hover:bg-slate-50/50">
              <td class="border border-slate-200 px-5 py-3 font-medium text-slate-800">{{ r.learning_area }}</td>
              <td class="border border-slate-200 px-5 py-3 text-center">
                <span class="inline-block px-3 py-0.5 rounded-full text-xs font-black" :class="scoreClass(r.score)">{{ r.score }}</span>
              </td>
              <td class="border border-slate-200 px-5 py-3 text-slate-500 italic text-xs">{{ r.remarks || '—' }}</td>
            </tr>
            <tr v-if="!reportData.results.length">
              <td colspan="3" class="border border-slate-200 px-5 py-8 text-center text-slate-400">No assessments recorded for this term.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Grading key -->
      <div class="mx-8 mb-6 bg-slate-50 border border-slate-200 rounded-lg p-4 print:mx-8">
        <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-2">CBC Grading Key</p>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
          <span><strong class="text-emerald-700">EE (4)</strong> — Exceeding Expectations</span>
          <span><strong class="text-blue-700">ME (3)</strong> — Meeting Expectations</span>
          <span><strong class="text-amber-600">AE (2)</strong> — Approaching Expectations</span>
          <span><strong class="text-red-600">BE (1)</strong> — Below Expectations</span>
        </div>
      </div>

      <!-- Signatures -->
      <div class="mx-8 mb-8 flex justify-between print:mx-8">
        <div class="w-52 border-t-2 border-slate-800 pt-2 text-center">
          <p class="text-xs font-bold text-slate-600">Class Teacher</p>
        </div>
        <div class="w-52 border-t-2 border-slate-800 pt-2 text-center">
          <p class="text-xs font-bold text-slate-600">Principal</p>
        </div>
      </div>

      <!-- Print button -->
      <div class="border-t border-slate-100 px-8 py-4 flex justify-end print:hidden">
        <button
          @click="window.print()"
          class="inline-flex items-center gap-2 bg-slate-800 text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-black transition"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
            <rect x="6" y="14" width="12" height="8"/>
          </svg>
          Print Report Card
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import studentService from '@/services/studentService'
import academicService from '@/services/academicService'

const students       = ref([])
const selectedStudent = ref('')
const selectedTerm   = ref('Term 1')
const reportData     = ref(null)
const generating     = ref(false)

const scoreClass = (s) => ({
  EE: 'bg-emerald-100 text-emerald-700',
  ME: 'bg-blue-100 text-blue-700',
  AE: 'bg-amber-100 text-amber-700',
  BE: 'bg-red-100 text-red-600',
}[s] || 'bg-slate-100 text-slate-600')

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
</script>

<style>
@media print {
  body * { visibility: hidden; }
  #report-card, #report-card * { visibility: visible; }
  #report-card { position: fixed; top: 0; left: 0; width: 100%; }
}
</style>
