<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="font-heading text-[22px] font-bold text-[#0F172A] tracking-tight">
          Finance Dashboard
        </h1>
        <p class="text-[13px] text-[#94A3B8] mt-1">
          Manage school collections, ledgers, and payroll.
        </p>
      </div>
    </div>

    <!-- Loading State -->
    <div
      v-if="loading"
      class="flex flex-col justify-center items-center py-20 text-slate-400 space-y-4"
    >
      <div
        class="w-8 h-8 border-4 border-[#E2E8F0] border-t-school-navy rounded-full animate-spin mx-auto"
      ></div>
      <span class="text-xs font-bold tracking-widest uppercase">Loading Finance Data...</span>
    </div>

    <div v-else class="space-y-8">
      <!-- High-Level Metrics -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-8">
        <!-- Goal Progress -->
        <div
          class="bg-white p-8 rounded-[12px] border border-[#E2E8F0] shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] col-span-1 sm:col-span-2 relative overflow-hidden group"
        >
          <div
            class="absolute right-0 top-0 w-32 h-32 bg-blue-50 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-110"
          ></div>
          <div class="relative z-10">
            <div class="flex justify-between items-end mb-4">
              <div>
                <div class="text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1">
                  {{ appStore.currentTerm }} Collection
                </div>
                <div class="text-4xl font-extrabold text-slate-800">
                  {{ formatCurrency(termCollected) }}
                </div>
              </div>
              <div class="text-right">
                <div class="text-sm font-bold text-school-navy">{{ collectionPercentage }}%</div>
                <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Target: {{ formatCurrency(termGoal) }}
                </div>
              </div>
            </div>
            <!-- Progress Bar -->
            <div class="w-full bg-slate-100 rounded-full h-3 mb-2">
              <div
                class="bg-school-navy h-3 rounded-full transition-all duration-1000"
                :style="{ width: collectionPercentage + '%' }"
              ></div>
            </div>
          </div>
        </div>

        <!-- Total Revenue -->
        <div
          class="bg-white p-8 rounded-[12px] border border-[#E2E8F0] shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] relative overflow-hidden group"
        >
          <div
            class="absolute right-0 top-0 w-24 h-24 bg-emerald-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"
          ></div>
          <div class="relative z-10 flex flex-col justify-between h-full">
            <div>
              <div class="text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1">
                Total Revenue
              </div>
              <div class="text-3xl font-extrabold text-emerald-600">
                {{ formatCurrency(totalRevenue) }}
              </div>
            </div>
            <div class="mt-4 flex items-center text-xs text-slate-500 font-medium">
              <span class="text-amber-500 mr-1">💰</span> Cumulative across all terms.
            </div>
          </div>
        </div>
      </div>

      <!-- Payroll Module -->
      <div
        class="bg-white rounded-[12px] border border-[#E2E8F0] shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] overflow-hidden"
      >
        <div
          class="border-b border-slate-100 px-8 py-6 flex items-center justify-between bg-slate-50"
        >
          <div>
            <h3 class="text-lg font-bold text-slate-800 tracking-tight">Payroll Ledger</h3>
            <p class="text-xs text-slate-500 mt-0.5">Staff salaries and disbursements.</p>
          </div>
          <button
            @click="openPayrollModal"
            class="bg-school-navy hover:bg-school-navy/90 text-white px-4 py-2 rounded-[12px] font-bold transition-all shadow-sm text-sm flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4v16m8-8H4"
              ></path>
            </svg>
            Execute Payroll
          </button>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr
                class="bg-white text-slate-500 text-[11px] uppercase tracking-wider border-b border-slate-100"
              >
                <th class="py-5 px-8 font-bold">Month</th>
                <th class="py-5 px-8 font-bold">Staff Member</th>
                <th class="py-5 px-8 font-bold text-right">Basic</th>
                <th class="py-5 px-8 font-bold text-right text-emerald-600">Allowances</th>
                <th class="py-5 px-8 font-bold text-right text-school-red">Deductions</th>
                <th class="py-5 px-8 pr-6 font-bold text-right text-slate-800">Net Pay</th>
              </tr>
            </thead>
            <tbody class="text-sm">
              <tr
                v-for="pay in payrollLedger"
                :key="pay.id"
                class="border-b border-slate-50 hover:bg-slate-50/50 transition duration-150"
              >
                <td class="py-5 px-8 font-medium text-slate-500">{{ pay.payment_month }}</td>
                <td class="py-5 px-8 font-bold text-slate-800">{{ getStaffName(pay.staff_id) }}</td>
                <td class="py-5 px-8 text-right text-slate-600">
                  {{ formatCurrency(pay.basic_salary) }}
                </td>
                <td class="py-5 px-8 text-right text-emerald-600">
                  {{ formatCurrency(pay.allowances) }}
                </td>
                <td class="py-5 px-8 text-right text-school-red">{{ formatCurrency(pay.deductions) }}</td>
                <td class="py-5 px-8 pr-6 text-right font-bold text-slate-800">
                  {{ formatCurrency(pay.net_pay) }}
                </td>
              </tr>
              <tr v-if="payrollLedger.length === 0">
                <td colspan="6" class="py-6 px-8 text-center text-slate-400 text-sm font-medium">
                  No payroll records found.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Payroll Modal -->
    <div
      v-if="showPayrollModal"
      class="fixed inset-0 bg-slate-900/40 flex items-center justify-center py-5 px-8 z-50 animate-fade-in"
    >
      <div
        class="bg-white rounded-[12px] shadow-2xl w-full max-w-md overflow-hidden border border-[#E2E8F0]"
      >
        <div class="p-8 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <h2 class="text-xl font-black text-slate-800 tracking-tight">Run Payroll</h2>
          <button
            @click="closePayrollModal"
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

        <form @submit.prevent="submitPayroll" class="p-8 space-y-6">
          <div>
            <label
              class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
              >Select Staff</label
            >
            <select
              v-model="payrollForm.staff_id"
              required
              class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all cursor-pointer"
            >
              <option disabled value="">-- Choose a staff member --</option>
              <option v-for="staff in activeStaff" :key="staff.id" :value="staff.id">
                {{ staff.name }} ({{ staff.job_title || staff.role }})
              </option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-8">
            <div>
              <label
                class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
                >Payment Month</label
              >
              <input
                v-model="payrollForm.payment_month"
                required
                type="month"
                class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all cursor-pointer"
              />
            </div>
            <div>
              <label
                class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
                >Basic Salary (Ksh)</label
              >
              <input
                v-model.number="payrollForm.basic_salary"
                type="number"
                min="0"
                required
                class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-bold text-slate-800 transition-all"
              />
            </div>
            <div>
              <label
                class="block text-xs font-bold text-emerald-600 uppercase tracking-widest mb-1.5"
                >Allowances (Ksh)</label
              >
              <input
                v-model.number="payrollForm.allowances"
                type="number"
                min="0"
                required
                class="w-full border border-emerald-200 rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none bg-emerald-50/50 font-bold text-emerald-700 transition-all"
              />
            </div>
            <div>
              <label
                class="block text-xs font-bold text-school-red uppercase tracking-widest mb-1.5"
                >Deductions (Ksh)</label
              >
              <input
                v-model.number="payrollForm.deductions"
                type="number"
                min="0"
                required
                class="w-full border border-red-200 rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-red/20 focus:border-school-red outline-none bg-red-50/50 font-bold text-school-red transition-all"
              />
            </div>
          </div>

          <!-- Net Pay Calculation -->
          <div
            class="py-5 px-8 bg-slate-50 rounded-[12px] border border-[#E2E8F0] flex justify-between items-center mt-2"
          >
            <span class="text-sm font-bold text-slate-500 uppercase tracking-widest"
              >Net Payable</span
            >
            <span class="text-xl font-black text-school-navy">{{
              formatCurrency(calculatedNetPay)
            }}</span>
          </div>

          <div class="flex justify-end gap-6 pt-4 mt-2">
            <button
              type="button"
              @click="closePayrollModal"
              class="px-8 py-4 text-slate-600 hover:bg-slate-100 rounded-[12px] font-bold transition-colors text-sm"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-8 py-4 bg-school-navy text-white rounded-[12px] font-bold hover:bg-school-navy/90 hover:shadow-md transition-all text-sm"
            >
              Disburse Funds
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
import staffService from '@/services/staffService'
import financeService from '@/services/financeService'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

