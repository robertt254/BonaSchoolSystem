<template>
  <div class="flex h-screen bg-gray-50 font-sans">
    <aside class="w-64 bg-slate-900 text-slate-300 flex flex-col shadow-2xl z-20">
      <div class="p-6 border-b border-slate-800 text-center">
        <h2 class="text-2xl font-black text-white tracking-widest uppercase">The Bona School</h2>
        <p class="text-xs text-slate-400 mt-1 uppercase tracking-widest">CBC Management</p>
      </div>

      <nav class="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        <router-link
          to="/"
          class="flex items-center px-4 py-2 text-sm font-medium rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors duration-150"
          active-class="bg-school-navy text-white shadow-lg"
        >
          <span class="mr-3">🏠</span> Dashboard
        </router-link>

        <template v-if="['senior_teacher', 'principal', 'admin'].includes(userRole)">
          <div class="pt-4 pb-2">
            <p class="px-3 text-xs font-bold text-slate-500 uppercase tracking-wider">Academics</p>
          </div>
          <router-link
            to="/academics/attendance"
            class="flex items-center px-4 py-2 text-sm font-medium rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors duration-150"
            active-class="bg-school-navy text-white shadow-lg"
          >
            <span class="mr-3">📋</span> Roll Call
          </router-link>
          <router-link
            to="/academics"
            class="flex items-center px-4 py-2 text-sm font-medium rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors duration-150"
            active-class="bg-school-navy text-white shadow-lg"
          >
            <span class="mr-3">📝</span> Grading
          </router-link>
          <router-link
            to="/academics/report-card"
            class="flex items-center px-4 py-2 text-sm font-medium rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors duration-150"
            active-class="bg-school-navy text-white shadow-lg"
          >
            <span class="mr-3">🎓</span> Report Cards
          </router-link>
        </template>

        <template v-if="['principal', 'secretary', 'admin'].includes(userRole)">
          <div class="pt-4 pb-2">
            <p class="px-3 text-xs font-bold text-slate-500 uppercase tracking-wider">
              Administration
            </p>
          </div>
          <router-link
            to="/office"
            class="flex items-center px-4 py-2 text-sm font-medium rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors duration-150"
            active-class="bg-school-navy text-white shadow-lg"
          >
            <span class="mr-3">👨‍🎓</span> Office & Admissions
          </router-link>
        </template>

        <template v-if="['accountant', 'principal', 'admin'].includes(userRole)">
          <div class="pt-4 pb-2">
            <p class="px-3 text-xs font-bold text-slate-500 uppercase tracking-wider">Finance</p>
          </div>
          <router-link
            to="/finance"
            class="flex items-center px-4 py-2 text-sm font-medium rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors duration-150"
            active-class="bg-school-navy text-white shadow-lg"
          >
            <span class="mr-3">💰</span> Fee Ledger
          </router-link>
          <router-link
            to="/finance/statements"
            class="flex items-center px-4 py-2 text-sm font-medium rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors duration-150"
            active-class="bg-school-navy text-white shadow-lg"
          >
            <span class="mr-3">📄</span> Statements
          </router-link>
        </template>

        <template v-if="['admin'].includes(userRole)">
          <div class="pt-4 pb-2">
            <p class="px-3 text-xs font-bold text-slate-500 uppercase tracking-wider">System</p>
          </div>
          <router-link
            to="/admin"
            class="flex items-center px-4 py-2 text-sm font-medium rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors duration-150"
            active-class="bg-school-navy text-white shadow-lg"
          >
            <span class="mr-3">⚙️</span> Admin Console
          </router-link>
          <router-link
            to="/admin/staff"
            class="flex items-center px-4 py-2 text-sm font-medium rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors duration-150"
            active-class="bg-school-navy text-white shadow-lg"
          >
            <span class="mr-3">🛡️</span> Staff & HR
          </router-link>
        </template>
      </nav>

      <div class="p-4 border-t border-slate-800 bg-slate-950">
        <div class="flex items-center mb-4 px-2">
          <div
            class="h-8 w-8 rounded-full bg-school-navy flex items-center justify-center text-white font-bold uppercase mr-3"
          >
            {{ userNameInitial }}
          </div>
          <div>
            <p class="text-sm font-bold text-white">{{ userName }}</p>
            <p class="text-xs text-slate-400 capitalize">{{ userRole }}</p>
          </div>
        </div>
        <button
          @click="logout"
          class="w-full bg-slate-800 hover:bg-red-900 text-white py-2 rounded transition text-sm font-medium"
        >
          Sign Out
        </button>
      </div>
    </aside>

    <main class="flex-1 overflow-y-auto">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

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
  router.push('/')
}
</script>
