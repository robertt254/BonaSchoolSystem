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
      <div class="w-8 h-8 border-4 border-[#E2E8F0] border-t-school-navy rounded-full animate-spin"></div>
      <span class="text-xs font-bold tracking-widest uppercase">Loading Profile...</span>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-6 rounded-[12px] text-sm font-medium">
      {{ error }}
    </div>

    <template v-else-if="profile">
      <!-- Profile header card -->
      <div class="bg-white rounded-[12px] border border-[#E2E8F0] p-6 flex flex-col sm:flex-row sm:items-center gap-6 relative overflow-hidden">
        <div class="absolute right-0 top-0 w-32 h-32 bg-blue-50 rounded-bl-full -mr-8 -mt-8 pointer-events-none"></div>
        <div class="w-20 h-20 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 font-bold text-3xl border-2 border-white shadow-sm z-10 shrink-0">
          {{ profile.student.first_name.charAt(0) }}
        </div>
        <div class="z-10 flex-1">
          <div class="flex items-center gap-3 mb-1 flex-wrap">
            <h2 class="text-2xl font-extrabold text-slate-800">
              {{ profile.student.first_name }} {{ profile.student.last_name }}
            </h2>
            <span
              class="px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded-full border"
              :class="profile.student.status === 'Active'
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                : 'bg-slate-50 text-slate-500 border-slate-200'"
            >{{ profile.student.status }}</span>
          </div>
          <div class="text-slate-500 text-sm flex flex-wrap gap-4">
            <span>Grade: <strong class="text-slate-700">{{ profile.student.grade_level }}</strong></span>
            <span>Adm No: <strong class="text-slate-700">{{ profile.student.admission_number }}</strong></span>
            <span v-if="profile.student.guardian_name">
              Guardian: <strong class="text-slate-700">{{ profile.student.guardian_name }}</strong>
              <span v-if="profile.student.guardian_phone"> · {{ profile.student.guardian_phone }}</span>
            </span>
          </div>
        </div>
      </div>

      <!-- Quick metrics -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="bg-white rounded-[12px] border border-[#E2E8F0] p-5">
          <div class="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Attendance</div>
          <div class="text-2xl font-extrabold text-school-navy">{{ profile.attendance_percentage }}%</div>
          <div class="text-xs text-slate-400 mt-1">{{ profile.days_present }}/{{ profile.total_days }} days</div>
        </div>
        <div class="bg-white rounded-[12px] border border-[#E2E8F0] p-5">
          <div class="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Fee Balance</div>
          <div class="text-2xl font-extrabold" :class="profile.fee_balance > 0 ? 'text-school-red' : 'text-emerald-600'">
            {{ formatCurrency(profile.fee_balance) }}
          </div>
          <div class="text-xs text-slate-400 mt-1">Paid {{ formatCurrency(profile.total_paid) }} this year</div>
        </div>
        <div class="bg-white rounded-[12px] border border-[#E2E8F0] p-5">
          <div class="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Subjects</div>
          <div class="text-2xl font-extrabold text-slate-800">{{ uniqueSubjects }}</div>
          <div class="text-xs text-slate-400 mt-1">Learning areas assessed</div>
        </div>
        <div class="bg-white rounded-[12px] border border-[#E2E8F0] p-5">
          <div class="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Payments</div>
          <div class="text-2xl font-extrabold text-slate-800">{{ profile.recent_payments.length }}</div>
          <div class="text-xs text-slate-400 mt-1">Recent transactions</div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="bg-white rounded-[12px] border border-[#E2E8F0] overflow-hidden">
        <div class="flex border-b border-[#E2E8F0]">
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

        <!-- Tab: Assessments -->
        <div v-if="activeTab === 'assessments'" class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 text-[11px] font-bold uppercase tracking-wider text-slate-400 border-b border-[#E2E8F0]">
                <th class="py-4 px-6">Term</th>
                <th class="py-4 px-6">Learning Area</th>
                <th class="py-4 px-6">Score</th>
                <th class="py-4 px-6">Remarks</th>
              </tr>
            </thead>
            <tbody class="text-sm">
              <tr
                v-for="a in profile.assessments"
                :key="a.id"
                class="border-b border-slate-50 hover:bg-slate-50/50"
              >
                <td class="py-4 px-6 text-slate-500 font-medium">{{ a.term }}</td>
                <td class="py-4 px-6 font-semibold text-slate-800">{{ a.learning_area }}</td>
                <td class="py-4 px-6">
                  <span
                    class="px-2.5 py-0.5 rounded-full text-xs font-bold"
                    :class="scoreClass(a.score)"
                  >{{ a.score }}</span>
                </td>
                <td class="py-4 px-6 text-slate-400 text-xs">{{ a.remarks || '—' }}</td>
              </tr>
              <tr v-if="!profile.assessments.length">
                <td colspan="4" class="py-10 text-center text-slate-400 text-sm">No assessments recorded yet.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Tab: Fee Payments -->
        <div v-if="activeTab === 'fees'" class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 text-[11px] font-bold uppercase tracking-wider text-slate-400 border-b border-[#E2E8F0]">
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
              <tr class="bg-slate-50 text-[11px] font-bold uppercase tracking-wider text-slate-400 border-b border-[#E2E8F0]">
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiFetch } from '@/services/api'
import studentService from '@/services/studentService'

const route = useRoute()
const loading = ref(true)
const error = ref(null)
const profile = ref(null)
const attendanceRecords = ref([])
const activeTab = ref('assessments')

const tabs = [
  { id: 'assessments', label: 'CBC Assessments' },
  { id: 'fees',        label: 'Fee Payments'   },
  { id: 'attendance',  label: 'Attendance'     },
]

const uniqueSubjects = computed(() =>
  new Set((profile.value?.assessments || []).map(a => a.learning_area)).size
)

const scoreClass = (score) => ({
  EE: 'bg-emerald-50 text-emerald-700',
  ME: 'bg-blue-50 text-blue-700',
  AE: 'bg-amber-50 text-amber-700',
  BE: 'bg-red-50 text-red-600',
}[score] || 'bg-slate-100 text-slate-600')

const formatCurrency = (amount) =>
  new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 }).format(amount)

const formatDate = (iso) => new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })

onMounted(async () => {
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
})
</script>
