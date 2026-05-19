<template>
  <div class="max-w-7xl mx-auto space-y-8 animate-fade-in pb-12">
    <!-- Welcome Banner -->
    <div
      class="bg-school-navy rounded-2xl p-8 sm:p-10 text-white shadow-xl flex justify-between items-center relative overflow-hidden"
    >
      <!-- Decorative background element -->
      <div
        class="absolute -top-32 -left-32 w-96 h-96 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-school-red/30 via-school-navy to-school-navy rounded-full blur-3xl"
      ></div>
      <div
        class="absolute -bottom-32 -right-32 w-96 h-96 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-white/10 via-school-navy to-school-navy rounded-full blur-3xl"
      ></div>

      <div class="relative z-10">
        <h1 class="text-3xl sm:text-4xl font-black font-heading tracking-tight mb-3">
          Welcome to The Bona School
        </h1>
        <p class="text-slate-300 text-lg max-w-2xl font-sans">
          Competency-Based Curriculum (CBC) Management System
        </p>
      </div>
      <div
        class="hidden md:flex items-center justify-center w-20 h-20 bg-white/10 rounded-2xl backdrop-blur-sm border border-white/10 relative z-10"
      >
        <span class="text-4xl drop-shadow-md">🎓</span>
      </div>
    </div>

    <!-- Loading State -->
    <div
      v-if="loading"
      class="flex flex-col justify-center items-center py-20 text-slate-400 space-y-4"
    >
      <div
        class="w-10 h-10 border-4 border-slate-200 border-t-school-navy rounded-full animate-spin"
      ></div>
      <span class="text-sm font-medium tracking-widest uppercase">Compiling analytics...</span>
    </div>

    <div v-else class="space-y-8">
      <!-- Key Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Students Card -->
        <div
          class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow duration-300 relative overflow-hidden group"
        >
          <div
            class="absolute top-0 left-0 w-1 h-full bg-school-navy group-hover:w-2 transition-all duration-300"
          ></div>
          <div class="flex justify-between items-start">
            <div>
              <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">
                Total Enrolled
              </p>
              <h2 class="text-4xl font-black text-slate-800 tracking-tight">{{ totalStudents }}</h2>
            </div>
            <div
              class="p-3.5 bg-slate-50 rounded-xl text-school-navy/80 text-xl border border-slate-100 shadow-sm group-hover:bg-school-navy group-hover:text-white transition-colors duration-300"
            >
              👨‍🎓
            </div>
          </div>
          <p class="text-[13px] text-slate-500 mt-5 font-medium flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            Across all CBC grades
          </p>
        </div>

        <!-- Revenue Card -->
        <div
          class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow duration-300 relative overflow-hidden group"
        >
          <div
            class="absolute top-0 left-0 w-1 h-full bg-school-red group-hover:w-2 transition-all duration-300"
          ></div>
          <div class="flex justify-between items-start">
            <div>
              <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">
                Total Revenue
              </p>
              <h2 class="text-3xl font-black text-slate-800 tracking-tight mt-1">
                {{ formatCurrency(totalRevenue) }}
              </h2>
            </div>
            <div
              class="p-3.5 bg-slate-50 rounded-xl text-school-red/80 text-xl border border-slate-100 shadow-sm group-hover:bg-school-red group-hover:text-white transition-colors duration-300"
            >
              💰
            </div>
          </div>
          <p class="text-[13px] text-slate-500 mt-5 font-medium flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            All historical payments
          </p>
        </div>

        <!-- Staff Card -->
        <div
          class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow duration-300 relative overflow-hidden group"
        >
          <div
            class="absolute top-0 left-0 w-1 h-full bg-slate-400 group-hover:w-2 transition-all duration-300"
          ></div>
          <div class="flex justify-between items-start">
            <div>
              <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">
                Active Staff
              </p>
              <h2 class="text-4xl font-black text-slate-800 tracking-tight">{{ totalStaff }}</h2>
            </div>
            <div
              class="p-3.5 bg-slate-50 rounded-xl text-slate-600 text-xl border border-slate-100 shadow-sm group-hover:bg-slate-600 group-hover:text-white transition-colors duration-300"
            >
              🧑‍🏫
            </div>
          </div>
          <p class="text-[13px] text-slate-500 mt-5 font-medium flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            Teachers & Administrators
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Column (Quick Actions) -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Quick Actions -->
          <div
            class="bg-white rounded-2xl shadow-sm border border-slate-100 p-8 hover:shadow-md transition-shadow duration-300"
          >
            <div class="flex items-center justify-between mb-6 border-b border-slate-100 pb-4">
              <h3 class="text-lg font-black font-heading text-slate-800 tracking-tight">
                Quick Actions
              </h3>
              <span class="text-xs font-bold text-slate-400 uppercase tracking-widest"
                >Common Tasks</span
              >
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <router-link
                to="/academics/attendance"
                class="flex flex-col items-center justify-center p-6 border border-slate-100 rounded-xl hover:bg-slate-50 hover:border-school-navy/20 transition-all duration-200 group text-center bg-white shadow-sm hover:-translate-y-1"
              >
                <div
                  class="w-12 h-12 flex items-center justify-center bg-slate-50 rounded-full mb-4 group-hover:bg-school-navy/5 group-hover:scale-110 transition-transform duration-300 border border-slate-100 shadow-inner text-2xl"
                >
                  📋
                </div>
                <p
                  class="font-bold text-sm text-slate-700 group-hover:text-school-navy font-heading"
                >
                  Roll Call
                </p>
                <p class="text-[11px] text-slate-400 mt-1 uppercase tracking-wider font-bold">
                  Mark attendance
                </p>
              </router-link>

              <router-link
                to="/finance"
                class="flex flex-col items-center justify-center p-6 border border-slate-100 rounded-xl hover:bg-slate-50 hover:border-school-red/20 transition-all duration-200 group text-center bg-white shadow-sm hover:-translate-y-1"
              >
                <div
                  class="w-12 h-12 flex items-center justify-center bg-slate-50 rounded-full mb-4 group-hover:bg-school-red/5 group-hover:scale-110 transition-transform duration-300 border border-slate-100 shadow-inner text-2xl"
                >
                  💵
                </div>
                <p
                  class="font-bold text-sm text-slate-700 group-hover:text-school-red font-heading"
                >
                  Log Payment
                </p>
                <p class="text-[11px] text-slate-400 mt-1 uppercase tracking-wider font-bold">
                  Record fee
                </p>
              </router-link>

              <router-link
                to="/academics"
                class="flex flex-col items-center justify-center p-6 border border-slate-100 rounded-xl hover:bg-slate-50 hover:border-school-navy/20 transition-all duration-200 group text-center bg-white shadow-sm hover:-translate-y-1"
              >
                <div
                  class="w-12 h-12 flex items-center justify-center bg-slate-50 rounded-full mb-4 group-hover:bg-school-navy/5 group-hover:scale-110 transition-transform duration-300 border border-slate-100 shadow-inner text-2xl"
                >
                  📝
                </div>
                <p
                  class="font-bold text-sm text-slate-700 group-hover:text-school-navy font-heading"
                >
                  Enter Grades
                </p>
                <p class="text-[11px] text-slate-400 mt-1 uppercase tracking-wider font-bold">
                  Update scores
                </p>
              </router-link>

              <router-link
                to="/office"
                class="flex flex-col items-center justify-center p-6 border border-slate-100 rounded-xl hover:bg-slate-50 hover:border-slate-300 transition-all duration-200 group text-center bg-white shadow-sm hover:-translate-y-1"
              >
                <div
                  class="w-12 h-12 flex items-center justify-center bg-slate-50 rounded-full mb-4 group-hover:bg-slate-200 group-hover:scale-110 transition-transform duration-300 border border-slate-100 shadow-inner text-2xl"
                >
                  ➕
                </div>
                <p class="font-bold text-sm text-slate-700 group-hover:text-slate-900 font-heading">
                  Admit Student
                </p>
                <p class="text-[11px] text-slate-400 mt-1 uppercase tracking-wider font-bold">
                  New enrollment
                </p>
              </router-link>
            </div>
          </div>
        </div>

        <!-- Sidebar Column (Activity Feed) -->
        <div class="lg:col-span-1">
          <div
            class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 h-full hover:shadow-md transition-shadow duration-300"
          >
            <div class="flex items-center justify-between mb-6 border-b border-slate-100 pb-4">
              <h3 class="text-lg font-black font-heading text-slate-800 tracking-tight">
                Recent Activity
              </h3>
              <button
                class="text-xs font-bold text-school-navy hover:text-school-red uppercase tracking-widest transition-colors"
              >
                View All
              </button>
            </div>

            <div class="space-y-6">
              <div v-for="activity in recentActivity" :key="activity.id" class="flex gap-4 group">
                <div class="flex-shrink-0">
                  <div
                    :class="[
                      'w-10 h-10 rounded-full flex items-center justify-center text-lg',
                      activity.bg,
                    ]"
                  >
                    {{ activity.icon }}
                  </div>
                </div>
                <div>
                  <p
                    class="text-sm font-medium text-slate-800 leading-snug group-hover:text-school-navy transition-colors"
                  >
                    {{ activity.action }}
                  </p>
                  <div class="flex items-center gap-2 mt-1.5 text-xs text-slate-500 font-medium">
                    <span :class="activity.color">{{ activity.user }}</span>
                    <span>•</span>
                    <span>{{ activity.time }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import studentService from '@/services/studentService'
import feeService from '@/services/feeService'
import staffService from '@/services/staffService'

const loading = ref(true)
const totalStudents = ref(0)
const totalRevenue = ref(0)
const totalStaff = ref(0)

const recentActivity = ref([
  {
    id: 1,
    type: 'payment',
    user: 'Finance Dept',
    action: 'Recorded Term 1 fees for John Doe (Grade 3)',
    time: '10 minutes ago',
    icon: '💰',
    color: 'text-emerald-500',
    bg: 'bg-emerald-50',
  },
  {
    id: 2,
    type: 'attendance',
    user: 'Mr. Smith',
    action: 'Marked Grade 4 attendance (100% present)',
    time: '1 hour ago',
    icon: '📋',
    color: 'text-school-navy',
    bg: 'bg-school-navy/10',
  },
  {
    id: 3,
    type: 'admission',
    user: 'Office',
    action: 'Admitted new student: Sarah Jenkins (Playgroup)',
    time: '2 hours ago',
    icon: '👨‍🎓',
    color: 'text-purple-500',
    bg: 'bg-purple-50',
  },
  {
    id: 4,
    type: 'grading',
    user: 'Ms. Alice',
    action: 'Submitted Math assessment scores for Grade 2',
    time: '3 hours ago',
    icon: '📝',
    color: 'text-blue-500',
    bg: 'bg-blue-50',
  },
  {
    id: 5,
    type: 'system',
    user: 'System Admin',
    action: 'Weekly database backup completed successfully',
    time: '5 hours ago',
    icon: '⚙️',
    color: 'text-slate-500',
    bg: 'bg-slate-100',
  },
])

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    maximumFractionDigits: 0,
  }).format(amount)
}

onMounted(async () => {
  try {
    // We use Promise.all to fetch everything at the exact same time
    const [students, fees, staff] = await Promise.all([
      studentService.getAllStudents().catch(() => []),
      feeService.getAllFees().catch(() => []),
      staffService.getAllStaff().catch(() => []),
    ])

    // Calculate the totals
    totalStudents.value = students.length
    totalStaff.value = staff.length

    // Add up every single payment in the ledger
    totalRevenue.value = fees.reduce((sum, fee) => sum + (fee.amount || 0), 0)
  } catch (error) {
    console.error('Failed to load dashboard analytics', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
@keyframes countUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-count-up {
  animation: countUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
</style>
