<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Welcome Banner -->
    <div class="relative bg-sidebar rounded-2xl px-7 py-6 overflow-hidden flex flex-col sm:flex-row items-center justify-between shadow-card animate-slide-in">
      <!-- Subtle dot grid -->
      <div class="pointer-events-none absolute inset-0 bg-[radial-gradient(rgba(255,255,255,0.04)_1px,transparent_1px)] bg-[length:22px_22px]" />
      <!-- Brand accent glow -->
      <div class="pointer-events-none absolute -top-12 -right-8 w-48 h-48 rounded-full bg-brand/20 blur-3xl" />

      <div class="relative z-10 text-left w-full sm:w-auto">
        <p class="text-xs font-bold uppercase tracking-widest text-white/40 mb-2">
          {{ greeting }}, {{ userName }}
        </p>
        <h1 class="font-heading text-3xl font-extrabold text-white leading-tight mb-1.5">
          Welcome to The Bona School
        </h1>
        <p class="text-sm text-white/50 max-w-sm leading-relaxed">
          CBC Management System — {{ appStore.currentTerm }} is active.
        </p>
        <router-link to="/academics/timetable"
          class="mt-4 inline-flex items-center gap-2 bg-white/10 border border-white/10 text-white/75 text-xs font-semibold px-5 py-2.5 rounded-card hover:bg-white/15 hover:text-white transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
            <line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
          </svg>
          View term schedule
        </router-link>
      </div>

      <div class="relative z-10 hidden lg:flex">
        <div class="w-20 h-20 rounded-full bg-white/5 border border-white/10 flex items-center justify-center">
          <svg class="w-9 h-9 text-white/60" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
            <path d="M6 12v5c3 3 9 3 12 0v-5"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- Skeleton loading state -->
    <div v-if="loading" class="space-y-4">
      <SkeletonLoader type="stats" :count="4" />
      <div class="bg-surface border border-border rounded-card p-6">
        <div class="skel h-3 w-40 mb-3" />
        <div class="skel h-2 w-full" />
      </div>
    </div>

    <!-- Error Banner -->
    <div
      v-else-if="loadError"
      class="bg-red-50 border border-red-200 rounded-xl p-5 flex items-center justify-between"
    >
      <div class="flex items-center gap-3">
        <svg class="w-5 h-5 text-red-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <div>
          <p class="text-sm font-semibold text-red-700">Failed to load dashboard data</p>
          <p class="text-xs text-red-500 mt-0.5">{{ loadError }}</p>
        </div>
      </div>
      <button
        @click="retryLoad"
        class="text-xs font-semibold text-red-600 border border-red-300 px-4 py-2 rounded-lg hover:bg-red-100 transition-colors"
      >
        Retry
      </button>
    </div>

    <div v-else class="space-y-4">
      <!-- Stats Grid -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total Enrolled" :value="displayStudents" sub="Across all grades" accent="blue" animation="slideIn 0.4s 0.06s ease both">
          <template #icon>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
          </template>
        </StatCard>

        <StatCard v-if="canViewFinance" label="Total Revenue" :value="formatCurrency(displayRevenue)" sub="Historical payments" accent="green" animation="slideIn 0.4s 0.14s ease both">
          <template #icon>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>
            </svg>
          </template>
        </StatCard>

        <StatCard v-if="canViewHR" label="Active Staff" :value="displayStaff" sub="Teachers & admin" accent="purple" animation="slideIn 0.4s 0.22s ease both">
          <template #icon>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
          </template>
        </StatCard>

        <StatCard label="Today's Attendance" :value="todayAttendancePct !== null ? displayAttendance + '%' : '—'" :sub="todayAttendancePct !== null ? 'Students present' : 'Not marked yet'" accent="amber" animation="slideIn 0.4s 0.30s ease both">
          <template #icon>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
            </svg>
          </template>
        </StatCard>
      </div>

      <!-- Term Fee Collection Progress — finance roles only -->
      <div
        v-if="canViewFinance"
        class="bg-white border border-slate-200 rounded-xl p-6"
        style="animation: slideIn 0.4s 0.14s ease both"
      >
        <div class="flex items-center justify-between mb-4">
          <div>
            <p class="text-xs font-bold uppercase tracking-[0.07em] text-text-muted">{{ appStore.currentTerm }} Fee Collection</p>
            <h3 class="font-heading text-2xl font-extrabold text-slate-800 mt-0.5">{{ formatCurrency(termCollected) }}</h3>
          </div>
          <div class="text-right">
            <div class="text-2xl font-extrabold"
              :class="termPct >= 80 ? 'text-emerald-600' : termPct >= 50 ? 'text-amber-500' : 'text-school-red'">
              {{ termPct }}%
            </div>
            <div class="text-xs text-text-muted">Target: {{ formatCurrency(termExpected) }}</div>
          </div>
        </div>
        <div class="w-full bg-slate-100 rounded-full h-2 mb-3">
          <div
            class="h-2 rounded-full transition-all duration-1000"
            :class="termPct >= 80 ? 'bg-emerald-500' : termPct >= 50 ? 'bg-amber-400' : 'bg-school-red'"
            :style="{ width: Math.min(termPct, 100) + '%' }"
          ></div>
        </div>
        <div class="flex items-center justify-between text-xs text-text-muted">
          <span>{{ defaultersCount }} student{{ defaultersCount !== 1 ? 's' : '' }} with outstanding balance</span>
          <router-link to="/finance" class="font-semibold text-school-purple hover:text-school-purple-l transition-colors">View Finance →</router-link>
        </div>
      </div>

      <!-- Two-Column Section -->
      <div
        class="grid grid-cols-1 lg:grid-cols-2 gap-4"
        style="animation: slideIn 0.4s 0.18s ease both"
      >
        <!-- Quick Actions Panel -->
        <div class="bg-white border border-border rounded-xl overflow-hidden">
          <div class="flex items-center justify-between px-5 py-4 border-b border-slate-100">
            <div>
              <h3 class="font-heading text-sm font-bold text-text-primary">Quick Actions</h3>
              <p class="text-xs text-text-muted mt-[1px]">Common tasks and shortcuts</p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4 p-4">
            <!-- Roll Call — teachers, secretary, principal, admin -->
            <router-link
              v-if="canMarkAttendance"
              to="/academics/attendance"
              class="flex items-center gap-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200 cursor-pointer transition-all duration-150 hover:bg-white hover:border-school-purple/30 hover:shadow-sm"
            >
              <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-[rgba(109,40,217,0.12)] text-school-purple">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                  <path d="M9 11l3 3L22 4" />
                  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-semibold text-text-primary leading-tight">Roll Call</p>
                <p class="text-xs text-text-muted mt-[1px]">Mark attendance</p>
              </div>
            </router-link>

            <!-- Log Payment — accountant, secretary, principal, admin -->
            <router-link
              v-if="canRecordPayments"
              to="/finance"
              class="flex items-center gap-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200 cursor-pointer transition-all duration-150 hover:bg-white hover:border-school-purple/30 hover:shadow-sm"
            >
              <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-success-bg text-success">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                  <rect x="2" y="5" width="20" height="14" rx="2" />
                  <line x1="2" y1="10" x2="22" y2="10" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-semibold text-text-primary leading-tight">Log Payment</p>
                <p class="text-xs text-text-muted mt-[1px]">Record fees</p>
              </div>
            </router-link>

            <!-- Enter Grades — teachers, principal, admin -->
            <router-link
              v-if="canEnterGrades"
              to="/academics"
              class="flex items-center gap-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200 cursor-pointer transition-all duration-150 hover:bg-white hover:border-school-purple/30 hover:shadow-sm"
            >
              <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-info-bg text-info">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-semibold text-text-primary leading-tight">Enter Grades</p>
                <p class="text-xs text-text-muted mt-[1px]">CBC Assessments</p>
              </div>
            </router-link>

            <!-- Admit Student — secretary, principal, admin -->
            <router-link
              v-if="canAdmitStudents"
              to="/office"
              class="flex items-center gap-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200 cursor-pointer transition-all duration-150 hover:bg-white hover:border-school-purple/30 hover:shadow-sm"
            >
              <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-warning-bg text-warning">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="16" />
                  <line x1="8" y1="12" x2="16" y2="12" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-semibold text-text-primary leading-tight">Admit Student</p>
                <p class="text-xs text-text-muted mt-[1px]">New enrollment</p>
              </div>
            </router-link>

            <!-- Report Cards — teachers, principal, admin -->
            <router-link
              v-if="canEnterGrades"
              to="/academics/report-card"
              class="flex items-center gap-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200 cursor-pointer transition-all duration-150 hover:bg-white hover:border-school-purple/30 hover:shadow-sm"
            >
              <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-[rgba(109,40,217,0.12)] text-school-purple">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-semibold text-text-primary leading-tight">Report Cards</p>
                <p class="text-xs text-text-muted mt-[1px]">Generate PDFs</p>
              </div>
            </router-link>

            <!-- Fee Statements — accountant, principal, admin -->
            <router-link
              v-if="canViewFinance"
              to="/finance/statements"
              class="flex items-center gap-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200 cursor-pointer transition-all duration-150 hover:bg-white hover:border-school-purple/30 hover:shadow-sm"
            >
              <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-info-bg text-info">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                  <line x1="18" y1="20" x2="18" y2="10" />
                  <line x1="12" y1="20" x2="12" y2="4" />
                  <line x1="6" y1="20" x2="6" y2="14" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-semibold text-text-primary leading-tight">Statements</p>
                <p class="text-xs text-text-muted mt-[1px]">Fee balances</p>
              </div>
            </router-link>

            <!-- Bulk SMS — secretary, principal, admin -->
            <router-link
              v-if="canAdmitStudents"
              to="/office/communications"
              class="flex items-center gap-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200 cursor-pointer transition-all duration-150 hover:bg-white hover:border-school-purple/30 hover:shadow-sm"
            >
              <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-success-bg text-success">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-semibold text-text-primary leading-tight">Bulk SMS</p>
                <p class="text-xs text-text-muted mt-[1px]">Notify parents</p>
              </div>
            </router-link>

            <!-- HR Staff — admin, principal -->
            <router-link
              v-if="canViewHR"
              to="/admin/staff"
              class="flex items-center gap-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200 cursor-pointer transition-all duration-150 hover:bg-white hover:border-school-purple/30 hover:shadow-sm"
            >
              <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-[rgba(109,40,217,0.12)] text-school-purple">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" />
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-semibold text-text-primary leading-tight">Staff HR</p>
                <p class="text-xs text-text-muted mt-[1px]">Manage staff</p>
              </div>
            </router-link>
          </div>
        </div>

        <!-- Activity Feed Panel -->
        <div class="bg-white border border-border rounded-xl overflow-hidden">
          <div class="flex items-center justify-between px-5 py-4 border-b border-slate-100">
            <div>
              <h3 class="font-heading text-sm font-bold text-text-primary">Activity Feed</h3>
              <p class="text-xs text-text-muted mt-[1px]">Latest system events</p>
            </div>
          </div>

          <div class="flex flex-col">
            <div
              v-if="filteredActivity.length === 0"
              class="px-5 py-8 text-center text-sm text-text-muted"
            >
              No recent activity
            </div>
            <div
              v-for="activity in filteredActivity"
              :key="activity.id"
              class="flex items-start gap-3 px-5 py-3.5 border-b border-slate-100 last:border-b-0 transition-colors hover:bg-slate-50"
            >
              <div
                class="w-8 h-8 rounded-full flex items-center justify-center font-heading font-bold text-sm flex-shrink-0 mt-[1px]"
                :class="activity.avatarClass"
              >
                {{ activity.user.charAt(0) }}
              </div>

              <div>
                <p class="text-sm font-medium text-text-primary leading-[1.45]">
                  <span class="font-semibold">{{ activity.user }}</span>
                  <span class="font-normal text-text-secondary"> {{ activity.action }}</span>
                </p>
                <p class="text-xs text-text-muted mt-[2px] flex items-center gap-1">
                  <span class="w-[5px] h-[5px] rounded-full" :class="activity.dotClass"></span>
                  {{ activity.time }} &middot; {{ activity.type }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
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
