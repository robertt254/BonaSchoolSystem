<template>
  <div class="p-8 bg-gray-50 min-h-screen print:p-0 print:bg-white">

    <div class="mb-8 bg-white p-6 rounded-xl shadow-sm border border-gray-100 print:hidden">
      <h1 class="text-2xl font-bold text-gray-800 mb-4">Generate Fee Statement</h1>

      <div class="flex space-x-4 items-end">
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-1">Select Student</label>
          <select v-model="selectedStudent" class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-600 outline-none">
            <option disabled value="">-- Choose a student --</option>
            <option v-for="student in students" :key="student.id" :value="student.id">
              {{ student.first_name }} {{ student.last_name }} ({{ student.admission_number }})
            </option>
          </select>
        </div>

        <div class="w-48">
          <label class="block text-sm font-medium text-gray-700 mb-1">Academic Term</label>
          <select v-model="selectedTerm" class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-600 outline-none">
            <option value="Term 1">Term 1</option>
            <option value="Term 2">Term 2</option>
            <option value="Term 3">Term 3</option>
          </select>
        </div>

        <button
          @click="generateStatement"
          :disabled="!selectedStudent"
          class="bg-emerald-700 text-white px-6 py-2 rounded-lg shadow hover:bg-emerald-600 transition disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          Generate Report
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-12 text-gray-500 print:hidden">
      <span class="animate-pulse">Calculating balances...</span>
    </div>

    <div
      v-if="statementData && !loading"
      class="bg-white max-w-3xl mx-auto p-10 rounded-xl shadow-lg border border-gray-200 print:shadow-none print:border-none print:m-0 print:p-0"
    >
      <div class="text-center border-b-2 border-gray-800 pb-6 mb-6">
        <h2 class="text-3xl font-black text-gray-900 uppercase tracking-widest">The Bona School</h2>
        <p class="text-gray-600 mt-1">Competency-Based Curriculum (CBC)</p>
        <p class="text-gray-500 text-sm">Nairobi, Kenya • Finance Department</p>
      </div>

      <div class="flex justify-between items-center mb-8">
        <h3 class="text-xl font-bold text-gray-800 bg-gray-100 px-4 py-2 rounded">OFFICIAL FEE STATEMENT</h3>
        <p class="text-gray-600 font-medium">Date: {{ currentDate }}</p>
      </div>

      <div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mb-8 grid grid-cols-2 gap-4">
        <div>
          <p class="text-sm text-gray-500 uppercase tracking-wider">Student Name</p>
          <p class="text-lg font-bold text-gray-900">{{ statementData.student_name }}</p>
        </div>
        <div class="text-right">
          <p class="text-sm text-gray-500 uppercase tracking-wider">Academic Level</p>
          <p class="text-lg font-bold text-gray-900">{{ statementData.grade_level }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500 uppercase tracking-wider">Billing Period</p>
          <p class="text-lg font-bold text-gray-900">{{ statementData.term_checked }}</p>
        </div>
      </div>

      <table class="w-full mb-8">
        <tbody>
          <tr class="border-b border-gray-200">
            <td class="py-4 text-gray-600 font-medium">Expected Fee for {{ statementData.term_checked }}</td>
            <td class="py-4 text-right font-bold text-gray-900">{{ formatCurrency(statementData.expected_term_fee) }}</td>
          </tr>
          <tr class="border-b border-gray-200 bg-emerald-50">
            <td class="py-4 px-2 text-emerald-800 font-medium">Total Installments Paid</td>
            <td class="py-4 px-2 text-right font-bold text-emerald-800">- {{ formatCurrency(statementData.total_paid_this_term) }}</td>
          </tr>
          <tr class="border-b-4 border-gray-800">
            <td class="py-6 text-xl font-black text-gray-900 uppercase">Outstanding Balance</td>
            <td class="py-6 text-right text-2xl font-black text-red-600">
              {{ formatCurrency(statementData.outstanding_balance) }}
            </td>
          </tr>
        </tbody>
      </table>

      <div class="mt-16 pt-8 flex justify-between">
        <div class="w-64 border-t border-gray-400 text-center pt-2">
          <p class="text-sm text-gray-600">Accountant Signature</p>
        </div>
        <div class="w-64 border-t border-gray-400 text-center pt-2">
          <p class="text-sm text-gray-600">Parent/Guardian Signature</p>
        </div>
      </div>

      <div class="mt-12 text-center print:hidden">
        <button
          @click="printDocument"
          class="bg-gray-800 text-white px-8 py-3 rounded-lg shadow-lg hover:bg-black transition font-bold"
        >
          🖨️ Print Statement
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import studentService from '@/services/studentService'
import feeService from '@/services/feeService'

// State
const students = ref([])
const selectedStudent = ref('')
const selectedTerm = ref('Term 1')
const statementData = ref(null)
const loading = ref(false)

// Get today's date formatted
const currentDate = computed(() => {
  return new Date().toLocaleDateString('en-GB', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
})

// Currency formatter for Ksh
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES' }).format(amount)
}

// Load dropdown data
onMounted(async () => {
  try {
    students.value = await studentService.getAllStudents()
  } catch (error) {
    console.error("Failed to load students", error)
  }
})

// Fetch the math from Python
const generateStatement = async () => {
  loading.value = true
  try {
    statementData.value = await feeService.getStudentBalance(selectedStudent.value, selectedTerm.value)
  } catch (error) {
    alert("Failed to generate statement. Make sure the backend is running.")
    console.error(error)
  } finally {
    loading.value = false
  }
}

// Trigger the browser's native print dialog
const printDocument = () => {
  window.print()
}
</script>
