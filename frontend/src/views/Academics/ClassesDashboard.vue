<template>
  <div class="max-w-7xl mx-auto space-y-6">

    <!-- Grade overview cards -->
    <div v-if="loadingSummary" class="py-16 flex justify-center">
      <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
    </div>

    <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
      <button
        v-for="cls in summary"
        :key="cls.grade_level"
        @click="openClass(cls.grade_level)"
        :class="[
          'bg-white rounded-[12px] border p-4 text-left hover:shadow-md transition-all group',
          selectedGrade === cls.grade_level
            ? 'border-school-purple ring-2 ring-school-purple/20'
            : 'border-[#E2E8F0] hover:border-school-purple/40',
        ]"
      >
        <div class="flex items-center justify-between mb-3">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center font-black text-xs text-white"
            :style="{ background: gradeColor(cls.grade_level) }">
            {{ cls.grade_level.replace('Grade ', 'G').replace('Play Group', 'PG') }}
          </div>
          <span class="text-[10px] font-bold uppercase text-slate-400">{{ cls.total }} pupils</span>
        </div>
        <p class="font-bold text-slate-800 text-sm leading-tight">{{ cls.grade_level }}</p>
        <div class="mt-2 grid grid-cols-2 gap-1 text-[10px] text-slate-500">
          <span class="flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>{{ cls.male }}M</span>
          <span class="flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-pink-400"></span>{{ cls.female }}F</span>
        </div>
        <div class="mt-2 h-1.5 bg-slate-100 rounded-full overflow-hidden">
          <div
            class="h-full bg-emerald-400 rounded-full transition-all"
            :style="{ width: cls.total > 0 && cls.present_today > 0 ? `${Math.round(cls.present_today / cls.total * 100)}%` : '0%' }"
          ></div>
        </div>
        <p class="text-[10px] text-slate-400 mt-1">
          {{ cls.present_today }}/{{ cls.total }} present today
        </p>
      </button>
    </div>

    <!-- Roster panel -->
    <div v-if="selectedGrade" class="bg-white rounded-[12px] border border-[#E2E8F0] overflow-hidden">
      <div class="border-b border-slate-100 px-6 py-4 bg-slate-50 flex items-center justify-between">
        <div>
          <h3 class="font-bold text-slate-800">{{ selectedGrade }} — Class Roster</h3>
          <p class="text-xs text-slate-400 mt-0.5">{{ roster.length }} students</p>
        </div>
        <div class="flex items-center gap-3">
          <div class="relative">
            <svg class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <input v-model="rosterSearch" type="text" placeholder="Search…" class="pl-9 pr-3 py-2 border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple w-44" />
          </div>
        </div>
      </div>

      <div v-if="loadingRoster" class="py-12 flex justify-center">
        <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200 text-[11px] font-bold uppercase tracking-wider text-slate-400">
              <th class="text-left px-6 py-3">#</th>
              <th class="text-left px-6 py-3">Student</th>
              <th class="text-left px-6 py-3">Adm No.</th>
              <th class="text-left px-6 py-3">Gender</th>
              <th class="text-left px-6 py-3">Age</th>
              <th class="text-center px-6 py-3">Attendance</th>
              <th class="text-right px-6 py-3">Fee Balance</th>
              <th class="text-right px-6 py-3">Status</th>
              <th class="text-right px-6 py-3"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr
              v-for="(s, i) in filteredRoster"
              :key="s.id"
              class="hover:bg-slate-50 transition-colors"
            >
              <td class="px-6 py-3.5 text-slate-400 text-xs">{{ i + 1 }}</td>
              <td class="px-6 py-3.5">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs shrink-0"
                    :class="s.gender === 'Female' ? 'bg-pink-100 text-pink-600' : 'bg-blue-100 text-blue-600'">
                    {{ s.first_name.charAt(0) }}{{ s.last_name.charAt(0) }}
                  </div>
                  <span class="font-semibold text-slate-800">{{ s.first_name }} {{ s.last_name }}</span>
                </div>
              </td>
              <td class="px-6 py-3.5 font-mono text-xs text-school-navy">{{ s.admission_number }}</td>
              <td class="px-6 py-3.5">
                <span v-if="s.gender" class="text-xs font-semibold px-2 py-0.5 rounded-full"
                  :class="s.gender === 'Female' ? 'bg-pink-50 text-pink-600' : 'bg-blue-50 text-blue-600'">
                  {{ s.gender }}
                </span>
                <span v-else class="text-slate-300">—</span>
              </td>
              <td class="px-6 py-3.5 text-slate-500 text-xs">
                {{ s.date_of_birth ? calcAge(s.date_of_birth) + 'y' : '—' }}
              </td>
              <td class="px-6 py-3.5 text-center">
                <template v-if="s.attendance_pct !== null">
                  <div class="flex items-center justify-center gap-2">
                    <div class="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                      <div class="h-full rounded-full transition-all"
                        :class="s.attendance_pct >= 80 ? 'bg-emerald-400' : s.attendance_pct >= 60 ? 'bg-amber-400' : 'bg-red-400'"
                        :style="{ width: s.attendance_pct + '%' }"></div>
                    </div>
                    <span class="text-xs font-bold" :class="s.attendance_pct >= 80 ? 'text-emerald-600' : s.attendance_pct >= 60 ? 'text-amber-600' : 'text-red-600'">
                      {{ s.attendance_pct }}%
                    </span>
                  </div>
                </template>
                <span v-else class="text-slate-300 text-xs">No data</span>
              </td>
              <td class="px-6 py-3.5 text-right font-bold" :class="s.fee_balance > 0 ? 'text-school-red' : 'text-emerald-600'">
                {{ s.fee_balance > 0 ? formatCurrency(s.fee_balance) : 'Paid' }}
              </td>
              <td class="px-6 py-3.5 text-right">
                <span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full"
                  :class="s.status === 'Active' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-500'">
                  {{ s.status }}
                </span>
              </td>
              <td class="px-6 py-3.5 text-right">
                <router-link :to="`/students/${s.id}`" class="text-xs font-semibold text-school-purple hover:text-school-purple-l transition">
                  Profile
                </router-link>
              </td>
            </tr>
            <tr v-if="filteredRoster.length === 0">
              <td colspan="9" class="px-6 py-10 text-center text-slate-400 text-sm">No students found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else-if="!loadingSummary" class="bg-white rounded-[12px] border border-[#E2E8F0] py-16 text-center text-slate-400 text-sm">
      Select a class above to view the full roster.
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '@/services/api'

