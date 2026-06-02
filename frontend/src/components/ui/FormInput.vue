<template>
  <div class="flex flex-col gap-1.5">
    <label v-if="label" :for="id" class="text-xs font-bold uppercase tracking-widest text-text-muted">
      {{ label }}<span v-if="required" class="text-danger ml-0.5">*</span>
    </label>
    <div class="relative">
      <div v-if="$slots.prefix" class="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted pointer-events-none">
        <slot name="prefix" />
      </div>
      <input
        :id="id"
        v-bind="$attrs"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :class="[
          'w-full border border-border rounded-card bg-surface-muted text-text-primary text-sm',
          'placeholder:text-text-muted transition-colors',
          'focus:outline-none focus:border-brand focus:ring-2 focus:ring-brand/20',
          $slots.prefix ? 'pl-9' : 'pl-3',
          'pr-3 py-2.5',
          $attrs.class,
        ]"
      />
    </div>
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
