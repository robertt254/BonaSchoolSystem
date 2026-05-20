<template>
  <div class="flex items-center justify-center py-12">
    <div
      class="animate-spin rounded-full border-4 border-gray-200 border-t-blue-600"
      :class="sizeClass"
      role="status"
      aria-label="Loading"
    />
    <span v-if="label" class="ml-3 text-gray-500 text-sm">{{ label }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: { type: String, default: 'md' },
  label: { type: String, default: '' },
})

const sizeClass = computed(() => ({
  sm: 'h-6 w-6',
  md: 'h-10 w-10',
  lg: 'h-16 w-16',
}[props.size] ?? 'h-10 w-10'))
</script>
