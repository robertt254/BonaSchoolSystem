<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 relative">
    <!-- Welcome Banner -->
    <div
      class="relative rounded-[18px] p-8 overflow-hidden flex flex-col sm:flex-row items-center justify-between shadow-sm animate-slide-in"
      style="background: linear-gradient(130deg, #0a192f 0%, #1a0f40 50%, #0f172a 100%)"
    >
      <!-- Decorative Layers -->
      <div
        class="pointer-events-none absolute inset-0 bg-[radial-gradient(rgba(255,255,255,0.04)_1px,transparent_1px)] bg-[length:22px_22px]"
      ></div>
      <div
        class="pointer-events-none absolute top-[-60px] right-[-40px] w-[220px] h-[220px] rounded-full bg-[radial-gradient(circle,rgba(211,47,47,0.25)_0%,transparent_65%)]"
      ></div>
      <div
        class="pointer-events-none absolute bottom-[-60px] right-[160px] w-[180px] h-[180px] rounded-full bg-[radial-gradient(circle,rgba(16,185,129,0.12)_0%,transparent_65%)]"
      ></div>

      <!-- Banner Content -->
      <div class="relative z-10 text-left w-full sm:w-auto">
        <p class="text-[10.5px] font-bold uppercase tracking-[0.12em] text-white/40 mb-[7px]">
          Good morning, {{ userName }} 👋
        </p>
        <h1 class="font-heading text-[26px] font-extrabold text-white leading-[1.15] mb-[6px]">
          Welcome to The Bona School
        </h1>
        <p class="text-[13px] text-white/40 max-w-[400px] leading-relaxed">
          Competency-Based Curriculum (CBC) Management System — {{ appStore.currentTerm }} is
          active.
        </p>
        <button
          class="mt-[16px] inline-flex items-center gap-[6px] bg-white/10 border border-white/[0.12] text-white/75 text-[12.5px] font-semibold px-6 py-3.5 rounded-[8px] cursor-pointer hover:bg-white/15 hover:text-white transition-all"
        >
          <svg
            class="w-[16px] h-[16px]"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            viewBox="0 0 24 24"
          >
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
            <line x1="16" y1="2" x2="16" y2="6" />
            <line x1="8" y1="2" x2="8" y2="6" />
            <line x1="3" y1="10" x2="21" y2="10" />
          </svg>
          View term schedule
        </button>
      </div>

      <!-- Banner Icon -->
      <div class="relative z-10 hidden lg:flex mt-6 sm:mt-0">
        <div
          class="w-[86px] h-[86px] rounded-full bg-white/[0.07] border border-white/10 flex items-center justify-center"
        >
          <div
            class="w-[66px] h-[66px] rounded-full bg-white/[0.08] flex items-center justify-center"
          >
            <svg
              class="w-[36px] h-[36px]"
              fill="none"
              stroke="rgba(255,255,255,0.7)"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
              viewBox="0 0 24 24"
            >
              <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
              <path d="M6 12v5c3 3 9 3 12 0v-5" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col justify-center items-center py-20 relative z-10">
      <div
        class="w-8 h-8 border-4 border-[#E2E8F0] border-t-school-navy rounded-full animate-spin mx-auto"
      ></div>
      <div
        class="text-[12px] font-semibold uppercase tracking-widest text-[#94A3B8] mt-4 text-center"
      >
        Loading...
      </div>
    </div>

    <div v-else class="space-y-[18px] relative z-10">
      <!-- Stats Grid -->
      <div
        class="grid grid-cols-1 md:grid-cols-3 gap-8"
        style="animation: slideIn 0.4s 0.08s ease both"
      >
        <!-- Total Enrolled -->
        <div
          class="bg-white border border-[#E2E8F0] rounded-[12px] p-[20px_22px] relative overflow-hidden transition-all duration-200 cursor-default hover:-translate-y-[2px] hover:shadow-[0_8px_28px_rgba(0,0,0,0.07)] hover:border-[#CBD5E1]"
        >
          <span
            class="absolute top-0 left-0 right-0 h-[3px] rounded-t-[12px] bg-gradient-to-r from-[#2563EB] to-[#818CF8]"
          ></span>
          <div class="flex items-start justify-between mb-[12px]">
            <span class="text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8]"
              >Total Enrolled</span
            >
            <div
              class="w-[38px] h-[38px] rounded-[9px] flex items-center justify-center bg-[rgba(37,99,235,0.1)] text-[#2563EB]"
            >
              <svg
                class="w-5 h-5"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                viewBox="0 0 24 24"
              >
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
              </svg>
            </div>
          </div>
          <h2
            class="font-heading text-[34px] font-extrabold text-[#0F172A] leading-none mb-[7px] animate-count-up"
            style="animation-delay: 0.05s"
          >
            {{ totalStudents }}
          </h2>
          <div class="flex items-center gap-[6px]">
            <span
              class="inline-flex items-center px-[8px] py-[2px] rounded-full text-[11px] font-bold bg-[rgba(100,116,139,0.09)] text-[#64748B]"
              >Active</span
            >
            <span class="text-[12px] text-[#94A3B8]">Across all grades</span>
          </div>
        </div>

        <!-- Total Revenue -->
        <div
          class="bg-white border border-[#E2E8F0] rounded-[12px] p-[20px_22px] relative overflow-hidden transition-all duration-200 cursor-default hover:-translate-y-[2px] hover:shadow-[0_8px_28px_rgba(0,0,0,0.07)] hover:border-[#CBD5E1]"
        >
          <span
            class="absolute top-0 left-0 right-0 h-[3px] rounded-t-[12px] bg-gradient-to-r from-[#059669] to-[#34D399]"
          ></span>
          <div class="flex items-start justify-between mb-[12px]">
            <span class="text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8]"
              >Total Revenue</span
            >
            <div
              class="w-[38px] h-[38px] rounded-[9px] flex items-center justify-center bg-[rgba(5,150,105,0.1)] text-[#059669]"
            >
              <svg
                class="w-5 h-5"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                viewBox="0 0 24 24"
              >
                <rect x="2" y="5" width="20" height="14" rx="2" />
                <line x1="2" y1="10" x2="22" y2="10" />
              </svg>
            </div>
          </div>
          <h2
            class="font-heading text-[34px] font-extrabold text-[#0F172A] leading-none mb-[7px] animate-count-up"
            style="animation-delay: 0.1s"
          >
            {{ formatCurrency(totalRevenue) }}
          </h2>
          <div class="flex items-center gap-[6px]">
            <span
              class="inline-flex items-center px-[8px] py-[2px] rounded-full text-[11px] font-bold bg-[rgba(100,116,139,0.09)] text-[#64748B]"
              >YTD</span
            >
            <span class="text-[12px] text-[#94A3B8]">Historical Payments</span>
          </div>
        </div>

        <!-- Active Staff -->
        <div
          class="bg-white border border-[#E2E8F0] rounded-[12px] p-[20px_22px] relative overflow-hidden transition-all duration-200 cursor-default hover:-translate-y-[2px] hover:shadow-[0_8px_28px_rgba(0,0,0,0.07)] hover:border-[#CBD5E1]"
        >
          <span
            class="absolute top-0 left-0 right-0 h-[3px] rounded-t-[12px] bg-gradient-to-r from-school-red to-red-400"
          ></span>
          <div class="flex items-start justify-between mb-[12px]">
            <span class="text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8]"
              >Active Staff</span
            >
            <div
              class="w-[38px] h-[38px] rounded-[9px] flex items-center justify-center bg-[rgba(211,47,47,0.1)] text-school-red"
            >
              <svg
                class="w-5 h-5"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                viewBox="0 0 24 24"
              >
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
              </svg>
            </div>
          </div>
          <h2
            class="font-heading text-[34px] font-extrabold text-[#0F172A] leading-none mb-[7px] animate-count-up"
            style="animation-delay: 0.15s"
          >
            {{ totalStaff }}
          </h2>
          <div class="flex items-center gap-[6px]">
            <span
              class="inline-flex items-center px-[8px] py-[2px] rounded-full text-[11px] font-bold bg-[rgba(100,116,139,0.09)] text-[#64748B]"
              >Active</span
            >
            <span class="text-[12px] text-[#94A3B8]">Teachers & Admin</span>
          </div>
        </div>
      </div>

      <!-- Two-Column Section -->
      <div
        class="grid grid-cols-1 lg:grid-cols-2 gap-8"
        style="animation: slideIn 0.4s 0.18s ease both"
      >
        <!-- Quick Actions Panel -->
        <div class="bg-white border border-[#E2E8F0] rounded-[12px] overflow-hidden">
          <div class="flex items-center justify-between p-8 border-b border-[#E2E8F0]">
            <div>
              <h3 class="font-heading text-[14.5px] font-bold text-[#0F172A]">Quick Actions</h3>
              <p class="text-[11.5px] text-[#94A3B8] mt-[1px]">Common tasks and shortcuts</p>
            </div>
            <span
              class="text-[12px] font-semibold text-school-red cursor-pointer hover:text-red-700 transition-colors"
              >View All</span
            >
          </div>
          <div class="grid grid-cols-2 gap-[10px] p-8">
            <router-link
              to="/academics/attendance"
              class="flex items-center gap-6 p-8 rounded-[10px] bg-school-grey border border-[#E2E8F0] cursor-pointer transition-all duration-[180ms] hover:bg-white hover:border-school-red/30 hover:-translate-y-[1px] hover:shadow-[0_4px_14px_rgba(211,47,47,0.09)]"
            >
              <div
                class="w-[40px] h-[40px] rounded-[10px] flex items-center justify-center flex-shrink-0 bg-[rgba(211,47,47,0.12)] text-school-red"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  viewBox="0 0 24 24"
                >
                  <path d="M9 11l3 3L22 4" />
                  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
                </svg>
              </div>
              <div>
                <p class="text-[13px] font-semibold text-[#0F172A] leading-tight">Roll Call</p>
                <p class="text-[11px] text-[#94A3B8] mt-[1px]">Mark attendance</p>
              </div>
            </router-link>

            <router-link
              to="/finance"
              class="flex items-center gap-6 p-8 rounded-[10px] bg-school-grey border border-[#E2E8F0] cursor-pointer transition-all duration-[180ms] hover:bg-white hover:border-school-red/30 hover:-translate-y-[1px] hover:shadow-[0_4px_14px_rgba(211,47,47,0.09)]"
            >
              <div
                class="w-[40px] h-[40px] rounded-[10px] flex items-center justify-center flex-shrink-0 bg-[rgba(5,150,105,0.1)] text-[#059669]"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  viewBox="0 0 24 24"
                >
                  <rect x="2" y="5" width="20" height="14" rx="2" />
                  <line x1="2" y1="10" x2="22" y2="10" />
                </svg>
              </div>
              <div>
                <p class="text-[13px] font-semibold text-[#0F172A] leading-tight">Log Payment</p>
                <p class="text-[11px] text-[#94A3B8] mt-[1px]">Record fees</p>
              </div>
            </router-link>

            <router-link
              to="/academics"
              class="flex items-center gap-6 p-8 rounded-[10px] bg-school-grey border border-[#E2E8F0] cursor-pointer transition-all duration-[180ms] hover:bg-white hover:border-school-red/30 hover:-translate-y-[1px] hover:shadow-[0_4px_14px_rgba(211,47,47,0.09)]"
            >
              <div
                class="w-[40px] h-[40px] rounded-[10px] flex items-center justify-center flex-shrink-0 bg-[rgba(37,99,235,0.1)] text-[#2563EB]"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  viewBox="0 0 24 24"
                >
                  <polygon
                    points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
                  />
                </svg>
              </div>
              <div>
                <p class="text-[13px] font-semibold text-[#0F172A] leading-tight">Enter Grades</p>
                <p class="text-[11px] text-[#94A3B8] mt-[1px]">CBC Assessments</p>
              </div>
            </router-link>

            <router-link
              to="/office"
              class="flex items-center gap-6 p-8 rounded-[10px] bg-school-grey border border-[#E2E8F0] cursor-pointer transition-all duration-[180ms] hover:bg-white hover:border-school-red/30 hover:-translate-y-[1px] hover:shadow-[0_4px_14px_rgba(211,47,47,0.09)]"
            >
              <div
                class="w-[40px] h-[40px] rounded-[10px] flex items-center justify-center flex-shrink-0 bg-[rgba(217,119,6,0.1)] text-[#D97706]"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  viewBox="0 0 24 24"
                >
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="16" />
                  <line x1="8" y1="12" x2="16" y2="12" />
                </svg>
              </div>
              <div>
                <p class="text-[13px] font-semibold text-[#0F172A] leading-tight">Admit Student</p>
                <p class="text-[11px] text-[#94A3B8] mt-[1px]">New enrollment</p>
              </div>
            </router-link>

            <router-link
              to="/academics/report-card"
              class="flex items-center gap-6 p-8 rounded-[10px] bg-school-grey border border-[#E2E8F0] cursor-pointer transition-all duration-[180ms] hover:bg-white hover:border-school-red/30 hover:-translate-y-[1px] hover:shadow-[0_4px_14px_rgba(211,47,47,0.09)]"
            >
              <div
                class="w-[40px] h-[40px] rounded-[10px] flex items-center justify-center flex-shrink-0 bg-[rgba(211,47,47,0.12)] text-school-red"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  viewBox="0 0 24 24"
                >
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                </svg>
              </div>
              <div>
                <p class="text-[13px] font-semibold text-[#0F172A] leading-tight">Report Cards</p>
                <p class="text-[11px] text-[#94A3B8] mt-[1px]">Generate PDFs</p>
              </div>
            </router-link>

            <router-link
              to="/finance/statements"
              class="flex items-center gap-6 p-8 rounded-[10px] bg-school-grey border border-[#E2E8F0] cursor-pointer transition-all duration-[180ms] hover:bg-white hover:border-school-red/30 hover:-translate-y-[1px] hover:shadow-[0_4px_14px_rgba(211,47,47,0.09)]"
            >
              <div
                class="w-[40px] h-[40px] rounded-[10px] flex items-center justify-center flex-shrink-0 bg-[rgba(37,99,235,0.1)] text-[#2563EB]"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  viewBox="0 0 24 24"
                >
                  <line x1="18" y1="20" x2="18" y2="10" />
                  <line x1="12" y1="20" x2="12" y2="4" />
                  <line x1="6" y1="20" x2="6" y2="14" />
                </svg>
              </div>
              <div>
                <p class="text-[13px] font-semibold text-[#0F172A] leading-tight">Statements</p>
                <p class="text-[11px] text-[#94A3B8] mt-[1px]">Fee balances</p>
              </div>
            </router-link>
          </div>
        </div>

        <!-- Activity Feed Panel -->
        <div class="bg-white border border-[#E2E8F0] rounded-[12px] overflow-hidden">
          <div class="flex items-center justify-between p-8 border-b border-[#E2E8F0]">
            <div>
              <h3 class="font-heading text-[14.5px] font-bold text-[#0F172A]">Activity Feed</h3>
              <p class="text-[11.5px] text-[#94A3B8] mt-[1px]">Latest system events</p>
            </div>
            <span
              class="text-[12px] font-semibold text-school-red cursor-pointer hover:text-red-700 transition-colors"
              >All Activity</span
            >
          </div>

          <div class="flex flex-col">
            <div
              v-for="activity in recentActivity"
              :key="activity.id"
              class="flex items-start gap-6 p-8 border-b border-[#E2E8F0] last:border-b-0 cursor-pointer transition-colors hover:bg-[#F8FAFC]"
            >
              <div
                class="w-[34px] h-[34px] rounded-full flex items-center justify-center font-heading font-bold text-[13px] flex-shrink-0 mt-[1px]"
                :class="activity.avatarClass"
              >
                {{ activity.user.charAt(0) }}
              </div>

              <div>
                <p class="text-[13px] font-medium text-[#0F172A] leading-[1.45]">
                  <span class="font-semibold">{{ activity.user }}</span>
                  <span class="font-normal text-[#475569]"> {{ activity.action }}</span>
                </p>
                <p class="text-[11px] text-[#94A3B8] mt-[2px] flex items-center gap-1">
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
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'
import { apiFetch } from '@/services/api'

