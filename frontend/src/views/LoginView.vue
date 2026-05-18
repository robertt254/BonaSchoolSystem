<template>
  <div class="min-h-screen bg-slate-900 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
      <div class="bg-blue-900 p-8 text-center">
        <div
          class="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-inner"
        >
          <span class="text-3xl">🎓</span>
        </div>
        <h1 class="text-2xl font-black text-white tracking-widest uppercase">The Bona School</h1>
        <p class="text-blue-200 text-sm mt-1 uppercase tracking-widest">Authorized Access Only</p>
      </div>

      <div class="p-8">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-600 p-4 rounded-r">
            <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
          </div>

          <div>
            <label class="block text-sm font-bold text-gray-700 mb-2">System Username</label>
            <input
              v-model="username"
              type="text"
              required
              class="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-900 focus:border-blue-900 outline-none transition font-mono text-sm"
              placeholder="e.g., admin_user"
            />
          </div>

          <div>
            <label class="block text-sm font-bold text-gray-700 mb-2">Password</label>
            <input
              v-model="password"
              type="password"
              required
              class="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-900 focus:border-blue-900 outline-none transition"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-blue-900 text-white font-bold py-3 rounded-lg shadow-lg hover:bg-blue-800 transition disabled:bg-blue-400 flex justify-center items-center"
          >
            <span v-if="isLoading" class="animate-pulse">Authenticating...</span>
            <span v-else>Secure Login</span>
          </button>
        </form>
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
