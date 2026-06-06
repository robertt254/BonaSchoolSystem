<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
      <div>
        <h2 class="text-2xl font-semibold" style="color:#1e293b;letter-spacing:-0.01em">Dashboard Overview</h2>
        <p class="text-sm mt-0.5" style="color:#64748b">{{ greeting }}, {{ userName }}. Here's what's happening today at The Bona School.</p>
      </div>
      <div class="flex items-center gap-3">
        <router-link to="/admin/reports" v-if="canViewFinance"
          class="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold border rounded transition-all hover:bg-slate-50 active:scale-95"
          style="border-color:#161b2b;color:#161b2b">
          <span class="material-symbols-outlined" style="font-size:16px">cloud_download</span>
          GENERATE REPORT
        </router-link>
        <router-link to="/academics/students" v-if="canAdmitStudents"
          class="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold text-white rounded transition-all hover:opacity-90 active:scale-95 shadow-sm"
          style="background:#712edd">
          <span class="material-symbols-outlined" style="font-size:16px">add</span>
          QUICK ACTION
        </router-link>
      </div>
    </div>

    <!-- Skeleton loading -->
    <div v-if="loading" class="space-y-4">
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="n in 4" :key="n" class="bg-white border border-slate-200 rounded p-6" style="min-height:120px">
          <div class="skel h-8 w-8 rounded mb-4" />
          <div class="skel h-3 w-20 rounded mb-2" />
          <div class="skel h-6 w-16 rounded" />
        </div>
      </div>
    </div>

    <!-- Error Banner -->
    <div v-else-if="loadError" class="bg-red-50 border border-red-200 rounded p-5 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="material-symbols-outlined text-red-500" style="font-size:20px">error</span>
        <div>
          <p class="text-sm font-semibold text-red-700">Failed to load dashboard data</p>
          <p class="text-xs text-red-500 mt-0.5">{{ loadError }}</p>
        </div>
      </div>
      <button @click="retryLoad" class="text-xs font-semibold text-red-600 border border-red-300 px-4 py-2 rounded hover:bg-red-100 transition-colors">Retry</button>
    </div>

    <template v-else>
      <!-- Stat Cards — Stitch design -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Total Students -->
        <div class="bg-white border border-slate-200 rounded p-6 flex flex-col justify-between" style="min-height:130px">
          <div class="flex justify-between items-start mb-4">
            <div class="p-2 rounded" style="background:rgba(113,46,221,0.1)">
              <span class="material-symbols-outlined" style="color:#712edd;font-size:22px">group</span>
            </div>
            <span class="text-xs font-semibold px-2 py-0.5 rounded" style="color:#16a34a;background:#f0fdf4">Active</span>
          </div>
          <div>
            <p class="text-xs font-semibold uppercase tracking-wider" style="color:#64748b">Total Students</p>
            <h3 class="text-2xl font-bold mt-0.5" style="color:#1e293b">{{ displayStudents }}</h3>
          </div>
        </div>

        <!-- Monthly Revenue — finance roles -->
        <div v-if="canViewFinance" class="bg-white border border-slate-200 rounded p-6 flex flex-col justify-between" style="min-height:130px">
          <div class="flex justify-between items-start mb-4">
            <div class="p-2 rounded" style="background:#dbeafe">
              <span class="material-symbols-outlined" style="color:#2563eb;font-size:22px">payments</span>
            </div>
            <span class="text-xs font-semibold px-2 py-0.5 rounded" style="color:#16a34a;background:#f0fdf4">YTD</span>
          </div>
          <div>
            <p class="text-xs font-semibold uppercase tracking-wider" style="color:#64748b">Total Revenue</p>
            <h3 class="text-xl font-bold mt-0.5" style="color:#1e293b">{{ formatCurrency(displayRevenue) }}</h3>
          </div>
        </div>

        <!-- Staff Count — HR roles -->
        <div v-if="canViewHR" class="bg-white border border-slate-200 rounded p-6 flex flex-col justify-between" style="min-height:130px">
          <div class="flex justify-between items-start mb-4">
            <div class="p-2 rounded" style="background:#fef3c7">
              <span class="material-symbols-outlined" style="color:#d97706;font-size:22px">badge</span>
            </div>
            <span class="text-xs font-semibold" style="color:#64748b">Stable</span>
          </div>
          <div>
            <p class="text-xs font-semibold uppercase tracking-wider" style="color:#64748b">Staff Count</p>
            <h3 class="text-2xl font-bold mt-0.5" style="color:#1e293b">{{ displayStaff }}</h3>
          </div>
        </div>

        <!-- Attendance -->
        <div class="bg-white border border-slate-200 rounded p-6 flex flex-col justify-between" style="min-height:130px">
          <div class="flex justify-between items-start mb-4">
            <div class="p-2 rounded" style="background:#fce7f3">
              <span class="material-symbols-outlined" style="color:#db2777;font-size:22px">how_to_reg</span>
            </div>
            <span class="text-xs font-semibold px-2 py-0.5 rounded"
              :style="todayAttendancePct !== null ? 'color:#16a34a;background:#f0fdf4' : 'color:#64748b;background:#f1f5f9'">
              {{ todayAttendancePct !== null ? 'Live' : 'No Data' }}
            </span>
          </div>
          <div>
            <p class="text-xs font-semibold uppercase tracking-wider" style="color:#64748b">Today's Attendance</p>
            <h3 class="text-2xl font-bold mt-0.5" style="color:#1e293b">{{ todayAttendancePct !== null ? displayAttendance + '%' : '—' }}</h3>
          </div>
        </div>
      </div>

      <!-- Main Content Grid: Activity + Quick Actions + Finance -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">

        <!-- Recent Activity (2 cols) -->
        <div class="lg:col-span-2 bg-white border border-slate-200 rounded overflow-hidden">
          <div class="flex items-center justify-between px-6 py-4 border-b border-slate-100">
            <h4 class="font-semibold text-sm" style="color:#1e293b">Recent Activity</h4>
            <router-link to="/admin/reports" v-if="canViewFinance" class="text-xs font-semibold hover:underline" style="color:#712edd">View All</router-link>
          </div>
          <div>
            <div v-if="filteredActivity.length === 0" class="px-6 py-10 text-center text-sm" style="color:#94a3b8">
              No recent activity recorded
            </div>
            <div
              v-for="activity in filteredActivity.slice(0, 6)"
              :key="activity.id"
              class="flex items-start gap-4 px-6 py-4 border-b border-slate-50 last:border-b-0 transition-colors cursor-default"
              style="--hover-bg:#f8fafc"
              onmouseover="this.style.background='#f8fafc'"
              onmouseout="this.style.background=''"
            >
              <div class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0 mt-0.5"
                :class="activity.avatarClass">
                {{ activity.user.charAt(0) }}
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm" style="color:#1e293b">
                  <span class="font-semibold">{{ activity.user }}</span>
                  <span style="color:#475569"> {{ activity.action }}</span>
                </p>
                <p class="text-xs mt-1 flex items-center gap-1.5" style="color:#94a3b8">
                  <span class="w-1.5 h-1.5 rounded-full inline-block" :class="activity.dotClass"></span>
                  {{ activity.time }} · {{ activity.type }}
                </p>
              </div>
              <span class="material-symbols-outlined text-slate-300 shrink-0 mt-0.5" style="font-size:18px">more_vert</span>
            </div>
          </div>
        </div>

        <!-- Right column -->
        <div class="space-y-4">
          <!-- Quick Actions -->
          <div class="bg-white border border-slate-200 rounded overflow-hidden">
            <div class="px-6 py-4 border-b border-slate-100">
              <h4 class="font-semibold text-sm" style="color:#1e293b">Quick Actions</h4>
            </div>
            <div class="p-4 space-y-2">
              <router-link v-if="canAdmitStudents" to="/office"
                class="flex items-center gap-3 px-4 py-3 rounded border transition-all hover:shadow-sm active:scale-[0.99]"
                style="border-color:#e2e8f0">
                <div class="w-9 h-9 rounded flex items-center justify-center shrink-0" style="background:rgba(113,46,221,0.1)">
                  <span class="material-symbols-outlined" style="color:#712edd;font-size:18px">person_add</span>
                </div>
                <div>
                  <p class="text-sm font-medium" style="color:#1e293b">Add Student</p>
                  <p class="text-xs" style="color:#94a3b8">New enrollment</p>
                </div>
              </router-link>

              <router-link v-if="canRecordPayments" to="/finance"
                class="flex items-center gap-3 px-4 py-3 rounded border transition-all hover:shadow-sm active:scale-[0.99]"
                style="border-color:#e2e8f0">
                <div class="w-9 h-9 rounded flex items-center justify-center shrink-0" style="background:#f0fdf4">
                  <span class="material-symbols-outlined" style="color:#16a34a;font-size:18px">payments</span>
                </div>
                <div>
                  <p class="text-sm font-medium" style="color:#1e293b">Record Payment</p>
                  <p class="text-xs" style="color:#94a3b8">Log fee collection</p>
                </div>
              </router-link>

              <router-link v-if="canMarkAttendance" to="/academics/attendance"
                class="flex items-center gap-3 px-4 py-3 rounded border transition-all hover:shadow-sm active:scale-[0.99]"
                style="border-color:#e2e8f0">
                <div class="w-9 h-9 rounded flex items-center justify-center shrink-0" style="background:#eff6ff">
                  <span class="material-symbols-outlined" style="color:#2563eb;font-size:18px">how_to_reg</span>
                </div>
                <div>
                  <p class="text-sm font-medium" style="color:#1e293b">Mark Attendance</p>
                  <p class="text-xs" style="color:#94a3b8">Daily roll call</p>
                </div>
              </router-link>

              <router-link v-if="canEnterGrades" to="/academics"
                class="flex items-center gap-3 px-4 py-3 rounded border transition-all hover:shadow-sm active:scale-[0.99]"
                style="border-color:#e2e8f0">
                <div class="w-9 h-9 rounded flex items-center justify-center shrink-0" style="background:#fef3c7">
                  <span class="material-symbols-outlined" style="color:#d97706;font-size:18px">grade</span>
                </div>
                <div>
                  <p class="text-sm font-medium" style="color:#1e293b">Enter Grades</p>
                  <p class="text-xs" style="color:#94a3b8">CBC assessments</p>
                </div>
              </router-link>
            </div>
          </div>

          <!-- Term Fee Progress (finance roles) -->
          <div v-if="canViewFinance" class="bg-white border border-slate-200 rounded p-5">
            <p class="text-xs font-semibold uppercase tracking-wider mb-1" style="color:#64748b">{{ appStore.currentTerm }} Collections</p>
            <p class="text-xl font-bold mb-3" style="color:#1e293b">{{ formatCurrency(termCollected) }}</p>
            <div class="w-full bg-slate-100 rounded-full h-2 mb-2">
              <div class="h-2 rounded-full transition-all duration-1000"
                :class="termPct >= 80 ? 'bg-emerald-500' : termPct >= 50 ? 'bg-amber-400' : 'bg-red-500'"
                :style="{ width: Math.min(termPct, 100) + '%' }"></div>
            </div>
            <div class="flex items-center justify-between">
              <p class="text-xs" style="color:#94a3b8">{{ defaultersCount }} with outstanding fees</p>
              <span class="text-sm font-bold" :class="termPct >= 80 ? 'text-emerald-600' : termPct >= 50 ? 'text-amber-500' : 'text-red-500'">{{ termPct }}%</span>
            </div>
            <router-link to="/finance" class="mt-3 flex items-center gap-1 text-xs font-semibold hover:underline" style="color:#712edd">
              View Finance <span class="material-symbols-outlined" style="font-size:14px">arrow_forward</span>
            </router-link>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'
