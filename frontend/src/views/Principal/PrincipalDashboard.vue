<template>
  <div class="max-w-7xl mx-auto space-y-6">

    <!-- Header -->
    <div>
      <h1 class="text-2xl font-extrabold text-slate-800">Principal Overview</h1>
      <p class="text-sm text-slate-400 mt-0.5">School-wide performance at a glance.</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center gap-3 py-12 text-slate-400">
      <div class="w-5 h-5 border-2 border-slate-200 border-t-school-navy rounded-full animate-spin"></div>
      <span class="text-sm font-medium">Loading dashboard…</span>
    </div>

    <template v-else>
      <!-- Stat cards -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total Students" :value="String(stats.total_students)" sub="Active enrolment" color="blue" />
        <StatCard label="Staff Members"  :value="String(stats.total_staff)"    sub="Teaching & admin"  color="red"  />
        <StatCard label="Total Revenue"  :value="formatCurrency(stats.total_revenue)" sub="All-time fee payments" color="green" />
        <StatCard
          label="Today's Attendance"
          :value="stats.today_attendance_pct !== null && stats.today_attendance_pct !== undefined ? stats.today_attendance_pct + '%' : '—'"
          sub="Students present today"
          color="amber"
        />
      </div>

      <!-- Term Fee Collection Progress -->
      <div class="bg-white rounded-lg border border-slate-200 p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <p class="text-xs font-bold uppercase tracking-widest text-slate-400">{{ appStore.currentTerm }} Fee Collection</p>
            <p class="text-2xl font-extrabold text-slate-800 mt-0.5">{{ formatCurrency(stats.term_collected || 0) }}</p>
          </div>
          <div class="text-right">
            <p class="text-2xl font-extrabold"
              :class="(stats.term_pct || 0) >= 80 ? 'text-emerald-600' : (stats.term_pct || 0) >= 50 ? 'text-amber-500' : 'text-school-red'">
              {{ stats.term_pct || 0 }}%
            </p>
            <p class="text-xs text-slate-400">Target: {{ formatCurrency(stats.term_expected || 0) }}</p>
          </div>
        </div>
        <div class="w-full bg-slate-100 rounded-full h-2 mb-3">
          <div
            class="h-2 rounded-full transition-all duration-1000"
            :class="(stats.term_pct || 0) >= 80 ? 'bg-emerald-500' : (stats.term_pct || 0) >= 50 ? 'bg-amber-400' : 'bg-school-red'"
            :style="{ width: Math.min(stats.term_pct || 0, 100) + '%' }"
          ></div>
        </div>
        <div class="flex items-center justify-between text-xs text-slate-400">
          <span>{{ stats.defaulters_count || 0 }} student{{ (stats.defaulters_count || 0) !== 1 ? 's' : '' }} with outstanding balance</span>
          <router-link to="/finance" class="font-semibold text-school-purple hover:text-school-purple-l transition-colors">View Finance →</router-link>
        </div>
      </div>

      <!-- Two-column section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">

        <!-- Enrollment by Grade (horizontal bar chart) -->
        <div class="bg-white rounded-lg border border-slate-200 overflow-hidden">
          <div class="px-5 py-4 border-b border-slate-100">
            <h3 class="font-bold text-slate-800 text-sm">Enrollment by Grade</h3>
            <p class="text-xs text-slate-400 mt-0.5">Active students per CBC level</p>
          </div>
          <div class="p-5 space-y-3">
            <div
              v-for="item in gradeStats"
              :key="item.grade"
              class="flex items-center gap-3"
            >
              <span class="w-20 text-right text-xs font-medium text-slate-500 shrink-0 leading-none">{{ item.grade }}</span>
              <div class="flex-1 h-6 bg-slate-100 rounded-lg overflow-hidden">
                <div
                  class="h-full bg-school-navy rounded-lg transition-all duration-700"
                  :style="{ width: maxEnrolment > 0 ? (item.count / maxEnrolment * 100) + '%' : '0%' }"
                ></div>
              </div>
              <span class="w-7 text-xs font-bold text-slate-600 shrink-0">{{ item.count }}</span>
            </div>
            <p v-if="!gradeStats.some(g => g.count > 0)" class="text-sm text-slate-400 text-center py-4">
              No active students found.
            </p>
          </div>
        </div>

        <!-- Attendance Summary per grade -->
        <div class="bg-white rounded-lg border border-slate-200 overflow-hidden">
          <div class="px-5 py-4 border-b border-slate-100">
            <h3 class="font-bold text-slate-800 text-sm">Attendance Overview</h3>
            <p class="text-xs text-slate-400 mt-0.5">All-time records per grade</p>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-slate-50 text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-100">
                  <th class="px-5 py-3 text-left">Grade</th>
                  <th class="px-5 py-3 text-right">Records</th>
                  <th class="px-5 py-3 text-right">Present</th>
                  <th class="px-5 py-3 text-right">Rate</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="row in attendanceSummary.filter(r => r.total_records > 0)"
                  :key="row.grade"
                  class="border-b border-slate-50 hover:bg-slate-50 transition-colors"
                >
                  <td class="px-5 py-3 font-medium text-slate-700">{{ row.grade }}</td>
                  <td class="px-5 py-3 text-right text-slate-500">{{ row.total_records }}</td>
                  <td class="px-5 py-3 text-right text-slate-500">{{ row.present }}</td>
                  <td class="px-5 py-3 text-right">
                    <span
                      class="inline-block px-2 py-0.5 rounded-full text-xs font-bold"
                      :class="rateClass(row.percentage)"
                    >{{ row.percentage !== null ? row.percentage + '%' : '—' }}</span>
                  </td>
                </tr>
                <tr v-if="!attendanceSummary.some(r => r.total_records > 0)">
                  <td colspan="4" class="px-5 py-8 text-center text-slate-400 text-sm">No attendance data yet.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-white rounded-lg border border-slate-200 overflow-hidden">
        <div class="px-5 py-4 border-b border-slate-100">
          <h3 class="font-bold text-slate-800 text-sm">Quick Reports</h3>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4">
          <router-link
            v-for="action in quickActions"
            :key="action.to"
            :to="action.to"
            class="flex flex-col items-center gap-2 p-4 rounded-xl bg-slate-50 border border-slate-200 hover:bg-white hover:border-school-purple/30 hover:shadow-sm transition-all text-center"
          >
            <div class="w-10 h-10 rounded-xl flex items-center justify-center" :class="action.iconBg">
              <svg class="w-5 h-5" :class="action.iconColor" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24" v-html="action.iconPath"></svg>
            </div>
            <span class="text-xs font-semibold text-slate-700">{{ action.label }}</span>
          </router-link>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, defineComponent, h } from 'vue'
