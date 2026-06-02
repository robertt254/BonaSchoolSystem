<template>
  <div class="bg-surface border border-border rounded-card overflow-hidden">
    <!-- Optional header slot -->
    <div v-if="$slots.header" class="px-5 py-4 border-b border-border bg-surface-muted flex items-center justify-between gap-4">
      <slot name="header" />
    </div>

    <!-- Loading skeleton -->
    <div v-if="loading" class="p-4 space-y-2">
      <div v-for="n in skeletonRows" :key="n"
        class="flex items-center gap-3 px-2 py-3 rounded-lg">
        <div class="skel h-8 w-8 rounded-full shrink-0" />
        <div class="flex-1 space-y-1.5">
          <div class="skel h-3 w-40 rounded" />
          <div class="skel h-2 w-24 rounded" />
        </div>
        <div class="skel h-3 w-16 rounded" />
        <div class="skel h-6 w-20 rounded-full" />
      </div>
    </div>

    <!-- Empty state -->
    <div v-else-if="!loading && isEmpty"
      class="py-16 flex flex-col items-center justify-center gap-2 text-text-muted">
      <svg class="w-10 h-10 opacity-30" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round"
          d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0H4" />
      </svg>
      <p class="text-sm font-medium">{{ emptyMessage }}</p>
    </div>

    <!-- Table -->
    <div v-else class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead v-if="$slots.thead">
          <tr class="bg-surface-muted border-b border-border text-xs font-bold uppercase tracking-widest text-text-muted">
            <slot name="thead" />
          </tr>
        </thead>
        <tbody class="divide-y divide-border">
          <slot />
        </tbody>
        <tfoot v-if="$slots.tfoot">
          <slot name="tfoot" />
        </tfoot>
      </table>
    </div>

    <!-- Pagination / footer slot -->
    <div v-if="$slots.footer" class="px-5 py-3 border-t border-border bg-surface-muted">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  loading:      Boolean,
  isEmpty:      Boolean,
  emptyMessage: { type: String, default: 'No data found.' },
  skeletonRows: { type: Number, default: 6 },
})
</script>
