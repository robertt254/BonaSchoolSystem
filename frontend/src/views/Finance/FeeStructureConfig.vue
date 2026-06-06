<template>
  <div class="max-w-5xl mx-auto space-y-6">

    <!-- Add entry form -->
    <div class="bg-white rounded-lg border border-border p-6">
      <h2 class="text-base font-bold text-slate-800 mb-5">Add / Update Fee Entry</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Grade</label>
          <select v-model="form.grade_level" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple">
            <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Term</label>
          <select v-model="form.term" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple">
            <option value="Term 1">Term 1</option>
            <option value="Term 2">Term 2</option>
            <option value="Term 3">Term 3</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Fee Type</label>
          <select v-model="form.fee_type" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple">
            <option value="Tuition">Tuition</option>
            <option value="Uniforms">Uniforms</option>
            <option value="Transport">Transport</option>
            <option value="Exam Fees">Exam Fees</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Amount (KES)</label>
          <input
            v-model.number="form.amount"
            type="number"
            min="1"
            class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple"
            placeholder="e.g. 18000"
          />
        </div>
        <div>
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Year</label>
          <input
            v-model.number="form.academic_year"
            type="number"
            class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple"
          />
        </div>
      </div>
      <div class="mt-4 flex items-center gap-3">
        <button
          @click="saveEntry"
          :disabled="saving"
          class="bg-school-purple text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition disabled:opacity-50"
        >
          {{ saving ? 'Saving…' : editingId ? 'Update Entry' : 'Add Entry' }}
        </button>
        <button v-if="editingId" @click="cancelEdit" class="text-sm text-slate-500 hover:text-slate-800 transition">Cancel</button>
        <span v-if="successMsg" class="text-sm text-emerald-600 font-medium">{{ successMsg }}</span>
        <span v-if="errorMsg" class="text-sm text-school-red font-medium">{{ errorMsg }}</span>
      </div>
    </div>

    <!-- Year filter -->
    <div class="flex items-center gap-3">
      <label class="text-xs font-bold uppercase tracking-widest text-slate-400">View Year:</label>
      <div class="flex gap-2">
        <button
          v-for="y in years"
          :key="y"
          @click="filterYear = y"
          :class="filterYear === y
            ? 'bg-school-purple text-white'
            : 'bg-white text-slate-600 border border-slate-200 hover:border-slate-300'"
          class="px-3 py-1.5 rounded-lg text-sm font-semibold transition"
        >{{ y }}</button>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-lg border border-border overflow-hidden">
      <div class="border-b border-slate-100 px-6 py-4 bg-slate-50 flex items-center justify-between">
        <h3 class="font-bold text-slate-800">Fee Schedule · {{ filterYear }}</h3>
        <span class="text-xs font-bold uppercase tracking-widest text-slate-400">{{ filteredEntries.length }} entries</span>
      </div>

      <div v-if="loading" class="py-16 flex justify-center">
        <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
      </div>

      <div v-else-if="filteredEntries.length === 0" class="py-16 text-center text-slate-400 text-sm">
        No fee structure entries for {{ filterYear }}. Add one above.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200">
              <th class="text-left px-6 py-3 text-xs font-bold uppercase tracking-wider text-slate-400">Grade</th>
              <th class="text-left px-6 py-3 text-xs font-bold uppercase tracking-wider text-slate-400">Term</th>
              <th class="text-left px-6 py-3 text-xs font-bold uppercase tracking-wider text-slate-400">Fee Type</th>
              <th class="text-right px-6 py-3 text-xs font-bold uppercase tracking-wider text-slate-400">Amount</th>
              <th class="text-right px-6 py-3 text-xs font-bold uppercase tracking-wider text-slate-400">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr
              v-for="e in filteredEntries"
              :key="e.id"
              class="hover:bg-slate-50 transition-colors"
              :class="editingId === e.id ? 'bg-violet-50/40' : ''"
            >
              <td class="px-6 py-3.5 font-semibold text-slate-800">{{ e.grade_level }}</td>
              <td class="px-6 py-3.5 text-slate-600">{{ e.term }}</td>
              <td class="px-6 py-3.5 text-slate-600">{{ e.fee_type }}</td>
              <td class="px-6 py-3.5 text-right font-bold text-emerald-700">{{ formatCurrency(e.amount) }}</td>
              <td class="px-6 py-3.5 text-right">
                <div class="flex justify-end gap-2">
                  <button @click="startEdit(e)" class="text-xs font-semibold text-school-purple hover:text-school-purple-l transition">Edit</button>
                  <button @click="deleteEntry(e.id)" class="text-xs font-semibold text-school-red hover:text-red-700 transition">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '@/services/api'
import { useAppStore } from '@/stores/app'
import { useToast } from '@/composables/useToast'
const toast = useToast()

const appStore = useAppStore()

const GRADES = ['Play Group', 'PP1', 'PP2', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6']
const grades = ref(GRADES)
const years = [new Date().getFullYear() - 1, new Date().getFullYear(), new Date().getFullYear() + 1]
const filterYear = ref(new Date().getFullYear())

const entries = ref([])
const loading = ref(false)
const saving = ref(false)
const editingId = ref(null)
const successMsg = ref('')
const errorMsg = ref('')

const form = ref({
  grade_level: 'Grade 1',
  term: 'Term 1',
  fee_type: 'Tuition',
  amount: 18000,
  academic_year: new Date().getFullYear(),
})

const filteredEntries = computed(() =>
  entries.value
    .filter(e => e.academic_year === filterYear.value)
    .sort((a, b) => GRADES.indexOf(a.grade_level) - GRADES.indexOf(b.grade_level) || a.term.localeCompare(b.term))
)

const formatCurrency = (v) =>
  new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 }).format(v)

const loadEntries = async () => {
  loading.value = true
  try {
    entries.value = await apiFetch('/api/fees/structure')
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const saveEntry = async () => {
  successMsg.value = ''
  errorMsg.value = ''
  if (!form.value.amount || form.value.amount <= 0) {
    errorMsg.value = 'Amount must be greater than 0.'
    return
  }
  saving.value = true
  try {
    if (editingId.value) {
      await apiFetch(`/api/fees/structure/${editingId.value}`, {
        method: 'PUT',
        body: JSON.stringify(form.value),
      })
      successMsg.value = 'Entry updated.'
    } else {
      await apiFetch('/api/fees/structure', {
        method: 'POST',
        body: JSON.stringify(form.value),
      })
      successMsg.value = 'Entry added.'
    }
    editingId.value = null
    await loadEntries()
    setTimeout(() => { successMsg.value = '' }, 3000)
  } catch (e) {
    errorMsg.value = e?.message || 'Save failed.'
  } finally {
    saving.value = false
  }
}

const startEdit = (e) => {
  editingId.value = e.id
  form.value = {
    grade_level: e.grade_level,
    term: e.term,
    fee_type: e.fee_type,
    amount: Number(e.amount),
    academic_year: e.academic_year,
  }
}

const cancelEdit = () => {
  editingId.value = null
  form.value.amount = 18000
}

const deleteEntry = async (id) => {
  if (!confirm('Delete this fee structure entry?')) return
  try {
    await apiFetch(`/api/fees/structure/${id}`, { method: 'DELETE' })
    await loadEntries()
  } catch (e) {
    toast.error('Delete failed: ' + (e?.message || ''))
  }
}

onMounted(loadEntries)
</script>
