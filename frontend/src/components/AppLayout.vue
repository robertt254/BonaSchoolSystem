<template>
  <div class="flex h-screen min-w-0 font-sans print:block print:h-auto" style="background:#fcf8fa">
    <!-- Mobile overlay -->
    <div
      v-if="isSidebarOpen"
      @click="isSidebarOpen = false"
      class="fixed inset-0 bg-black/50 z-40 md:hidden print:hidden"
    ></div>

    <!-- ─── SIDEBAR ─────────────────────────────────────────────────────── -->
    <aside
      :class="[
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
        'fixed inset-y-0 left-0 z-50 md:relative md:translate-x-0',
        'flex flex-col w-[260px] shrink-0 transition-transform duration-300 ease-out',
        'print:hidden',
      ]"
      style="background:#161b2b"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-5 py-5 border-b border-white/10">
        <div class="w-10 h-10 rounded flex items-center justify-center shrink-0" style="background:#712edd">
          <span class="material-symbols-outlined text-white" style="font-variation-settings:'FILL' 1,'wght' 400">school</span>
        </div>
        <div>
          <p class="font-semibold text-white text-sm leading-tight">The Bona School</p>
          <p class="text-xs capitalize" style="color:rgba(255,255,255,0.45)">{{ userRole.replace('_',' ') }} Portal</p>
        </div>
      </div>

      <!-- Nav -->
      <nav class="flex-1 overflow-y-auto py-3 hide-scrollbar">

        <NavItem to="/" :exact="true" icon="dashboard">Dashboard</NavItem>

        <template v-if="['teacher','senior_teacher','principal','admin','secretary'].includes(userRole)">
          <p class="px-5 pt-4 pb-1 text-xs font-semibold uppercase tracking-widest" style="color:rgba(255,255,255,0.25)">Academics</p>
          <NavItem to="/academics/students" icon="group">Students</NavItem>
          <NavItem to="/academics/classes" icon="meeting_room">Classes</NavItem>
        </template>

        <template v-if="['teacher','senior_teacher','principal','admin','secretary'].includes(userRole)">
          <NavItem to="/academics/attendance" icon="how_to_reg">Roll Call</NavItem>
          <NavItem v-if="userRole !== 'secretary'" to="/academics" icon="grade">Grading</NavItem>
          <NavItem to="/academics/report-card" icon="description">Report Cards</NavItem>
          <NavItem to="/academics/timetable" icon="schedule">Timetable</NavItem>
          <NavItem v-if="userRole !== 'secretary'" to="/academics/exams" icon="quiz">Exams &amp; Marks</NavItem>
          <NavItem to="/academics/discipline" icon="gavel">Discipline</NavItem>
        </template>

        <template v-if="['teacher','senior_teacher','principal','admin','accountant','secretary'].includes(userRole)">
          <NavItem to="/library" icon="library_books">Library</NavItem>
          <NavItem to="/calendar" icon="event">Calendar</NavItem>
        </template>

        <template v-if="['secretary','principal','admin'].includes(userRole)">
          <p class="px-5 pt-4 pb-1 text-xs font-semibold uppercase tracking-widest" style="color:rgba(255,255,255,0.25)">Administration</p>
          <NavItem to="/office" icon="home_work">Office</NavItem>
          <NavItem to="/office/communications" icon="forum">Communications</NavItem>
        </template>

        <template v-if="['accountant','principal','admin','secretary'].includes(userRole)">
          <p class="px-5 pt-4 pb-1 text-xs font-semibold uppercase tracking-widest" style="color:rgba(255,255,255,0.25)">Finance</p>
          <NavItem to="/finance" icon="account_balance">Dashboard</NavItem>
          <NavItem to="/finance/statements" icon="receipt_long">Statements</NavItem>
          <NavItem to="/finance/defaulters" icon="warning">Defaulters</NavItem>
          <NavItem v-if="['admin','principal','accountant','secretary'].includes(userRole)" to="/finance/fee-structure" icon="list_alt">Fee Structure</NavItem>
          <NavItem v-if="['accountant','admin'].includes(userRole)" to="/finance/payslips" icon="payments">Payroll</NavItem>
          <NavItem v-if="userRole !== 'secretary'" to="/finance/petty-cash" icon="savings">Petty Cash</NavItem>
          <NavItem v-if="userRole !== 'secretary'" to="/finance/budget" icon="bar_chart">Budget</NavItem>
        </template>

        <template v-if="['admin','principal'].includes(userRole)">
          <p class="px-5 pt-4 pb-1 text-xs font-semibold uppercase tracking-widest" style="color:rgba(255,255,255,0.25)">System</p>
          <NavItem v-if="userRole === 'admin'" to="/admin" icon="admin_panel_settings">Console</NavItem>
          <NavItem to="/admin/staff" icon="badge">HR &amp; Staff</NavItem>
          <NavItem to="/admin/leave" icon="beach_access">Leave</NavItem>
          <NavItem to="/admin/promotion" icon="upgrade">Promotion</NavItem>
          <NavItem to="/admin/year-transition" icon="sync">Year Transition</NavItem>
          <NavItem to="/admin/reports" icon="summarize">Reports</NavItem>
        </template>

      </nav>

      <!-- Bottom: Settings + Logout -->
      <div class="shrink-0 border-t border-white/10 px-3 py-3 space-y-0.5">
        <button
          @click="showChangePassword = true"
          class="w-full flex items-center gap-3 px-4 py-2.5 text-sm transition-colors rounded"
          style="color:rgba(255,255,255,0.6)"
          onmouseover="this.style.background='rgba(255,255,255,0.07)';this.style.color='rgba(255,255,255,0.9)'"
          onmouseout="this.style.background='';this.style.color='rgba(255,255,255,0.6)'"
        >
          <span class="material-symbols-outlined text-[20px] shrink-0">settings</span>
          <span class="font-medium">Settings</span>
        </button>
        <button
          @click="logout"
          class="w-full flex items-center gap-3 px-4 py-2.5 text-sm transition-colors rounded"
          style="color:rgba(255,255,255,0.6)"
          onmouseover="this.style.background='rgba(255,255,255,0.07)';this.style.color='rgba(255,255,255,0.9)'"
          onmouseout="this.style.background='';this.style.color='rgba(255,255,255,0.6)'"
        >
          <span class="material-symbols-outlined text-[20px] shrink-0">logout</span>
          <span class="font-medium">Logout</span>
        </button>
      </div>
    </aside>

    <ChangePasswordModal v-if="showChangePassword" @close="showChangePassword = false" />

    <!-- ─── MAIN ──────────────────────────────────────────────────────────── -->
    <div class="flex-1 min-w-0 flex flex-col overflow-hidden print:overflow-visible">

      <!-- Top bar -->
      <header class="shrink-0 h-16 bg-white border-b border-slate-200 flex items-center justify-between px-5 gap-4 print:hidden" style="border-color:#e2e8f0">
        <!-- Mobile toggle + Search -->
        <div class="flex items-center gap-3 flex-1 max-w-xl">
          <button
            @click="isSidebarOpen = true"
            class="md:hidden p-2 rounded-lg text-slate-500 hover:bg-slate-100 transition-colors"
          >
            <span class="material-symbols-outlined">menu</span>
          </button>
          <div class="relative flex-1">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" style="font-size:18px">search</span>
            <input
              type="text"
              placeholder="Search students, staff, or records..."
              class="w-full rounded-lg pl-10 pr-4 py-2 text-sm outline-none transition-all"
              style="background:#f1f5f9;border:none;color:#334155"
              onfocus="this.style.boxShadow='0 0 0 2px #712edd33'"
              onblur="this.style.boxShadow='none'"
            />
          </div>
        </div>

        <!-- Right side -->
        <div class="flex items-center gap-2">
          <!-- Year selector -->
          <div class="relative flex items-center gap-1.5 bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 hover:border-slate-300 transition-colors">
            <span class="material-symbols-outlined text-slate-400" style="font-size:16px">calendar_today</span>
            <select v-model="appStore.currentYear" class="bg-transparent text-sm font-semibold text-slate-700 outline-none cursor-pointer appearance-none pr-3">
              <option v-for="y in appStore.years" :key="y" :value="y">{{ y }}</option>
            </select>
          </div>
          <!-- Term selector -->
          <div class="relative flex items-center gap-1.5 bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 hover:border-slate-300 transition-colors">
            <span class="w-2 h-2 rounded-full bg-emerald-500 shrink-0"></span>
            <select v-model="appStore.currentTerm" class="bg-transparent text-sm font-semibold text-slate-700 outline-none cursor-pointer appearance-none pr-3">
              <option v-for="t in appStore.terms" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>
          <!-- Bell -->
          <button class="w-10 h-10 rounded-full flex items-center justify-center text-slate-500 hover:bg-slate-100 transition-colors relative">
            <span class="material-symbols-outlined">notifications</span>
          </button>
          <!-- Help -->
          <button class="w-10 h-10 rounded-full flex items-center justify-center text-slate-500 hover:bg-slate-100 transition-colors">
            <span class="material-symbols-outlined">help</span>
          </button>
          <!-- Divider -->
          <div class="w-px h-6 bg-slate-200 mx-1"></div>
          <!-- User profile -->
          <div class="flex items-center gap-2 cursor-pointer group" @click="showChangePassword = true">
            <div class="text-right hidden sm:block">
              <p class="text-sm font-semibold text-slate-800 leading-tight">{{ userName }}</p>
              <p class="text-xs text-slate-500 capitalize">{{ userRole.replace('_', ' ') }}</p>
            </div>
            <div class="w-9 h-9 rounded-full flex items-center justify-center text-white font-bold text-sm shrink-0" style="background:#712edd">
              {{ userNameInitial }}
            </div>
          </div>
        </div>
      </header>

      <!-- Session expiry warning banner -->
      <div
        v-if="showSessionWarning"
        class="shrink-0 bg-amber-50 border-b border-amber-200 px-6 py-2.5 flex items-center gap-3 text-amber-800 text-xs print:hidden"
      >
        <span class="material-symbols-outlined text-amber-500" style="font-size:16px">warning</span>
        <span>Your session expires in <strong>{{ sessionMinutesLeft }} minute{{ sessionMinutesLeft !== 1 ? 's' : '' }}</strong>. Save your work.</span>
        <router-link to="/login" class="ml-auto font-bold underline hover:no-underline whitespace-nowrap">Sign in again</router-link>
      </div>

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto print:overflow-visible print:h-auto" style="background:#fcf8fa">
        <div class="p-6 lg:p-8 max-w-[1400px] mx-auto">
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
      class: 'text-xs font-semibold uppercase tracking-widest px-5 pt-4 pb-1',
      style: 'color:rgba(255,255,255,0.25)',
    }, slots.default?.())
  },
})