import { apiFetch } from '@/services/api'
import { useCounter } from '@/composables/useCounter'
import SkeletonLoader from '@/components/ui/SkeletonLoader.vue'
import StatCard from '@/components/ui/StatCard.vue'

const authStore = useAuthStore()
const appStore = useAppStore()

const userName = computed(() => authStore.user?.name || 'User')

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})
const userRole = computed(() => authStore.user?.role || '')

// RBAC helpers
const canViewFinance   = computed(() => ['admin', 'principal', 'accountant'].includes(userRole.value))
const canViewHR        = computed(() => ['admin', 'principal'].includes(userRole.value))
const canMarkAttendance = computed(() => ['admin', 'principal', 'teacher', 'secretary'].includes(userRole.value))
const canRecordPayments = computed(() => ['admin', 'principal', 'accountant', 'secretary'].includes(userRole.value))
const canEnterGrades   = computed(() => ['admin', 'principal', 'teacher'].includes(userRole.value))
const canAdmitStudents = computed(() => ['admin', 'principal', 'secretary'].includes(userRole.value))

// Activity feed resource visibility per role
const ROLE_RESOURCES = {
  admin:      null,  // null = show all
  principal:  null,
  accountant: ['fee', 'payroll', 'expense', 'student'],
  teacher:    ['attendance', 'assessment', 'student'],
  secretary:  ['student', 'attendance'],
}

