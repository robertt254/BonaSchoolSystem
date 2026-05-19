<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 bg-slate-50 min-h-screen print:p-0 print:bg-white">
    <div class="mb-8 bg-white p-8 rounded-[12px] shadow-sm border border-[#E2E8F0] print:hidden">
      <h1 class="font-heading text-[22px] font-bold text-[#0F172A] mb-4">
        Generate Official Report Card
      </h1>

      <div class="flex gap-8 items-end">
        <div class="flex-1">
          <label class="block text-sm font-medium text-slate-700 mb-1">Select Student</label>
          <select
            v-model="selectedStudent"
            class="w-full border px-4 py-3.5 rounded-lg focus:ring-2 focus:ring-school-navy outline-none"
          >
            <option disabled value="">-- Choose a student --</option>
            <option v-for="student in students" :key="student.id" :value="student.id">
              {{ student.first_name }} {{ student.last_name }} ({{ student.admission_number }})
            </option>
          </select>
        </div>

        <div class="w-48">
          <label class="block text-sm font-medium text-slate-700 mb-1">Academic Term</label>
          <select
            v-model="selectedTerm"
            class="w-full border px-4 py-3.5 rounded-lg focus:ring-2 focus:ring-school-navy outline-none"
          >
            <option value="Term 1">Term 1</option>
            <option value="Term 2">Term 2</option>
            <option value="Term 3">Term 3</option>
          </select>
        </div>

        <button
          @click="loadReport"
          :disabled="!selectedStudent"
          class="bg-school-navy text-white px-6 py-3.5 rounded-lg font-medium hover:bg-school-navy/90 transition disabled:bg-gray-300"
        >
          Generate Report
        </button>
      </div>
    </div>

    <div
      v-if="reportData"
      class="bg-white max-w-4xl mx-auto p-12 rounded-[12px] shadow-lg border border-gray-200 print:shadow-none print:border-none print:m-0 print:p-0"
    >
      <div class="text-center border-b-4 border-school-navy pb-6 mb-8">
        <h1 class="text-4xl font-black text-gray-900 uppercase tracking-wider">The Bona School</h1>
        <p class="text-lg text-gray-700 font-medium mt-2">
          Competency-Based Curriculum (CBC) Performance Report
        </p>
      </div>

      <div
        class="flex justify-between items-center bg-school-grey/50 p-8 rounded-lg mb-8 border border-school-grey/80"
      >
        <div>
          <p class="text-sm text-school-navy/90 font-bold uppercase tracking-wider">Student Name</p>
          <p class="text-2xl font-black text-gray-900">{{ reportData.student_name }}</p>
        </div>
        <div class="text-right">
          <p class="text-sm text-school-navy/90 font-bold uppercase tracking-wider">Details</p>
          <p class="text-lg font-bold text-gray-900">
            {{ reportData.grade_level }} • {{ reportData.term }}
          </p>
          <p class="text-sm text-gray-600">ADM: {{ reportData.admission_number }}</p>
        </div>
      </div>

      <table class="w-full mb-12 border-collapse border border-gray-300">
        <thead>
          <tr class="bg-gray-100">
            <th
              class="py-5 px-8 text-left font-bold text-gray-800 uppercase text-sm w-1/3"
            >
              Learning Area
            </th>
            <th
              class="py-5 px-8 text-center font-bold text-gray-800 uppercase text-sm w-1/6"
            >
              Score
            </th>
            <th
              class="py-5 px-8 text-left font-bold text-gray-800 uppercase text-sm"
            >
              Teacher's Remarks
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in reportData.results" :key="result.learning_area">
            <td class="py-5 px-8 font-medium text-gray-900">
              {{ result.learning_area }}
            </td>
            <td
              class="py-5 px-8 text-center font-black text-lg"
              :class="{
                'text-green-600': result.score === 'EE',
                'text-school-navy/70': result.score === 'ME',
                'text-orange-500': result.score === 'AE',
                'text-red-600': result.score === 'BE',
              }"
            >
              {{ result.score }}
            </td>
            <td class="py-5 px-8 text-gray-700 italic">
              {{ result.remarks || '---' }}
            </td>
          </tr>
          <tr v-if="reportData.results.length === 0">
            <td colspan="3" class="py-6 px-8 text-center text-gray-500 font-medium">
              No assessments recorded for this term yet.
            </td>
          </tr>
        </tbody>
      </table>

      <div class="bg-gray-50 border border-gray-200 p-8 rounded-lg mb-12">
        <h4 class="font-bold text-gray-800 uppercase text-sm mb-4 border-b pb-2">
          CBC Grading Key
        </h4>
        <div class="grid grid-cols-2 gap-4 text-sm text-gray-700">
          <p><span class="font-bold text-green-600">EE (4):</span> Exceeding Expectations</p>
          <p><span class="font-bold text-school-navy/70">ME (3):</span> Meeting Expectations</p>
          <p><span class="font-bold text-orange-500">AE (2):</span> Approaching Expectations</p>
          <p><span class="font-bold text-red-600">BE (1):</span> Below Expectations</p>
        </div>
      </div>

      <div class="flex justify-between pt-12 mt-12">
        <div class="w-64 border-t-2 border-gray-800 text-center pt-2">
          <p class="font-bold text-gray-800">Class Teacher</p>
        </div>
        <div class="w-64 border-t-2 border-gray-800 text-center pt-2">
          <p class="font-bold text-gray-800">Principal</p>
        </div>
      </div>

      <div class="mt-16 text-center print:hidden">
        <button
          @click="printDoc"
          class="bg-gray-900 text-white px-8 py-4 rounded-lg shadow-lg hover:bg-black font-bold"
        >
          🖨️ Print Report Card
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import studentService from '@/services/studentService'
import academicService from '@/services/academicService'

const students = ref([])
const selectedStudent = ref('')
const selectedTerm = ref('Term 1')
const reportData = ref(null)

onMounted(async () => {
  try {
    students.value = await studentService.getAllStudents()
  } catch (error) {
    console.error(error)
  }
})

const loadReport = async () => {
  try {
    reportData.value = await academicService.getReportCard(
      selectedStudent.value,
      selectedTerm.value,
    )
  } catch {
    alert('Failed to load report card.')
  }
}

const printDoc = () => window.print()
</script>
