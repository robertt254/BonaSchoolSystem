<template>
  <div class="max-w-3xl mx-auto space-y-5">

    <!-- Controls (hidden when printing) -->
    <div class="bg-white rounded-xl border border-slate-200 p-5 print:hidden">
      <h2 class="text-base font-bold text-slate-800 mb-4">Generate Fee Statement</h2>
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
          @click="generateStatement"
          :disabled="!selectedStudent || loading"
          class="bg-emerald-700 text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-emerald-600 transition disabled:opacity-50"
        >
          {{ loading ? 'Loading…' : 'Generate Statement' }}
        </button>
      </div>
    </div>

    <!-- Statement document -->
    <div
      v-if="statementData && !loading"
      id="fee-statement"
      class="bg-white rounded-xl border border-slate-200 overflow-hidden print:rounded-none print:border-none"
    >
      <!-- Header band -->
      <div class="bg-school-navy text-white px-8 py-7 print:py-5">
        <div class="flex items-start justify-between">
          <div>
            <h1 class="text-xl font-black uppercase tracking-wider">The Bona School</h1>
            <p class="text-white/50 text-xs mt-1">Nairobi, Kenya · Finance Department</p>
          </div>
          <div class="text-right">
            <p class="text-xs font-bold uppercase tracking-widest text-white/40">Fee Statement</p>
            <p class="text-white font-bold text-sm mt-0.5">{{ currentDate }}</p>
          </div>
        </div>
      </div>

      <!-- Student info strip -->
      <div class="grid grid-cols-3 gap-0 border-b border-slate-200 bg-slate-50 divide-x divide-slate-200">
        <div class="px-6 py-4">
          <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Student</p>
          <p class="font-bold text-slate-800 mt-0.5">{{ statementData.student_name }}</p>
        </div>
        <div class="px-6 py-4">
          <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Grade</p>
          <p class="font-bold text-slate-800 mt-0.5">{{ statementData.grade_level }}</p>
        </div>
        <div class="px-6 py-4">
          <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Billing Period</p>
          <p class="font-bold text-slate-800 mt-0.5">{{ statementData.term_checked }}</p>
        </div>
      </div>

      <!-- Summary table -->
      <div class="px-8 py-6">
        <h3 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-3">Fee Summary</h3>
        <table class="w-full text-sm border-collapse">
          <tbody>
            <tr class="border-b border-slate-200">
              <td class="py-3 text-slate-600 font-medium">Expected Term Fee ({{ statementData.term_checked }})</td>
              <td class="py-3 text-right font-bold text-slate-800">{{ formatCurrency(statementData.expected_term_fee) }}</td>
            </tr>
            <tr class="border-b border-slate-200 bg-emerald-50/40">
              <td class="py-3 px-2 text-emerald-800 font-medium">Total Paid This Term</td>
              <td class="py-3 px-2 text-right font-bold text-emerald-700">− {{ formatCurrency(statementData.total_paid_this_term) }}</td>
            </tr>
            <tr v-if="statementData.rollover_credit > 0" class="border-b border-slate-200 bg-blue-50/40">
              <td class="py-3 px-2 text-blue-700 font-medium">Credit from Previous Terms</td>
              <td class="py-3 px-2 text-right font-bold text-blue-700">− {{ formatCurrency(statementData.rollover_credit) }}</td>
            </tr>
            <tr>
              <td class="py-4 text-lg font-black text-slate-800 uppercase tracking-wide">Outstanding Balance</td>
              <td class="py-4 text-right text-2xl font-black" :class="statementData.outstanding_balance > 0 ? 'text-school-red' : 'text-emerald-600'">
                {{ formatCurrency(statementData.outstanding_balance) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Itemized payment history for this term -->
      <div v-if="termPayments.length" class="px-8 pb-6">
        <h3 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-3">Payment History · {{ statementData.term_checked }}</h3>
        <table class="w-full text-xs border-collapse border border-slate-200">
          <thead>
            <tr class="bg-slate-50">
              <th class="border border-slate-200 px-4 py-2 text-left font-bold text-slate-500 uppercase tracking-wider">Receipt</th>
              <th class="border border-slate-200 px-4 py-2 text-left font-bold text-slate-500 uppercase tracking-wider">Date</th>
              <th class="border border-slate-200 px-4 py-2 text-left font-bold text-slate-500 uppercase tracking-wider">Type</th>
              <th class="border border-slate-200 px-4 py-2 text-right font-bold text-slate-500 uppercase tracking-wider">Amount</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in termPayments" :key="p.id" class="hover:bg-slate-50/50">
              <td class="border border-slate-200 px-4 py-2 font-mono text-school-navy">{{ p.receipt_number || '—' }}</td>
              <td class="border border-slate-200 px-4 py-2 text-slate-500">{{ formatDate(p.payment_date) }}</td>
              <td class="border border-slate-200 px-4 py-2 text-slate-600">{{ p.payment_type }}</td>
              <td class="border border-slate-200 px-4 py-2 text-right font-bold text-emerald-700">{{ formatCurrency(p.amount) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Signatures -->
      <div class="mx-8 pb-8 flex justify-between">
        <div class="w-48 border-t border-slate-400 pt-2 text-center">
          <p class="text-xs text-slate-500">Finance Officer Signature</p>
        </div>
        <div class="w-48 border-t border-slate-400 pt-2 text-center">
          <p class="text-xs text-slate-500">Parent / Guardian Signature</p>
        </div>
      </div>

      <!-- Print button -->
      <div class="border-t border-slate-100 px-8 py-4 flex justify-end print:hidden">
        <button
          @click="printPage()"
          class="inline-flex items-center gap-2 bg-slate-800 text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-black transition"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
            <rect x="6" y="14" width="12" height="8"/>
          </svg>
          Print Statement
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import studentService from '@/services/studentService'
import feeService from '@/services/feeService'
import { apiFetch } from '@/services/api'

const printPage = () => window.print()

const students        = ref([])
const selectedStudent = ref('')
const selectedTerm    = ref('Term 1')
const statementData   = ref(null)
const allPayments     = ref([])
const loading         = ref(false)

const currentDate = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })

const termPayments = computed(() =>
  allPayments.value.filter(p => p.term === selectedTerm.value)
    .sort((a, b) => new Date(b.payment_date) - new Date(a.payment_date))
)

const formatCurrency = (v) =>
  new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 }).format(v)

const formatDate = (iso) =>
  new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })

onMounted(async () => {
  try { students.value = await studentService.getAllStudents() }
  catch (e) { console.error(e) }
})

const generateStatement = async () => {
  loading.value = true
  statementData.value = null
  allPayments.value   = []
  try {
    const [stmt, payments] = await Promise.all([
      feeService.getStudentBalance(selectedStudent.value, selectedTerm.value),
      apiFetch(`/api/fees/student/${selectedStudent.value}`),
    ])
    statementData.value = stmt
    allPayments.value   = payments
  } catch {
    alert('Failed to generate statement.')
  } finally {
    loading.value = false
  }
}
</script>

<style>
@media print {
  .print\:rounded-none { border-radius: 0 !important; }
  .print\:border-none { border: none !important; }
}
</style>
