<template>
  <span :class="[
    'inline-flex items-center font-semibold rounded-full',
    sizeClass,
    variantClass,
  ]">
    <slot />
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: { type: String, default: 'neutral' }, // success | warning | danger | info | neutral | brand
  size:    { type: String, default: 'sm' },       // xs | sm | md
})

const variantClass = computed(() => ({
  success: 'bg-success-bg text-success-text',
  warning: 'bg-warning-bg text-warning-text',
  danger:  'bg-danger-bg  text-danger-text',
  info:    'bg-info-bg    text-info-text',
  brand:   'bg-brand-dim  text-brand-light',
  neutral: 'bg-surface-hover text-text-subtle',
}[props.variant]))

const sizeClass = computed(() => ({
  xs: 'text-xs px-1.5 py-px',
  sm: 'text-xs px-2   py-0.5',
  md: 'text-sm px-2.5 py-1',
}[props.size]))
</script>
