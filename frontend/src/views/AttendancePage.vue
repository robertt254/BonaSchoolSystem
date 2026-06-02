<template>
  <div class="max-w-5xl mx-auto space-y-6">

    <!-- Page header + tabs -->
    <div>
      <h1 class="text-2xl font-extrabold text-slate-800">Attendance</h1>
      <p class="text-sm text-slate-400 mt-0.5">Daily roll call and school-wide attendance summary.</p>
    </div>

    <!-- Tab bar -->
    <div class="flex gap-1 bg-slate-100 p-1 rounded-xl w-fit">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="activeTab = tab.id"
        class="px-4 py-2 text-sm font-semibold rounded-lg transition-all"
        :class="activeTab === tab.id
          ? 'bg-white text-slate-800 shadow-sm'
          : 'text-slate-500 hover:text-slate-700'"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- ── TAB: Daily Roll Call ─────────────────────────────────────── -->
    <template v-if="activeTab === 'rollcall'">
      <div class="bg-white rounded-xl border border-slate-200 p-6 flex flex-col sm:flex-row gap-4 items-end">
        <div class="flex-1 max-w-xs">
          <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">CBC Grade</label>
          <select
            v-model="selectedGrade"
            class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none"
          >
            <option v-for="g in GRADES" :key="g" :value="g">{{ g }}</option>
          </select>
        </div>
        <button
          @click="loadClassList"
          :disabled="loadingClass"
          class="bg-school-navy text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-navy/90 transition disabled:opacity-60"
        >
          {{ loadingClass ? 'Loading…' : 'Load Students' }}
        </button>
      </div>

      <div v-if="classList.length > 0" class="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div class="flex items-center justify-between px-5 py-3.5 border-b border-slate-100 bg-slate-50">
          <span class="font-semibold text-sm text-slate-700">{{ selectedGrade }} · {{ todayFormatted }}</span>
          <span class="text-xs font-bold text-slate-400">{{ classList.length }} students</span>
        </div>
        <table class="w-full text-sm">
          <thead>
            <tr class="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-100">
              <th class="px-5 py-4 text-left">Student</th>
              <th class="px-5 py-4">Status</th>
              <th class="px-5 py-4 text-left">Remarks</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="s in classList"
              :key="s.student_id"
              class="border-b border-slate-50 hover:bg-slate-50 transition-colors"
            >
              <td class="px-5 py-4 font-medium text-slate-800">{{ s.name }}</td>
              <td class="px-5 py-4 text-center">
                <button
                  @click="s.is_present = !s.is_present"
                  class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold transition-colors"
                  :class="s.is_present
                    ? 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
                    : 'bg-red-50 text-red-600 hover:bg-red-100'"
                >
                  <span class="w-1.5 h-1.5 rounded-full" :class="s.is_present ? 'bg-emerald-500' : 'bg-red-500'"></span>
                  {{ s.is_present ? 'Present' : 'Absent' }}
                </button>
              </td>
              <td class="px-5 py-4">
                <input
                  v-model="s.remarks"
                  placeholder="Optional note…"
                  class="w-full border border-slate-200 px-3 py-1.5 rounded-lg text-xs focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none"
                />
              </td>
            </tr>
          </tbody>
        </table>
        <div class="flex items-center justify-between px-5 py-4 bg-slate-50 border-t border-slate-100">
          <span class="text-xs text-slate-400">
            {{ classList.filter(s => s.is_present).length }} present ·
            {{ classList.filter(s => !s.is_present).length }} absent
          </span>
          <button
            @click="saveAttendance"
            :disabled="saving"
            class="bg-emerald-600 text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-emerald-700 transition disabled:opacity-60"
          >
            {{ saving ? 'Saving…' : 'Submit Roll Call' }}
          </button>
        </div>
      </div>

      <div v-else-if="hasSearched && !loadingClass" class="bg-white rounded-xl border border-slate-200 py-12 text-center text-slate-400 text-sm">
        No students found in {{ selectedGrade }}.
      </div>
    </template>

    <!-- ── TAB: Attendance Summary ─────────────────────────────────── -->
    <template v-if="activeTab === 'summary'">
      <div v-if="loadingSummary" class="flex items-center gap-3 py-10 text-slate-400">
        <div class="w-4 h-4 border-2 border-slate-200 border-t-school-navy rounded-full animate-spin"></div>
        <span class="text-sm">Loading summary…</span>
      </div>

      <div v-else class="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div class="px-5 py-4 border-b border-slate-100">
          <h3 class="font-bold text-slate-800 text-sm">School-wide Attendance by Grade</h3>
          <p class="text-xs text-slate-400 mt-0.5">All records since the start of the system.</p>
        </div>
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-slate-50 text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-100">
              <th class="px-5 py-3 text-left">Grade</th>
              <th class="px-5 py-3 text-right">Total Days</th>
              <th class="px-5 py-3 text-right">Present</th>
              <th class="px-5 py-3 text-right">Absent</th>
              <th class="px-5 py-3 text-right">Attendance Rate</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="row in summary"
              :key="row.grade"
              class="border-b border-slate-50 hover:bg-slate-50 transition-colors"
            >
              <td class="px-5 py-3.5 font-semibold text-slate-700">{{ row.grade }}</td>
              <td class="px-5 py-3.5 text-right text-slate-500">{{ row.total_records || '—' }}</td>
              <td class="px-5 py-3.5 text-right text-emerald-600 font-medium">{{ row.present || '—' }}</td>
              <td class="px-5 py-3.5 text-right text-red-400">{{ row.total_records > 0 ? row.total_records - row.present : '—' }}</td>
              <td class="px-5 py-3.5 text-right">
                <template v-if="row.total_records > 0">
                  <span
                    class="inline-block px-2.5 py-0.5 rounded-full text-xs font-bold"
                    :class="rateClass(row.percentage)"
                  >{{ row.percentage }}%</span>
                  <div class="mt-1 h-1 w-24 ml-auto bg-slate-100 rounded-full overflow-hidden">
                    <div
                      class="h-full rounded-full"
                      :class="row.percentage >= 90 ? 'bg-emerald-500' : row.percentage >= 75 ? 'bg-amber-400' : 'bg-red-400'"
                      :style="{ width: row.percentage + '%' }"
                    ></div>
                  </div>
                </template>
                <span v-else class="text-slate-300 text-xs">No data</span>
              </td>
            </tr>
          </tbody>
          <tfoot v-if="overallRate !== null">
            <tr class="bg-slate-50 border-t-2 border-slate-200 font-bold">
              <td class="px-5 py-3 text-slate-700">Overall</td>
              <td class="px-5 py-3 text-right text-slate-600">{{ totalRecords }}</td>
              <td class="px-5 py-3 text-right text-emerald-600">{{ totalPresent }}</td>
              <td class="px-5 py-3 text-right text-red-400">{{ totalRecords - totalPresent }}</td>
              <td class="px-5 py-3 text-right">
                <span class="inline-block px-2.5 py-0.5 rounded-full text-xs font-bold" :class="rateClass(overallRate)">
                  {{ overallRate }}%
                </span>
              </td>
            </tr>
          </tfoot>
        </table>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '@/services/api'
