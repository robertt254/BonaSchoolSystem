<template>
  <button
    v-bind="$attrs"
    :disabled="disabled || loading"
    :class="[baseClass, variantClass, sizeClass, 'inline-flex items-center justify-center gap-2 font-semibold transition-all duration-150 select-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed']"
  >
    <svg v-if="loading" class="animate-spin shrink-0" :class="iconSize" viewBox="0 0 24 24" fill="none">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/>
    </svg>
    <slot />
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: { type: String, default: 'primary' },  // primary | secondary | ghost | danger
  size:    { type: String, default: 'md' },        // sm | md | lg
  loading: Boolean,
  disabled: Boolean,
})

const baseClass = 'rounded-card'

const variantClass = computed(() => ({
  primary:   'bg-brand text-white hover:bg-brand-light shadow-sm hover:shadow-card-hover',
  secondary: 'bg-surface border border-border text-text-primary hover:bg-surface-hover shadow-card',
  ghost:     'text-text-secondary hover:bg-surface-hover',
  danger:    'bg-danger text-white hover:bg-danger/90 shadow-sm',
  success:   'bg-success text-white hover:bg-success/90 shadow-sm',
}[props.variant]))

const sizeClass = computed(() => ({
  sm: 'px-3 py-1.5 text-xs',
  md: 'px-4 py-2.5 text-sm',
  lg: 'px-6 py-3 text-sm',
}[props.size]))

const iconSize = computed(() => ({
  sm: 'w-3 h-3',
  md: 'w-4 h-4',
  lg: 'w-4 h-4',
}[props.size]))
</script>