const GRADE_COLORS = {
  'Play Group': '#F59E0B', 'PP1': '#8B5CF6', 'PP2': '#7C3AED',
  'Grade 1': '#3B82F6', 'Grade 2': '#06B6D4', 'Grade 3': '#10B981',
  'Grade 4': '#6366F1', 'Grade 5': '#EC4899', 'Grade 6': '#EF4444',
}

const summary = ref([])
const roster = ref([])
const loadingSummary = ref(false)
const loadingRoster = ref(false)
const selectedGrade = ref('')
const rosterSearch = ref('')

const gradeColor = (g) => GRADE_COLORS[g] || '#64748B'

const filteredRoster = computed(() => {
  const q = rosterSearch.value.toLowerCase()
  if (!q) return roster.value
  return roster.value.filter(s =>
    `${s.first_name} ${s.last_name}`.toLowerCase().includes(q) ||
    s.admission_number.toLowerCase().includes(q)
  )
})

const formatCurrency = (v) =>
  new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 }).format(v)

const calcAge = (dob) => Math.floor((Date.now() - new Date(dob).getTime()) / (1000 * 60 * 60 * 24 * 365.25))

const openClass = async (grade) => {
  if (selectedGrade.value === grade) {
    selectedGrade.value = ''
    roster.value = []
    return
  }
  selectedGrade.value = grade
  loadingRoster.value = true
  try {
    roster.value = await apiFetch(`/api/students/classes/${encodeURIComponent(grade)}`)
  } catch (e) {
    console.error(e)
  } finally {
    loadingRoster.value = false
  }
}

onMounted(async () => {
  loadingSummary.value = true
  try {
    summary.value = await apiFetch('/api/students/classes/summary')
  } catch (e) {
    console.error(e)
  } finally {
    loadingSummary.value = false
  }
})
</script>
