<template>
  <div class="max-w-3xl mx-auto space-y-5">

    <!-- Controls (hidden when printing) -->
    <div class="bg-white rounded-xl border border-slate-200 p-5 print:hidden">
      <h2 class="text-base font-bold text-slate-800 mb-4">Generate Fee Statement</h2>
      <div class="flex flex-col sm:flex-row gap-4 items-end flex-wrap">
        <div class="flex-1 min-w-[200px]">
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Student</label>
          <select
            v-model="selectedStudent"
            @change="onStudentChange"
            class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none"
          >
            <option disabled value="">— Choose a student —</option>
            <option v-for="s in students" :key="s.id" :value="s.id">
              {{ s.first_name }} {{ s.last_name }} · {{ s.admission_number }}
            </option>
          </select>
        </div>
        <div class="w-28">
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Year</label>
          <select
            v-model="selectedYear"
            class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none"
          >
            <option v-for="y in appStore.years" :key="y" :value="y">{{ y }}</option>
          </select>
        </div>
        <div class="w-36">
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

    <!-- Carry-Forward Adjustments panel (visible when student is selected) -->
    <div v-if="selectedStudent" class="bg-white rounded-xl border border-slate-200 overflow-hidden print:hidden">
      <div class="px-5 py-3.5 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
        <div>
          <h3 class="font-bold text-slate-800 text-sm">Balance Adjustments (Carry-Forward)</h3>
          <p class="text-xs text-slate-400 mt-0.5">Cross-year / cross-term balances carried into a specific period</p>
        </div>
        <button
          @click="showCfForm = !showCfForm"
          class="flex items-center gap-1.5 bg-amber-600 text-white px-3.5 py-1.5 rounded-lg text-xs font-semibold hover:bg-amber-700 transition"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
          Add Adjustment
        </button>
      </div>

      <!-- Add form -->
      <div v-if="showCfForm" class="px-5 py-4 border-b border-slate-100 bg-amber-50/50">
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-3">
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Year</label>
            <select v-model="cfForm.academic_year"
              class="w-full border border-slate-300 px-2.5 py-2 rounded-lg text-sm outline-none">
              <option v-for="y in appStore.years" :key="y" :value="y">{{ y }}</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Term</label>
            <select v-model="cfForm.term"
              class="w-full border border-slate-300 px-2.5 py-2 rounded-lg text-sm outline-none">
              <option value="Term 1">Term 1</option>
              <option value="Term 2">Term 2</option>
              <option value="Term 3">Term 3</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Amount (KES)</label>
            <input v-model.number="cfForm.amount" type="number" step="0.01"
              placeholder="+ = owed   − = credit"
              class="w-full border border-slate-300 px-2.5 py-2 rounded-lg text-sm outline-none" />
          </div>
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Note</label>
            <input v-model="cfForm.note" type="text" placeholder="Optional reason"
              class="w-full border border-slate-300 px-2.5 py-2 rounded-lg text-sm outline-none" />
          </div>
        </div>
        <div class="flex justify-end gap-2">
          <button @click="showCfForm = false" class="px-4 py-1.5 text-sm text-slate-600 hover:text-slate-800">Cancel</button>
          <button @click="saveCarryForward" :disabled="cfSaving"
            class="bg-amber-600 text-white px-5 py-1.5 rounded-lg text-sm font-semibold hover:bg-amber-700 disabled:opacity-50 transition">
            {{ cfSaving ? 'Saving…' : 'Save' }}
          </button>
        </div>
      </div>

      <!-- Adjustments list -->
      <div v-if="carryForwards.length" class="divide-y divide-slate-50">
        <div v-for="cf in carryForwards" :key="cf.id" class="px-5 py-3 flex items-center justify-between hover:bg-slate-50 transition-colors">
          <div class="flex items-center gap-3 flex-wrap">
            <span class="text-sm font-bold" :class="cf.amount > 0 ? 'text-red-600' : 'text-emerald-600'">
              {{ cf.amount > 0 ? '+' : '' }}{{ formatCurrency(cf.amount) }}
            </span>
            <span class="text-xs font-medium text-slate-500 bg-slate-100 px-2 py-0.5 rounded">{{ cf.academic_year }} · {{ cf.term }}</span>
            <span v-if="cf.note" class="text-xs text-slate-500">— {{ cf.note }}</span>
          </div>
          <div class="flex items-center gap-3 shrink-0">
            <span class="text-xs text-slate-400">{{ cf.recorded_by }}</span>
            <button @click="deleteCarryForward(cf.id)" class="text-xs text-red-400 hover:text-red-600 font-semibold">Del</button>
          </div>
        </div>
      </div>
      <div v-else-if="!showCfForm" class="px-5 py-5 text-sm text-slate-400 text-center">
        No balance adjustments recorded for this student.
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
      <div class="grid grid-cols-4 gap-0 border-b border-slate-200 bg-slate-50 divide-x divide-slate-200">
        <div class="px-6 py-4">
          <p class="text-xs font-bold uppercase tracking-widest text-slate-400">Student</p>
          <p class="font-bold text-slate-800 mt-0.5">{{ statementData.student_name }}</p>
        </div>
        <div class="px-6 py-4">
          <p class="text-xs font-bold uppercase tracking-widest text-slate-400">Grade</p>
          <p class="font-bold text-slate-800 mt-0.5">{{ statementData.grade_level }}</p>
        </div>
        <div class="px-6 py-4">
          <p class="text-xs font-bold uppercase tracking-widest text-slate-400">Billing Period</p>
          <p class="font-bold text-slate-800 mt-0.5">{{ statementData.term_checked }}</p>
        </div>
        <div class="px-6 py-4">
          <p class="text-xs font-bold uppercase tracking-widest text-slate-400">Academic Year</p>
          <p class="font-bold text-slate-800 mt-0.5">{{ selectedYear }}</p>
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
            <tr v-if="statementData.carry_forward && statementData.carry_forward !== 0" class="border-b border-slate-200 bg-amber-50/40">
              <td class="py-3 px-2 text-amber-800 font-medium">
                {{ statementData.carry_forward > 0 ? 'Balance Carried Forward (Arrears)' : 'Balance Carried Forward (Credit)' }}
              </td>
              <td class="py-3 px-2 text-right font-bold" :class="statementData.carry_forward > 0 ? 'text-amber-700' : 'text-emerald-700'">
                {{ statementData.carry_forward > 0 ? '+' : '− ' }}{{ formatCurrency(Math.abs(statementData.carry_forward)) }}
              </td>
            </tr>
            <tr class="border-b border-slate-200 bg-emerald-50/40">
              <td class="py-3 px-2 text-emerald-800 font-medium">Total Paid This Term</td>
              <td class="py-3 px-2 text-right font-bold text-emerald-700">− {{ formatCurrency(statementData.total_paid_this_term) }}</td>
            </tr>
            <tr v-if="statementData.rollover_credit > 0" class="border-b border-slate-200 bg-blue-50/40">
              <td class="py-3 px-2 text-blue-700 font-medium">Credit from Previous Terms (This Year)</td>
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

    <!-- ── Payment Log ────────────────────────────────────────────────────── -->
    <div class="bg-white rounded-xl border border-border overflow-hidden print:hidden">
      <div class="px-5 py-4 border-b border-border bg-surface-muted flex items-center justify-between">
        <div>
          <h3 class="font-bold text-text-primary text-sm">All Fee Payments Log</h3>
          <p class="text-xs text-text-muted mt-0.5">Complete record of every logged payment · latest first</p>
        </div>
        <button @click="loadLog" :disabled="logLoading"
          class="text-xs font-semibold text-brand hover:text-brand-light transition-colors">
          {{ logLoading ? 'Loading…' : 'Refresh' }}
        </button>
      </div>

      <!-- log skeleton -->
      <div v-if="logLoading" class="p-4 space-y-2">
        <div v-for="n in 6" :key="n" class="flex items-center gap-3 py-2.5 px-1">
          <div class="skel h-3 w-24 rounded" />
          <div class="skel h-3 w-32 rounded" />
          <div class="skel h-3 w-20 rounded" />
          <div class="skel h-3 w-16 rounded" />
          <div class="skel h-3 w-28 rounded" />
        </div>
      </div>

      <!-- log table -->
      <div v-else-if="paymentLog.length" class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-surface-muted border-b border-border text-xs font-bold uppercase tracking-widest text-text-muted">
              <th class="px-5 py-3 text-left">Date & Time</th>
              <th class="px-5 py-3 text-left">Student</th>
              <th class="px-5 py-3 text-left">Grade</th>
              <th class="px-5 py-3 text-left">Type · Term</th>
              <th class="px-5 py-3 text-left">Receipt</th>
              <th class="px-5 py-3 text-right">Amount</th>
              <th class="px-5 py-3 text-left">Logged by</th>
              <th v-if="canDeletePayments" class="px-5 py-3 text-center w-20">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-for="p in paymentLog" :key="p.id"
              class="hover:bg-surface-hover transition-colors"
              :class="deletingId === p.id ? 'opacity-40' : ''">
              <td class="px-5 py-3 text-text-muted font-mono text-xs whitespace-nowrap">
                {{ formatDateTime(p.payment_date) }}
              </td>
              <td class="px-5 py-3">
                <span class="font-semibold text-text-primary">{{ p.student_name }}</span>
                <span class="text-text-muted text-xs ml-1.5 font-mono">{{ p.admission_number }}</span>
              </td>
              <td class="px-5 py-3 text-text-secondary text-xs">{{ p.grade_level }}</td>
              <td class="px-5 py-3 text-xs text-text-secondary">
                {{ p.payment_type }}
                <span class="text-text-muted">· {{ p.term }}</span>
              </td>
              <td class="px-5 py-3 font-mono text-xs text-brand">{{ p.receipt_number || '—' }}</td>
              <td class="px-5 py-3 text-right font-bold text-success">{{ formatCurrency(p.amount) }}</td>
              <td class="px-5 py-3 text-xs text-text-muted">{{ p.recorded_by }}</td>
              <td v-if="canDeletePayments" class="px-5 py-3 text-center">
                <button @click="confirmDelete(p)"
                  class="text-xs font-semibold text-danger/70 hover:text-danger transition-colors">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="py-12 text-center text-text-muted text-sm">
        No payments recorded yet.
      </div>
    </div>

    <!-- Delete confirmation modal -->
    <div v-if="deleteTarget" class="fixed inset-0 bg-slate-900/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-modal border border-border w-full max-w-md overflow-hidden">
        <div class="px-6 py-5 border-b border-border bg-danger-bg flex items-start gap-3">
          <svg class="w-5 h-5 text-danger shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
          </svg>
          <div>
            <h3 class="text-sm font-bold text-danger-text">Delete Fee Payment</h3>
            <p class="text-xs text-danger-text/80 mt-0.5">This action is permanent and will be recorded in the audit log.</p>
          </div>
        </div>
        <div class="px-6 py-5 space-y-2 text-sm text-text-primary">
          <p><span class="text-text-muted">Student:</span> <strong>{{ deleteTarget.student_name }}</strong></p>
          <p><span class="text-text-muted">Amount:</span> <strong class="text-success">{{ formatCurrency(deleteTarget.amount) }}</strong></p>
          <p><span class="text-text-muted">Receipt:</span> <span class="font-mono text-brand">{{ deleteTarget.receipt_number || 'none' }}</span></p>
          <p><span class="text-text-muted">Logged by:</span> {{ deleteTarget.recorded_by }}</p>
          <p><span class="text-text-muted">Date:</span> {{ formatDateTime(deleteTarget.payment_date) }}</p>
        </div>
        <div class="flex justify-end gap-3 px-6 pb-5">
          <button @click="deleteTarget = null"
            class="px-4 py-2 text-sm font-semibold text-text-secondary hover:bg-surface-hover rounded-lg transition-colors">
            Cancel
          </button>
          <button @click="executeDelete" :disabled="deletingId !== null"
            class="px-4 py-2 text-sm font-bold bg-danger text-white rounded-lg hover:bg-danger/90 transition-colors disabled:opacity-50">
            {{ deletingId ? 'Deleting…' : 'Confirm Delete' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import studentService from '@/services/studentService'
import feeService from '@/services/feeService'
import { apiFetch } from '@/services/api'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
const toast = useToast()


const printPage = () => window.print()

const appStore  = useAppStore()
const authStore = useAuthStore()

const students        = ref([])
const selectedStudent = ref('')
const selectedYear    = ref(appStore.currentYear)
const selectedTerm    = ref(appStore.currentTerm || 'Term 1')
const statementData   = ref(null)
const allPayments     = ref([])
const loading         = ref(false)

const carryForwards = ref([])
const showCfForm    = ref(false)
const cfSaving      = ref(false)
const cfForm        = ref({ academic_year: appStore.currentYear, term: 'Term 1', amount: '', note: '' })

const currentDate = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })

