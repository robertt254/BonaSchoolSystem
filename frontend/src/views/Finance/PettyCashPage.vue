<template>
  <div class="max-w-4xl mx-auto space-y-5">

    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-extrabold text-slate-800">Petty Cash</h1>
        <p class="text-sm text-slate-400 mt-0.5">Imprest ledger — track all small cash in/out movements.</p>
      </div>
      <button @click="showModal = true; resetForm()"
        class="bg-school-purple text-white px-4 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Add Entry
      </button>
    </div>

    <!-- Balance card -->
    <div class="bg-white rounded-xl border border-slate-200 p-5 flex items-center gap-6">
      <div>
        <p class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Current Balance</p>
        <p class="text-3xl font-extrabold" :class="balance >= 0 ? 'text-emerald-600' : 'text-red-600'">
          KES {{ fmt(balance) }}
        </p>
      </div>
      <div class="ml-auto flex gap-6 text-center">
        <div>
          <p class="text-xs text-slate-400 font-medium">Total In</p>
          <p class="text-lg font-bold text-emerald-600">KES {{ fmt(totalIn) }}</p>
        </div>
        <div>
          <p class="text-xs text-slate-400 font-medium">Total Out</p>
          <p class="text-lg font-bold text-red-500">KES {{ fmt(totalOut) }}</p>
        </div>
      </div>
    </div>

    <!-- Ledger -->
    <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-100 bg-slate-50">
              <th class="px-5 py-3 text-left">Date</th>
              <th class="px-5 py-3 text-left">Description</th>
              <th class="px-5 py-3 text-left">Category</th>
              <th class="px-5 py-3 text-center">Type</th>
              <th class="px-5 py-3 text-right">Amount</th>
              <th class="px-5 py-3 text-right">Balance</th>
              <th class="px-5 py-3 text-right w-12"></th>
            </tr>
          </thead>
          <tbody v-if="transactions.length > 0">
            <tr v-for="tx in transactions" :key="tx.id" class="border-b border-slate-50 hover:bg-slate-50">
              <td class="px-5 py-3 text-slate-500 text-xs whitespace-nowrap">{{ fmtDate(tx.transaction_date) }}</td>
              <td class="px-5 py-3 text-slate-700">{{ tx.description }}</td>
              <td class="px-5 py-3 text-slate-500 text-xs">{{ tx.category || '—' }}</td>
              <td class="px-5 py-3 text-center">
                <span class="px-2.5 py-0.5 rounded-full text-xs font-bold"
                  :class="tx.transaction_type === 'IN' ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-600'">
                  {{ tx.transaction_type }}
                </span>
              </td>
              <td class="px-5 py-3 text-right font-semibold"
                :class="tx.transaction_type === 'IN' ? 'text-emerald-600' : 'text-red-500'">
                {{ tx.transaction_type === 'IN' ? '+' : '-' }}{{ fmt(tx.amount) }}
              </td>
              <td class="px-5 py-3 text-right font-mono text-xs text-slate-600">{{ fmt(tx.running_balance) }}</td>
              <td class="px-5 py-3 text-right">
                <button @click="deleteTx(tx.id)" class="text-xs text-red-400 hover:text-red-600">Del</button>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr><td colspan="7" class="py-12 text-center text-slate-400 text-sm">No transactions yet.</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-base font-bold text-slate-800">New Transaction</h3>
          <button @click="showModal = false" class="text-slate-400 hover:text-slate-600 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-100">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="space-y-3">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Type</label>
              <select v-model="form.transaction_type" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
                <option value="IN">IN (Receipt)</option>
                <option value="OUT">OUT (Payment)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Amount (KES)</label>
              <input v-model.number="form.amount" type="number" min="0.01" step="0.01"
                class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
            </div>
          </div>
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Description *</label>
            <input v-model="form.description" type="text"
              class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
          </div>
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Category</label>
            <input v-model="form.category" type="text" placeholder="e.g. Stationery, Transport"
              class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
          </div>
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button @click="showModal = false" class="px-4 py-2 text-sm text-slate-600 hover:text-slate-800">Cancel</button>
          <button @click="saveEntry" :disabled="saving"
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

const transactions = ref([])
const showModal = ref(false)
const saving = ref(false)
const form = ref({ transaction_type: 'OUT', amount: '', description: '', category: '' })

const balance = computed(() => transactions.value.length ? transactions.value[transactions.value.length - 1]?.running_balance ?? 0 : 0)
const totalIn = computed(() => transactions.value.filter(t => t.transaction_type === 'IN').reduce((s, t) => s + Number(t.amount), 0))
const totalOut = computed(() => transactions.value.filter(t => t.transaction_type === 'OUT').reduce((s, t) => s + Number(t.amount), 0))

const fmt = (n) => Number(n || 0).toLocaleString('en-KE', { minimumFractionDigits: 2 })
const fmtDate = (d) => d ? new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : ''

const load = async () => {
  try {
    const data = await apiFetch('/api/finance/petty-cash')
    transactions.value = (data.transactions || data).slice().reverse()
  } catch { /* silent */ }
}

const resetForm = () => {
  form.value = { transaction_type: 'OUT', amount: '', description: '', category: '' }
}

const saveEntry = async () => {
  if (!form.value.description.trim() || !form.value.amount) return
  saving.value = true
  try {
    await apiFetch('/api/finance/petty-cash', { method: 'POST', body: JSON.stringify(form.value) })
    showModal.value = false
    await load()
  } catch (e) { alert(e?.message || 'Failed to save.') }
  finally { saving.value = false }
}

const deleteTx = async (id) => {
  if (!confirm('Delete this entry?')) return
  try {
    await apiFetch(`/api/finance/petty-cash/${id}`, { method: 'DELETE' })
    await load()
  } catch { alert('Delete failed.') }
}

onMounted(load)
</script>
