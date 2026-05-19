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
      <div
        class="absolute -top-32 -left-32 w-64 h-64 bg-school-red/40 rounded-full blur-[80px] animate-pulse-glow"
      ></div>
      <div
        class="absolute bottom-0 right-0 w-80 h-80 bg-blue-500/20 rounded-full blur-[100px] animate-float"
      ></div>

      <!-- Sidebar Header (Logo Area) -->
      <div
        class="relative flex items-center justify-center h-24 border-b border-white/10 px-6 bg-white/5 backdrop-blur-md"
      >
        <div class="text-center transform hover:scale-110 transition-transform duration-300">
          <h2
            class="text-2xl font-black font-heading text-transparent bg-clip-text bg-gradient-to-r from-white via-red-200 to-white animate-gradient-xy tracking-widest uppercase filter drop-shadow-[0_0_10px_rgba(255,255,255,0.5)]"
          >
            Bona School
          </h2>
          <p class="text-[10px] text-red-200 mt-1 uppercase tracking-widest animate-pulse">
            CBC Management
          </p>
        </div>
      </div>

      <!-- Navigation Links -->
      <nav class="relative flex-1 px-4 py-8 space-y-2 overflow-y-auto z-10">
        <router-link
          to="/"
          class="flex items-center gap-4 px-4 py-3.5 text-sm font-bold rounded-xl text-slate-300 hover:bg-white/10 hover:text-white hover:scale-105 hover:shadow-[0_0_15px_rgba(255,255,255,0.1)] transition-all duration-300 group"
          active-class="bg-gradient-to-r from-school-red/80 to-school-red/20 text-white shadow-[0_0_20px_rgba(211,47,47,0.6)] border-l-4 border-white scale-105"
        >
          <span class="text-xl group-hover:animate-bounce">🏠</span> Dashboard
        </router-link>

        <template v-if="['senior_teacher', 'principal', 'admin'].includes(userRole)">
          <div class="pt-6 pb-2">
            <p
              class="px-4 text-[10px] font-black text-red-300/80 uppercase tracking-[0.2em] animate-pulse"
            >
              Academics
            </p>
          </div>
          <router-link
            to="/academics/attendance"
            class="flex items-center gap-4 px-4 py-3.5 text-sm font-bold rounded-xl text-slate-300 hover:bg-white/10 hover:text-white hover:scale-105 transition-all duration-300 group"
            active-class="bg-gradient-to-r from-school-red/80 to-school-red/20 text-white shadow-[0_0_20px_rgba(211,47,47,0.6)] border-l-4 border-white scale-105"
          >
            <span class="text-xl group-hover:animate-spin-slow">📋</span> Roll Call
          </router-link>
          <router-link
            to="/academics"
            class="flex items-center gap-4 px-4 py-3.5 text-sm font-bold rounded-xl text-slate-300 hover:bg-white/10 hover:text-white hover:scale-105 transition-all duration-300 group"
            active-class="bg-gradient-to-r from-school-red/80 to-school-red/20 text-white shadow-[0_0_20px_rgba(211,47,47,0.6)] border-l-4 border-white scale-105"
          >
            <span class="text-xl group-hover:animate-float">📝</span> Grading
          </router-link>
          <router-link
            to="/academics/report-card"
            class="flex items-center gap-4 px-4 py-3.5 text-sm font-bold rounded-xl text-slate-300 hover:bg-white/10 hover:text-white hover:scale-105 transition-all duration-300 group"
            active-class="bg-gradient-to-r from-school-red/80 to-school-red/20 text-white shadow-[0_0_20px_rgba(211,47,47,0.6)] border-l-4 border-white scale-105"
          >
            <span class="text-xl group-hover:animate-pulse">🎓</span> Report Cards
          </router-link>
        </template>

        <template v-if="['secretary', 'principal', 'admin'].includes(userRole)">
          <div class="pt-6 pb-2">
            <p
              class="px-4 text-[10px] font-black text-red-300/80 uppercase tracking-[0.2em] animate-pulse"
            >
              Administration
            </p>
          </div>
          <router-link
            to="/office"
            class="flex items-center gap-4 px-4 py-3.5 text-sm font-bold rounded-xl text-slate-300 hover:bg-white/10 hover:text-white hover:scale-105 transition-all duration-300 group"
            active-class="bg-gradient-to-r from-school-red/80 to-school-red/20 text-white shadow-[0_0_20px_rgba(211,47,47,0.6)] border-l-4 border-white scale-105"
          >
            <span class="text-xl group-hover:animate-bounce">👨‍🎓</span> Office
          </router-link>
        </template>

        <template v-if="['finance', 'principal', 'admin'].includes(userRole)">
          <div class="pt-6 pb-2">
            <p
              class="px-4 text-[10px] font-black text-red-300/80 uppercase tracking-[0.2em] animate-pulse"
            >
              Finance
            </p>
          </div>
          <router-link
            to="/finance"
            class="flex items-center gap-4 px-4 py-3.5 text-sm font-bold rounded-xl text-slate-300 hover:bg-white/10 hover:text-white hover:scale-105 transition-all duration-300 group"
            active-class="bg-gradient-to-r from-school-red/80 to-school-red/20 text-white shadow-[0_0_20px_rgba(211,47,47,0.6)] border-l-4 border-white scale-105"
          >
            <span class="text-xl group-hover:animate-spin-slow">💰</span> Dashboard
          </router-link>
          <router-link
            to="/finance/statements"
            class="flex items-center gap-4 px-4 py-3.5 text-sm font-bold rounded-xl text-slate-300 hover:bg-white/10 hover:text-white hover:scale-105 transition-all duration-300 group"
            active-class="bg-gradient-to-r from-school-red/80 to-school-red/20 text-white shadow-[0_0_20px_rgba(211,47,47,0.6)] border-l-4 border-white scale-105"
          >
            <span class="text-xl group-hover:animate-float">📄</span> Statements
          </router-link>
        </template>

        <template v-if="['admin', 'principal'].includes(userRole)">
          <div class="pt-6 pb-2">
            <p
              class="px-4 text-[10px] font-black text-red-300/80 uppercase tracking-[0.2em] animate-pulse"
            >
              System
            </p>
          </div>
          <router-link
            v-if="userRole === 'admin'"
            to="/admin"
            class="flex items-center gap-4 px-4 py-3.5 text-sm font-bold rounded-xl text-slate-300 hover:bg-white/10 hover:text-white hover:scale-105 transition-all duration-300 group"
            active-class="bg-gradient-to-r from-school-red/80 to-school-red/20 text-white shadow-[0_0_20px_rgba(211,47,47,0.6)] border-l-4 border-white scale-105"
          >
            <span class="text-xl group-hover:animate-spin-slow">⚙️</span> Console
          </router-link>
          <router-link
            to="/hr"
            class="flex items-center gap-4 px-4 py-3.5 text-sm font-bold rounded-xl text-slate-300 hover:bg-white/10 hover:text-white hover:scale-105 transition-all duration-300 group"
            active-class="bg-gradient-to-r from-school-red/80 to-school-red/20 text-white shadow-[0_0_20px_rgba(211,47,47,0.6)] border-l-4 border-white scale-105"
          >
            <span class="text-xl group-hover:animate-pulse">🛡️</span> HR
          </router-link>
        </template>
      </nav>

      <!-- Sidebar Footer (Logout) -->
      <div class="relative p-4 border-t border-white/10 bg-black/20 backdrop-blur-md">
        <div
          class="flex items-center mb-4 px-2 hover:translate-x-2 transition-transform duration-300"
        >
          <div
            class="h-12 w-12 rounded-full bg-gradient-to-tr from-school-red to-orange-500 flex items-center justify-center text-white font-black uppercase mr-3 shadow-[0_0_15px_rgba(211,47,47,0.8)] border-2 border-white animate-pulse-glow"
          >
            {{ userNameInitial }}
          </div>
          <div class="overflow-hidden">
            <p class="text-base font-black font-heading text-white truncate drop-shadow-md">
              {{ userName }}
            </p>
            <p class="text-[10px] text-red-200 uppercase tracking-widest truncate font-bold">
              {{ userRole }}
            </p>
          </div>
        </div>
        <button
          @click="logout"
          class="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-white/5 to-white/10 hover:from-school-red hover:to-red-600 text-white py-3 rounded-xl transition-all duration-500 text-sm font-bold border border-white/10 hover:border-transparent hover:shadow-[0_0_20px_rgba(211,47,47,0.8)] group hover:-translate-y-1"
        >
          <svg
            class="w-5 h-5 text-red-300 group-hover:text-white transition-colors group-hover:animate-bounce"
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
    <div class="flex-1 flex flex-col min-w-0 bg-[#f8f9fc] overflow-hidden relative">
      <!-- Animated Background elements for main content -->
      <div
        class="absolute top-0 right-0 w-full h-[500px] bg-gradient-to-b from-school-navy/5 to-transparent pointer-events-none"
      ></div>

      <!-- TOP NAVIGATION BAR -->
      <header
        class="bg-white/60 backdrop-blur-xl border-b border-white shadow-[0_4px_30px_rgba(0,0,0,0.05)] h-24 flex items-center justify-between px-8 z-30 shrink-0 sticky top-0"
      >
        <!-- Mobile Menu Button -->
        <button
          @click="isSidebarOpen = true"
          class="md:hidden p-3 -ml-2 text-school-navy bg-white shadow-md hover:shadow-lg rounded-xl focus:outline-none transition-all hover:scale-110 active:scale-95"
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
            class="flex items-center gap-2 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-1.5"
          >
            <span class="hover:text-school-navy transition-colors cursor-pointer">{{
              routeName
            }}</span>
            <span class="text-slate-300">/</span>
            <span class="text-school-red animate-pulse">{{ pageTitle }}</span>
          </div>
          <h1
            class="text-3xl font-black font-heading text-transparent bg-clip-text bg-gradient-to-r from-school-navy to-blue-600 tracking-tight leading-none drop-shadow-sm hover:scale-105 origin-left transition-transform duration-300"
          >
            {{ pageTitle }}
          </h1>
        </div>
        <div
          class="md:hidden text-xl font-black font-heading text-school-navy tracking-tight drop-shadow-sm"
        >
          Bona School
        </div>

        <!-- Right Side: Search, Term Selector, Notifications -->
        <div class="flex items-center gap-6 ml-auto">
          <!-- Search Bar -->
          <div
            class="hidden lg:flex items-center bg-white border border-slate-100 rounded-2xl px-5 py-3 hover:border-blue-300 transition-all shadow-[0_5px_15px_rgba(0,0,0,0.05)] hover:shadow-[0_8px_25px_rgba(10,25,47,0.1)] group w-72 hover:w-80 duration-500 ease-out focus-within:w-80 focus-within:border-school-navy focus-within:ring-4 ring-school-navy/10"
          >
            <svg
              class="w-5 h-5 text-slate-300 group-hover:text-school-navy transition-colors mr-3 group-hover:animate-spin-slow"
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
              placeholder="Search the extravagant..."
              class="bg-transparent border-none outline-none text-sm w-full text-slate-700 placeholder-slate-300 font-bold"
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
                class="w-5 h-5 text-school-red mr-3 animate-pulse"
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
                class="bg-transparent text-sm font-black text-school-navy outline-none cursor-pointer appearance-none pr-4 uppercase tracking-wider"
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
              class="relative p-3.5 text-slate-400 hover:text-white hover:bg-school-navy rounded-full transition-all duration-300 focus:outline-none bg-white shadow-[0_5px_15px_rgba(0,0,0,0.05)] hover:shadow-lg hover:scale-110 active:scale-95 border border-slate-100 group-hover:border-transparent"
            >
              <svg
                class="w-6 h-6 group-hover:animate-bounce-slow"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                ></path>
              </svg>
              <span
                class="absolute top-2.5 right-2.5 block h-3 w-3 rounded-full bg-gradient-to-r from-school-red to-orange-500 ring-4 ring-white animate-pulse"
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
