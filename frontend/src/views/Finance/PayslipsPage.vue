<template>
  <div class="max-w-6xl mx-auto space-y-6">

    <div>
      <h1 class="text-2xl font-extrabold text-slate-800">Payroll</h1>
      <p class="text-sm text-slate-400 mt-0.5">Review and adjust each staff member's allowances and deductions, then execute payroll for the month.</p>
    </div>

    <!-- Month selector -->
    <div class="bg-white rounded-lg border border-slate-200 p-6 flex flex-wrap gap-4 items-end">
      <div>
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Payroll Month</label>
        <input v-model="selectedMonth" type="month" @change="loadData"
          class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
      </div>
      <div v-if="!loading && staffRows.length" class="ml-auto text-right">
        <p class="text-xs text-slate-400 font-medium">Total Payable</p>
        <p class="text-lg font-extrabold text-slate-800">KES {{ fmt(totalPayable) }}</p>
      </div>
    </div>

    <!-- Error banner -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-xl px-5 py-4 flex items-start gap-3">
      <svg class="w-5 h-5 text-red-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <div>
        <p class="font-bold text-red-800 text-sm">Error</p>
        <p class="text-red-700 text-xs mt-0.5">{{ error }}</p>
      </div>
      <button @click="error = null" class="ml-auto text-red-400 hover:text-red-600">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
      </button>
    </div>

    <!-- Success banner -->
    <div v-if="runResult" class="bg-emerald-50 border border-emerald-200 rounded-xl px-5 py-4 flex items-start gap-3">
      <svg class="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
      <div>
        <p class="font-bold text-emerald-800 text-sm">Payroll executed — {{ fmtMonthLabel(selectedMonth) }}</p>
        <p class="text-emerald-700 text-xs mt-0.5">
          {{ runResult.created }} payslip{{ runResult.created !== 1 ? 's' : '' }} generated
          <span v-if="runResult.skipped > 0"> · {{ runResult.skipped }} skipped</span>
        </p>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="bg-white rounded-lg border border-slate-200 p-12 text-center">
      <p class="text-slate-400 text-sm">Loading payroll data…</p>
    </div>

    <!-- Staff table -->
    <div v-else-if="staffRows.length" class="bg-white rounded-lg border border-slate-200 overflow-hidden">
      <div class="px-5 py-3.5 border-b border-slate-100 bg-slate-50 flex items-center gap-4">
        <div>
          <h3 class="font-bold text-slate-800 text-sm">{{ fmtMonthLabel(selectedMonth) }} Payroll</h3>
          <p class="text-xs text-slate-400 mt-0.5">
            {{ pendingRows.length }} pending ·
            {{ paidRows.length }} paid ·
            {{ noSalaryRows.length }} no salary configured
          </p>
        </div>
        <div v-if="paidRows.length > 0" class="ml-auto flex items-center gap-2">
          <button @click="exportPayroll"
            class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 bg-white border border-slate-200 px-3 py-1.5 rounded-lg hover:bg-slate-50 transition">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            Export CSV
          </button>
          <button v-if="isAdmin" @click="confirmVoid" :disabled="voiding"
            class="flex items-center gap-1.5 text-xs font-semibold text-red-600 bg-white border border-red-200 px-3 py-1.5 rounded-lg hover:bg-red-50 transition disabled:opacity-50">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            {{ voiding ? 'Voiding…' : 'Void Payroll' }}
          </button>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-100 bg-slate-50/50">
              <th class="px-5 py-3 text-left">Staff Member</th>
              <th class="px-5 py-3 text-right">Basic Salary</th>
              <th class="px-5 py-3 text-right w-40">Allowances</th>
              <th class="px-5 py-3 text-right w-40">Deductions</th>
              <th class="px-5 py-3 text-right">Net Pay</th>
              <th class="px-5 py-3 text-center w-28">Status</th>
              <th class="px-3 py-3 w-24"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in staffRows" :key="row.staff_id"
              class="border-b border-slate-50 hover:bg-slate-50/60 transition-colors"
              :class="{ 'opacity-40': row.basic_salary === 0 }">

              <!-- Staff info -->
              <td class="px-5 py-3.5">
                <p class="font-semibold text-slate-800">{{ row.staff_name }}</p>
                <p class="text-xs text-slate-400">{{ row.job_title || row.role?.replace('_', ' ') || '—' }}</p>
              </td>

              <!-- Basic salary — always read-only -->
              <td class="px-5 py-3.5 text-right font-mono text-xs text-slate-600">
                {{ fmt(row.basic_salary) }}
              </td>

              <!-- Allowances — editable for pending staff -->
              <td class="px-5 py-3.5 text-right">
                <input v-if="!row.already_paid && row.basic_salary > 0"
                  v-model.number="editMap[row.staff_id].allowances"
                  type="number" min="0" step="100"
                  class="w-32 text-right border border-slate-200 rounded-lg px-2 py-1 text-xs font-mono text-emerald-700 focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-200 bg-emerald-50/40" />
                <span v-else class="font-mono text-xs text-emerald-600">{{ fmt(row.allowances) }}</span>
              </td>

              <!-- Deductions — editable for pending staff -->
              <td class="px-5 py-3.5 text-right">
                <input v-if="!row.already_paid && row.basic_salary > 0"
                  v-model.number="editMap[row.staff_id].deductions"
                  type="number" min="0" step="100"
                  class="w-32 text-right border border-slate-200 rounded-lg px-2 py-1 text-xs font-mono text-red-600 focus:outline-none focus:border-red-300 focus:ring-1 focus:ring-red-100 bg-red-50/40" />
                <span v-else class="font-mono text-xs text-red-500">{{ fmt(row.deductions) }}</span>
              </td>

              <!-- Net pay — live-computed for pending, actual for paid -->
              <td class="px-5 py-3.5 text-right font-bold text-slate-800">
                KES {{ row.already_paid ? fmt(row.net_pay) : fmt(computedNet(row)) }}
              </td>

              <!-- Status badge -->
              <td class="px-5 py-3.5 text-center">
                <span v-if="row.already_paid"
                  class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700">Paid</span>
                <span v-else-if="row.basic_salary === 0"
                  class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-100 text-slate-400">No Salary</span>
                <span v-else
                  class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-50 text-amber-700">Pending</span>
              </td>

              <!-- Payslip action for paid rows -->
              <td class="px-3 py-3.5 text-right">
                <button v-if="row.already_paid" @click="viewPayslip(row.payroll_id)"
                  class="bg-school-purple/10 text-school-purple px-3 py-1.5 rounded-lg text-xs font-semibold hover:bg-school-purple/20 transition">
                  Payslip
                </button>
              </td>
            </tr>
          </tbody>

          <!-- Totals row for pending -->
          <tfoot v-if="pendingRows.length > 0">
            <tr class="border-t-2 border-slate-200 bg-slate-50">
              <td colspan="4" class="px-5 py-3 text-sm font-semibold text-slate-500">
                Total payable — {{ pendingRows.length }} pending staff
              </td>
              <td class="px-5 py-3 text-right font-extrabold text-slate-800">KES {{ fmt(totalPayable) }}</td>
              <td colspan="2"></td>
            </tr>
          </tfoot>
        </table>
      </div>

      <!-- Execute payroll footer -->
      <div v-if="pendingRows.length > 0" class="px-5 py-4 border-t border-slate-100 flex items-center justify-between gap-4">
        <p class="text-xs text-slate-400 leading-relaxed">
          Payroll will create individual payslips for <strong>{{ pendingRows.length }}</strong> staff member{{ pendingRows.length !== 1 ? 's' : '' }}.
          Each entry is logged separately and cannot be undone.
        </p>
        <button @click="confirmRun" :disabled="running"
          class="shrink-0 bg-emerald-600 text-white px-6 py-2.5 rounded-lg text-sm font-semibold hover:bg-emerald-700 transition disabled:opacity-50 flex items-center gap-2">
          <svg v-if="!running" class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
          </svg>
          {{ running ? 'Processing…' : `Execute Payroll — ${fmtMonthLabel(selectedMonth)}` }}
        </button>
      </div>

      <!-- All-paid summary footer -->
      <div v-else-if="paidRows.length > 0 && pendingRows.length === 0 && noSalaryRows.length === staffRows.length - paidRows.length"
        class="px-5 py-4 border-t border-slate-100">
        <p class="text-xs text-slate-500">
          Payroll complete for <strong>{{ fmtMonthLabel(selectedMonth) }}</strong>.
          Total disbursed: <strong>KES {{ fmt(totalDisbursed) }}</strong>
        </p>
      </div>
    </div>

    <!-- Payslip print modal -->
    <div v-if="selectedPayslip" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl w-full max-w-lg shadow-2xl">
        <div class="flex items-center justify-between px-6 py-4 border-b border-slate-100 print:hidden">
          <h3 class="font-bold text-slate-800">Payslip Preview</h3>
          <div class="flex gap-3">
            <button @click="printPage"
              class="bg-school-purple text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition">
              Print
            </button>
            <button @click="selectedPayslip = null"
              class="text-slate-400 hover:text-slate-600 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-100">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
            </button>
          </div>
        </div>
        <div id="payslip-content" class="p-8 space-y-5">
          <div class="text-center border-b border-slate-200 pb-4">
            <p class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">THE BONA SCHOOL</p>
            <h2 class="text-xl font-extrabold text-slate-800">PAYSLIP</h2>
            <p class="text-sm text-slate-500 mt-0.5">{{ selectedPayslip.payment_month }}</p>
          </div>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p class="text-xs text-slate-400 font-semibold uppercase tracking-wider mb-1">Employee</p>
              <p class="font-bold text-slate-800">{{ selectedPayslip.staff_name || 'N/A' }}</p>
              <p class="text-slate-500 text-xs mt-0.5">{{ selectedPayslip.job_title || '' }}</p>
            </div>
            <div class="text-right">
              <p class="text-xs text-slate-400 font-semibold uppercase tracking-wider mb-1">Staff ID</p>
              <p class="font-mono text-slate-700">#{{ selectedPayslip.staff_id }}</p>
              <p v-if="selectedPayslip.kra_pin" class="text-xs text-slate-500 mt-0.5">KRA: {{ selectedPayslip.kra_pin }}</p>
            </div>
          </div>
          <div class="border border-slate-100 rounded-xl overflow-hidden">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-slate-50 text-xs font-bold uppercase tracking-wider text-slate-400">
                  <th class="px-4 py-2.5 text-left">Earnings / Deductions</th>
                  <th class="px-4 py-2.5 text-right">Amount (KES)</th>
                </tr>
              </thead>
              <tbody>
                <tr class="border-t border-slate-100">
                  <td class="px-4 py-2 text-slate-700">Basic Salary</td>
                  <td class="px-4 py-2 text-right font-mono">{{ fmt(selectedPayslip.basic_salary) }}</td>
                </tr>
                <tr class="border-t border-slate-100">
                  <td class="px-4 py-2 text-slate-700">Allowances</td>
                  <td class="px-4 py-2 text-right font-mono text-emerald-600">{{ fmt(selectedPayslip.allowances) }}</td>
                </tr>
                <tr class="border-t border-slate-100">
                  <td class="px-4 py-2 text-slate-700">Deductions (PAYE / NSSF / NHIF)</td>
                  <td class="px-4 py-2 text-right font-mono text-red-500">({{ fmt(selectedPayslip.deductions) }})</td>
                </tr>
                <tr class="border-t-2 border-slate-300 bg-slate-50">
                  <td class="px-4 py-3 font-extrabold text-slate-800 uppercase text-xs tracking-wider">Net Pay</td>
                  <td class="px-4 py-3 text-right font-extrabold text-slate-800">{{ fmt(selectedPayslip.net_pay) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="grid grid-cols-2 gap-4 text-xs text-slate-500 border-t border-slate-100 pt-4">
            <div>
              <p v-if="selectedPayslip.nssf_number">NSSF: {{ selectedPayslip.nssf_number }}</p>
              <p v-if="selectedPayslip.nhif_number">NHIF: {{ selectedPayslip.nhif_number }}</p>
            </div>
            <div class="text-right">
              <p class="text-slate-300">— Authorised Signature —</p>
              <p class="mt-4 border-t border-slate-200 pt-1">Date: _______________</p>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import financeService from '@/services/financeService'
import { downloadCsv } from '@/utils/csvExport'

const printPage = () => window.print()

const authStore = useAuthStore()
const isAdmin = computed(() => authStore.user?.role === 'admin')

const today = new Date()
const selectedMonth = ref(`${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`)

const staffRows      = ref([])
const editMap        = ref({})
const selectedPayslip = ref(null)
const loading        = ref(false)
const running        = ref(false)
const voiding        = ref(false)
const error          = ref(null)
const runResult      = ref(null)

const pendingRows   = computed(() => staffRows.value.filter(r => !r.already_paid && r.basic_salary > 0))
const paidRows      = computed(() => staffRows.value.filter(r => r.already_paid))
const noSalaryRows  = computed(() => staffRows.value.filter(r => !r.already_paid && r.basic_salary === 0))

const computedNet = (row) => {
  const e = editMap.value[row.staff_id] || { allowances: 0, deductions: 0 }
  return Math.max(0, row.basic_salary + Number(e.allowances || 0) - Number(e.deductions || 0))
}

const totalPayable   = computed(() => pendingRows.value.reduce((s, r) => s + computedNet(r), 0))
const totalDisbursed = computed(() => paidRows.value.reduce((s, r) => s + Number(r.net_pay), 0))

const fmt = (n) => Number(n || 0).toLocaleString('en-KE', { minimumFractionDigits: 2 })
const fmtMonthLabel = (ym) => {
  if (!ym) return ''
  const [y, m] = ym.split('-')
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  return `${months[parseInt(m) - 1]} ${y}`
}

const loadData = async () => {
  loading.value = true
  error.value = null
  runResult.value = null
  try {
    const data = await financeService.getPayrollMonthly(selectedMonth.value)

    // Build history map keyed by staff_id — take newest record (history is ordered desc)
    const histMap = {}
    for (const h of data.history) {
      if (!histMap[h.staff_id]) histMap[h.staff_id] = h
    }

    // Merge: for paid staff, overlay the actual paid figures from history
    staffRows.value = data.preview.map(p => {
      if (p.already_paid && histMap[p.staff_id]) {
        const h = histMap[p.staff_id]
        return { ...p, allowances: h.allowances, deductions: h.deductions, net_pay: h.net_pay, payroll_id: h.id }
      }
      return { ...p, payroll_id: null }
    })

    // Initialise editable values for pending staff from their profile defaults
    const map = {}
    for (const r of staffRows.value) {
      if (!r.already_paid && r.basic_salary > 0) {
        map[r.staff_id] = { allowances: r.allowances, deductions: r.deductions }
      }
    }
    editMap.value = map
  } catch (e) {
    error.value = e?.message || 'Failed to load payroll data.'
  } finally {
    loading.value = false
  }
}

const confirmRun = () => {
  if (!confirm(
    `Execute payroll for ${fmtMonthLabel(selectedMonth.value)}?\n\n` +
    `${pendingRows.value.length} payslip(s) will be created. This cannot be undone.`
  )) return
  runPayroll()
}

const runPayroll = async () => {
  running.value = true
  error.value = null
  try {
    const entries = pendingRows.value.map(r => ({
      staff_id: r.staff_id,
      allowances: Number(editMap.value[r.staff_id]?.allowances || 0),
      deductions: Number(editMap.value[r.staff_id]?.deductions || 0),
    }))
    runResult.value = await financeService.runMonthPayroll(selectedMonth.value, entries)
    await loadData()
  } catch (e) {
    error.value = e?.message || 'Payroll execution failed.'
  } finally {
    running.value = false
  }
}

const confirmVoid = () => {
  if (!confirm(
    `Void all payroll records for ${fmtMonthLabel(selectedMonth.value)}?\n\n` +
    `This will permanently delete ${paidRows.value.length} payslip(s) and cannot be undone.`
  )) return
  voidPayroll()
}

const voidPayroll = async () => {
  voiding.value = true
  error.value = null
  try {
    await financeService.voidPayrollMonth(selectedMonth.value)
    runResult.value = null
    await loadData()
  } catch (e) {
    error.value = e?.message || 'Failed to void payroll.'
  } finally {
    voiding.value = false
  }
}

const viewPayslip = async (id) => {
  try {
    selectedPayslip.value = await apiFetch(`/api/finance/payslip/${id}`)
  } catch (e) {
    error.value = e?.message || 'Could not load payslip.'
  }
}

const exportPayroll = () => {
  downloadCsv(`payroll-${selectedMonth.value}`, [
    { key: 'staff_name',   label: 'Staff Name' },
    { key: 'job_title',    label: 'Job Title' },
    { key: 'basic_salary', label: 'Basic Salary' },
    { key: 'allowances',   label: 'Allowances' },
    { key: 'deductions',   label: 'Deductions' },
    { key: 'net_pay',      label: 'Net Pay' },
  ], paidRows.value)
}

onMounted(loadData)
</script>

<style>
@media print {
  /* Hide everything, then reveal only the payslip content */
  body * { visibility: hidden !important; }
  #payslip-content,
  #payslip-content * { visibility: visible !important; }
  #payslip-content {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    padding: 2rem !important;
    background: white !important;
  }
}
</style>
