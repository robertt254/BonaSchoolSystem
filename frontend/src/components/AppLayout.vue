<template>
  <div class="flex h-screen bg-school-grey font-sans relative overflow-hidden">
    <!-- Mobile Sidebar Overlay -->
    <div
      v-if="isSidebarOpen"
      @click="isSidebarOpen = false"
      class="fixed inset-0 bg-school-navy/50 z-20 md:hidden transition-opacity"
    ></div>

    <!-- SIDEBAR -->
    <aside
      :class="[
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
        'fixed inset-y-0 left-0 z-40 w-72 bg-gradient-to-br from-school-navy via-[#1A2A42] to-school-navy text-white transition-all duration-500 ease-out transform md:relative md:translate-x-0 flex flex-col border-r border-white/10 overflow-hidden shadow-[10px_0_30px_rgba(0,0,0,0.5)]',
      ]"
    >
      <!-- Extravagant glowing orbs -->

      <!-- Sidebar Header (Logo Area) -->
      <div
        class="flex items-center justify-center h-20 border-b border-white/10 px-6 bg-school-navy"
      >
        <div class="text-center">
          <h2 class="text-xl font-medium font-heading text-white tracking-widest uppercase">
            Bona School
          </h2>
          <p class="text-[10px] text-slate-400 mt-1 uppercase tracking-widest">CBC Management</p>
        </div>
      </div>

      <!-- Navigation Links -->
      <nav class="relative flex-1 px-4 py-8 space-y-2 overflow-y-auto z-10">
        <router-link
          to="/"
          class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl text-slate-300 hover:bg-white/10 hover:text-white transition-colors duration-200 group"
          active-class="bg-white/10 text-white border-l-4 border-school-red rounded-l-none"
        >
          <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
            />
          </svg>
          Dashboard
        </router-link>

        <template v-if="['senior_teacher', 'principal', 'admin'].includes(userRole)">
          <div class="pt-6 pb-2">
            <p class="px-4 text-[10px] font-medium text-slate-400 uppercase tracking-widest">
              Academics
            </p>
          </div>
          <router-link
            to="/academics/attendance"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl text-slate-300 hover:bg-white/10 hover:text-white transition-colors duration-200 group"
            active-class="bg-white/10 text-white border-l-4 border-school-red rounded-l-none"
          >
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
              />
            </svg>
            Roll Call
          </router-link>
          <router-link
            to="/academics"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl text-slate-300 hover:bg-white/10 hover:text-white transition-colors duration-200 group"
            active-class="bg-white/10 text-white border-l-4 border-school-red rounded-l-none"
          >
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
            Grading
          </router-link>
          <router-link
            to="/academics/report-card"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl text-slate-300 hover:bg-white/10 hover:text-white transition-colors duration-200 group"
            active-class="bg-white/10 text-white border-l-4 border-school-red rounded-l-none"
          >
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 14l9-5-9-5-9 5 9 5z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222"
              />
            </svg>
            Report Cards
          </router-link>
        </template>

        <template v-if="['secretary', 'principal', 'admin'].includes(userRole)">
          <div class="pt-6 pb-2">
            <p class="px-4 text-[10px] font-medium text-slate-400 uppercase tracking-widest">
              Administration
            </p>
          </div>
          <router-link
            to="/office"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl text-slate-300 hover:bg-white/10 hover:text-white transition-colors duration-200 group"
            active-class="bg-white/10 text-white border-l-4 border-school-red rounded-l-none"
          >
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
              />
            </svg>
            Office
          </router-link>
        </template>

        <template v-if="['finance', 'principal', 'admin'].includes(userRole)">
          <div class="pt-6 pb-2">
            <p class="px-4 text-[10px] font-medium text-slate-400 uppercase tracking-widest">
              Finance
            </p>
          </div>
          <router-link
            to="/finance"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl text-slate-300 hover:bg-white/10 hover:text-white transition-colors duration-200 group"
            active-class="bg-white/10 text-white border-l-4 border-school-red rounded-l-none"
          >
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            Dashboard
          </router-link>
          <router-link
            to="/finance/statements"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl text-slate-300 hover:bg-white/10 hover:text-white transition-colors duration-200 group"
            active-class="bg-white/10 text-white border-l-4 border-school-red rounded-l-none"
          >
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            Statements
          </router-link>
        </template>

        <template v-if="['admin', 'principal'].includes(userRole)">
          <div class="pt-6 pb-2">
            <p class="px-4 text-[10px] font-medium text-slate-400 uppercase tracking-widest">
              System
            </p>
          </div>
          <router-link
            v-if="userRole === 'admin'"
            to="/admin"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl text-slate-300 hover:bg-white/10 hover:text-white transition-colors duration-200 group"
            active-class="bg-white/10 text-white border-l-4 border-school-red rounded-l-none"
          >
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
            </svg>
            Console
          </router-link>
          <router-link
            to="/hr"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl text-slate-300 hover:bg-white/10 hover:text-white transition-colors duration-200 group"
            active-class="bg-white/10 text-white border-l-4 border-school-red rounded-l-none"
          >
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
              />
            </svg>
            HR
          </router-link>
        </template>
      </nav>

      <!-- Sidebar Footer (Logout) -->
      <div class="relative p-4 border-t border-white/10 bg-black/20 backdrop-blur-md">
        <div
          class="flex items-center mb-4 px-2 hover:translate-x-2 transition-transform duration-300"
        >
          <div
            class="h-10 w-10 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-white font-semibold uppercase mr-3"
          >
            {{ userNameInitial }}
          </div>
          <div class="overflow-hidden">
            <p class="text-base font-medium font-heading text-white truncate drop-shadow-md">
              {{ userName }}
            </p>
            <p class="text-[10px] text-red-200 uppercase tracking-widest truncate font-medium">
              {{ userRole }}
            </p>
          </div>
        </div>
        <button
          @click="logout"
          class="w-full flex items-center justify-center gap-2 bg-slate-800/50 hover:bg-school-red text-white py-3 rounded-xl transition-all duration-500 text-sm font-medium border border-white/10 hover:border-transparent hover: group"
        >
          <svg
            class="w-5 h-5 text-red-300 group-hover:text-white transition-colors"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2.5"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
            ></path>
          </svg>
          SIGN OUT
        </button>
      </div>
    </aside>

    <!-- MAIN CONTENT WRAPPER -->
    <div class="flex-1 flex flex-col min-w-0 bg-school-grey overflow-hidden relative">
      <!-- TOP NAVIGATION BAR -->
      <header
        class="bg-white border-b border-slate-200 h-20 flex items-center justify-between px-8 z-30 shrink-0 sticky top-0"
      >
        <!-- Mobile Menu Button -->
        <button
          @click="isSidebarOpen = true"
          class="md:hidden p-3 -ml-2 text-school-navy bg-white shadow-md hover:shadow-lg rounded-xl focus:outline-none transition-all"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            ></path>
          </svg>
        </button>

        <!-- Contextual Header Area (Breadcrumbs) -->
        <div class="hidden md:flex flex-col animate-slide-up">
          <div
            class="flex items-center gap-2 text-[10px] font-medium text-slate-400 uppercase tracking-[0.2em] mb-1.5"
          >
            <span class="hover:text-school-navy transition-colors cursor-pointer">{{
              routeName
            }}</span>
            <span class="text-slate-300">/</span>
            <span class="text-school-red">{{ pageTitle }}</span>
          </div>
          <h1
            class="text-3xl font-medium font-heading text-transparent bg-clip-text bg-gradient-to-r from-school-navy to-blue-600 tracking-tight leading-none drop-shadow-sm hover:scale-105 origin-left transition-transform duration-300"
          >
            {{ pageTitle }}
          </h1>
        </div>
        <div
          class="md:hidden text-xl font-medium font-heading text-school-navy tracking-tight drop-shadow-sm"
        >
          Bona School
        </div>

        <!-- Right Side: Search, Term Selector, Notifications -->
        <div class="flex items-center gap-6 ml-auto">
          <!-- Search Bar -->
          <div
            class="hidden lg:flex items-center bg-white border border-slate-100 rounded-2xl px-5 py-3 hover:border-blue-300 transition-all shadow-[0_5px_15px_rgba(0,0,0,0.05)] w-64 focus-within:ring-2 focus-within:border-school-navy focus-within:ring-4 ring-school-navy/10"
          >
            <svg
              class="w-5 h-5 text-slate-300 group-hover:text-school-navy transition-colors mr-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2.5"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              ></path>
            </svg>
            <input
              type="text"
              placeholder="Search students, staff..."
              class="bg-transparent border-none outline-none text-sm w-full text-slate-700 placeholder-slate-300 font-medium"
            />
          </div>

          <!-- Global Term Selector -->
          <div class="relative group">
            <div
              class="absolute -inset-1 bg-gradient-to-r from-school-red to-orange-400 rounded-2xl blur opacity-20 group-hover:opacity-60 transition duration-500 group-hover:duration-200"
            ></div>
            <div
              class="relative flex items-center bg-white border border-slate-100 rounded-2xl px-5 py-3 shadow-sm hover:shadow-md transition-all"
            >
              <svg
                class="w-5 h-5 text-school-red mr-3"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                ></path>
              </svg>
              <select
                v-model="appStore.currentTerm"
                class="bg-transparent text-sm font-medium text-school-navy outline-none cursor-pointer appearance-none pr-4 uppercase tracking-wider"
              >
                <option v-for="term in appStore.terms" :key="term" :value="term">{{ term }}</option>
              </select>
            </div>
          </div>

          <!-- Notification Bell -->
          <div class="relative group">
            <div
              class="absolute -inset-1 bg-gradient-to-r from-blue-400 to-school-navy rounded-full blur opacity-0 group-hover:opacity-40 transition duration-500"
            ></div>
            <button
              class="relative p-3.5 text-slate-400 hover:text-white hover:bg-school-navy rounded-full transition-all duration-300 focus:outline-none bg-white shadow-[0_5px_15px_rgba(0,0,0,0.05)] hover:shadow-lg border border-slate-100 group-hover:border-transparent"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                ></path>
              </svg>
              <span
                class="absolute top-2.5 right-2.5 block h-3 w-3 rounded-full bg-gradient-to-r from-school-red to-orange-500 ring-4 ring-white"
              ></span>
            </button>
          </div>
        </div>
      </header>

      <!-- DYNAMIC PAGE CONTENT WITH TRANSITIONS -->
      <main class="flex-1 overflow-y-auto p-4 sm:p-10 relative z-10">
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
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.fade-scale-enter-from {
  opacity: 0;
  transform: scale(0.95) translateY(20px) rotateX(-10deg);
}
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(1.05) translateY(-20px) rotateX(10deg);
}

/* Custom scrollbar for sidebar */
aside nav::-webkit-scrollbar {
  width: 4px;
}
aside nav::-webkit-scrollbar-track {
  background: transparent;
}
aside nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}
aside nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
