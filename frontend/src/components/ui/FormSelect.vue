<template>
  <div class="flex flex-col gap-1.5">
    <label v-if="label" :for="id" class="text-xs font-bold uppercase tracking-widest text-text-muted">
      {{ label }}<span v-if="required" class="text-danger ml-0.5">*</span>
    </label>
    <select
      :id="id"
      v-bind="$attrs"
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
      :class="[
        'w-full border border-border rounded-card bg-surface-muted text-text-primary text-sm',
        'px-3 py-2.5 cursor-pointer transition-colors appearance-none',
        'focus:outline-none focus:border-brand focus:ring-2 focus:ring-brand/20',
        $attrs.class,
      ]"
    >
      <slot />
    </select>
  </div>
</template>

<script setup>
defineProps({
  modelValue: { type: [String, Number], default: '' },
  label:      { type: String, default: null },
  id:         { type: String, default: null },
  required:   Boolean,
})
defineEmits(['update:modelValue'])
</script>