const fees = ref([])
const students = ref([])
const activeStaff = ref([])
const payrollLedger = ref([])
const loading = ref(true)

const showPayrollModal = ref(false)

const payrollForm = reactive({
  staff_id: '',
  payment_month: '',
  basic_salary: 0,
  allowances: 0,
  deductions: 0,
})

const loadData = async () => {
  loading.value = true
  try {
    const [fetchedFees, fetchedStudents, fetchedStaff, fetchedPayroll] = await Promise.all([
      feeService.getAllFees().catch(() => []),
      studentService.getAllStudents().catch(() => []),
      staffService.getAllStaff().catch(() => []),
      financeService.getPayrollLedger().catch(() => []),
    ])
    fees.value = fetchedFees
    students.value = fetchedStudents
    activeStaff.value = fetchedStaff // you could filter by active if staff had a status
    payrollLedger.value = fetchedPayroll.sort((a, b) => b.id - a.id) // simplistic sort latest first
  } catch (error) {
    console.error('Error loading finance data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(loadData)

// --- COMPUTED FINANCE METRICS ---
const filteredFees = computed(() => {
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

// --- PAYROLL MODAL ---
const calculatedNetPay = computed(() => {
  return payrollForm.basic_salary + payrollForm.allowances - payrollForm.deductions
})

const openPayrollModal = () => {
  // Set default month to current YYYY-MM
  const date = new Date()
  const yyyy = date.getFullYear()
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  payrollForm.payment_month = `${yyyy}-${mm}`
  payrollForm.staff_id = ''
  payrollForm.basic_salary = 0
  payrollForm.allowances = 0
  payrollForm.deductions = 0
  showPayrollModal.value = true
}

const closePayrollModal = () => {
  showPayrollModal.value = false
}

const submitPayroll = async () => {
  try {
    const payload = {
      ...payrollForm,
      net_pay: calculatedNetPay.value,
    }
    await financeService.executePayroll(payload)
    closePayrollModal()
    await loadData()
  } catch (error) {
    alert(error.message || 'Failed to execute payroll.')
    console.error(error)
  }
}

// --- HELPER FUNCTIONS ---
const getStaffName = (id) => {
  const staff = activeStaff.value.find((s) => s.id === id)
  return staff ? staff.name : 'Unknown Staff'
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    maximumFractionDigits: 0,
  }).format(amount)
}
</script>