const authStore = useAuthStore()
const appStore = useAppStore()

const userName = computed(() => authStore.user?.name || 'User')

const loading = ref(true)
const totalStudents = ref(0)
const totalRevenue = ref(0)
const totalStaff = ref(0)
const recentActivity = ref([])

const RESOURCE_STYLE = {
  student:    { avatar: 'bg-[rgba(217,119,6,0.1)] text-[#D97706]',   dot: 'bg-[#D97706]' },
  fee:        { avatar: 'bg-[rgba(5,150,105,0.1)] text-[#059669]',   dot: 'bg-[#059669]' },
  assessment: { avatar: 'bg-[rgba(37,99,235,0.1)] text-[#2563EB]',   dot: 'bg-[#2563EB]' },
  attendance: { avatar: 'bg-[rgba(37,99,235,0.1)] text-[#2563EB]',   dot: 'bg-[#2563EB]' },
  staff:      { avatar: 'bg-[rgba(211,47,47,0.12)] text-school-red', dot: 'bg-school-red' },
  payroll:    { avatar: 'bg-[rgba(5,150,105,0.1)] text-[#059669]',   dot: 'bg-[#059669]' },
  expense:    { avatar: 'bg-[rgba(211,47,47,0.12)] text-school-red', dot: 'bg-school-red' },
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

onMounted(async () => {
  try {
    const stats = await apiFetch('/api/dashboard/stats')
    totalStudents.value = stats.total_students
    totalStaff.value    = stats.total_staff
    totalRevenue.value  = stats.total_revenue

    recentActivity.value = (stats.recent_activity || []).map((log) => {
      const style = RESOURCE_STYLE[log.resource] || RESOURCE_STYLE.staff
      return {
        id:          log.id,
        type:        log.resource,
        user:        log.user_name || 'System',
        action:      `${ACTION_LABELS[log.action] || log.action} a ${log.resource} record`,
        time:        formatRelativeTime(log.timestamp),
        avatarClass: style.avatar,
        dotClass:    style.dot,
      }
    })
  } catch (error) {
    console.error('Failed to load dashboard analytics', error)
  } finally {
    loading.value = false
  }
})
</script>
