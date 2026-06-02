<template>
  <div
    class="bg-surface border border-border rounded-card p-5 relative overflow-hidden transition-all duration-200 hover:-translate-y-0.5 hover:shadow-card-hover cursor-default"
    :style="animation ? { animation } : {}"
  >
    <!-- top accent bar -->
    <div :class="['absolute top-0 left-0 right-0 h-0.5 rounded-t-card', accentGradient]" />

    <div class="flex items-start justify-between mb-3">
      <span class="text-xs font-bold uppercase tracking-widest text-text-muted">{{ label }}</span>
      <div v-if="$slots.icon" :class="['w-10 h-10 rounded-xl flex items-center justify-center shrink-0', iconBg]">
        <slot name="icon" />
      </div>
    </div>

    <div class="font-heading font-extrabold text-text-primary leading-none mb-2">
      <span class="text-3xl">{{ value ?? '—' }}</span>
    </div>

    <div class="flex items-center gap-1.5">
      <slot name="sub">
        <span v-if="sub" class="text-xs text-text-muted">{{ sub }}</span>
      </slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label:     { type: String, required: true },
  value:     { type: [String, Number], default: null },
  sub:       { type: String, default: null },
  accent:    { type: String, default: 'blue' },   // blue | green | purple | amber | red
  animation: { type: String, default: null },
})

const GRADIENTS = {
  blue:   'bg-gradient-to-r from-info to-info/50',
  green:  'bg-gradient-to-r from-success to-success/50',
  purple: 'bg-gradient-to-r from-brand to-brand-lighter',
  amber:  'bg-gradient-to-r from-warning to-warning/50',
  red:    'bg-gradient-to-r from-danger to-danger/50',
}
const ICON_BG = {
  blue:   'bg-info-bg   text-info',
  green:  'bg-success-bg text-success',
  purple: 'bg-brand-dim  text-brand',
  amber:  'bg-warning-bg text-warning',
  red:    'bg-danger-bg  text-danger',
}

const accentGradient = computed(() => GRADIENTS[props.accent] ?? GRADIENTS.blue)
const iconBg         = computed(() => ICON_BG[props.accent]   ?? ICON_BG.blue)
</script>
