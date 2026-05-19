<template>
  <div class="flex h-screen bg-school-grey font-sans relative overflow-hidden">
    <!-- Mobile Sidebar Overlay -->
    <div
      v-if="isSidebarOpen"
      @click="isSidebarOpen = false"
      class="fixed inset-0 bg-school-navy/50 z-[90] md:hidden transition-opacity"
    ></div>

    <!-- SIDEBAR -->
    <aside
      :class="[
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
        'fixed inset-y-0 left-0 z-[100] w-[264px] bg-school-navy text-white transition-all duration-300 ease-out transform md:relative md:translate-x-0 flex flex-col overflow-hidden',
      ]"
    >
      <!-- Decorative Gradient -->
      <div
        class="absolute bottom-[-120px] right-[-80px] w-[260px] h-[260px] rounded-full bg-[radial-gradient(circle,rgba(211,47,47,0.14)_0%,transparent_70%)] pointer-events-none"
      ></div>

      <!-- Sidebar Header (Logo Area) -->
      <div
        class="flex flex-row items-center gap-[12px] p-[22px_18px_18px] border-b border-white/[0.06] bg-school-navy relative z-10"
      >
        <div
          class="w-[42px] h-[42px] rounded-[11px] bg-gradient-to-br from-school-red to-red-400 flex items-center justify-center font-heading font-extrabold text-[17px] text-white shadow-[0_6px_16px_rgba(211,47,47,0.35)] shrink-0"
        >
          BS
        </div>
        <div class="flex flex-col">
          <h2 class="font-heading font-bold text-[13.5px] text-white leading-tight">
            The Bona School
          </h2>
          <p class="text-[9.5px] font-semibold uppercase tracking-[0.1em] text-white/30 mt-0.5">
            CBC Management
          </p>
        </div>
      </div>

      <!-- Navigation Links -->
      <nav
        class="flex-1 overflow-y-auto py-[18px] px-[10px] space-y-0 hide-scrollbar relative z-10"
      >
        <router-link
          to="/"
          class="flex items-center gap-[10px] px-[10px] py-[9px] rounded-[9px] text-[13.5px] font-medium text-white/50 transition-all duration-150 cursor-pointer mb-[1px] hover:bg-white/[0.07] hover:text-white/85 relative group"
          active-class="bg-[rgba(211,47,47,0.12)] text-red-300 active-nav-item hover:bg-[rgba(211,47,47,0.12)] hover:text-red-300"
        >
          <div
            class="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-[20px] bg-school-red rounded-[0_3px_3px_0] hidden"
          ></div>
          <svg
            class="w-[17px] h-[17px] shrink-0 opacity-70 group-hover:opacity-100 transition-opacity nav-icon"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            viewBox="0 0 24 24"
          >
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
          Dashboard
        </router-link>

        <template v-if="['senior_teacher', 'principal', 'admin'].includes(userRole)">
          <div class="pt-[16px] pb-[5px]">
            <span
              class="text-[9.5px] font-bold uppercase tracking-[0.1em] text-white/20 px-[10px] block"
            >
              Academics
            </span>
          </div>
          <router-link
            to="/academics/attendance"
            class="flex items-center gap-[10px] px-[10px] py-[9px] rounded-[9px] text-[13.5px] font-medium text-white/50 transition-all duration-150 cursor-pointer mb-[1px] hover:bg-white/[0.07] hover:text-white/85 relative group"
            active-class="bg-[rgba(211,47,47,0.12)] text-red-300 active-nav-item hover:bg-[rgba(211,47,47,0.12)] hover:text-red-300"
          >
            <div
              class="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-[20px] bg-school-red rounded-[0_3px_3px_0] hidden"
            ></div>
            <svg
              class="w-[17px] h-[17px] shrink-0 opacity-70 group-hover:opacity-100 transition-opacity nav-icon"
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
            Roll Call
          </router-link>
          <router-link
            to="/academics"
            class="flex items-center gap-[10px] px-[10px] py-[9px] rounded-[9px] text-[13.5px] font-medium text-white/50 transition-all duration-150 cursor-pointer mb-[1px] hover:bg-white/[0.07] hover:text-white/85 relative group"
            active-class="bg-[rgba(211,47,47,0.12)] text-red-300 active-nav-item hover:bg-[rgba(211,47,47,0.12)] hover:text-red-300"
          >
            <div
              class="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-[20px] bg-school-red rounded-[0_3px_3px_0] hidden"
            ></div>
            <svg
              class="w-[17px] h-[17px] shrink-0 opacity-70 group-hover:opacity-100 transition-opacity nav-icon"
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
            Grading
          </router-link>
          <router-link
            to="/academics/report-card"
            class="flex items-center gap-[10px] px-[10px] py-[9px] rounded-[9px] text-[13.5px] font-medium text-white/50 transition-all duration-150 cursor-pointer mb-[1px] hover:bg-white/[0.07] hover:text-white/85 relative group"
            active-class="bg-[rgba(211,47,47,0.12)] text-red-300 active-nav-item hover:bg-[rgba(211,47,47,0.12)] hover:text-red-300"
          >
            <div
              class="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-[20px] bg-school-red rounded-[0_3px_3px_0] hidden"
            ></div>
            <svg
              class="w-[17px] h-[17px] shrink-0 opacity-70 group-hover:opacity-100 transition-opacity nav-icon"
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
            Report Cards
          </router-link>
        </template>

        <template v-if="['secretary', 'principal', 'admin'].includes(userRole)">
          <div class="pt-[16px] pb-[5px]">
            <span
              class="text-[9.5px] font-bold uppercase tracking-[0.1em] text-white/20 px-[10px] block"
            >
              Administration
            </span>
          </div>
          <router-link
            to="/office"
            class="flex items-center gap-[10px] px-[10px] py-[9px] rounded-[9px] text-[13.5px] font-medium text-white/50 transition-all duration-150 cursor-pointer mb-[1px] hover:bg-white/[0.07] hover:text-white/85 relative group"
            active-class="bg-[rgba(211,47,47,0.12)] text-red-300 active-nav-item hover:bg-[rgba(211,47,47,0.12)] hover:text-red-300"
          >
            <div
              class="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-[20px] bg-school-red rounded-[0_3px_3px_0] hidden"
            ></div>
            <svg
              class="w-[17px] h-[17px] shrink-0 opacity-70 group-hover:opacity-100 transition-opacity nav-icon"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              viewBox="0 0 24 24"
            >
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
              <rect x="9" y="14" width="6" height="7" />
            </svg>
            Office
          </router-link>
        </template>

        <template v-if="['finance', 'principal', 'admin'].includes(userRole)">
          <div class="pt-[16px] pb-[5px]">
            <span
              class="text-[9.5px] font-bold uppercase tracking-[0.1em] text-white/20 px-[10px] block"
            >
              Finance
            </span>
          </div>
          <router-link
            to="/finance"
            class="flex items-center gap-[10px] px-[10px] py-[9px] rounded-[9px] text-[13.5px] font-medium text-white/50 transition-all duration-150 cursor-pointer mb-[1px] hover:bg-white/[0.07] hover:text-white/85 relative group"
            active-class="bg-[rgba(211,47,47,0.12)] text-red-300 active-nav-item hover:bg-[rgba(211,47,47,0.12)] hover:text-red-300"
          >
            <div
              class="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-[20px] bg-school-red rounded-[0_3px_3px_0] hidden"
            ></div>
            <svg
              class="w-[17px] h-[17px] shrink-0 opacity-70 group-hover:opacity-100 transition-opacity nav-icon"
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
            Dashboard
          </router-link>
          <router-link
            to="/finance/statements"
            class="flex items-center gap-[10px] px-[10px] py-[9px] rounded-[9px] text-[13.5px] font-medium text-white/50 transition-all duration-150 cursor-pointer mb-[1px] hover:bg-white/[0.07] hover:text-white/85 relative group"
            active-class="bg-[rgba(211,47,47,0.12)] text-red-300 active-nav-item hover:bg-[rgba(211,47,47,0.12)] hover:text-red-300"
          >
            <div
              class="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-[20px] bg-school-red rounded-[0_3px_3px_0] hidden"
            ></div>
            <svg
              class="w-[17px] h-[17px] shrink-0 opacity-70 group-hover:opacity-100 transition-opacity nav-icon"
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
            Statements
          </router-link>
        </template>

        <template v-if="['admin', 'principal'].includes(userRole)">
          <div class="pt-[16px] pb-[5px]">
            <span
              class="text-[9.5px] font-bold uppercase tracking-[0.1em] text-white/20 px-[10px] block"
            >
              System
            </span>
          </div>
          <router-link
            v-if="userRole === 'admin'"
            to="/admin"
            class="flex items-center gap-[10px] px-[10px] py-[9px] rounded-[9px] text-[13.5px] font-medium text-white/50 transition-all duration-150 cursor-pointer mb-[1px] hover:bg-white/[0.07] hover:text-white/85 relative group"
            active-class="bg-[rgba(211,47,47,0.12)] text-red-300 active-nav-item hover:bg-[rgba(211,47,47,0.12)] hover:text-red-300"
          >
            <div
              class="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-[20px] bg-school-red rounded-[0_3px_3px_0] hidden"
            ></div>
            <svg
              class="w-[17px] h-[17px] shrink-0 opacity-70 group-hover:opacity-100 transition-opacity nav-icon"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              viewBox="0 0 24 24"
            >
              <circle cx="12" cy="12" r="3" />
              <path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14" />
            </svg>
            Console
          </router-link>
          <router-link
            to="/hr"
            class="flex items-center gap-[10px] px-[10px] py-[9px] rounded-[9px] text-[13.5px] font-medium text-white/50 transition-all duration-150 cursor-pointer mb-[1px] hover:bg-white/[0.07] hover:text-white/85 relative group"
            active-class="bg-[rgba(211,47,47,0.12)] text-red-300 active-nav-item hover:bg-[rgba(211,47,47,0.12)] hover:text-red-300"
          >
            <div
              class="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-[20px] bg-school-red rounded-[0_3px_3px_0] hidden"
            ></div>
            <svg
              class="w-[17px] h-[17px] shrink-0 opacity-70 group-hover:opacity-100 transition-opacity nav-icon"
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
            HR
          </router-link>
        </template>
      </nav>

      <!-- Sidebar Footer (Logout) -->
      <div class="border-t border-white/[0.06] p-[14px_10px] relative z-10 bg-school-navy">
        <div
          class="flex items-center gap-[10px] p-[9px_10px] rounded-[9px] bg-white/[0.05] cursor-pointer hover:bg-white/[0.08] transition-all"
        >
          <div
            class="w-[32px] h-[32px] rounded-full bg-gradient-to-br from-school-red to-red-400 font-heading font-bold text-[12px] text-white flex items-center justify-center flex-shrink-0"
          >
            {{ userNameInitial }}
          </div>
          <div class="overflow-hidden">
            <p class="text-[13px] font-semibold text-white truncate">{{ userName }}</p>
            <p class="text-[10.5px] text-white/30 mt-[1px] truncate">{{ userRole }}</p>
          </div>
          <svg
            class="ml-auto opacity-30 flex-shrink-0 w-[14px] h-[14px]"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            viewBox="0 0 24 24"
          >
            <circle cx="12" cy="5" r="1" />
            <circle cx="12" cy="12" r="1" />
            <circle cx="12" cy="19" r="1" />
          </svg>
        </div>
        <button
          @click="logout"
          class="w-full flex items-center justify-center gap-2 p-[7px_10px] rounded-[8px] cursor-pointer mt-[4px] text-white/30 text-[12.5px] font-medium transition-all hover:bg-[rgba(211,47,47,0.12)] hover:text-red-300"
        >
          <svg
            class="w-[14px] h-[14px]"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            viewBox="0 0 24 24"
          >
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
          Sign Out
        </button>
      </div>
    </aside>

    <!-- MAIN CONTENT WRAPPER -->
    <div class="flex-1 flex flex-col min-w-0 bg-school-grey overflow-hidden relative">
      <!-- TOP NAVIGATION BAR -->
      <header
        class="bg-white h-[62px] px-[30px] flex items-center justify-between border-b border-[#E2E8F0] sticky top-0 z-50 shrink-0"
      >
        <!-- Mobile Menu Button -->
        <button
          @click="isSidebarOpen = true"
          class="md:hidden p-2 -ml-4 text-school-navy bg-white hover:bg-slate-50 rounded-lg focus:outline-none transition-all"
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
            <path d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>

        <!-- Contextual Header Area (Breadcrumbs) -->
        <div class="hidden md:flex flex-col">
          <div class="text-[11px] font-semibold uppercase tracking-[0.06em] text-[#94A3B8]">
            {{ routeName }}
          </div>
          <h1 class="font-heading text-[17px] font-bold text-[#0F172A] leading-tight">
            {{ pageTitle }}
          </h1>
        </div>
        <div class="md:hidden font-heading text-[17px] font-bold text-[#0F172A] leading-tight">
          Bona School
        </div>

        <!-- Right Side: Search, Term Selector, Notifications -->
        <div class="flex items-center gap-[10px] ml-auto">
          <!-- Search Bar -->
          <div
            class="hidden lg:flex items-center gap-2 bg-school-grey border border-[#E2E8F0] rounded-[9px] px-[14px] py-[7px] cursor-text hover:border-[#CBD5E1] transition-all"
          >
            <svg
              class="w-[14px] h-[14px] text-[#94A3B8]"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              viewBox="0 0 24 24"
            >
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input
              type="text"
              placeholder="Search..."
              class="bg-transparent border-none outline-none text-[13px] w-48 text-[#94A3B8] placeholder-[#94A3B8]"
            />
          </div>

          <!-- Global Term Selector -->
          <div class="relative group">
            <div
              class="flex items-center gap-[7px] px-[14px] py-[7px] bg-school-grey border border-[#E2E8F0] rounded-[9px] cursor-pointer hover:border-school-red hover:text-school-red transition-all relative text-[#0F172A]"
            >
              <span class="w-[7px] h-[7px] rounded-full bg-emerald-500 shrink-0"></span>
              <select
                v-model="appStore.currentTerm"
                class="bg-transparent text-[13px] font-semibold outline-none cursor-pointer appearance-none pr-5 z-10 relative"
              >
                <option v-for="term in appStore.terms" :key="term" :value="term">{{ term }}</option>
              </select>
              <svg
                class="w-[14px] h-[14px] absolute right-3 pointer-events-none"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                viewBox="0 0 24 24"
              >
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </div>
          </div>

          <!-- Notification Bell -->
          <button
            class="w-[38px] h-[38px] rounded-[9px] bg-school-grey border border-[#E2E8F0] flex items-center justify-center cursor-pointer hover:bg-white hover:border-[#CBD5E1] text-[#475569] relative transition-all"
          >
            <svg
              class="w-[17px] h-[17px]"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              viewBox="0 0 24 24"
            >
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
              <path d="M13.73 21a2 2 0 0 1-3.46 0" />
            </svg>
            <span
              class="absolute top-[7px] right-[7px] w-[7px] h-[7px] rounded-full bg-school-red border-[1.5px] border-white"
            ></span>
          </button>
        </div>
      </header>

      <!-- DYNAMIC PAGE CONTENT WITH TRANSITIONS -->
      <main class="flex-1 overflow-y-auto p-4 sm:p-8 relative z-10">
        <router-view v-slot="{ Component }">
          <transition name="fade-scale" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const appStore = useAppStore()

