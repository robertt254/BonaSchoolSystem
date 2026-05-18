<script setup>
import { ref, computed } from 'vue'
import { RouterView, useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const isSidebarOpen = ref(false)

// --- MOCK USER SESSION ---
// Change the role here to visually test the different sidebars!
// Options: 'admin', 'principal', 'secretary', 'accountant', 'senior_teacher'
const currentUser = ref({
  name: 'Jane Doe',
  role: 'accountant',
})

// Define all possible sidebar menus and strictly define which roles can see them based on your JSON
const allMenuItems = [
  { name: 'Admin Core', path: '/app/admin', roles: ['admin'], icon: '⚙️' },
  { name: 'Principal Overview', path: '/app/principal', roles: ['principal'], icon: '📊' },
  {
    name: 'Office & Admissions',
    path: '/app/office',
    roles: ['admin', 'principal', 'secretary'],
    icon: '🏢',
  },
  {
    name: 'Finance & Fees',
    path: '/app/finance',
    roles: ['admin', 'accountant', 'principal'],
    icon: '💰',
  },
  {
    name: 'Academics & Grading',
    path: '/app/academics',
    roles: ['admin', 'principal', 'senior_teacher'],
    icon: '📚',
  },
]

// Filter the menu items based on the active user's role
const visibleMenuItems = computed(() => {
  return allMenuItems.filter((item) => item.roles.includes(currentUser.value.role))
})

const handleLogout = () => {
  router.push('/')
}
</script>

<template>
  <div class="flex h-screen bg-bona-bg font-sans overflow-hidden">
    <!-- Mobile Sidebar Overlay -->
    <div
      v-if="isSidebarOpen"
      @click="isSidebarOpen = false"
      class="fixed inset-0 bg-slate-900/50 z-20 md:hidden"
    ></div>

    <!-- SIDEBAR -->
    <aside
      :class="[
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
        'fixed inset-y-0 left-0 z-30 w-72 bg-school-navy text-white transition duration-300 transform md:relative md:translate-x-0 flex flex-col shadow-2xl border-r border-slate-800',
      ]"
    >
      <!-- Sidebar Header (Logo Area) -->
      <div class="flex items-center h-20 border-b border-slate-800 px-8">
        <h1 class="text-xl font-extrabold tracking-wide text-white uppercase">The Bona School</h1>
      </div>

      <!-- Navigation Links -->
      <nav class="flex-1 px-4 py-8 space-y-3 overflow-y-auto">
        <RouterLink
          v-for="item in visibleMenuItems"
          :key="item.path"
          :to="item.path"
          :class="[
            route.path === item.path
              ? 'text-white border-l-4 border-school-red bg-white/5 font-semibold'
              : 'text-slate-400 hover:text-white hover:bg-white/5 border-l-4 border-transparent font-medium',
            'flex items-center gap-4 px-6 py-3.5 rounded-r-lg transition-all duration-200',
          ]"
        >
          <span class="text-2xl">{{ item.icon }}</span>
          <span class="text-[15px]">{{ item.name }}</span>
        </RouterLink>
      </nav>

      <!-- Sidebar Footer (Logout) -->
      <div class="p-6 border-t border-slate-800">
        <button
          @click="handleLogout"
          class="flex items-center justify-center gap-3 w-full px-4 py-3 text-sm font-medium text-slate-300 rounded-lg hover:bg-school-red hover:text-white hover:shadow-lg transition-all duration-200"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
    <div class="flex-1 flex flex-col min-w-0 bg-slate-50">
      <!-- TOP NAVIGATION BAR -->
      <header
        class="bg-white border-b border-slate-200 h-20 flex items-center justify-between px-6 sm:px-10 z-10 sticky top-0"
      >
        <!-- Mobile Menu Button -->
        <button
          @click="isSidebarOpen = true"
          class="md:hidden text-slate-500 hover:text-slate-800 focus:outline-none transition-colors"
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

        <!-- Page Title Placeholder -->
        <div class="hidden md:flex items-center gap-4">
          <h2 class="text-2xl font-bold text-slate-800 tracking-tight">Overview</h2>
        </div>

        <!-- User Profile Area -->
        <div class="flex items-center gap-5 ml-auto">
          <div class="text-right hidden sm:block">
            <p class="text-sm font-bold text-slate-800">{{ currentUser.name }}</p>
            <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">
              {{ currentUser.role }}
            </p>
          </div>
          <!-- Avatar -->
          <div
            class="h-11 w-11 rounded-full bg-school-navy flex items-center justify-center text-white font-bold shadow-sm ring-4 ring-slate-50"
          >
            {{
              currentUser.name
                .split(' ')
                .map((n) => n[0])
                .join('')
            }}
          </div>
        </div>
      </header>

      <!-- DYNAMIC PAGE CONTENT -->
      <main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
        <!-- This is where AdminDashboard.vue or AccountantDashboard.vue will appear -->
        <RouterView />
      </main>
    </div>
  </div>
</template>
