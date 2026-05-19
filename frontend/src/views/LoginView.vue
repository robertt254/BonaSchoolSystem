<template>
  <!-- Main Container: Uses bona-bg for overall cleanliness -->
  <div class="min-h-screen bg-slate-50 flex items-center justify-center p-4 font-sans antialiased">
    <!-- Login Card: Two-column layout on larger screens -->
    <div
      class="bg-white w-full max-w-4xl rounded-[18px] shadow-2xl flex overflow-hidden border border-slate-100"
    >
      <!-- Left Column: School Branding (Visible on md screens and up) -->
      <div
        class="hidden md:flex md:w-1/2 bg-school-navy p-12 flex-col justify-between text-white relative overflow-hidden"
      >
        <div class="absolute -right-20 -top-20 w-64 h-64 rounded-full bg-white/5 blur-3xl"></div>
        <div
          class="absolute -left-10 -bottom-10 w-48 h-48 rounded-full bg-school-red/10 blur-2xl"
        ></div>
        <div class="relative z-10">
          <h1 class="text-4xl font-extrabold font-heading tracking-tight uppercase mb-2">
            The Bona School
          </h1>
          <p class="text-school-grey/80 font-medium">Student Management System</p>
        </div>

        <div class="border-t border-slate-700 pt-6 relative z-10">
          <p class="text-sm text-slate-300">Secure access for staff and administration only.</p>
          <p class="text-xs mt-2 text-slate-400">
            In case of access issues, contact the IT Administrator.
          </p>
        </div>
      </div>

      <!-- Right Column: Login Form -->
      <div class="w-full md:w-1/2 p-8 sm:p-12 lg:p-16 flex flex-col justify-center">
        <!-- Mobile Logo (Only visible on small screens) -->
        <div class="md:hidden text-center mb-10">
          <h1
            class="text-3xl font-extrabold font-heading text-school-navy uppercase tracking-tight"
          >
            The Bona School
          </h1>
          <p class="text-slate-500 font-medium mt-1">SMS Login</p>
        </div>

        <div class="mb-10 hidden md:block">
          <h2 class="text-3xl font-bold font-heading text-slate-900 tracking-tight">
            Welcome Back
          </h2>
          <p class="text-slate-500 mt-2 font-medium">
            Please enter your credentials to access your dashboard.
          </p>
        </div>

        <!-- Error Alert (Accent Red applied here) -->
        <div
          v-if="errorMessage"
          class="mb-6 bg-red-50 border border-school-red/30 text-school-red p-4 rounded-lg text-sm font-medium"
        >
          {{ errorMessage }}
        </div>

        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Username Input -->
          <div>
            <label class="block text-sm font-semibold text-slate-800 mb-1.5">Username</label>
            <input
              v-model="username"
              type="text"
              required
              placeholder="e.g. j.doe"
              class="w-full px-4 py-3 rounded-[9px] border border-slate-300 focus:ring-2 focus:ring-school-red/10 focus:border-school-red transition duration-150 outline-none"
            />
          </div>

          <!-- Password Input -->
          <div>
            <label class="block text-sm font-semibold text-slate-800 mb-1.5">Password</label>
            <input
              v-model="password"
              type="password"
              required
              placeholder="••••••••"
              class="w-full px-4 py-3 rounded-[9px] border border-slate-300 focus:ring-2 focus:ring-school-red/10 focus:border-school-red transition duration-150 outline-none"
            />
          </div>

          <!-- Submit Button (Accent Red applied for call-to-action) -->
          <div>
            <button
              type="submit"
              :disabled="isLoading"
              class="w-full bg-school-red text-white font-semibold py-3.5 px-4 rounded-[9px] shadow-none hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition duration-200 active:scale-[0.98] disabled:bg-school-grey disabled:text-slate-500 flex justify-center items-center"
            >
              <span v-if="isLoading" class="animate-spin mr-2">
                <!-- simple SVG spinner inline -->
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 4v2m0 12v2m8-8h-2M6 12H4m13.657-5.657l-1.414 1.414M6.343 17.657l1.414-1.414m12.02 0l-1.414-1.414M6.343 6.343l1.414 1.414"
                  />
                </svg>
              </span>
              <span v-if="isLoading">Authenticating...</span>
              <span v-else>Sign In</span>
            </button>
          </div>
        </form>

        <div class="mt-10 text-center text-[11px] text-[#94A3B8]">
          Powered by The Bona School IT Dept | &copy; 2025
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  errorMessage.value = ''
  isLoading.value = true

  try {
    await authStore.login(username.value, password.value)
    // If successful, push them to the main dashboard!
    router.push('/')
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    isLoading.value = false
  }
}
</script>