const isSidebarOpen = ref(false)

// Close sidebar on route change for mobile
watch(
  () => route.path,
  () => {
    isSidebarOpen.value = false
  },
)

const routeName = computed(() => {
  const path = route.path
  if (path.startsWith('/academics')) return 'Academics'
  if (path.startsWith('/finance')) return 'Finance'
  if (path.startsWith('/office')) return 'Administration'
  if (path.startsWith('/admin')) return 'System'
  return 'Overview'
})

const pageTitle = computed(() => {
  const name = route.name
  if (name === 'dashboard') return 'Dashboard'
  if (name === 'admin-dash') return 'Admin Console'
  if (name === 'staff-directory') return 'Staff Directory'
  if (name === 'secretary-dash') return 'Office & Admissions'
  if (name === 'finance-dash') return 'Finance Dashboard'
  if (name === 'fee-statement') return 'Statements'
  if (name === 'teacher-dash') return 'Grading'
  if (name === 'report-card') return 'Report Cards'
  if (name === 'attendance-page') return 'Roll Call'
  return 'Overview'
})

// Extract user details from the store
const userRole = computed(() => {
  if (authStore.user?.role) {
    return authStore.user.role
  }
  return 'guest'
})

const userName = computed(() => {
  if (authStore.user?.name) {
    return authStore.user.name
  }
  return 'User'
})

const userNameInitial = computed(() => {
  return userName.value.charAt(0).toUpperCase()
})

const logout = () => {
  // Use the auth store's logout method
  authStore.logout()

  // Redirect to login
  router.push('/login')
}
</script>

<style scoped>
/* Extravagant Router Transitions */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.3s ease;
}
.fade-scale-enter-from {
  opacity: 0;
}
.fade-scale-leave-to {
  opacity: 0;
}

/* Hide scrollbar for sidebar nav */
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

/* Nav item active accent */
.active-nav-item div {
  display: block;
}
.active-nav-item .nav-icon {
  opacity: 1;
}
</style>
