<template>
  <div class="flex items-start justify-between gap-4 flex-wrap">
    <div>
      <h1 class="font-heading text-2xl font-extrabold text-text-primary tracking-tight">{{ title }}</h1>
      <p v-if="description" class="text-sm text-text-muted mt-1">{{ description }}</p>
    </div>
    <div v-if="$slots.actions" class="flex items-center gap-2 flex-wrap">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title:       { type: String, required: true },
  description: { type: String, default: null },
})
</script>
