<template>
  <div class="flex h-screen min-w-0 bg-school-grey font-sans print:block print:h-auto">
    <!-- Mobile overlay -->
    <div
      v-if="isSidebarOpen"
      @click="isSidebarOpen = false"
      class="fixed inset-0 bg-black/40 z-40 md:hidden print:hidden"
    ></div>

    <!-- ─── SIDEBAR ─────────────────────────────────────────────────────── -->
    <aside
      :class="[
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
        'fixed inset-y-0 left-0 z-50 md:relative md:translate-x-0',
        'flex flex-col w-[280px] shrink-0 bg-school-navy transition-transform duration-300 ease-out',
        'print:hidden',
      ]"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-5 py-5 border-b border-white/8">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-light to-brand-lighter flex items-center justify-center font-bold text-sm text-white shadow-lg shrink-0">
          BS
        </div>
        <div>
          <p class="text-sm font-bold text-white leading-tight">The Bona School</p>
          <p class="text-xs font-semibold uppercase tracking-widest text-white/30 mt-0.5">CBC System</p>
        </div>
      </div>

      <!-- Nav -->
      <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-0.5 hide-scrollbar">

        <NavItem to="/" :exact="true">
          <template #icon>
            <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
          </template>
          Dashboard
        </NavItem>

        <template v-if="['teacher','senior_teacher','principal','admin','secretary'].includes(userRole)">
          <SectionLabel>Academics</SectionLabel>
          <NavItem to="/academics/students">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </template>
            Students
          </NavItem>
          <NavItem to="/academics/classes">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>
              </svg>
            </template>
            Classes
          </NavItem>
        </template>

        <template v-if="['teacher','senior_teacher','principal','admin','secretary'].includes(userRole)">
          <NavItem to="/academics/attendance">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
              </svg>
            </template>
            Roll Call
          </NavItem>
          <NavItem v-if="userRole !== 'secretary'" to="/academics">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
              </svg>
            </template>
            Grading
          </NavItem>
          <NavItem to="/academics/report-card">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
            </template>
            Report Cards
          </NavItem>
          <NavItem to="/academics/timetable">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
            </template>
            Timetable
          </NavItem>
          <NavItem v-if="userRole !== 'secretary'" to="/academics/exams">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
            </template>
            Exams &amp; Marks
          </NavItem>
          <NavItem to="/academics/discipline">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            </template>
            Discipline
          </NavItem>
        </template>

        <template v-if="['teacher','senior_teacher','principal','admin','accountant','secretary'].includes(userRole)">
          <NavItem to="/library">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
            </template>
            Library
          </NavItem>
          <NavItem to="/calendar">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
            </template>
            Calendar
          </NavItem>
        </template>

        <template v-if="['secretary','principal','admin'].includes(userRole)">
          <SectionLabel>Administration</SectionLabel>
          <NavItem to="/office">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><rect x="9" y="14" width="6" height="7"/>
              </svg>
            </template>
            Office
          </NavItem>
          <NavItem to="/office/communications">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
            </template>
            Communications
          </NavItem>
        </template>

        <template v-if="['accountant','principal','admin','secretary'].includes(userRole)">
          <SectionLabel>Finance</SectionLabel>
          <NavItem to="/finance">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>
              </svg>
            </template>
            Dashboard
          </NavItem>
          <NavItem to="/finance/statements">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
            </template>
            Statements
          </NavItem>
          <NavItem to="/finance/defaulters">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
            </template>
            Defaulters
          </NavItem>
          <NavItem v-if="['admin','principal'].includes(userRole)" to="/finance/fee-structure">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
              </svg>
            </template>
            Fee Structure
          </NavItem>
          <NavItem v-if="['accountant','admin'].includes(userRole)" to="/finance/payslips">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>
              </svg>
            </template>
            Payroll
          </NavItem>
          <NavItem v-if="userRole !== 'secretary'" to="/finance/petty-cash">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
              </svg>
            </template>
            Petty Cash
          </NavItem>
          <NavItem v-if="userRole !== 'secretary'" to="/finance/budget">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
              </svg>
            </template>
            Budget
          </NavItem>
        </template>

        <template v-if="['admin','principal'].includes(userRole)">
          <SectionLabel>System</SectionLabel>
          <NavItem v-if="userRole === 'admin'" to="/admin">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/>
              </svg>
            </template>
            Console
          </NavItem>
          <NavItem to="/admin/staff">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </template>
            HR &amp; Staff
          </NavItem>
          <NavItem to="/admin/leave">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M20 9V7a2 2 0 0 0-2-2h-4L12 3l-2 2H6a2 2 0 0 0-2 2v2"/><path d="M9 22h6"/><path d="M12 22v-7"/><path d="M4 9h16"/><path d="M4 9v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9"/>
              </svg>
            </template>
            Leave
          </NavItem>
          <NavItem to="/admin/promotion">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <polyline points="17 11 12 6 7 11"/><polyline points="17 18 12 13 7 18"/>
              </svg>
            </template>
            Promotion
          </NavItem>
          <NavItem to="/admin/year-transition">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.5"/>
              </svg>
            </template>
            Year Transition
          </NavItem>
          <NavItem to="/admin/reports">
            <template #icon>
              <svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
            </template>
            Reports
          </NavItem>
        </template>

      </nav>

      <!-- Footer -->
      <div class="shrink-0 border-t border-white/10 p-4 space-y-2">
        <!-- User card -->
        <div class="flex items-center gap-3 px-3 py-3 rounded-xl bg-white/[0.06] border border-white/[0.06]">
          <div class="w-9 h-9 rounded-full bg-gradient-to-br from-[#7C3AED] to-[#A855F7] font-bold text-sm text-white flex items-center justify-center shrink-0 shadow-sm">
            {{ userNameInitial }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold text-white truncate">{{ userName }}</p>
            <p class="text-xs text-white/40 capitalize truncate">{{ userRole }}</p>
          </div>
        </div>
        <!-- Actions -->
        <button
          @click="showChangePassword = true"
          class="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-xs font-medium text-white/55 hover:bg-white/[0.07] hover:text-white/80 transition-colors"
        >
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
          </svg>
          Change Password
        </button>
        <button
          @click="logout"
          class="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-xs font-semibold text-white/70 hover:bg-[rgba(225,29,72,0.15)] hover:text-[#FCA5A5] transition-colors border border-transparent hover:border-red-500/20"
        >
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          Sign Out
        </button>
      </div>
    </aside>

    <ChangePasswordModal v-if="showChangePassword" @close="showChangePassword = false" />

    <!-- ─── MAIN ──────────────────────────────────────────────────────────── -->
    <div class="flex-1 min-w-0 flex flex-col overflow-hidden print:overflow-visible">

      <!-- Top bar -->
      <header class="shrink-0 h-16 bg-white border-b border-slate-200 flex items-center px-6 gap-4 print:hidden">
        <!-- Mobile toggle -->
        <button
          @click="isSidebarOpen = true"
          class="md:hidden -ml-1 p-2 rounded-lg text-slate-500 hover:bg-slate-100 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>

        <!-- Breadcrumb -->
        <div class="hidden md:block">
          <p class="text-xs font-semibold uppercase tracking-widest text-slate-400">{{ routeSection }}</p>
          <h1 class="text-base font-bold text-slate-800 leading-tight">{{ pageTitle }}</h1>
        </div>
        <p class="md:hidden text-base font-bold text-slate-800">Bona School</p>

        <div class="flex items-center gap-2 ml-auto">
          <!-- Year selector -->
          <div class="relative flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 hover:border-slate-300 transition-colors">
            <svg class="w-3.5 h-3.5 text-slate-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            <select
              v-model="appStore.currentYear"
              class="bg-transparent text-sm font-semibold text-slate-700 outline-none cursor-pointer appearance-none pr-4"
            >
              <option v-for="y in appStore.years" :key="y" :value="y">{{ y }}</option>
            </select>
            <svg class="w-3.5 h-3.5 absolute right-2.5 pointer-events-none text-slate-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <polyline points="6 9 12 15 18 9"/>
            </svg>
          </div>
          <!-- Term selector -->
          <div class="relative flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 hover:border-slate-300 transition-colors">
            <span class="w-2 h-2 rounded-full bg-emerald-500 shrink-0"></span>
            <select
              v-model="appStore.currentTerm"
              class="bg-transparent text-sm font-semibold text-slate-700 outline-none cursor-pointer appearance-none pr-4"
            >
              <option v-for="t in appStore.terms" :key="t" :value="t">{{ t }}</option>
            </select>
            <svg class="w-3.5 h-3.5 absolute right-2.5 pointer-events-none text-slate-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <polyline points="6 9 12 15 18 9"/>
            </svg>
          </div>
          <!-- Bell -->
          <button class="relative w-9 h-9 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-500 hover:bg-white hover:border-slate-300 transition-colors">
            <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
            <span class="absolute top-2 right-2 w-1.5 h-1.5 rounded-full bg-school-purple"></span>
          </button>
        </div>
      </header>

      <!-- Session expiry warning banner -->
      <div
        v-if="showSessionWarning"
        class="shrink-0 bg-amber-50 border-b border-amber-200 px-6 py-2.5 flex items-center gap-3 text-amber-800 text-xs print:hidden"
      >
        <svg class="w-4 h-4 shrink-0 text-amber-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <span>Your session expires in <strong>{{ sessionMinutesLeft }} minute{{ sessionMinutesLeft !== 1 ? 's' : '' }}</strong>. Save your work before it expires.</span>
        <router-link to="/login" class="ml-auto font-bold underline hover:no-underline whitespace-nowrap">Sign in again</router-link>
      </div>

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto bg-school-grey print:overflow-visible print:h-auto">
        <div class="p-6 lg:p-8">
          <router-view v-slot="{ Component }">
            <transition name="page-fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>
    </div>
  </div>
  <ToastContainer />
</template>

<script setup>
import { computed, ref, watch, onMounted, onUnmounted, defineComponent, h, resolveComponent } from 'vue'
import { useRouter, useRoute, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'
import ChangePasswordModal from '@/components/ChangePasswordModal.vue'
import ToastContainer from '@/components/ui/ToastContainer.vue'

// ── Sub-components ────────────────────────────────────────────────────────────

const SectionLabel = defineComponent({
  setup(_, { slots }) {
    return () => h('p', {
      class: 'text-xs font-bold uppercase tracking-widest text-white/25 px-3 pt-5 pb-1.5',
    }, slots.default?.())
  },
})

const NavItem = defineComponent({
  props: { to: String, exact: Boolean },
  setup(props, { slots }) {
    const route = useRoute()
    const isActive = computed(() =>
      props.exact ? route.path === props.to : route.path.startsWith(props.to)
    )
    return () => h(RouterLink, {
      to: props.to,
      class: [
        'flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 group relative',
        isActive.value
          ? 'bg-[rgba(109,40,217,0.14)] text-violet-300'
          : 'text-white/50 hover:bg-white/7 hover:text-white/80',
      ].join(' '),
    }, () => [
      isActive.value && h('span', {
        class: 'absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 bg-[#8B5CF6] rounded-r',
      }),
      h('span', {
        class: ['w-5 h-5 shrink-0', isActive.value ? 'opacity-100' : 'opacity-60 group-hover:opacity-90'].join(' '),
      }, slots.icon?.()),
      slots.default?.(),
    ])
  },
})

// ── State ─────────────────────────────────────────────────────────────────────

const router = useRouter()
const route  = useRoute()
const authStore = useAuthStore()
const appStore  = useAppStore()

const isSidebarOpen      = ref(false)
const showChangePassword = ref(false)
const now                = ref(Date.now())
let nowTimer             = null

onMounted(() => { nowTimer = setInterval(() => { now.value = Date.now() }, 30_000) })
onUnmounted(() => { clearInterval(nowTimer) })

const sessionMinutesLeft = computed(() => {
  const exp = authStore.tokenExpiresAt
  if (!exp) return null
  return Math.floor((exp - now.value) / 60_000)
})

const showSessionWarning = computed(() =>
  sessionMinutesLeft.value !== null &&
  sessionMinutesLeft.value <= 10 &&
  sessionMinutesLeft.value > 0
)

watch(() => route.path, () => { isSidebarOpen.value = false })

// ── Computed ──────────────────────────────────────────────────────────────────

const routeSection = computed(() => {
  const p = route.path
  if (p.startsWith('/academics')) return 'Academics'
  if (p.startsWith('/finance'))   return 'Finance'
  if (p.startsWith('/office'))    return 'Administration'
  if (p.startsWith('/admin'))     return 'System'
  if (p.startsWith('/students'))  return 'Students'
  return 'Overview'
})

const pageTitle = computed(() => {
  const m = {
    'dashboard':       'Dashboard',
    'admin-dash':      'Admin Console',
    'staff-directory': 'Staff Directory',
    'secretary-dash':  'Office & Admissions',
    'accountant-dash': 'Finance Dashboard',
    'fee-statement':   'Fee Statements',
    'fee-defaulters':  'Fee Defaulters',
    'fee-structure':   'Fee Structure',
    'teacher-dash':    'Grading',
    'report-card':     'Report Cards',
    'attendance-page': 'Roll Call',
    'student-profile': 'Student Profile',
    'principal-dash':  'Principal Dashboard',
    'timetable':          'Class Timetable',
    'leave-management':   'Leave Management',
    'students-dashboard': 'Students',
    'classes-dashboard':  'Classes',
    'exams':              'Exams & Marks',
    'discipline':         'Disciplinary Records',
    'library':            'Library',
    'calendar':           'School Calendar',
    'petty-cash':         'Petty Cash',
    'budget':             'Budget vs Actual',
    'payslips':           'Payroll',
    'promotion':          'Student Promotion',
    'year-transition':    'Year Transition',
    'reports':            'Report Builder',
  }
  return m[route.name] || 'Overview'
})

const userRole        = computed(() => authStore.user?.role || 'guest')
const userName        = computed(() => authStore.user?.name || 'User')
const userNameInitial = computed(() => userName.value.charAt(0).toUpperCase())

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.page-fade-enter-active,
.page-fade-leave-active { transition: opacity 0.18s ease; }
.page-fade-enter-from,
.page-fade-leave-to    { opacity: 0; }

.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>
