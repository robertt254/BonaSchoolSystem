<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-8">
    <div class="text-center max-w-md">
      <p class="text-6xl font-bold text-gray-300 mb-4">403</p>
      <h1 class="text-2xl font-semibold text-gray-800 mb-2">Access Denied</h1>
      <p class="text-gray-500 mb-6">
        Your account role ({{ userRole }}) does not have permission to view this page.
      </p>
      <button
        class="px-5 py-2 rounded-lg bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 transition-colors"
        @click="$router.push('/')"
      >
        Back to Dashboard
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const userRole = computed(() => useAuthStore().user?.role ?? 'unknown')
</script>
