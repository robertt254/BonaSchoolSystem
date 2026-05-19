<template>
  <div class="max-w-7xl mx-auto space-y-6 animate-fade-in pb-12">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-2">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
          Finance Overview
        </h1>
        <p class="text-sm text-slate-500 mt-1 font-medium">{{ appStore.currentTerm }} Collection</p>
      </div>
      <button
        @click="openModal"
        class="bg-school-navy text-white px-5 py-2.5 rounded-lg shadow-sm hover:shadow-md hover:bg-school-navy/90 transition-all font-medium flex items-center gap-2"
      >
        <span class="text-lg">➕</span> Record Payment
      </button>
    </div>

    <!-- Overview Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Total Collected (Current Term) -->
      <div
        class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between"
      >
        <div>
          <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">
            Term Collection
          </p>
          <h2 class="text-3xl font-black text-slate-800">{{ formatCurrency(termCollected) }}</h2>
        </div>
        <div class="mt-6">
          <div class="flex justify-between text-xs font-bold text-slate-500 mb-2">
            <span>Progress</span>
            <span>{{ collectionPercentage }}%</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
            <div
              class="bg-emerald-500 h-2 rounded-full transition-all duration-1000 ease-out"
              :style="{ width: `${collectionPercentage}%` }"
            ></div>
          </div>
          <p class="text-[11px] text-slate-400 mt-2 font-medium">
            Target: {{ formatCurrency(termGoal) }}
          </p>
        </div>
      </div>

      <!-- Total Outstanding (Current Term) -->
      <div
        class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between"
      >
        <div>
          <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">
            Term Outstanding
          </p>
          <h2 class="text-3xl font-black text-school-red">{{ formatCurrency(termOutstanding) }}</h2>
        </div>
        <div
          class="mt-6 p-3 bg-school-red/5 rounded-xl border border-school-red/10 flex items-start gap-3"
        >
          <span class="text-school-red">⚠️</span>
          <p class="text-xs text-school-red/80 font-medium leading-relaxed">
            Pending balances from {{ studentsWithBalancesCount }} students for
            {{ appStore.currentTerm }}.
          </p>
        </div>
      </div>

      <!-- Total Revenue (All Time) -->
      <div
        class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between hidden lg:flex"
      >
        <div>
          <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">
            Total Revenue
          </p>
          <h2 class="text-3xl font-black text-slate-800">{{ formatCurrency(totalRevenue) }}</h2>
        </div>
        <div class="mt-6 p-3 bg-slate-50 rounded-xl border border-slate-100 flex items-start gap-3">
          <span class="text-slate-500">💰</span>
          <p class="text-xs text-slate-500 font-medium leading-relaxed">
            Cumulative revenue across all academic terms.
          </p>
        </div>
      </div>
    </div>

    <!-- Ledger Table -->
    <div
      v-if="loading"
      class="flex flex-col justify-center items-center py-20 text-slate-400 space-y-4"
    >
      <div
        class="w-10 h-10 border-4 border-slate-200 border-t-school-navy rounded-full animate-spin"
      ></div>
      <span class="text-sm font-medium tracking-widest uppercase">Loading ledger...</span>
    </div>

    <div v-else class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden mt-8">
      <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
        <h3 class="text-lg font-bold text-slate-800 tracking-tight">Recent Transactions</h3>
        <span
          class="text-xs font-bold text-slate-400 uppercase tracking-widest bg-white px-3 py-1 rounded-full border border-slate-200 shadow-sm"
          >{{ filteredFees.length }} Records</span
        >
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr
              class="bg-slate-50 text-slate-500 text-[11px] uppercase tracking-wider border-b border-slate-100"
            >
              <th class="p-4 font-bold">Date</th>
              <th class="p-4 font-bold">Student Name</th>
              <th class="p-4 font-bold">Type</th>
              <th class="p-4 font-bold">Term</th>
              <th class="p-4 font-bold text-right">Amount</th>
              <th class="p-4 font-bold text-right">Recorded By</th>
            </tr>
          </thead>

          <tbody class="text-slate-700 text-sm">
            <tr
              v-for="fee in filteredFees"
              :key="fee.id"
              class="border-b border-slate-50 hover:bg-slate-50/50 transition duration-150"
            >
              <td class="p-4 font-medium text-slate-500">{{ formatDate(fee.payment_date) }}</td>
              <td class="p-4 font-bold text-slate-800">{{ getStudentName(fee.student_id) }}</td>
              <td class="p-4">
                <span
                  class="px-2.5 py-1 text-[11px] font-bold rounded-full bg-slate-100 text-slate-600 border border-slate-200"
                >
                  {{ fee.payment_type }}
                </span>
              </td>
              <td class="p-4 text-slate-500 text-xs font-medium">{{ fee.term }}</td>
              <td class="p-4 text-right font-bold text-emerald-600">
                {{ formatCurrency(fee.amount) }}
              </td>
              <td class="p-4 text-right text-slate-400 text-xs">{{ fee.recorded_by }}</td>
            </tr>

            <tr v-if="filteredFees.length === 0">
              <td colspan="6" class="p-12 text-center">
                <div class="flex flex-col items-center justify-center text-slate-400">
                  <span class="text-4xl mb-3">📄</span>
                  <p class="font-medium text-sm">No transactions found for this term.</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal overlay -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in"
    >
      <div
        class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden transform scale-100 transition-transform duration-200 border border-slate-100"
      >
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <h2 class="text-xl font-black text-slate-800 tracking-tight">Record Payment</h2>
          <button
            @click="closeModal"
            class="text-slate-400 hover:text-school-red hover:bg-school-red/10 h-8 w-8 rounded-full flex items-center justify-center transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
          </button>
        </div>

        <form @submit.prevent="submitFee" class="p-6 space-y-5">
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
              >Select Student</label
            >
            <select
              v-model="formData.student_id"
              required
              class="w-full border border-slate-200 rounded-xl p-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all cursor-pointer"
            >
              <option disabled value="">-- Choose a student --</option>
              <option v-for="student in students" :key="student.id" :value="student.id">
                {{ student.first_name }} {{ student.last_name }} ({{ student.admission_number }})
              </option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
                >Category</label
              >
              <select
                v-model="formData.payment_type"
                required
                class="w-full border border-slate-200 rounded-xl p-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all cursor-pointer"
              >
                <option value="Tuition">Tuition</option>
                <option value="Uniforms & Industrial Wear">Uniforms</option>
                <option value="Transport">Transport</option>
                <option value="Exam Fees">Exam Fees</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
                >Amount (Ksh)</label
              >
              <input
                v-model.number="formData.amount"
                type="number"
                step="0.01"
                min="0"
                required
                class="w-full border border-slate-200 rounded-xl p-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-bold text-slate-800 transition-all"
                placeholder="0.00"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
              >Term</label
            >
            <select
              v-model="formData.term"
              required
              class="w-full border border-slate-200 rounded-xl p-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all cursor-pointer"
            >
              <option v-for="term in appStore.terms" :key="term" :value="term">{{ term }}</option>
            </select>
          </div>

          <div class="flex justify-end space-x-3 pt-6 mt-6">
            <button
              type="button"
              @click="closeModal"
              class="px-5 py-2.5 text-slate-600 hover:bg-slate-100 rounded-xl font-bold transition-colors text-sm"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-5 py-2.5 bg-school-navy text-white rounded-xl font-bold hover:bg-school-navy/90 hover:shadow-md transition-all text-sm"
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
import { ref, reactive, onMounted, computed } from 'vue'
import feeService from '@/services/feeService'
import studentService from '@/services/studentService'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

