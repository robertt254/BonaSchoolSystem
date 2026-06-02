<template>
  <div :class="[
    'bg-surface border border-border rounded-card',
    hover && 'transition-shadow duration-200 hover:shadow-card-hover',
    padding,
  ]">
    <div v-if="accent" :class="['h-0.5 rounded-t-card -mt-px -mx-px mb-4', accentClass]" />
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  accent:  { type: String, default: null },  // blue | green | purple | amber | red
  padding: { type: String, default: 'p-6' },
  hover:   Boolean,
})

const accentClass = computed(() => ({
  blue:   'bg-gradient-to-r from-info to-info/60',
  green:  'bg-gradient-to-r from-success to-success/60',
  purple: 'bg-gradient-to-r from-brand to-brand-lighter',
  amber:  'bg-gradient-to-r from-warning to-warning/60',
  red:    'bg-gradient-to-r from-danger to-danger/60',
}[props.accent] ?? ''))
</script>
