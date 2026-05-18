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
        'fixed inset-y-0 left-0 z-30 w-64 bg-school-navy text-white transition duration-300 transform md:relative md:translate-x-0 flex flex-col shadow-xl',
      ]"
    >
      <!-- Sidebar Header (Logo Area) -->
      <div class="flex items-center justify-center h-16 border-b border-school-navy/90 px-4">
        <h1 class="text-xl font-bold tracking-wider">THE BONA SCHOOL</h1>
      </div>

      <!-- Navigation Links -->
      <nav class="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        <RouterLink
          v-for="item in visibleMenuItems"
          :key="item.path"
          :to="item.path"
          :class="[
            route.path === item.path
              ? 'bg-school-navy/90 text-white font-medium'
              : 'text-school-grey hover:bg-school-navy/90/50 hover:text-white transition-colors',
            'flex items-center gap-3 px-4 py-3 rounded-lg',
          ]"
        >
          <span class="text-xl">{{ item.icon }}</span>
          {{ item.name }}
        </RouterLink>
      </nav>

      <!-- Sidebar Footer (Logout) -->
      <div class="p-4 border-t border-school-navy/90">
        <button
          @click="handleLogout"
          class="flex items-center gap-3 w-full px-4 py-2 text-sm font-medium text-school-grey rounded-lg hover:bg-school-red hover:text-white transition-colors"
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
    <div class="flex-1 flex flex-col min-w-0">
      <!-- TOP NAVIGATION BAR -->
      <header
        class="bg-white shadow-sm h-16 flex items-center justify-between px-4 sm:px-6 z-10"
      >
        <!-- Mobile Menu Button -->
        <button
          @click="isSidebarOpen = true"
          class="md:hidden text-slate-500 hover:text-slate-700 focus:outline-none"
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
        <div class="hidden md:block">
          <h2 class="text-xl font-semibold text-slate-800">Overview</h2>
        </div>

        <!-- User Profile Area -->
        <div class="flex items-center gap-4 ml-auto">
          <div class="text-right hidden sm:block">
            <p class="text-sm font-bold text-slate-800">{{ currentUser.name }}</p>
            <p class="text-xs text-slate-500">{{ currentUser.role }}</p>
          </div>
          <!-- Avatar -->
          <div
            class="h-10 w-10 rounded-full bg-school-navy flex items-center justify-center text-white font-bold shadow-md ring-2 ring-school-grey/80"
          >
            AU
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
