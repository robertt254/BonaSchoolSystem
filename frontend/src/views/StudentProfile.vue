<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="font-heading text-[22px] font-bold text-[#0F172A] tracking-tight">
          Student Profile
        </h1>
        <p class="text-slate-500 mt-1 text-sm font-medium">Detailed student record</p>
      </div>
      <button
        @click="$router.back()"
        class="text-sm font-bold text-school-navy bg-slate-100 hover:bg-slate-200 px-6 py-3.5 rounded-lg transition-colors"
      >
        &larr; Back
      </button>
    </div>

    <!-- Loading State -->
    <div
      v-if="loading"
      class="flex flex-col justify-center items-center py-20 text-slate-400 space-y-4"
    >
      <div
        class="w-8 h-8 border-4 border-[#E2E8F0] border-t-school-navy rounded-full animate-spin mx-auto"
      ></div>
      <span class="text-xs font-bold tracking-widest uppercase">Loading Profile...</span>
    </div>

    <!-- Content -->
    <div v-else-if="profile" class="space-y-8">
      <!-- Profile Card -->
      <div
        class="bg-white rounded-[12px] border border-[#E2E8F0] shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] p-8 flex flex-col sm:flex-row sm:items-center gap-8 relative overflow-hidden group"
      >
        <div
          class="absolute right-0 top-0 w-32 h-32 bg-blue-50 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-110"
        ></div>
        <div
          class="w-24 h-24 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 font-bold text-4xl border-2 border-white shadow-sm z-10 shrink-0"
        >
          {{ profile.student.first_name.charAt(0) }}
        </div>
        <div class="z-10 flex-1">
          <div class="flex items-center gap-3 mb-1">
            <h2 class="text-2xl font-extrabold text-slate-800">
              {{ profile.student.first_name }} {{ profile.student.last_name }}
            </h2>
            <span
              class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-full border"
              :class="
                profile.student.status === 'Active'
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  : 'bg-slate-50 text-slate-600 border-slate-200'
              "
            >
              {{ profile.student.status }}
            </span>
          </div>
          <div class="text-slate-500 font-medium text-sm flex gap-4">
            <span
              >Class:
              <strong class="text-slate-700">{{ profile.student.grade_level }}</strong></span
            >
            <span
              >ID: <strong class="text-slate-700">{{ formatId(profile.student.id) }}</strong></span
            >
            <span
              >Admission No:
              <strong class="text-slate-700">{{ profile.student.admission_number }}</strong></span
            >
          </div>
        </div>
      </div>

      <!-- Quick Metrics Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-8">
        <!-- Attendance -->
        <div
          class="bg-white p-8 rounded-[12px] border border-[#E2E8F0] shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] relative overflow-hidden group"
        >
          <div
            class="absolute right-0 top-0 w-24 h-24 bg-purple-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"
          ></div>
          <div class="relative z-10">
            <div class="text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1">
              Attendance Rate
            </div>
            <div class="text-3xl font-extrabold text-slate-800 flex items-baseline gap-1">
              {{ profile.attendance_percentage }}<span class="text-lg text-slate-500">%</span>
            </div>
            <div class="mt-3 w-full bg-slate-100 rounded-full h-2">
              <div
                class="bg-school-navy h-2 rounded-full"
                :style="{ width: profile.attendance_percentage + '%' }"
              ></div>
            </div>
          </div>
        </div>

        <!-- Finance -->
        <div
          class="bg-white p-8 rounded-[12px] border border-[#E2E8F0] shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] relative overflow-hidden group"
        >
          <div
            class="absolute right-0 top-0 w-24 h-24 bg-emerald-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"
          ></div>
          <div class="relative z-10">
            <div class="text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1">
              Fee Balance
            </div>
            <div
              class="text-3xl font-extrabold flex items-baseline gap-1"
              :class="profile.fee_balance > 0 ? 'text-school-red' : 'text-emerald-600'"
            >
              {{ formatCurrency(profile.fee_balance) }}
            </div>
            <p
              class="text-xs font-medium mt-2"
              :class="profile.fee_balance > 0 ? 'text-school-red/80' : 'text-emerald-600/80'"
            >
              {{
                profile.fee_balance > 0
                  ? 'Outstanding balance for the year.'
                  : 'Fully paid. No outstanding balance.'
              }}
            </p>
          </div>
        </div>
      </div>

      <!-- Assessments -->
      <div
        class="bg-white rounded-[12px] border border-[#E2E8F0] shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] overflow-hidden"
      >
        <div class="border-b border-slate-100 px-8 py-6">
          <h3 class="text-lg font-bold text-slate-800 tracking-tight">CBC Assessments</h3>
          <p class="text-xs text-slate-500 mt-0.5">Academic progress and scores.</p>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr
                class="bg-school-grey border-b border-[#E2E8F0] text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8]"
              >
                <th class="py-5 px-8 font-bold">Term</th>
                <th class="py-5 px-8 font-bold">Learning Area</th>
                <th class="py-5 px-8 font-bold">Score</th>
                <th class="py-5 px-8 font-bold">Remarks</th>
              </tr>
            </thead>
            <tbody class="text-sm">
              <tr
                v-for="assessment in profile.assessments"
                :key="assessment.id"
                class="border-b border-slate-50 hover:bg-slate-50/50 transition duration-150"
              >
                <td class="py-5 px-8 font-medium text-slate-500">{{ assessment.term }}</td>
                <td class="py-5 px-8 font-bold text-slate-800">{{ assessment.learning_area }}</td>
                <td class="py-5 px-8 font-bold text-school-navy">{{ assessment.score }}</td>
                <td class="py-5 px-8 text-slate-500 text-xs">{{ assessment.remarks || '-' }}</td>
              </tr>
              <tr v-if="profile.assessments.length === 0">
                <td colspan="4" class="py-6 px-8 text-center text-slate-400 text-sm font-medium">
                  No assessments recorded yet.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import studentService from '@/services/studentService'

const route = useRoute()
const loading = ref(true)
const profile = ref(null)

const loadProfile = async () => {
  loading.value = true
  try {
    const studentId = route.params.id
    profile.value = await studentService.getStudentProfile(studentId)
  } catch (error) {
    console.error('Failed to load profile', error)
    alert('Failed to load student profile.')
  } finally {
    loading.value = false
  }
}

onMounted(loadProfile)

// Helper to format ID to 4 digits with leading zeros
const formatId = (id) => {
  return String(id).padStart(4, '0')
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    maximumFractionDigits: 0,
  }).format(amount)
}
</script>