const termPayments = computed(() =>
  allPayments.value.filter(p => p.term === selectedTerm.value)
    .sort((a, b) => new Date(b.payment_date) - new Date(a.payment_date))
)

const formatCurrency = (v) =>
  new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 }).format(v)

const formatDate = (iso) =>
  new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })

const formatDateTime = (iso) => {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
       + ' ' + d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })
}

// ── Payment log ──────────────────────────────────────────────────────────────
const paymentLog  = ref([])
const logLoading  = ref(false)
const deleteTarget = ref(null)
const deletingId  = ref(null)

const canDeletePayments = computed(() =>
  ['admin', 'principal'].includes(authStore.user?.role)
)

const loadLog = async () => {
  logLoading.value = true
  try {
    paymentLog.value = await apiFetch('/api/fees/log')
  } catch (e) {
    toast.error('Failed to load payment log.')
  } finally {
    logLoading.value = false
  }
}

const confirmDelete = (payment) => {
  deleteTarget.value = payment
}

const executeDelete = async () => {
  if (!deleteTarget.value) return
  deletingId.value = deleteTarget.value.id
  try {
    await apiFetch(`/api/fees/${deleteTarget.value.id}`, { method: 'DELETE' })
    toast.success('Payment deleted. Action has been logged in the audit trail.')
    deleteTarget.value = null
    await loadLog()
  } catch (e) {
    toast.error(e?.message || 'Delete failed.')
  } finally {
    deletingId.value = null
  }
}

