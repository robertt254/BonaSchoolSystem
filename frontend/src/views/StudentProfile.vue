<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
    <!-- Back -->
    <button
      @click="$router.back()"
      class="text-sm font-bold text-school-navy bg-slate-100 hover:bg-slate-200 px-5 py-2.5 rounded-lg transition-colors"
    >
      &larr; Back
    </button>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center py-20 text-slate-400 space-y-4">
      <div class="w-8 h-8 border-4 border-border border-t-school-navy rounded-full animate-spin"></div>
      <span class="text-xs font-bold tracking-widest uppercase">Loading Profile...</span>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-6 rounded-xl text-sm font-medium">
      {{ error }}
    </div>

    <template v-else-if="profile">
      <!-- Profile header card -->
      <div class="bg-white rounded-lg border border-border p-6 flex flex-col sm:flex-row sm:items-center gap-6 relative overflow-hidden">
        <div class="absolute right-0 top-0 w-32 h-32 rounded-bl-full -mr-8 -mt-8 pointer-events-none"
          :class="profile.student.gender === 'Female' ? 'bg-pink-50' : 'bg-blue-50'"></div>
        <div class="w-20 h-20 rounded-full flex items-center justify-center font-bold text-2xl border-2 border-white shadow-sm z-10 shrink-0"
          :class="profile.student.gender === 'Female' ? 'bg-pink-100 text-pink-500' : profile.student.gender === 'Male' ? 'bg-blue-100 text-blue-600' : 'bg-slate-100 text-slate-500'">
          {{ profile.student.first_name.charAt(0) }}{{ profile.student.last_name.charAt(0) }}
        </div>
        <div class="z-10 flex-1">
          <div class="flex items-center gap-3 mb-1 flex-wrap">
            <h2 class="text-2xl font-extrabold text-slate-800">
              {{ profile.student.first_name }} {{ profile.student.last_name }}
            </h2>
            <span
              class="px-2.5 py-0.5 text-xs font-bold uppercase tracking-wider rounded-full border"
              :class="profile.student.status === 'Active'
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                : 'bg-slate-50 text-slate-500 border-slate-200'"
            >{{ profile.student.status }}</span>
            <span v-if="profile.student.gender"
              class="px-2.5 py-0.5 text-xs font-bold uppercase tracking-wider rounded-full"
              :class="profile.student.gender === 'Female' ? 'bg-pink-50 text-pink-600' : 'bg-blue-50 text-blue-600'">
              {{ profile.student.gender }}
            </span>
            <!-- Deactivate (Transfer) — only for active students, authorised roles -->
            <button
              v-if="profile.student.status === 'Active' && canDeactivate"
              @click="showDeactivateModal = true"
              class="ml-auto px-4 py-1.5 text-xs font-bold text-amber-700 bg-amber-50 border border-amber-200 rounded-lg hover:bg-amber-100 transition-colors"
            >
              Deactivate (Transfer)
            </button>
          </div>
          <div class="text-slate-500 text-sm flex flex-wrap gap-x-5 gap-y-1.5 mt-1">
            <span>Grade: <strong class="text-slate-700">{{ profile.student.grade_level }}</strong></span>
            <span>Adm No: <strong class="text-slate-700 font-mono">{{ profile.student.admission_number }}</strong></span>
            <span v-if="profile.student.date_of_birth">
              DOB: <strong class="text-slate-700">{{ formatDate(profile.student.date_of_birth) }}</strong>
              <span class="text-slate-400 ml-1">({{ calcAge(profile.student.date_of_birth) }}y)</span>
            </span>
            <span v-if="profile.student.guardian_name">
              Guardian: <strong class="text-slate-700">{{ profile.student.guardian_name }}</strong>
              <span v-if="profile.student.guardian_phone"> · {{ profile.student.guardian_phone }}</span>
            </span>
          </div>
        </div>
      </div>

      <!-- Quick metrics -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="bg-white rounded-lg border border-border p-6">
          <div class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Attendance</div>
          <div class="text-2xl font-extrabold text-school-navy">{{ profile.attendance_percentage }}%</div>
          <div class="text-xs text-slate-400 mt-1">{{ profile.days_present }}/{{ profile.total_days }} days</div>
        </div>
        <div class="bg-white rounded-lg border border-border p-6">
          <div class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Fee Balance</div>
          <div class="text-2xl font-extrabold" :class="profile.fee_balance > 0 ? 'text-school-red' : 'text-emerald-600'">
            {{ formatCurrency(profile.fee_balance) }}
          </div>
          <div class="text-xs text-slate-400 mt-1">Paid {{ formatCurrency(profile.total_paid) }} this year</div>
        </div>
        <div class="bg-white rounded-lg border border-border p-6">
          <div class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Subjects</div>
          <div class="text-2xl font-extrabold text-slate-800">{{ uniqueSubjects }}</div>
          <div class="text-xs text-slate-400 mt-1">Learning areas assessed</div>
        </div>
        <div class="bg-white rounded-lg border border-border p-6">
          <div class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Payments</div>
          <div class="text-2xl font-extrabold text-slate-800">{{ profile.recent_payments.length }}</div>
          <div class="text-xs text-slate-400 mt-1">Recent transactions</div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="bg-white rounded-lg border border-border overflow-hidden">
        <div class="flex border-b border-border">
          <button
            v-for="t in tabs"
            :key="t.id"
            @click="activeTab = t.id"
            class="px-6 py-4 text-sm font-semibold transition-colors"
            :class="activeTab === t.id
              ? 'border-b-2 border-school-purple text-school-purple'
              : 'text-slate-500 hover:text-slate-700'"
          >
            {{ t.label }}
          </button>
        </div>

        <!-- Tab: Personal Info -->
        <div v-if="activeTab === 'info'" class="p-6">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-8">
            <!-- Student Details -->
            <div>
              <h4 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4">Student Details</h4>
              <dl class="space-y-0">
                <div v-for="(item, i) in [
                  { label: 'Full Name', value: profile.student.first_name + ' ' + profile.student.last_name },
                  { label: 'Admission No.', value: profile.student.admission_number, mono: true },
                  { label: 'Grade Level', value: profile.student.grade_level },
                  { label: 'Status', value: profile.student.status, badge: true },
                  { label: 'Gender', value: profile.student.gender, genderBadge: true },
                  { label: 'Date of Birth', value: profile.student.date_of_birth ? formatDate(profile.student.date_of_birth) + ' (' + calcAge(profile.student.date_of_birth) + 'y)' : null },
                  { label: 'Home Address', value: profile.student.address },
                  { label: 'Previous School', value: profile.student.previous_school },
                ]" :key="i" class="flex items-center justify-between py-2.5 border-b border-slate-50 last:border-0">
                  <dt class="text-sm text-slate-500">{{ item.label }}</dt>
                  <dd class="text-sm text-right max-w-[60%]">
                    <span v-if="item.badge"
                      class="px-2 py-0.5 text-xs font-bold uppercase rounded-full"
                      :class="item.value === 'Active' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-500'">
                      {{ item.value || '—' }}
                    </span>
                    <span v-else-if="item.genderBadge && item.value"
                      class="px-2 py-0.5 text-xs font-bold uppercase rounded-full"
                      :class="item.value === 'Female' ? 'bg-pink-50 text-pink-600' : 'bg-blue-50 text-blue-600'">
                      {{ item.value }}
                    </span>
                    <span v-else-if="item.mono && item.value" class="font-mono font-semibold text-school-navy">{{ item.value }}</span>
                    <span v-else class="font-semibold text-slate-800">{{ item.value || '—' }}</span>
                  </dd>
                </div>
              </dl>
            </div>
            <!-- Guardian Details -->
            <div>
              <h4 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4">Guardian / Parent Details</h4>
              <dl class="space-y-0">
                <div v-for="(item, i) in [
                  { label: 'Primary Guardian', value: profile.student.guardian_name },
                  { label: 'Primary Phone', value: profile.student.guardian_phone },
                  { label: 'Second Guardian', value: profile.student.guardian2_name },
                  { label: 'Second Phone', value: profile.student.guardian2_phone },
                ]" :key="i" class="flex items-center justify-between py-2.5 border-b border-slate-50 last:border-0">
                  <dt class="text-sm text-slate-500">{{ item.label }}</dt>
                  <dd class="text-sm font-semibold text-slate-800">{{ item.value || '—' }}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>

        <!-- Tab: Assessments -->
        <div v-if="activeTab === 'assessments'">
          <div v-if="!groupedAssessments.length" class="py-10 text-center text-slate-400 text-sm">
            No assessments recorded yet.
          </div>
          <div v-for="([term, items]) in groupedAssessments" :key="term">
            <div class="px-6 py-2.5 bg-slate-50 border-y border-border text-xs font-bold uppercase tracking-widest text-slate-400">
              {{ term }}
            </div>
            <table class="w-full text-left border-collapse">
              <tbody class="text-sm">
                <tr v-for="a in items" :key="a.id" class="border-b border-slate-50 hover:bg-slate-50/50">
                  <td class="py-3.5 px-6 font-semibold text-slate-800 w-2/5">{{ a.learning_area }}</td>
                  <td class="py-3.5 px-6 w-24">
                    <span class="px-2.5 py-0.5 rounded-full text-xs font-bold" :class="scoreClass(a.score)">{{ a.score }}</span>
                  </td>
                  <td class="py-3.5 px-6 text-slate-400 text-xs">{{ a.remarks || '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Tab: Fee Payments -->
        <div v-if="activeTab === 'fees'" class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-border">
                <th class="py-4 px-6">Receipt</th>
                <th class="py-4 px-6">Date</th>
                <th class="py-4 px-6">Term</th>
                <th class="py-4 px-6">Type</th>
                <th class="py-4 px-6 text-right">Amount</th>
                <th class="py-4 px-6">Recorded By</th>
              </tr>
            </thead>
            <tbody class="text-sm">
              <tr
                v-for="p in profile.recent_payments"
                :key="p.id"
                class="border-b border-slate-50 hover:bg-slate-50/50"
              >
                <td class="py-4 px-6 font-mono text-xs text-school-navy font-semibold">{{ p.receipt_number || '—' }}</td>
                <td class="py-4 px-6 text-slate-500">{{ formatDate(p.payment_date) }}</td>
                <td class="py-4 px-6 text-slate-600">{{ p.term }}</td>
                <td class="py-4 px-6 text-slate-600">{{ p.payment_type }}</td>
                <td class="py-4 px-6 text-right font-bold text-emerald-700">{{ formatCurrency(p.amount) }}</td>
                <td class="py-4 px-6 text-slate-400 text-xs">{{ p.recorded_by }}</td>
              </tr>
              <tr v-if="!profile.recent_payments.length">
                <td colspan="6" class="py-10 text-center text-slate-400 text-sm">No payments recorded yet.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Tab: Attendance -->
        <div v-if="activeTab === 'attendance'" class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-border">
                <th class="py-4 px-6">Date</th>
                <th class="py-4 px-6">Status</th>
                <th class="py-4 px-6">Remarks</th>
              </tr>
            </thead>
            <tbody class="text-sm">
              <tr
                v-for="r in attendanceRecords"
                :key="r.date"
                class="border-b border-slate-50 hover:bg-slate-50/50"
              >
                <td class="py-4 px-6 font-medium text-slate-700">{{ r.date }}</td>
                <td class="py-4 px-6">
                  <span
                    class="px-2.5 py-0.5 rounded-full text-xs font-bold"
                    :class="r.is_present ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-600'"
                  >{{ r.is_present ? 'Present' : 'Absent' }}</span>
                </td>
                <td class="py-4 px-6 text-slate-400 text-xs">{{ r.remarks || '—' }}</td>
              </tr>
              <tr v-if="!attendanceRecords.length">
                <td colspan="3" class="py-10 text-center text-slate-400 text-sm">No attendance records found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <!-- Deactivate confirmation modal -->
    <div v-if="showDeactivateModal" class="fixed inset-0 bg-slate-900/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-2xl border border-border w-full max-w-md overflow-hidden">
        <div class="p-6 border-b border-slate-100 bg-amber-50 flex items-start gap-3">
          <svg class="w-5 h-5 text-amber-600 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
          </svg>
          <div>
            <h3 class="text-sm font-bold text-amber-800">Deactivate Student</h3>
            <p class="text-xs text-amber-700 mt-0.5">This will mark the student as Transferred. All records (fees, assessments, attendance) are preserved.</p>
          </div>
        </div>
        <div class="p-6 space-y-3">
          <p class="text-sm text-slate-700">
            You are about to deactivate <strong>{{ profile?.student.first_name }} {{ profile?.student.last_name }}</strong>.
          </p>
          <div v-if="profile?.fee_balance > 0" class="bg-red-50 border border-red-200 rounded-lg p-3 text-xs text-red-700 font-medium">
            Outstanding balance of {{ formatCurrency(profile.fee_balance) }} must be cleared before deactivation.
          </div>
          <p class="text-xs text-slate-500">This action cannot be undone from this screen. Contact an admin to reactivate.</p>
        </div>
        <div class="flex justify-end gap-3 px-6 pb-6">
          <button @click="showDeactivateModal = false"
            class="px-5 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors">
            Cancel
          </button>
          <button
            @click="deactivateStudent"
            :disabled="deactivating || (profile?.fee_balance ?? 0) > 0"
            class="px-5 py-2.5 text-sm font-bold bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition-colors disabled:opacity-50">
            {{ deactivating ? 'Deactivating…' : 'Confirm Deactivation' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiFetch } from '@/services/api'
import studentService from '@/services/studentService'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const route = useRoute()
const authStore = useAuthStore()
const toast = useToast()

const loading = ref(true)
const error = ref(null)
const profile = ref(null)
const attendanceRecords = ref([])
const activeTab = ref('info')
const showDeactivateModal = ref(false)
const deactivating = ref(false)

const canDeactivate = computed(() =>
  ['admin', 'principal', 'secretary'].includes(authStore.user?.role)
)

const tabs = [
  { id: 'info',        label: 'Personal Info'  },
  { id: 'assessments', label: 'CBC Assessments' },
  { id: 'fees',        label: 'Fee Payments'   },
  { id: 'attendance',  label: 'Attendance'     },
]

const uniqueSubjects = computed(() =>
  new Set((profile.value?.assessments || []).map(a => a.learning_area)).size
)

const groupedAssessments = computed(() => {
  const groups = {}
  for (const a of profile.value?.assessments || []) {
    if (!groups[a.term]) groups[a.term] = []
    groups[a.term].push(a)
  }
  return Object.entries(groups).sort((a, b) => a[0].localeCompare(b[0]))
})

const calcAge = (dob) => Math.floor((Date.now() - new Date(dob).getTime()) / (1000 * 60 * 60 * 24 * 365.25))

const scoreClass = (score) => ({
  EE: 'bg-emerald-50 text-emerald-700',
  ME: 'bg-blue-50 text-blue-700',
  AE: 'bg-amber-50 text-amber-700',
  BE: 'bg-red-50 text-red-600',
}[score] || 'bg-slate-100 text-slate-600')

const formatCurrency = (amount) =>
  new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 }).format(amount)

const formatDate = (iso) => new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })

async function loadProfile() {
  const id = route.params.id
  try {
    const [prof, att] = await Promise.all([
      studentService.getStudentProfile(id),
      apiFetch(`/api/attendance/student/${id}`).catch(() => ({ records: [] })),
    ])
    profile.value = prof
    attendanceRecords.value = att.records || []
  } catch (err) {
    error.value = err.message || 'Failed to load student profile.'
  } finally {
    loading.value = false
  }
}

async function deactivateStudent() {
  if (!profile.value) return
  deactivating.value = true
  try {
    const res = await apiFetch(`/api/students/${profile.value.student.id}/deactivate`, { method: 'PATCH' })
    toast.success(res.message || 'Student deactivated successfully.')
    showDeactivateModal.value = false
    await loadProfile()
  } catch (err) {
    toast.error(err.message || 'Deactivation failed.')
  } finally {
    deactivating.value = false
  }
}

onMounted(loadProfile)
</script>