const loading = ref(true)
const loadError = ref(null)
const totalStudents = ref(0)
const totalRevenue = ref(0)
const totalStaff = ref(0)
const todayAttendancePct = ref(null)

// Animated display counters
const displayStudents   = useCounter(totalStudents)
const displayRevenue    = useCounter(totalRevenue)
const displayStaff      = useCounter(totalStaff)
const displayAttendance = useCounter(computed(() => todayAttendancePct.value ?? 0), 700, 1)
const termCollected = ref(0)
const termExpected = ref(0)
const termPct = ref(0)
const defaultersCount = ref(0)
const recentActivity = ref([])
let refreshTimer = null

const RESOURCE_STYLE = {
  student:    { avatar: 'bg-warning-bg text-warning',      dot: 'bg-warning' },
  fee:        { avatar: 'bg-success-bg text-success',      dot: 'bg-success' },
  assessment: { avatar: 'bg-info-bg text-info',      dot: 'bg-info' },
  attendance: { avatar: 'bg-info-bg text-info',      dot: 'bg-info' },
  staff:      { avatar: 'bg-[rgba(109,40,217,0.12)] text-school-purple', dot: 'bg-school-purple' },
  payroll:    { avatar: 'bg-success-bg text-success',      dot: 'bg-success' },
  expense:    { avatar: 'bg-[rgba(109,40,217,0.12)] text-school-purple', dot: 'bg-school-purple' },
}

