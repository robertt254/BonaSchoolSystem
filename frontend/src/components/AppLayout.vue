<template>
  <div class="flex h-screen bg-school-grey font-sans overflow-hidden">
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
        'fixed inset-y-0 left-0 z-30 w-72 bg-school-navy text-white transition-transform duration-300 ease-in-out transform md:relative md:translate-x-0 flex flex-col shadow-2xl border-r border-slate-800',
      ]"
    >
      <!-- Sidebar Header (Logo Area) -->
      <div class="flex items-center justify-center h-20 border-b border-slate-800 px-6">
        <div class="text-center">
          <h2 class="text-xl font-black text-white tracking-widest uppercase">The Bona School</h2>
          <p class="text-[10px] text-slate-400 mt-1 uppercase tracking-widest">CBC Management</p>
        </div>
      </div>

      <!-- Navigation Links -->
      <nav class="flex-1 px-4 py-8 space-y-1 overflow-y-auto">
        <router-link
          to="/"
          class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg text-slate-300 hover:bg-white/5 hover:text-white transition-all duration-200"
          active-class="bg-school-navy shadow-inner text-white border-l-4 border-school-red rounded-l-none"
        >
          <span class="text-lg">🏠</span> Dashboard
        </router-link>

        <template v-if="['senior_teacher', 'principal', 'admin'].includes(userRole)">
          <div class="pt-6 pb-2">
            <p class="px-4 text-xs font-bold text-slate-500 uppercase tracking-widest">Academics</p>
          </div>
          <router-link
            to="/academics/attendance"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg text-slate-300 hover:bg-white/5 hover:text-white transition-all duration-200"
            active-class="bg-school-navy shadow-inner text-white border-l-4 border-school-red rounded-l-none"
          >
            <span class="text-lg">📋</span> Roll Call
          </router-link>
          <router-link
            to="/academics"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg text-slate-300 hover:bg-white/5 hover:text-white transition-all duration-200"
            active-class="bg-school-navy shadow-inner text-white border-l-4 border-school-red rounded-l-none"
          >
            <span class="text-lg">📝</span> Grading
          </router-link>
          <router-link
            to="/academics/report-card"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg text-slate-300 hover:bg-white/5 hover:text-white transition-all duration-200"
            active-class="bg-school-navy shadow-inner text-white border-l-4 border-school-red rounded-l-none"
          >
            <span class="text-lg">🎓</span> Report Cards
          </router-link>
        </template>

        <template v-if="['principal', 'secretary', 'admin'].includes(userRole)">
          <div class="pt-6 pb-2">
            <p class="px-4 text-xs font-bold text-slate-500 uppercase tracking-widest">
              Administration
            </p>
          </div>
          <router-link
            to="/office"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg text-slate-300 hover:bg-white/5 hover:text-white transition-all duration-200"
            active-class="bg-school-navy shadow-inner text-white border-l-4 border-school-red rounded-l-none"
          >
            <span class="text-lg">👨‍🎓</span> Office & Admissions
          </router-link>
        </template>

        <template v-if="['finance', 'principal', 'admin'].includes(userRole)">
          <div class="pt-6 pb-2">
            <p class="px-4 text-xs font-bold text-slate-500 uppercase tracking-widest">Finance</p>
          </div>
          <router-link
            to="/finance"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg text-slate-300 hover:bg-white/5 hover:text-white transition-all duration-200"
            active-class="bg-school-navy shadow-inner text-white border-l-4 border-school-red rounded-l-none"
          >
            <span class="text-lg">💰</span> Finance Dashboard
          </router-link>
          <router-link
            to="/finance/statements"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg text-slate-300 hover:bg-white/5 hover:text-white transition-all duration-200"
            active-class="bg-school-navy shadow-inner text-white border-l-4 border-school-red rounded-l-none"
          >
            <span class="text-lg">📄</span> Statements
          </router-link>
        </template>

        <template v-if="['admin', 'principal'].includes(userRole)">
          <div class="pt-6 pb-2">
            <p class="px-4 text-xs font-bold text-slate-500 uppercase tracking-widest">System</p>
          </div>
          <router-link
            v-if="userRole === 'admin'"
            to="/admin"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg text-slate-300 hover:bg-white/5 hover:text-white transition-all duration-200"
            active-class="bg-school-navy shadow-inner text-white border-l-4 border-school-red rounded-l-none"
          >
            <span class="text-lg">⚙️</span> Admin Console
          </router-link>
          <router-link
            to="/hr"
            class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg text-slate-300 hover:bg-white/5 hover:text-white transition-all duration-200"
            active-class="bg-school-navy shadow-inner text-white border-l-4 border-school-red rounded-l-none"
          >
            <span class="text-lg">🛡️</span> Staff & HR
          </router-link>
        </template>
      </nav>

      <!-- Sidebar Footer (Logout) -->
      <div class="p-4 border-t border-slate-800 bg-school-navy">
        <div class="flex items-center mb-4 px-2">
          <div
            class="h-10 w-10 rounded-full bg-slate-800 flex items-center justify-center text-white font-bold uppercase mr-3 border border-slate-700 shadow-sm"
          >
            {{ userNameInitial }}
          </div>
          <div class="overflow-hidden">
            <p class="text-sm font-bold text-white truncate">{{ userName }}</p>
            <p class="text-[11px] text-slate-400 uppercase tracking-wider truncate">
              {{ userRole }}
            </p>
          </div>
        </div>
        <button
          @click="logout"
          class="w-full flex items-center justify-center gap-2 bg-slate-800/50 hover:bg-school-red/90 text-white py-2.5 rounded-lg transition-all duration-200 text-sm font-medium border border-slate-700 hover:border-school-red group"
        >
          <svg
            class="w-4 h-4 text-slate-400 group-hover:text-white transition-colors"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
            ></path>
          </svg>
          Sign Out
        </button>
      </div>
    </aside>

    <!-- MAIN CONTENT WRAPPER -->
    <div class="flex-1 flex flex-col min-w-0 bg-school-grey overflow-hidden">
      <!-- TOP NAVIGATION BAR -->
      <header
        class="bg-white border-b border-slate-200 h-20 flex items-center justify-between px-6 sm:px-8 z-10 shrink-0"
      >
        <!-- Mobile Menu Button -->
        <button
          @click="isSidebarOpen = true"
          class="md:hidden p-2 -ml-2 text-slate-500 hover:bg-slate-100 rounded-lg focus:outline-none transition-colors"
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

        <!-- Contextual Header Area -->
        <div class="hidden md:flex flex-col">
          <div class="flex items-center gap-2 text-sm font-medium mb-1">
            <span class="text-slate-500">{{ routeName }}</span>
          </div>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight leading-none">
            {{ pageTitle }}
          </h1>
        </div>
        <div class="md:hidden text-lg font-bold text-slate-800">Bona School</div>

        <!-- Right Side: Term Selector, Notifications -->
        <div class="flex items-center gap-4 sm:gap-6 ml-auto">
          <!-- Global Term Selector -->
          <div
            class="flex items-center bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 shadow-sm"
          >
            <svg
              class="w-4 h-4 text-slate-400 mr-2"
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
              class="bg-transparent text-sm font-medium text-slate-700 outline-none cursor-pointer pr-2"
            >
              <option v-for="term in appStore.terms" :key="term" :value="term">{{ term }}</option>
            </select>
          </div>

          <!-- Notification Bell -->
          <button
            class="relative p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-full transition-colors focus:outline-none"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
              ></path>
            </svg>
            <span
              class="absolute top-1.5 right-1.5 block h-2 w-2 rounded-full bg-school-red ring-2 ring-white"
            ></span>
          </button>
        </div>
      </header>

      <!-- DYNAMIC PAGE CONTENT -->
      <main class="flex-1 overflow-y-auto p-4 sm:p-8 bg-school-grey">
        <router-view />
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
/* Optional: Custom scrollbar for sidebar */
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
  background: rgba(255, 255, 255, 0.2);
}
</style>
