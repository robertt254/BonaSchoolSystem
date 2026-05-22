<template>
  <div class="max-w-6xl mx-auto space-y-6">

    <!-- Controls -->
    <div class="bg-white rounded-[12px] border border-[#E2E8F0] p-5">
      <div class="flex flex-col sm:flex-row items-start sm:items-end gap-4">
        <div>
          <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Term</label>
          <select
            v-model="selectedTerm"
            @change="loadDefaulters"
            class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none"
          >
            <option value="Term 1">Term 1</option>
            <option value="Term 2">Term 2</option>
            <option value="Term 3">Term 3</option>
          </select>
        </div>
        <div class="flex-1">
          <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Search</label>
          <input
            v-model="search"
            type="text"
            placeholder="Name or admission number…"
            class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none"
          />
        </div>
        <button
          @click="printList"
          class="flex items-center gap-2 border border-slate-200 text-slate-600 px-4 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-50 transition print:hidden"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
            <rect x="6" y="14" width="12" height="8"/>
          </svg>
          Print List
        </button>
      </div>
    </div>

    <!-- Summary strip -->
    <div class="grid grid-cols-3 gap-4">
      <div class="bg-white rounded-[12px] border border-[#E2E8F0] p-5 text-center">
        <p class="text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1">Defaulters</p>
        <p class="text-3xl font-extrabold text-school-red">{{ filtered.length }}</p>
      </div>
      <div class="bg-white rounded-[12px] border border-[#E2E8F0] p-5 text-center">
        <p class="text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1">Total Outstanding</p>
        <p class="text-2xl font-extrabold text-school-red">{{ formatCurrency(totalOutstanding) }}</p>
      </div>
      <div class="bg-white rounded-[12px] border border-[#E2E8F0] p-5 text-center">
        <p class="text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1">Avg Per Student</p>
        <p class="text-2xl font-extrabold text-slate-700">{{ formatCurrency(avgBalance) }}</p>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-[12px] border border-[#E2E8F0] overflow-hidden">
      <div class="border-b border-slate-100 px-6 py-4 flex items-center justify-between bg-slate-50">
        <h3 class="font-bold text-slate-800">Fee Defaulters · {{ selectedTerm }}</h3>
        <span class="text-[11px] font-bold uppercase tracking-widest text-slate-400">{{ filtered.length }} students</span>
      </div>

      <div v-if="loading" class="py-20 flex justify-center">
        <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
      </div>

      <div v-else-if="filtered.length === 0" class="py-16 text-center text-slate-400 text-sm">
        No defaulters found for {{ selectedTerm }}.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200">
              <th class="text-left px-6 py-3 text-[11px] font-bold uppercase tracking-wider text-slate-400">#</th>
              <th class="text-left px-6 py-3 text-[11px] font-bold uppercase tracking-wider text-slate-400">Student</th>
              <th class="text-left px-6 py-3 text-[11px] font-bold uppercase tracking-wider text-slate-400">Adm No.</th>
              <th class="text-left px-6 py-3 text-[11px] font-bold uppercase tracking-wider text-slate-400">Grade</th>
              <th class="text-right px-6 py-3 text-[11px] font-bold uppercase tracking-wider text-slate-400">Expected</th>
              <th class="text-right px-6 py-3 text-[11px] font-bold uppercase tracking-wider text-slate-400">Paid</th>
              <th class="text-right px-6 py-3 text-[11px] font-bold uppercase tracking-wider text-slate-400">Credit</th>
              <th class="text-right px-6 py-3 text-[11px] font-bold uppercase tracking-wider text-slate-400">Outstanding</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr
              v-for="(d, i) in filtered"
              :key="d.student_id"
              class="hover:bg-slate-50 transition-colors"
            >
              <td class="px-6 py-3.5 text-slate-400 text-xs">{{ i + 1 }}</td>
              <td class="px-6 py-3.5 font-semibold text-slate-800">{{ d.student_name }}</td>
              <td class="px-6 py-3.5 font-mono text-xs text-school-navy">{{ d.admission_number }}</td>
              <td class="px-6 py-3.5 text-slate-600">{{ d.grade_level }}</td>
              <td class="px-6 py-3.5 text-right text-slate-600">{{ formatCurrency(d.expected_fee) }}</td>
              <td class="px-6 py-3.5 text-right text-emerald-700 font-medium">{{ formatCurrency(d.total_paid) }}</td>
              <td class="px-6 py-3.5 text-right text-blue-600 text-xs">
                {{ d.rollover_credit > 0 ? '− ' + formatCurrency(d.rollover_credit) : '—' }}
              </td>
              <td class="px-6 py-3.5 text-right font-bold text-school-red">{{ formatCurrency(d.outstanding_balance) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import feeService from '@/services/feeService'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()
const selectedTerm = ref(appStore.currentTerm)
const search = ref('')
const defaulters = ref([])
const loading = ref(false)

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  if (!q) return defaulters.value
  return defaulters.value.filter(d =>
    d.student_name.toLowerCase().includes(q) ||
    d.admission_number.toLowerCase().includes(q)
  )
})

const totalOutstanding = computed(() => filtered.value.reduce((s, d) => s + d.outstanding_balance, 0))
const avgBalance = computed(() => filtered.value.length ? totalOutstanding.value / filtered.value.length : 0)

const formatCurrency = (v) =>
  new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 }).format(v)

const loadDefaulters = async () => {
  loading.value = true
  try {
    defaulters.value = await feeService.getDefaulters(selectedTerm.value)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const printList = () => window.print()

onMounted(loadDefaulters)
</script>

<style>
@media print {
  .print\:hidden { display: none !important; }
}
</style>
