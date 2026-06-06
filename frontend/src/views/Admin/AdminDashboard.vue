<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="font-heading text-2xl font-bold text-text-primary tracking-tight">
        Administrator Dashboard
      </h1>
      <p class="text-sm text-text-muted mt-1">System overview, user activity, and live metrics.</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col justify-center items-center py-20 text-slate-400 space-y-4">
      <div class="w-8 h-8 border-4 border-border border-t-school-navy rounded-full animate-spin"></div>
      <span class="text-xs font-bold tracking-widest uppercase">Loading Dashboard…</span>
    </div>

    <template v-else>
      <!-- Stat Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <!-- Total Students -->
        <div class="bg-white p-6 rounded-lg border border-border hover:shadow-md transition-shadow relative overflow-hidden group">
          <div class="absolute right-0 top-0 w-20 h-20 bg-blue-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"></div>
          <div class="flex justify-between items-start relative z-10">
            <div>
              <div class="text-xs font-bold uppercase tracking-[0.07em] text-text-muted mb-1">Total Students</div>
              <div class="text-3xl font-extrabold text-slate-800">{{ stats.total_students }}</div>
            </div>
            <div class="p-2.5 bg-blue-100/50 text-blue-600 rounded-xl">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
              </svg>
            </div>
          </div>
          <div class="mt-3 text-xs text-slate-400 relative z-10">Active across all grades</div>
        </div>

        <!-- Active Staff -->
        <div class="bg-white p-6 rounded-lg border border-border hover:shadow-md transition-shadow relative overflow-hidden group">
          <div class="absolute right-0 top-0 w-20 h-20 bg-violet-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"></div>
          <div class="flex justify-between items-start relative z-10">
            <div>
              <div class="text-xs font-bold uppercase tracking-[0.07em] text-text-muted mb-1">Active Staff</div>
              <div class="text-3xl font-extrabold text-slate-800">{{ stats.total_staff }}</div>
            </div>
            <div class="p-2.5 bg-violet-100/50 text-school-purple rounded-xl">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
            </div>
          </div>
          <div class="mt-3 text-xs text-slate-400 relative z-10">Teachers &amp; administration</div>
        </div>

        <!-- Total Revenue -->
        <div class="bg-white p-6 rounded-lg border border-border hover:shadow-md transition-shadow relative overflow-hidden group">
          <div class="absolute right-0 top-0 w-20 h-20 bg-emerald-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"></div>
          <div class="flex justify-between items-start relative z-10">
            <div>
              <div class="text-xs font-bold uppercase tracking-[0.07em] text-text-muted mb-1">Total Revenue</div>
              <div class="text-2xl font-extrabold text-emerald-600">{{ formatCurrency(stats.total_revenue) }}</div>
            </div>
            <div class="p-2.5 bg-emerald-100/50 text-emerald-600 rounded-xl">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>
              </svg>
            </div>
          </div>
          <div class="mt-3 text-xs text-slate-400 relative z-10">Cumulative fee payments</div>
        </div>

        <!-- System Status -->
        <div class="bg-white p-6 rounded-lg border border-border hover:shadow-md transition-shadow relative overflow-hidden group">
          <div class="absolute right-0 top-0 w-20 h-20 bg-emerald-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"></div>
          <div class="flex justify-between items-start relative z-10">
            <div>
              <div class="text-xs font-bold uppercase tracking-[0.07em] text-text-muted mb-1">System Status</div>
              <div class="flex items-center gap-2 mt-2">
                <span class="relative flex h-2.5 w-2.5">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                </span>
                <span class="text-sm font-bold text-emerald-600">Operational</span>
              </div>
            </div>
            <div class="p-2.5 bg-emerald-100/50 text-emerald-600 rounded-xl">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
            </div>
          </div>
          <div class="mt-3 text-xs text-slate-400 relative z-10">Last sync: {{ lastSyncTime }}</div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="bg-white rounded-lg border border-border overflow-hidden">
        <div class="border-b border-slate-100 px-8 py-5 flex items-center justify-between bg-slate-50">
          <div>
            <h3 class="text-lg font-bold text-slate-800 tracking-tight">Recent Activity</h3>
            <p class="text-xs text-slate-500 mt-0.5">Latest actions across all modules</p>
          </div>
          <span class="text-xs font-bold uppercase tracking-widest text-slate-400">Audit Log</span>
        </div>

        <div v-if="recentActivity.length === 0" class="py-16 text-center text-slate-400 text-sm">
          No activity recorded yet.
        </div>

        <div v-else class="divide-y divide-slate-50">
          <div
            v-for="activity in recentActivity"
            :key="activity.id"
            class="flex items-start gap-4 px-8 py-4 hover:bg-slate-50 transition-colors"
          >
            <div
              class="w-9 h-9 rounded-full flex items-center justify-center font-bold text-sm shrink-0 mt-0.5"
              :class="activity.avatarClass"
            >
              {{ activity.user.charAt(0).toUpperCase() }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-text-primary leading-snug">
                <span class="font-semibold">{{ activity.user }}</span>
                <span class="text-text-secondary"> {{ activity.description }}</span>
              </p>
              <p class="text-xs text-text-muted mt-0.5 flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full shrink-0" :class="activity.dotClass"></span>
                {{ activity.time }} · {{ activity.type }}
              </p>
            </div>
            <span
              class="text-xs font-bold uppercase px-2 py-0.5 rounded-full shrink-0 mt-0.5"
              :class="actionBadge(activity.action)"
            >{{ activity.actionLabel }}</span>
          </div>
        </div>
      </div>
      <!-- Danger Zone -->
      <div class="bg-white rounded-lg border-2 border-red-200 overflow-hidden">
        <div class="border-b border-red-100 px-8 py-5 bg-red-50/50">
          <h3 class="text-lg font-bold text-red-700 tracking-tight">Danger Zone</h3>
          <p class="text-xs text-red-500 mt-0.5">Irreversible system maintenance</p>
        </div>
        <div class="px-8 py-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <p class="text-sm font-semibold text-slate-800">Reset system data</p>
            <p class="text-xs text-slate-500 mt-0.5 max-w-md">
              Permanently deletes all students, fee payments, statements, grades, attendance and
              activity logs. Keeps staff logins, fee structure and term dates. Cannot be undone.
            </p>
          </div>
          <button @click="openReset"
            class="shrink-0 bg-red-600 text-white px-5 py-2.5 rounded text-sm font-semibold hover:bg-red-700 transition">
            Reset Data…
          </button>
        </div>
      </div>
    </template>

    <!-- Reset confirmation modal -->
    <div v-if="showReset" class="fixed inset-0 bg-slate-900/50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded shadow-2xl w-full max-w-md overflow-hidden border border-border">
        <div class="px-6 py-5 border-b border-slate-100 bg-red-50">
          <h2 class="text-lg font-bold text-red-700">Reset System Data</h2>
          <p class="text-xs text-red-500 mt-0.5">This permanently deletes operational data and cannot be undone.</p>
        </div>
        <div class="p-6 space-y-4">
          <ul class="text-xs text-slate-600 space-y-1 bg-slate-50 border border-slate-200 rounded p-3">
            <li>• Students (and their grades, attendance, discipline, exam results)</li>
            <li>• Fee payments, carry-forwards &amp; statements</li>
            <li>• Activity / audit logs</li>
            <li class="text-slate-400 pt-1">Kept: staff logins, fee structure, term dates</li>
          </ul>
          <label class="flex items-center gap-2 text-sm text-slate-700">
            <input type="checkbox" v-model="resetWithFinance" class="rounded border-slate-300" />
            Also clear expenses, payroll &amp; petty cash
          </label>
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">
              Type <span class="text-red-600">RESET</span> to confirm
            </label>
            <input v-model="resetConfirm" type="text" placeholder="RESET"
              class="w-full border border-slate-300 rounded px-3 py-2.5 text-sm outline-none focus:ring-2 focus:ring-red-500/30 focus:border-red-500" />
          </div>
        </div>
        <div class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3">
          <button @click="showReset = false" class="px-5 py-2.5 text-slate-600 hover:bg-slate-100 rounded font-semibold text-sm">Cancel</button>
          <button @click="doReset" :disabled="resetConfirm.trim().toUpperCase() !== 'RESET' || resetting"
            class="px-5 py-2.5 bg-red-600 text-white rounded font-semibold text-sm hover:bg-red-700 disabled:opacity-40 transition">
            {{ resetting ? 'Resetting…' : 'Permanently Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiFetch } from '@/services/api'
import { useToast } from '@/composables/useToast'

const toast = useToast()

const loading = ref(true)
const stats = ref({ total_students: 0, total_staff: 0, total_revenue: 0 })
const recentActivity = ref([])
const lastSyncTime = ref('—')

// ── Danger zone: reset system data ────────────────────────────────────────────
const showReset = ref(false)
const resetConfirm = ref('')
const resetWithFinance = ref(false)
const resetting = ref(false)

const openReset = () => {
  resetConfirm.value = ''
  resetWithFinance.value = false
  showReset.value = true
}

const doReset = async () => {
  if (resetConfirm.value.trim().toUpperCase() !== 'RESET') return
  resetting.value = true
  try {
    const res = await apiFetch('/api/admin/reset-data', {
      method: 'POST',
      body: JSON.stringify({ confirm: resetConfirm.value.trim(), with_finance: resetWithFinance.value }),
    })
    const total = Object.values(res.cleared || {}).reduce((a, b) => a + b, 0)
    toast.success(`System data reset — ${total} record(s) cleared.`)
    showReset.value = false
    setTimeout(() => window.location.reload(), 900)
  } catch (e) {
    toast.error(e?.message || 'Reset failed.')
  } finally {
    resetting.value = false
  }
}

const RESOURCE_STYLE = {
  student:    { avatar: 'bg-amber-100 text-amber-700',   dot: 'bg-amber-500' },
  fee:        { avatar: 'bg-emerald-100 text-emerald-700', dot: 'bg-emerald-500' },
  assessment: { avatar: 'bg-blue-100 text-blue-700',    dot: 'bg-blue-500' },
  attendance: { avatar: 'bg-blue-100 text-blue-700',    dot: 'bg-blue-500' },
  staff:      { avatar: 'bg-violet-100 text-violet-700', dot: 'bg-violet-500' },
  payroll:    { avatar: 'bg-emerald-100 text-emerald-700', dot: 'bg-emerald-500' },
  expense:    { avatar: 'bg-red-100 text-red-600',      dot: 'bg-red-500' },
}

const ACTION_MAP = {
  CREATE: { label: 'Created', badge: 'bg-emerald-50 text-emerald-700' },
  UPDATE: { label: 'Updated', badge: 'bg-blue-50 text-blue-700' },
  DELETE: { label: 'Deleted', badge: 'bg-red-50 text-red-600' },
}

const actionBadge = (action) => ACTION_MAP[action]?.badge || 'bg-slate-100 text-slate-500'

function formatRelativeTime(iso) {
  if (!iso) return ''
  const diff = Math.floor((Date.now() - new Date(iso)) / 1000)
  if (diff < 60) return `${diff}s ago`
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}

const formatCurrency = (v) =>
  new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 }).format(v)

onMounted(async () => {
  try {
    const data = await apiFetch('/api/dashboard/stats')
    stats.value = data
    lastSyncTime.value = new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })

    recentActivity.value = (data.recent_activity || []).map((log) => {
      const style = RESOURCE_STYLE[log.resource] || RESOURCE_STYLE.staff
      const am = ACTION_MAP[log.action] || { label: log.action }
      return {
        id:          log.id,
        type:        log.resource,
        user:        log.user_name || 'System',
        description: log.description || `${am.label?.toLowerCase()} a ${log.resource} record`,
        action:      log.action,
        actionLabel: am.label,
        avatarClass: style.avatar,
        dotClass:    style.dot,
        time:        formatRelativeTime(log.timestamp),
      }
    })
  } catch (err) {
    console.error('Admin dashboard load failed', err)
  } finally {
    loading.value = false
  }
})
</script>