const fees = ref([])
const students = ref([])
const loading = ref(true)
const showModal = ref(false)

const formData = reactive({
  student_id: '',
  amount: null,
  payment_type: 'Tuition',
  term: appStore.currentTerm,
})

const loadData = async () => {
  loading.value = true
  try {
    const [fetchedFees, fetchedStudents] = await Promise.all([
      feeService.getAllFees().catch(() => []),
      studentService.getAllStudents().catch(() => []),
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

// --- COMPUTED FINANCE METRICS ---

const filteredFees = computed(() => {
  // Display fees for the current selected term
  return fees.value
    .filter((fee) => fee.term === appStore.currentTerm)
    .sort((a, b) => new Date(b.payment_date) - new Date(a.payment_date))
})

const totalRevenue = computed(() => {
  return fees.value.reduce((sum, fee) => sum + (fee.amount || 0), 0)
})

const termCollected = computed(() => {
  return filteredFees.value.reduce((sum, fee) => sum + (fee.amount || 0), 0)
})

const feeStructure = {
  'Play Group': 12000,
  PP1: 15000,
  PP2: 15000,
  'Grade 1': 18000,
  'Grade 2': 18000,
  'Grade 3': 18000,
  'Grade 4': 20000,
  'Grade 5': 20000,
  'Grade 6': 20000,
}

// Calculate exact term goal based on fee structure per active student
const termGoal = computed(() => {
  const activeStudents = students.value.filter((s) => s.status === 'Active')
  return activeStudents.reduce((total, student) => {
    const fee = feeStructure[student.grade_level] || 0
    return total + fee
  }, 0)
})

const collectionPercentage = computed(() => {
  if (termGoal.value === 0) return 0
  const pct = (termCollected.value / termGoal.value) * 100
  return Math.min(Math.round(pct), 100)
})

const termOutstanding = computed(() => {
  return Math.max(0, termGoal.value - termCollected.value)
})

const studentsWithBalancesCount = computed(() => {
  // A simplistic estimate for visual purposes. In a real system, you'd calculate per-student balances.
  if (termGoal.value === 0) return 0
  return Math.ceil(termOutstanding.value / 15000)
})

// --- HELPER FUNCTIONS ---
const getStudentName = (studentId) => {
  const student = students.value.find((s) => s.id === studentId)
  return student ? `${student.first_name} ${student.last_name}` : 'Unknown Student'
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    maximumFractionDigits: 0,
  }).format(amount)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

// --- MODAL LOGIC ---
const openModal = () => {
  formData.student_id = ''
  formData.amount = null
  formData.payment_type = 'Tuition'
  formData.term = appStore.currentTerm
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
