<template>
  <div class="rounded-lg border border-red-200 bg-red-50 p-4 flex items-start gap-3" role="alert">
    <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-red-500" viewBox="0 0 20 20" fill="currentColor">
      <path
        fill-rule="evenodd"
        d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
        clip-rule="evenodd"
      />
    </svg>
    <div class="flex-1">
      <p class="text-sm font-medium text-red-800">{{ message }}</p>
    </div>
    <button
      v-if="onRetry"
      class="ml-2 rounded px-3 py-1 text-xs font-medium text-red-700 border border-red-300 hover:bg-red-100 transition-colors"
      @click="onRetry"
    >
      Retry
    </button>
  </div>
</template>

<script setup>
defineProps({
  message: { type: String, required: true },
  onRetry: { type: Function, default: null },
})
</script>
