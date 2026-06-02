<template>
  <!-- stat cards row -->
  <div v-if="type === 'stats'" class="grid grid-cols-2 lg:grid-cols-4 gap-4">
    <div v-for="n in count" :key="n" class="bg-surface border border-border rounded-card p-5">
      <div class="skel h-3 w-20 mb-3" />
      <div class="skel h-8 w-16 mb-2" />
      <div class="skel h-2 w-28" />
    </div>
  </div>

  <!-- table rows -->
  <div v-else-if="type === 'table'" class="space-y-2">
    <div v-for="n in count" :key="n" class="flex items-center gap-4 px-4 py-3 bg-surface border border-border rounded-lg">
      <div class="skel w-8 h-8 rounded-full shrink-0" />
      <div class="flex-1 space-y-1.5">
        <div class="skel h-3 w-40" />
        <div class="skel h-2 w-24" />
      </div>
      <div class="skel h-3 w-16" />
      <div class="skel h-6 w-20 rounded-full" />
    </div>
  </div>

  <!-- generic block -->
  <div v-else class="bg-surface border border-border rounded-card p-5">
    <div v-for="n in count" :key="n" class="skel h-4 mb-2" :style="{ width: widths[n % widths.length] }" />
  </div>
</template>

<script setup>
defineProps({
  type:  { type: String, default: 'block' },
  count: { type: Number, default: 4 },
})
const widths = ['100%', '80%', '60%', '90%', '70%']
</script>