const NavItem = defineComponent({
  props: { to: String, exact: Boolean, icon: String },
  setup(props, { slots }) {
    const route = useRoute()
    const isActive = computed(() =>
      props.exact ? route.path === props.to : route.path.startsWith(props.to)
    )
    return () => h(RouterLink, {
      to: props.to,
      style: isActive.value
        ? 'border-left:3px solid #712edd;background:rgba(255,255,255,0.07);color:#ffffff;padding-left:21px'
        : 'border-left:3px solid transparent;color:rgba(255,255,255,0.55);padding-left:21px',
      class: 'flex items-center gap-3 py-2.5 pr-4 text-sm font-medium transition-all duration-150',
      onMouseover: (e) => { if (!isActive.value) e.currentTarget.style.background = 'rgba(255,255,255,0.06)'; e.currentTarget.style.color = 'rgba(255,255,255,0.9)' },
      onMouseout:  (e) => { if (!isActive.value) { e.currentTarget.style.background = ''; e.currentTarget.style.color = 'rgba(255,255,255,0.55)' } },
    }, () => [
      props.icon && h('span', {
        class: 'material-symbols-outlined shrink-0',
        style: 'font-size:20px',
      }, props.icon),
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

onMounted(() => {
  nowTimer = setInterval(() => { now.value = Date.now() }, 30_000)
  appStore.loadCurrentTerm()
})
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
