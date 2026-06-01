<template>
  <!-- stat cards row -->
  <div v-if="type === 'stats'" class="grid grid-cols-2 lg:grid-cols-4 gap-4">
    <div v-for="n in count" :key="n" class="skel-card">
      <div class="skel-bar h-3 w-20 mb-3 rounded" />
      <div class="skel-bar h-8 w-16 mb-2 rounded" />
      <div class="skel-bar h-2 w-28 rounded" />
    </div>
  </div>

  <!-- table rows -->
  <div v-else-if="type === 'table'" class="space-y-2">
    <div v-for="n in count" :key="n" class="skel-row flex items-center gap-4 px-4 py-3 rounded-lg">
      <div class="skel-bar h-8 w-8 rounded-full flex-shrink-0" />
      <div class="flex-1 space-y-1.5">
        <div class="skel-bar h-3 w-40 rounded" />
        <div class="skel-bar h-2 w-24 rounded" />
      </div>
      <div class="skel-bar h-3 w-16 rounded" />
      <div class="skel-bar h-3 w-16 rounded" />
      <div class="skel-bar h-6 w-20 rounded-full" />
    </div>
  </div>

  <!-- generic block -->
  <div v-else class="skel-card">
    <div v-for="n in count" :key="n" class="skel-bar h-4 rounded mb-2" :style="{ width: widths[n % widths.length] }" />
  </div>
</template>

<script setup>
defineProps({
  type:  { type: String, default: 'block' },
  count: { type: Number, default: 4 },
})
const widths = ['100%', '80%', '60%', '90%', '70%']
</script>

<style scoped>
.skel-card {
  background: white;
  border: 1px solid #f1f5f9;
  border-radius: 0.75rem;
  padding: 1.25rem;
}
.skel-row {
  background: white;
  border: 1px solid #f1f5f9;
}
.skel-bar {
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}
@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
