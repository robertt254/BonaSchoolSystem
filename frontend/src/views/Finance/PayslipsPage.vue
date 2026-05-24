<template>
  <div class="max-w-5xl mx-auto space-y-5">

    <div>
      <h1 class="text-2xl font-extrabold text-slate-800">Payroll</h1>
      <p class="text-sm text-slate-400 mt-0.5">Preview and execute monthly payroll for all staff. Salary data is drawn from each staff member's profile.</p>
    </div>

    <!-- Month selector -->
    <div class="bg-white rounded-xl border border-slate-200 p-5 flex flex-wrap gap-4 items-end">
      <div>
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Month</label>
        <input v-model="selectedMonth" type="month"
          class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
      </div>
      <button @click="loadPreview" :disabled="loadingPreview"
        class="bg-school-navy text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-navy/90 transition disabled:opacity-50">
        {{ loadingPreview ? 'Loading…' : 'Preview Payroll' }}
      </button>
      <button v-if="preview.length > 0 && unpaidCount > 0" @click="confirmRun"
        class="bg-emerald-600 text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-emerald-700 transition flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
        Run Payroll for {{ fmtMonthLabel(selectedMonth) }}
      </button>
    </div>

    <!-- Error banner -->
    <div v-if="loadError" class="bg-red-50 border border-red-200 rounded-xl px-5 py-4 flex items-start gap-3">
      <svg class="w-5 h-5 text-red-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <div>
        <p class="font-bold text-red-800 text-sm">Failed to load payroll data</p>
        <p class="text-red-700 text-xs mt-0.5">{{ loadError }}</p>
      </div>
      <button @click="loadError = null" class="ml-auto text-red-400 hover:text-red-600">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
      </button>
    </div>

    <!-- Run result banner -->
    <div v-if="runResult" class="bg-emerald-50 border border-emerald-200 rounded-xl px-5 py-4 flex items-start gap-3">
      <svg class="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
      <div>
        <p class="font-bold text-emerald-800 text-sm">Payroll executed successfully</p>
        <p class="text-emerald-700 text-xs mt-0.5">
          {{ runResult.created }} payslip{{ runResult.created !== 1 ? 's' : '' }} generated
          <span v-if="runResult.skipped > 0"> · {{ runResult.skipped }} skipped (no salary or already paid)</span>
        </p>
      </div>
    </div>

    <!-- Preview table -->
    <div v-if="preview.length > 0" class="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div class="px-5 py-3.5 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
        <div>
          <h3 class="font-bold text-slate-800 text-sm">{{ fmtMonthLabel(selectedMonth) }} Payroll Preview</h3>
          <p class="text-xs text-slate-400 mt-0.5">{{ unpaidCount }} pending · {{ paidCount }} already paid</p>
        </div>
        <div class="text-right">
          <p class="text-xs text-slate-400 font-medium">Total Payable</p>
          <p class="text-sm font-extrabold text-slate-800">KES {{ fmt(totalPayable) }}</p>
        </div>
      </div>
      <table class="w-full text-sm">
        <thead>
          <tr class="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-100">
            <th class="px-5 py-3 text-left">Staff</th>
            <th class="px-5 py-3 text-right">Basic</th>
            <th class="px-5 py-3 text-right">Allowances</th>
            <th class="px-5 py-3 text-right">Deductions</th>
            <th class="px-5 py-3 text-right">Net Pay</th>
            <th class="px-5 py-3 text-center w-24">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in preview" :key="row.staff_id" class="border-b border-slate-50 hover:bg-slate-50"
            :class="row.basic_salary === 0 ? 'opacity-40' : ''">
            <td class="px-5 py-3.5">
              <p class="font-semibold text-slate-800">{{ row.staff_name }}</p>
              <p class="text-xs text-slate-400">{{ row.job_title || '—' }}</p>
            </td>
            <td class="px-5 py-3.5 text-right font-mono text-xs text-slate-600">{{ fmt(row.basic_salary) }}</td>
            <td class="px-5 py-3.5 text-right font-mono text-xs text-emerald-600">+{{ fmt(row.allowances) }}</td>
            <td class="px-5 py-3.5 text-right font-mono text-xs text-red-500">-{{ fmt(row.deductions) }}</td>
            <td class="px-5 py-3.5 text-right font-bold text-slate-800">KES {{ fmt(row.net_pay) }}</td>
            <td class="px-5 py-3.5 text-center">
              <span v-if="row.already_paid" class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700">Paid</span>
              <span v-else-if="row.basic_salary === 0" class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-100 text-slate-400">No Salary</span>
              <span v-else class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-50 text-amber-700">Pending</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Historical payslips for this month -->
    <div v-if="payroll.length > 0" class="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div class="px-5 py-3.5 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
        <span class="font-semibold text-sm text-slate-700">{{ payroll.length }} payslip{{ payroll.length !== 1 ? 's' : '' }} — {{ fmtMonthLabel(selectedMonth) }}</span>
        <div class="flex items-center gap-3">
          <span class="text-sm font-bold text-slate-800">Total: KES {{ fmt(totalNet) }}</span>
          <button @click="exportPayroll"
            class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 bg-white border border-slate-200 px-3 py-1.5 rounded-lg hover:bg-slate-50 transition">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            Export CSV
          </button>
        </div>
      </div>
      <table class="w-full text-sm">
        <thead>
          <tr class="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-100">
            <th class="px-5 py-3 text-left">Staff</th>
            <th class="px-5 py-3 text-right">Basic</th>
            <th class="px-5 py-3 text-right">Allowances</th>
            <th class="px-5 py-3 text-right">Deductions</th>
            <th class="px-5 py-3 text-right">Net Pay</th>
            <th class="px-5 py-3 text-right w-28"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in payroll" :key="p.id" class="border-b border-slate-50 hover:bg-slate-50">
            <td class="px-5 py-3.5">
              <p class="font-semibold text-slate-800">{{ p.staff_name || `Staff #${p.staff_id}` }}</p>
              <p class="text-xs text-slate-400">{{ p.payment_month }}</p>
            </td>
            <td class="px-5 py-3.5 text-right font-mono text-xs text-slate-600">{{ fmt(p.basic_salary) }}</td>
            <td class="px-5 py-3.5 text-right font-mono text-xs text-emerald-600">+{{ fmt(p.allowances) }}</td>
            <td class="px-5 py-3.5 text-right font-mono text-xs text-red-500">-{{ fmt(p.deductions) }}</td>
            <td class="px-5 py-3.5 text-right font-bold text-slate-800">KES {{ fmt(p.net_pay) }}</td>
            <td class="px-5 py-3.5 text-right">
              <button @click="viewPayslip(p.id)"
                class="bg-school-purple/10 text-school-purple px-3 py-1.5 rounded-lg text-xs font-semibold hover:bg-school-purple/20 transition">
                Print Payslip
              </button>
            </td>
          </tr>
        </tbody>
      </table>
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
            <button @click="selectedPayslip = null" class="text-slate-400 hover:text-slate-600 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-100">
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
                  <td class="px-4 py-2 text-slate-700">Deductions (PAYE/NSSF/NHIF)</td>
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
import financeService from '@/services/financeService'
import { downloadCsv } from '@/utils/csvExport'