onMounted(async () => {
  try {
    await Promise.all([
      studentService.getAllStudents().then(r => { students.value = r }),
      loadLog(),
    ])
  } catch (e) { console.error(e) }
})

const onStudentChange = () => {
  statementData.value = null
  loadCarryForwards()
}

const loadCarryForwards = async () => {
  if (!selectedStudent.value) return
  try {
    carryForwards.value = await feeService.getCarryForwards(selectedStudent.value)
  } catch { carryForwards.value = [] }
}

const saveCarryForward = async () => {
  if (!cfForm.value.amount) return
  cfSaving.value = true
  try {
    await feeService.addCarryForward({
      student_id: selectedStudent.value,
      academic_year: cfForm.value.academic_year,
      term: cfForm.value.term,
      amount: cfForm.value.amount,
      note: cfForm.value.note,
      recorded_by: authStore.user?.name || authStore.user?.username || 'Admin',
    })
    showCfForm.value = false
    cfForm.value = { academic_year: appStore.currentYear, term: 'Term 1', amount: '', note: '' }
    await loadCarryForwards()
    if (statementData.value) await generateStatement()
  } catch (e) { toast.error(e?.message || 'Failed to save.') }
  finally { cfSaving.value = false }
}

const deleteCarryForward = async (id) => {
  if (!confirm('Delete this adjustment?')) return
  try {
    await feeService.deleteCarryForward(id)
    await loadCarryForwards()
    if (statementData.value) await generateStatement()
  } catch { toast.error('Delete failed.') }
}

const generateStatement = async () => {
  loading.value = true
  statementData.value = null
  allPayments.value   = []
  try {
    const [stmt, payments] = await Promise.all([
      feeService.getStudentBalance(selectedStudent.value, selectedTerm.value, selectedYear.value),
      apiFetch(`/api/fees/student/${selectedStudent.value}`),
    ])
    statementData.value = stmt
    allPayments.value   = payments
  } catch {
    toast.error('Failed to generate statement.')
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
