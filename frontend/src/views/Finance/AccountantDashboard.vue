<template>
  <div class="p-8 bg-gray-50 min-h-screen">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">Finance & Fees</h1>
      <button
        @click="openModal"
        class="bg-emerald-700 text-white px-4 py-2 rounded shadow hover:bg-emerald-600 transition"
      >
        + Record Payment
      </button>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-12 text-gray-500">
      <span class="animate-pulse text-lg">Loading financial ledger...</span>
    </div>

    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr
            class="bg-gray-100 text-gray-600 text-sm uppercase tracking-wider border-b border-gray-200"
          >
            <th class="p-4 font-semibold">Date</th>
            <th class="p-4 font-semibold">Student Name</th>
            <th class="p-4 font-semibold">Payment Type</th>
            <th class="p-4 font-semibold text-right">Amount</th>
            <th class="p-4 font-semibold">Recorded By</th>
          </tr>
        </thead>

        <tbody class="text-gray-700">
          <tr
            v-for="fee in fees"
            :key="fee.id"
            class="border-b border-gray-50 hover:bg-gray-50 transition duration-150"
          >
            <td class="p-4 text-sm text-gray-500">{{ formatDate(fee.payment_date) }}</td>
            <td class="p-4 font-medium text-school-navy">{{ getStudentName(fee.student_id) }}</td>
            <td class="p-4">
              <span class="px-3 py-1 text-xs font-bold rounded-full bg-gray-100 text-gray-700">
                {{ fee.payment_type }}
              </span>
            </td>
            <td class="p-4 text-right font-bold text-emerald-700">
              {{ formatCurrency(fee.amount) }}
            </td>
            <td class="p-4 text-sm text-gray-500">{{ fee.recorded_by }}</td>
          </tr>

          <tr v-if="fees.length === 0">
            <td colspan="5" class="p-8 text-center text-gray-500 italic">
              No payments have been recorded yet.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
    >
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center">
          <h2 class="text-xl font-bold text-gray-800">Record New Payment</h2>
          <button @click="closeModal" class="text-gray-400 hover:text-gray-600 font-bold text-xl">
            &times;
          </button>
        </div>

        <form @submit.prevent="submitFee" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Select Student</label>
            <select
              v-model="formData.student_id"
              required
              class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-600 outline-none"
            >
              <option disabled value="">-- Choose a student --</option>
              <option v-for="student in students" :key="student.id" :value="student.id">
                {{ student.first_name }} {{ student.last_name }} ({{ student.admission_number }})
              </option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
              <select
                v-model="formData.payment_type"
                required
                class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-600 outline-none"
              >
                <option value="Tuition">Tuition</option>
                <option value="Uniforms & Industrial Wear">Uniforms & Industrial Wear</option>
                <option value="Transport">Transport</option>
                <option value="Exam Fees">Exam Fees</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Amount (Ksh)</label>
              <input
                v-model.number="formData.amount"
                type="number"
                step="0.01"
                min="0"
                required
                class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-600 outline-none"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Term</label>
            <select
              v-model="formData.term"
              required
              class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-emerald-600 outline-none"
            >
              <option value="Term 1">Term 1</option>
              <option value="Term 2">Term 2</option>
              <option value="Term 3">Term 3</option>
            </select>
          </div>

          <div class="flex justify-end space-x-3 pt-4 border-t border-gray-100 mt-6">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg font-medium transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-emerald-700 text-white rounded-lg font-medium hover:bg-emerald-600 transition"
            >
              Save Payment
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import feeService from '@/services/feeService'
import studentService from '@/services/studentService' // Needed for the dropdown!

const fees = ref([])
const students = ref([])
const loading = ref(true)
const showModal = ref(false)

const formData = reactive({
  student_id: '',
  amount: null,
  payment_type: 'Tuition',
  term: 'Term 1',
})

const loadData = async () => {
  loading.value = true
  try {
    // Fetch both simultaneously to save time
    const [fetchedFees, fetchedStudents] = await Promise.all([
      feeService.getAllFees(),
      studentService.getAllStudents(),
    ])
    fees.value = fetchedFees
    students.value = fetchedStudents
  } catch (error) {
    console.error('Error loading finance data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(loadData)

// --- HELPER FUNCTIONS ---
const getStudentName = (studentId) => {
  const student = students.value.find((s) => s.id === studentId)
  return student ? `${student.first_name} ${student.last_name}` : 'Unknown Student'
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES' }).format(amount)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-GB')
}

// --- MODAL LOGIC ---
const openModal = () => {
  formData.student_id = ''
  formData.amount = null
  formData.payment_type = 'Tuition'
  formData.term = 'Term 1'
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const submitFee = async () => {
  try {
    await feeService.recordFee(formData)
    closeModal()
    await loadData() // Refresh the ledger
  } catch (error) {
    alert('Failed to save the payment.')
    console.error(error)
  }
}
</script>
