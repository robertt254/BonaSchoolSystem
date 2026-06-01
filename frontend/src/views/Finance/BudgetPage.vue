<template>
  <div class="max-w-5xl mx-auto space-y-5">

    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-extrabold text-slate-800">Budget vs Actual</h1>
        <p class="text-sm text-slate-400 mt-0.5">Plan and track spending against budget per category.</p>
      </div>
      <div class="flex gap-2">
        <button v-if="budgets.length > 0" @click="exportBudget"
          class="flex items-center gap-1.5 bg-white border border-slate-200 text-slate-600 px-4 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-50 transition">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Export CSV
        </button>
        <button @click="showModal = true; resetForm()"
          class="bg-school-purple text-white px-4 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Add Budget
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-slate-200 p-4 flex flex-wrap gap-4 items-end">
      <div>
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Academic Year</label>
        <select v-model="filterYear" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
          <option v-for="y in appStore.years" :key="y" :value="y">{{ y }}</option>
        </select>
      </div>
      <div>
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Term</label>
        <select v-model="filterTerm" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
          <option value="">All Terms</option>
          <option value="Term 1">Term 1</option>
          <option value="Term 2">Term 2</option>
          <option value="Term 3">Term 3</option>
        </select>
      </div>
      <button @click="load" :disabled="loading"
        class="bg-school-navy text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-navy/90 transition disabled:opacity-50">
        {{ loading ? 'Loading…' : 'View' }}
      </button>
    </div>

    <!-- Summary cards -->
    <div v-if="budgets.length > 0" class="grid grid-cols-3 gap-4">
      <div class="bg-white rounded-xl border border-slate-200 p-4 text-center">
        <p class="text-xs text-slate-400 font-semibold uppercase tracking-widest mb-1">Total Budgeted</p>
        <p class="text-xl font-extrabold text-slate-800">KES {{ fmt(totalBudgeted) }}</p>
      </div>
      <div class="bg-white rounded-xl border border-slate-200 p-4 text-center">
        <p class="text-xs text-slate-400 font-semibold uppercase tracking-widest mb-1">Total Spent</p>
        <p class="text-xl font-extrabold text-slate-800">KES {{ fmt(totalSpent) }}</p>
      </div>
      <div class="bg-white rounded-xl border border-slate-200 p-4 text-center">
        <p class="text-xs text-slate-400 font-semibold uppercase tracking-widest mb-1">Remaining</p>
        <p class="text-xl font-extrabold" :class="totalRemaining >= 0 ? 'text-emerald-600' : 'text-red-600'">
          KES {{ fmt(totalRemaining) }}
        </p>
      </div>
    </div>

    <!-- Table -->
    <div v-if="budgets.length > 0" class="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-100 bg-slate-50">
            <th class="px-5 py-3 text-left">Category</th>
            <th class="px-5 py-3 text-left">Term</th>
            <th class="px-5 py-3 text-right">Budgeted</th>
            <th class="px-5 py-3 text-right">Actual</th>
            <th class="px-5 py-3 text-right">Variance</th>
            <th class="px-5 py-3 text-center w-16">%</th>
            <th class="px-5 py-3 text-right w-20"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in budgets" :key="b.id" class="border-b border-slate-50 hover:bg-slate-50">
            <td class="px-5 py-3.5 font-semibold text-slate-800">{{ b.category }}</td>
            <td class="px-5 py-3.5 text-slate-500 text-xs">{{ b.term }}</td>
            <td class="px-5 py-3.5 text-right text-slate-700 font-mono text-xs">{{ fmt(b.budgeted_amount) }}</td>
            <td class="px-5 py-3.5 text-right font-mono text-xs" :class="b.actual_spent > b.budgeted_amount ? 'text-red-600 font-bold' : 'text-slate-700'">
              {{ fmt(b.actual_spent) }}
            </td>
            <td class="px-5 py-3.5 text-right font-mono text-xs font-bold"
              :class="b.variance >= 0 ? 'text-emerald-600' : 'text-red-600'">
              {{ b.variance >= 0 ? '+' : '' }}{{ fmt(b.variance) }}
            </td>
            <td class="px-5 py-3.5 text-center">
              <span v-if="b.budgeted_amount > 0" class="px-2 py-0.5 rounded-full text-xs font-bold"
                :class="pctClass(b.actual_spent / b.budgeted_amount * 100)">
                {{ Math.round(b.actual_spent / b.budgeted_amount * 100) }}%
              </span>
            </td>
            <td class="px-5 py-3.5 text-right flex gap-2 justify-end">
              <button @click="editBudget(b)" class="text-xs text-school-purple hover:underline">Edit</button>
              <button @click="deleteBudget(b.id)" class="text-xs text-red-400 hover:text-red-600">Del</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else-if="loaded" class="bg-white rounded-xl border border-slate-200 py-12 text-center text-slate-400 text-sm">
      No budget entries for this selection.
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-base font-bold text-slate-800">{{ editingId ? 'Edit Budget' : 'Add Budget' }}</h3>
          <button @click="showModal = false" class="text-slate-400 hover:text-slate-600 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-100">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="space-y-3">
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Category *</label>
            <input v-model="form.category" type="text" placeholder="e.g. Stationery, Utilities"
              class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Term</label>
              <select v-model="form.term" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
                <option value="Term 1">Term 1</option>
                <option value="Term 2">Term 2</option>
                <option value="Term 3">Term 3</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Amount (KES)</label>
              <input v-model.number="form.budgeted_amount" type="number" min="0"
                class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
            </div>
          </div>
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button @click="showModal = false" class="px-4 py-2 text-sm text-slate-600 hover:text-slate-800">Cancel</button>
          <button @click="save" :disabled="saving"
            class="bg-school-purple text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-school-purple-l disabled:opacity-50">
            {{ saving ? 'Saving…' : 'Save' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '@/services/api'
import { useAppStore } from '@/stores/app'
import { downloadCsv } from '@/utils/csvExport'
import { useToast } from '@/composables/useToast'
const toast = useToast()


const appStore = useAppStore()

const budgets = ref([])
const loaded = ref(false)
const loading = ref(false)
const showModal = ref(false)
const saving = ref(false)
const editingId = ref(null)
const filterYear = ref(appStore.currentYear)
const filterTerm = ref('')
const form = ref({ category: '', term: 'Term 1', budgeted_amount: '' })

const totalBudgeted = computed(() => budgets.value.reduce((s, b) => s + Number(b.budgeted_amount), 0))
const totalSpent = computed(() => budgets.value.reduce((s, b) => s + Number(b.actual_spent || 0), 0))
const totalRemaining = computed(() => totalBudgeted.value - totalSpent.value)

const fmt = (n) => Number(n || 0).toLocaleString('en-KE', { minimumFractionDigits: 2 })
const pctClass = (pct) => pct > 100 ? 'bg-red-50 text-red-600' : pct > 80 ? 'bg-amber-50 text-amber-600' : 'bg-emerald-50 text-emerald-600'

const exportBudget = () => {
  downloadCsv(`budget-${filterYear.value}${filterTerm.value ? '-' + filterTerm.value : ''}`, [
    { key: 'category', label: 'Category' },
    { key: 'term', label: 'Term' },
    { key: 'budgeted_amount', label: 'Budgeted (KES)' },
    { key: 'actual_spent', label: 'Actual Spent (KES)' },
    { key: 'variance', label: 'Variance (KES)' },
  ], budgets.value)
}

const load = async () => {
  loading.value = true
  try {
    const qs = new URLSearchParams({ academic_year: filterYear.value })
    if (filterTerm.value) qs.set('term', filterTerm.value)
    budgets.value = await apiFetch(`/api/finance/budget?${qs}`)
    loaded.value = true
  } catch { /* silent */ }
  finally { loading.value = false }
}

const resetForm = () => {
  form.value = { category: '', term: 'Term 1', budgeted_amount: '' }
  editingId.value = null
}

const editBudget = (b) => {
  editingId.value = b.id
  form.value = { category: b.category, term: b.term, budgeted_amount: b.budgeted_amount }
  showModal.value = true
}

const save = async () => {
  if (!form.value.category.trim() || !form.value.budgeted_amount) return
  saving.value = true
  try {
    const body = { ...form.value, academic_year: filterYear.value }
    if (editingId.value) {
      await apiFetch(`/api/finance/budget/${editingId.value}`, { method: 'PUT', body: JSON.stringify(body) })
    } else {
      await apiFetch('/api/finance/budget', { method: 'POST', body: JSON.stringify(body) })
    }
    showModal.value = false
    await load()
  } catch (e) { toast.error(e?.message || 'Failed to save.') }
  finally { saving.value = false }
}

const deleteBudget = async (id) => {
  if (!confirm('Delete this budget entry?')) return
  try {
    await apiFetch(`/api/finance/budget/${id}`, { method: 'DELETE' })
    await load()
  } catch { toast.error('Delete failed.') }
}

onMounted(load)
</script>
