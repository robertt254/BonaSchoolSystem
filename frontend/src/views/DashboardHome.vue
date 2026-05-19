<template>
  <div class="max-w-7xl mx-auto space-y-12 animate-slide-up pb-20 relative">
    <!-- Background Extravaganza -->
    <div class="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      <div
        class="absolute top-[10%] right-[10%] w-[500px] h-[500px] bg-gradient-to-br from-school-red/10 to-transparent rounded-full blur-[120px] animate-pulse-glow"
      ></div>
      <div
        class="absolute bottom-[20%] left-[5%] w-[600px] h-[600px] bg-gradient-to-tr from-blue-400/10 to-transparent rounded-full blur-[150px] animate-float"
        style="animation-delay: 2s"
      ></div>
    </div>

    <!-- Welcome Banner -->
    <div
      class="relative bg-school-navy rounded-[2.5rem] p-10 sm:p-14 text-white shadow-[0_30px_60px_-15px_rgba(10,25,47,0.5)] flex justify-between items-center overflow-hidden group hover:scale-[1.02] transition-transform duration-700 ease-out z-10 border border-white/10"
    >
      <!-- Moving Gradient Background -->
      <div
        class="absolute inset-0 bg-gradient-to-br from-school-navy via-[#1A2A42] to-school-navy opacity-90 z-0"
      ></div>
      <div
        class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMSIgY3k9IjEiIHI9IjEiIGZpbGw9InJnYmEoMjU1LDI1NSwyNTUsMC4wNSkiLz48L3N2Zz4=')] z-0"
      ></div>

      <!-- Glowing Orbs inside Banner -->
      <div
        class="absolute -top-40 -left-40 w-[500px] h-[500px] bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-school-red/40 via-school-red/5 to-transparent rounded-full blur-3xl group-hover:scale-150 transition-transform duration-[2s] z-0"
      ></div>
      <div
        class="absolute -bottom-40 -right-40 w-[500px] h-[500px] bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-500/30 via-school-navy to-transparent rounded-full blur-3xl animate-pulse-glow z-0"
      ></div>

      <div class="relative z-10 max-w-3xl">
        <div
          class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-md border border-white/20 mb-6 animate-slide-up"
          style="animation-delay: 100ms"
        >
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-xs font-bold uppercase tracking-widest text-emerald-100"
            >System Online & Active</span
          >
        </div>
        <h1
          class="text-4xl sm:text-6xl font-black font-heading tracking-tight mb-4 leading-tight drop-shadow-[0_0_30px_rgba(255,255,255,0.3)] animate-slide-up"
          style="animation-delay: 200ms"
        >
          Welcome to
          <span
            class="text-transparent bg-clip-text bg-gradient-to-r from-red-400 to-white animate-gradient-xy"
            >The Bona School</span
          >
        </h1>
        <p
          class="text-slate-300/80 text-xl font-bold max-w-2xl font-sans tracking-wide leading-relaxed animate-slide-up"
          style="animation-delay: 300ms"
        >
          Experience the pinnacle of Competency-Based Curriculum management.
        </p>
      </div>

      <div
        class="hidden lg:flex relative z-10 group-hover:rotate-12 group-hover:scale-125 transition-all duration-700"
      >
        <div
          class="absolute inset-0 bg-school-red/20 blur-2xl rounded-full animate-pulse-glow"
        ></div>
        <div
          class="w-32 h-32 bg-gradient-to-br from-white/20 to-white/5 rounded-3xl backdrop-blur-xl border border-white/30 flex items-center justify-center shadow-[0_0_40px_rgba(255,255,255,0.1)] transform -rotate-6"
        >
          <span class="text-6xl drop-shadow-[0_10px_20px_rgba(0,0,0,0.5)] animate-float">🎓</span>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col justify-center items-center py-32 relative z-10">
      <div class="relative w-24 h-24">
        <div class="absolute inset-0 border-8 border-slate-100 rounded-full"></div>
        <div
          class="absolute inset-0 border-8 border-school-red border-t-transparent rounded-full animate-spin"
        ></div>
        <div class="absolute inset-4 bg-school-navy rounded-full animate-pulse-glow"></div>
      </div>
      <span
        class="mt-8 font-black font-heading text-xl tracking-[0.2em] text-school-navy uppercase animate-pulse"
        >Compiling Extravagance...</span
      >
    </div>

    <div v-else class="space-y-12 relative z-10">
      <!-- Key Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Students Card -->
        <div class="relative group">
          <div
            class="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-school-navy rounded-[2rem] blur opacity-20 group-hover:opacity-100 transition duration-500 group-hover:duration-200"
          ></div>
          <div
            class="relative bg-white/80 backdrop-blur-xl rounded-[2rem] p-8 shadow-xl border border-white hover:-translate-y-2 transition-all duration-300 h-full"
          >
            <div class="flex justify-between items-start">
              <div>
                <p
                  class="text-[10px] font-black text-blue-600 uppercase tracking-[0.3em] mb-2 font-heading"
                >
                  Total Enrolled
                </p>
                <h2
                  class="text-6xl font-black font-heading text-school-navy tracking-tighter drop-shadow-sm animate-count-up"
                >
                  {{ totalStudents }}
                </h2>
              </div>
              <div
                class="p-5 bg-gradient-to-br from-blue-50 to-white rounded-2xl text-4xl shadow-inner border border-blue-100 group-hover:rotate-[20deg] group-hover:scale-125 transition-all duration-500"
              >
                👨‍🎓
              </div>
            </div>
            <div class="mt-8 pt-6 border-t border-slate-100/50">
              <p
                class="text-sm text-slate-500 font-bold uppercase tracking-wider flex items-center gap-3"
              >
                <span
                  class="w-3 h-3 rounded-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.6)] animate-pulse"
                ></span>
                Across all grades
              </p>
            </div>
          </div>
        </div>

        <!-- Revenue Card -->
        <div class="relative group">
          <div
            class="absolute -inset-0.5 bg-gradient-to-r from-emerald-400 to-teal-500 rounded-[2rem] blur opacity-20 group-hover:opacity-100 transition duration-500 group-hover:duration-200"
          ></div>
          <div
            class="relative bg-white/80 backdrop-blur-xl rounded-[2rem] p-8 shadow-xl border border-white hover:-translate-y-2 transition-all duration-300 h-full"
          >
            <div class="flex justify-between items-start">
              <div>
                <p
                  class="text-[10px] font-black text-emerald-600 uppercase tracking-[0.3em] mb-2 font-heading"
                >
                  Total Revenue
                </p>
                <h2
                  class="text-5xl font-black font-heading text-slate-800 tracking-tighter drop-shadow-sm animate-count-up"
                  style="animation-delay: 100ms"
                >
                  {{ formatCurrency(totalRevenue) }}
                </h2>
              </div>
              <div
                class="p-5 bg-gradient-to-br from-emerald-50 to-white rounded-2xl text-4xl shadow-inner border border-emerald-100 group-hover:-rotate-[20deg] group-hover:scale-125 transition-all duration-500"
              >
                💰
              </div>
            </div>
            <div class="mt-8 pt-6 border-t border-slate-100/50">
              <p
                class="text-sm text-slate-500 font-bold uppercase tracking-wider flex items-center gap-3"
              >
                <span
                  class="w-3 h-3 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.6)] animate-pulse"
                ></span>
                Historical Payments
              </p>
            </div>
          </div>
        </div>

        <!-- Staff Card -->
        <div class="relative group">
          <div
            class="absolute -inset-0.5 bg-gradient-to-r from-school-red to-orange-500 rounded-[2rem] blur opacity-20 group-hover:opacity-100 transition duration-500 group-hover:duration-200"
          ></div>
          <div
            class="relative bg-white/80 backdrop-blur-xl rounded-[2rem] p-8 shadow-xl border border-white hover:-translate-y-2 transition-all duration-300 h-full"
          >
            <div class="flex justify-between items-start">
              <div>
                <p
                  class="text-[10px] font-black text-school-red uppercase tracking-[0.3em] mb-2 font-heading"
                >
                  Active Staff
                </p>
                <h2
                  class="text-6xl font-black font-heading text-slate-800 tracking-tighter drop-shadow-sm animate-count-up"
                  style="animation-delay: 200ms"
                >
                  {{ totalStaff }}
                </h2>
              </div>
              <div
                class="p-5 bg-gradient-to-br from-red-50 to-white rounded-2xl text-4xl shadow-inner border border-red-100 group-hover:rotate-[20deg] group-hover:scale-125 transition-all duration-500"
              >
                🧑‍🏫
              </div>
            </div>
            <div class="mt-8 pt-6 border-t border-slate-100/50">
              <p
                class="text-sm text-slate-500 font-bold uppercase tracking-wider flex items-center gap-3"
              >
                <span
                  class="w-3 h-3 rounded-full bg-school-red shadow-[0_0_10px_rgba(211,47,47,0.6)] animate-pulse"
                ></span>
                Teachers & Admin
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Column (Quick Actions) -->
        <div class="lg:col-span-2">
          <div
            class="bg-white/70 backdrop-blur-2xl rounded-[2rem] shadow-[0_20px_50px_-15px_rgba(0,0,0,0.05)] border border-white p-10 hover:shadow-2xl transition-shadow duration-500 h-full"
          >
            <div class="flex items-center justify-between mb-10 pb-6 border-b border-slate-200/50">
              <h3
                class="text-2xl font-black font-heading text-school-navy tracking-tight flex items-center gap-4"
              >
                <span class="p-2.5 bg-blue-50 text-blue-600 rounded-xl animate-float">⚡</span>
                Quick Actions
              </h3>
              <span
                class="px-4 py-2 bg-slate-100 rounded-full text-xs font-black text-slate-400 uppercase tracking-widest shadow-inner"
                >Command Center</span
              >
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-6">
              <router-link to="/academics/attendance" class="relative group">
                <div
                  class="absolute inset-0 bg-school-navy rounded-2xl blur-lg opacity-0 group-hover:opacity-20 transition-opacity duration-300"
                ></div>
                <div
                  class="relative flex flex-col items-center p-8 bg-white border-2 border-slate-100 rounded-2xl group-hover:border-school-navy transition-all duration-300 transform group-hover:-translate-y-2 shadow-sm group-hover:shadow-xl"
                >
                  <div
                    class="w-16 h-16 flex items-center justify-center bg-slate-50 rounded-2xl mb-6 group-hover:bg-school-navy group-hover:text-white transition-all duration-500 shadow-inner group-hover:shadow-[0_10px_20px_rgba(10,25,47,0.3)] group-hover:rotate-12"
                  >
                    <span class="text-3xl">📋</span>
                  </div>
                  <p
                    class="font-black text-base text-slate-700 group-hover:text-school-navy font-heading"
                  >
                    Roll Call
                  </p>
                </div>
              </router-link>

              <router-link to="/finance" class="relative group" style="animation-delay: 100ms">
                <div
                  class="absolute inset-0 bg-emerald-500 rounded-2xl blur-lg opacity-0 group-hover:opacity-20 transition-opacity duration-300"
                ></div>
                <div
                  class="relative flex flex-col items-center p-8 bg-white border-2 border-slate-100 rounded-2xl group-hover:border-emerald-500 transition-all duration-300 transform group-hover:-translate-y-2 shadow-sm group-hover:shadow-xl"
                >
                  <div
                    class="w-16 h-16 flex items-center justify-center bg-slate-50 rounded-2xl mb-6 group-hover:bg-emerald-500 group-hover:text-white transition-all duration-500 shadow-inner group-hover:shadow-[0_10px_20px_rgba(16,185,129,0.3)] group-hover:-rotate-12"
                  >
                    <span class="text-3xl">💵</span>
                  </div>
                  <p
                    class="font-black text-base text-slate-700 group-hover:text-emerald-600 font-heading"
                  >
                    Log Payment
                  </p>
                </div>
              </router-link>

              <router-link to="/academics" class="relative group" style="animation-delay: 200ms">
                <div
                  class="absolute inset-0 bg-purple-500 rounded-2xl blur-lg opacity-0 group-hover:opacity-20 transition-opacity duration-300"
                ></div>
                <div
                  class="relative flex flex-col items-center p-8 bg-white border-2 border-slate-100 rounded-2xl group-hover:border-purple-500 transition-all duration-300 transform group-hover:-translate-y-2 shadow-sm group-hover:shadow-xl"
                >
                  <div
                    class="w-16 h-16 flex items-center justify-center bg-slate-50 rounded-2xl mb-6 group-hover:bg-purple-500 group-hover:text-white transition-all duration-500 shadow-inner group-hover:shadow-[0_10px_20px_rgba(168,85,247,0.3)] group-hover:rotate-12"
                  >
                    <span class="text-3xl">📝</span>
                  </div>
                  <p
                    class="font-black text-base text-slate-700 group-hover:text-purple-600 font-heading"
                  >
                    Enter Grades
                  </p>
                </div>
              </router-link>

              <router-link to="/office" class="relative group" style="animation-delay: 300ms">
                <div
                  class="absolute inset-0 bg-school-red rounded-2xl blur-lg opacity-0 group-hover:opacity-20 transition-opacity duration-300"
                ></div>
                <div
                  class="relative flex flex-col items-center p-8 bg-white border-2 border-slate-100 rounded-2xl group-hover:border-school-red transition-all duration-300 transform group-hover:-translate-y-2 shadow-sm group-hover:shadow-xl"
                >
                  <div
                    class="w-16 h-16 flex items-center justify-center bg-slate-50 rounded-2xl mb-6 group-hover:bg-school-red group-hover:text-white transition-all duration-500 shadow-inner group-hover:shadow-[0_10px_20px_rgba(211,47,47,0.3)] group-hover:-rotate-12"
                  >
                    <span class="text-3xl">➕</span>
                  </div>
                  <p
                    class="font-black text-base text-slate-700 group-hover:text-school-red font-heading"
                  >
                    Admit
                  </p>
                </div>
              </router-link>
            </div>
          </div>
        </div>

        <!-- Sidebar Column (Activity Feed) -->
        <div class="lg:col-span-1">
          <div
            class="bg-white/70 backdrop-blur-2xl rounded-[2rem] shadow-[0_20px_50px_-15px_rgba(0,0,0,0.05)] border border-white p-8 h-full hover:shadow-2xl transition-shadow duration-500 relative overflow-hidden"
          >
            <!-- Decorative background element -->
            <div
              class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-slate-100 to-transparent rounded-bl-[100px] -z-10"
            ></div>

            <div class="flex items-center justify-between mb-8 pb-4 border-b border-slate-200/50">
              <h3
                class="text-xl font-black font-heading text-slate-800 tracking-tight flex items-center gap-3"
              >
                <span class="animate-pulse-glow text-2xl">📡</span> Live Feed
              </h3>
              <button
                class="text-[10px] font-black text-school-red bg-red-50 px-3 py-1.5 rounded-full hover:bg-school-red hover:text-white uppercase tracking-[0.2em] transition-all hover:shadow-[0_0_15px_rgba(211,47,47,0.4)]"
              >
                All Logs
              </button>
            </div>

            <div class="space-y-6">
              <div
                v-for="(activity, index) in recentActivity"
                :key="activity.id"
                class="flex gap-5 group p-3 rounded-2xl hover:bg-white hover:shadow-[0_10px_20px_rgba(0,0,0,0.03)] transition-all duration-300 border border-transparent hover:border-slate-100"
                :style="`animation-delay: ${index * 100}ms`"
                :class="'animate-slide-up'"
              >
                <div class="flex-shrink-0">
                  <div
                    :class="[
                      'w-14 h-14 rounded-2xl flex items-center justify-center text-2xl shadow-inner group-hover:scale-110 transition-transform duration-500',
                      activity.bg,
                    ]"
                  >
                    <span class="group-hover:animate-bounce-slow">{{ activity.icon }}</span>
                  </div>
                </div>
                <div class="flex flex-col justify-center">
                  <p
                    class="text-sm font-black text-slate-800 leading-snug group-hover:text-school-navy transition-colors font-heading"
                  >
                    {{ activity.action }}
                  </p>
                  <div
                    class="flex items-center gap-3 mt-2 text-[11px] text-slate-500 font-bold uppercase tracking-wider"
                  >
                    <span
                      :class="[
                        'px-2 py-0.5 rounded-full bg-opacity-10',
                        activity.color,
                        activity.bg.replace('/10', '/30'),
                      ]"
                      >{{ activity.user }}</span
                    >
                    <span>•</span>
                    <span class="flex items-center gap-1"
                      ><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                        ></path></svg
                      >{{ activity.time }}</span
                    >
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
    user: 'Finance',
    action: 'Recorded Term 1 fees for John Doe',
    time: '10m ago',
    icon: '💰',
    color: 'text-emerald-600',
    bg: 'bg-emerald-50',
  },
  {
    id: 2,
    type: 'attendance',
    user: 'Mr. Smith',
    action: 'Marked Grade 4 attendance (100%)',
    time: '1h ago',
    icon: '📋',
    color: 'text-school-navy',
    bg: 'bg-blue-50',
  },
  {
    id: 3,
    type: 'admission',
    user: 'Office',
    action: 'Admitted Sarah Jenkins (Playgroup)',
    time: '2h ago',
    icon: '👨‍🎓',
    color: 'text-purple-600',
    bg: 'bg-purple-50',
  },
  {
    id: 4,
    type: 'grading',
    user: 'Ms. Alice',
    action: 'Submitted Math scores for Grade 2',
    time: '3h ago',
    icon: '📝',
    color: 'text-orange-600',
    bg: 'bg-orange-50',
  },
  {
    id: 5,
    type: 'system',
    user: 'System',
    action: 'Weekly automated backup completed',
    time: '5h ago',
    icon: '⚙️',
    color: 'text-slate-600',
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
    const [students, fees, staff] = await Promise.all([
      studentService.getAllStudents().catch(() => []),
      feeService.getAllFees().catch(() => []),
      staffService.getAllStaff().catch(() => []),
    ])

    totalStudents.value = students.length
    totalStaff.value = staff.length
    totalRevenue.value = fees.reduce((sum, fee) => sum + (fee.amount || 0), 0)
  } catch (error) {
    console.error('Failed to load dashboard analytics', error)
  } finally {
    setTimeout(() => {
      loading.value = false
    }, 800) // Artificial delay to show off loading animation
  }
})
</script>

<style scoped>
@keyframes countUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.animate-count-up {
  animation: countUp 1s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}
</style>