const ACTION_LABELS = { CREATE: 'created', UPDATE: 'updated', DELETE: 'deleted' }

function formatRelativeTime(isoString) {
  if (!isoString) return ''
  const diff = Math.floor((Date.now() - new Date(isoString)) / 1000)
  if (diff < 60) return `${diff}s ago`
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}

function formatCurrency(amount) {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    maximumFractionDigits: 0,
  }).format(amount)
}

const filteredActivity = computed(() => {
  const allowed = ROLE_RESOURCES[userRole.value]
  if (!allowed) return recentActivity.value
  return recentActivity.value.filter(a => allowed.includes(a.type))
})

async function loadStats() {
  try {
    const term = encodeURIComponent(appStore.currentTerm)
    const stats = await apiFetch(`/api/dashboard/stats?term=${term}`)
    loadError.value          = null
    totalStudents.value      = stats.total_students
    totalStaff.value         = stats.total_staff
    totalRevenue.value       = stats.total_revenue
    todayAttendancePct.value = stats.today_attendance_pct ?? null
    termCollected.value      = stats.term_collected ?? 0
    termExpected.value       = stats.term_expected ?? 0
    termPct.value            = stats.term_pct ?? 0
    defaultersCount.value    = stats.defaulters_count ?? 0

    recentActivity.value = (stats.recent_activity || []).map((log) => {
      const style = RESOURCE_STYLE[log.resource] || RESOURCE_STYLE.staff
      return {
        id:          log.id,
        type:        log.resource,
        user:        log.user_name || 'System',
        action:      log.description || `${ACTION_LABELS[log.action] || log.action} a ${log.resource} record`,
        time:        formatRelativeTime(log.timestamp),
        avatarClass: style.avatar,
        dotClass:    style.dot,
      }
    })
  } catch (error) {
    console.error('Failed to load dashboard analytics', error)
    loadError.value = error?.message || 'Unable to reach the server. Please check your connection.'
  } finally {
    loading.value = false
  }
}

function retryLoad() {
  loading.value = true
  loadError.value = null
  loadStats()
}

onMounted(() => {
  loadStats()
  refreshTimer = setInterval(loadStats, 30_000)
})

onUnmounted(() => {
  clearInterval(refreshTimer)
})
</script>
