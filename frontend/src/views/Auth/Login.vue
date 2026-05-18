<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const username = ref('')
const password = ref('')
const loginError = ref(false)

const roleRouteMap = {
  admin: '/app/admin',
  principal: '/app/principal',
  secretary: '/app/office',
  accountant: '/app/finance',
  senior_teacher: '/app/academics',
}

const handleLogin = async () => {
  loginError.value = false
  console.log('Starting login attempt...')

  const body = new URLSearchParams()
  body.append('username', username.value)
  body.append('password', password.value)
  console.log('Login data:', { username: username.value, password: password.value })

  try {
    const response = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body,
    })

    console.log('Response status:', response.status)
    console.log('Response ok:', response.ok)

    if (!response.ok) {
      const errorText = await response.text()
      console.log('Error response:', errorText)
      loginError.value = true
      password.value = ''
      return
    }

    const data = await response.json()
    console.log('Login successful, data:', data)
    const route = roleRouteMap[data.user_info.role]

    if (!route) {
      console.log('No route found for role:', data.user_info.role)
      loginError.value = true
      password.value = ''
      return
    }

    console.log('Redirecting to:', route)
    // Store the token and user in auth store and localStorage
    authStore.setToken(data.access_token)
    authStore.setUser(data.user_info)
    localStorage.setItem('user_role', data.user_info.role)
    localStorage.setItem('user_name', data.user_info.name)

    router.push(route)
  } catch (error) {
    console.error('Login error:', error)
    loginError.value = true
    password.value = ''
  }
}
</script>

<template>
  <!-- Main Container: Uses bona-bg for overall cleanliness -->
  <div class="min-h-screen bg-bona-bg flex items-center justify-center p-4 font-sans antialiased">
    
    <!-- Login Card: Two-column layout on larger screens -->
    <div class="bg-bona-white w-full max-w-4xl rounded-2xl shadow-xl flex overflow-hidden">
      
      <!-- Left Column: School Branding (Visible on md screens and up) -->
      <div class="hidden md:flex md:w-1/2 bg-bona-navy p-12 flex-col justify-between text-bona-white">
        <div>
          <h1 class="text-3xl font-extrabold tracking-tight">The Bona School</h1>
          <p class="mt-2 text-blue-100 opacity-90">Student Management System</p>
        </div>
        
        <div class="border-t border-blue-800 pt-6">
          <p class="text-sm text-blue-200">Secure access for staff and administration only.</p>
          <p class="text-xs mt-2 text-blue-300">In case of access issues, contact the IT Administrator.</p>
        </div>
      </div>

      <!-- Right Column: Login Form -->
      <div class="w-full md:w-1/2 p-8 sm:p-12">
        
        <!-- Mobile Logo (Only visible on small screens) -->
        <div class="md:hidden text-center mb-8">
            <h1 class="text-3xl font-extrabold text-bona-navy">The Bona School</h1>
            <p class="text-slate-600">SMS Login</p>
        </div>

        <div class="mb-10 hidden md:block">
          <h2 class="text-2xl font-bold text-slate-900">Welcome Back</h2>
          <p class="text-slate-600 mt-1">Please enter your credentials to access your dashboard.</p>
        </div>

        <!-- Error Alert (Accent Red applied here) -->
        <div v-if="loginError" class="mb-6 bg-red-50 border border-bona-red/30 text-bona-red p-4 rounded-lg text-sm font-medium">
          The username or password provided is incorrect. Please try again.
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
              class="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-bona-navy/20 focus:border-bona-navy transition duration-150 outline-none"
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
              class="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-bona-navy/20 focus:border-bona-navy transition duration-150 outline-none"
            />
          </div>
          
          <!-- Submit Button (Accent Red applied for call-to-action) -->
          <div>
            <button 
              type="submit" 
              class="w-full bg-bona-red text-bona-white font-semibold py-3.5 px-4 rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition duration-200 active:scale-[0.98]"
            >
              Sign In
            </button>
          </div>
        </form>
        
        <div class="mt-10 text-center text-xs text-slate-500">
            Powered by The Bona School IT Dept | &copy; 2024
        </div>
      </div>
    </div>
  </div>
</template>