const printPage = () => window.print()

const today = new Date()
const selectedMonth = ref(`${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`)

const preview        = ref([])
const payroll        = ref([])
const selectedPayslip = ref(null)
const loadingPreview = ref(false)
const runResult      = ref(null)
const loadError      = ref(null)

const unpaidCount  = computed(() => preview.value.filter(r => !r.already_paid && r.basic_salary > 0).length)
const paidCount    = computed(() => preview.value.filter(r => r.already_paid).length)
const totalPayable = computed(() => preview.value.filter(r => !r.already_paid).reduce((s, r) => s + r.net_pay, 0))
const totalNet     = computed(() => payroll.value.reduce((s, p) => s + Number(p.net_pay), 0))

const fmt = (n) => Number(n || 0).toLocaleString('en-KE', { minimumFractionDigits: 2 })

const fmtMonthLabel = (ym) => {
  if (!ym) return ''
  const [y, m] = ym.split('-')
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  return `${months[parseInt(m) - 1]} ${y}`
}

const loadPreview = async () => {
  loadingPreview.value = true
  loadError.value = null
  runResult.value = null
  try {
    const data = await financeService.getPayrollMonthly(selectedMonth.value)
    preview.value = data.preview
    payroll.value = data.history
  } catch (e) {
    loadError.value = e?.message || 'An unexpected error occurred.'
  } finally { loadingPreview.value = false }
}

const confirmRun = () => {
  if (!confirm(`Run payroll for ${fmtMonthLabel(selectedMonth.value)}?\n\nThis will create payslips for ${unpaidCount.value} staff members. This cannot be undone.`)) return
  runPayroll()
}

const runPayroll = async () => {
  try {
    runResult.value = await financeService.runMonthPayroll(selectedMonth.value)
    await loadPreview()
  } catch (e) { loadError.value = e?.message || 'Payroll execution failed.' }
}

const viewPayslip = async (id) => {
  try {
    selectedPayslip.value = await apiFetch(`/api/finance/payslip/${id}`)
  } catch (e) { loadError.value = e?.message || 'Could not load payslip.' }
}

const exportPayroll = () => {
  downloadCsv(`payroll-${selectedMonth.value}`, [
    { key: 'staff_name', label: 'Staff Name' },
    { key: 'payment_month', label: 'Month' },
    { key: 'basic_salary', label: 'Basic Salary' },
    { key: 'allowances', label: 'Allowances' },
    { key: 'deductions', label: 'Deductions' },
    { key: 'net_pay', label: 'Net Pay' },
  ], payroll.value)
}

onMounted(loadPreview)
</script>

<style>
@media print {
  body > *:not(#payslip-content) { display: none !important; }
  #payslip-content { display: block !important; position: static !important; }
}
</style>