import { useToast } from '@/composables/useToast'
const toast = useToast()


const GRADES = ['Play Group','PP1','PP2','Grade 1','Grade 2','Grade 3','Grade 4','Grade 5','Grade 6']

const tabs = [
  { id: 'rollcall', label: 'Daily Roll Call' },
  { id: 'summary',  label: 'Attendance Summary' },
]
const activeTab = ref('rollcall')

// ── Roll Call state ───────────────────────────────────────────────────────────
const selectedGrade = ref('Grade 1')
const classList     = ref([])
const hasSearched   = ref(false)
const loadingClass  = ref(false)
const saving        = ref(false)

const todayFormatted = new Date().toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })

const loadClassList = async () => {
  hasSearched.value = true
  loadingClass.value = true
  try {
    classList.value = await apiFetch(`/api/attendance/today/${encodeURIComponent(selectedGrade.value)}`)
  } catch {
    toast.error('Error loading class list.')
  } finally {
    loadingClass.value = false
  }
}

const saveAttendance = async () => {
  saving.value = true
  try {
    await apiFetch('/api/attendance/bulk', {
      method: 'POST',
      body: JSON.stringify(classList.value),
    })
    toast.success('Roll call submitted successfully.')
  } catch {
    toast.error('Error saving attendance.')
  } finally {
    saving.value = false
  }
}

// ── Summary state ─────────────────────────────────────────────────────────────
const summary        = ref([])
const loadingSummary = ref(false)

const totalRecords = computed(() => summary.value.reduce((s, r) => s + r.total_records, 0))
const totalPresent = computed(() => summary.value.reduce((s, r) => s + r.present, 0))
const overallRate  = computed(() => totalRecords.value > 0
  ? Math.round(totalPresent.value / totalRecords.value * 100)
  : null
)

const rateClass = (pct) => {
  if (pct === null) return 'bg-slate-100 text-slate-400'
  if (pct >= 90)    return 'bg-emerald-50 text-emerald-700'
  if (pct >= 75)    return 'bg-amber-50 text-amber-700'
  return 'bg-red-50 text-red-600'
}

onMounted(async () => {
  loadingSummary.value = true
  try {
    summary.value = await apiFetch('/api/attendance/summary')
  } catch (err) {
    console.error('Failed to load attendance summary', err)
  } finally {
    loadingSummary.value = false
  }
})
</script>