import { apiFetch } from '@/services/api'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

// ── Stat Card sub-component ───────────────────────────────────────────────────
const CARD_COLORS = {
  blue:  { bar: 'from-blue-500 to-indigo-400',  icon: 'bg-blue-50 text-blue-600'  },
  red:   { bar: 'from-school-purple to-school-purple-ll', icon: 'bg-violet-50 text-school-purple' },
  green: { bar: 'from-emerald-500 to-teal-400', icon: 'bg-emerald-50 text-emerald-600' },
  amber: { bar: 'from-amber-400 to-yellow-300', icon: 'bg-amber-50 text-amber-600' },
}

const StatCard = defineComponent({
  props: { label: String, value: String, sub: String, color: String },
  setup(props) {
    const c = computed(() => CARD_COLORS[props.color] || CARD_COLORS.blue)
    return () => h('div', { class: 'bg-white rounded-lg border border-slate-200 p-6 relative overflow-hidden' }, [
      h('span', { class: `absolute top-0 inset-x-0 h-0.5 rounded-t-xl bg-gradient-to-r ${c.value.bar}` }),
      h('p', { class: 'text-xs font-bold uppercase tracking-widest text-slate-400 mb-2' }, props.label),
      h('p', { class: 'text-3xl font-extrabold text-slate-800 leading-none mb-1' }, props.value),
      h('p', { class: 'text-xs text-slate-400' }, props.sub),
    ])
  },
})

// ── State ─────────────────────────────────────────────────────────────────────
const loading          = ref(true)
const stats            = ref({ total_students: 0, total_staff: 0, total_revenue: 0 })
const gradeStats       = ref([])
const attendanceSummary = ref([])

const maxEnrolment = computed(() => Math.max(...gradeStats.value.map(g => g.count), 1))

const avgAttendance = computed(() => {
  const rows = attendanceSummary.value.filter(r => r.total_records > 0)
  if (!rows.length) return null
  const totalPresent = rows.reduce((s, r) => s + r.present, 0)
  const totalRecords = rows.reduce((s, r) => s + r.total_records, 0)
  return totalRecords > 0 ? Math.round(totalPresent / totalRecords * 100) : null
})

const rateClass = (pct) => {
  if (pct === null) return 'bg-slate-100 text-slate-400'
  if (pct >= 90)    return 'bg-emerald-50 text-emerald-700'
  if (pct >= 75)    return 'bg-amber-50 text-amber-700'
  return 'bg-red-50 text-red-600'
}

const formatCurrency = (v) =>
  new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 }).format(v)

const quickActions = [
  { to: '/office',              label: 'Student Directory',  iconBg: 'bg-blue-50',    iconColor: 'text-blue-600',    iconPath: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>' },
  { to: '/finance',             label: 'Fee Dashboard',      iconBg: 'bg-emerald-50', iconColor: 'text-emerald-600', iconPath: '<rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>' },
  { to: '/academics/report-card', label: 'Report Cards',    iconBg: 'bg-violet-50',  iconColor: 'text-school-purple', iconPath: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>' },
  { to: '/finance/statements',  label: 'Fee Statements',     iconBg: 'bg-indigo-50',  iconColor: 'text-indigo-600',  iconPath: '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>' },
]

// ── Data load ─────────────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    const [s, g, a] = await Promise.all([
      apiFetch('/api/dashboard/stats'),
      apiFetch('/api/dashboard/grade-stats'),
      apiFetch('/api/attendance/summary'),
    ])
    stats.value             = s
    gradeStats.value        = g
    attendanceSummary.value = a
  } catch (err) {
    console.error('Principal dashboard load failed', err)
  } finally {
    loading.value = false
  }
})
</script>
