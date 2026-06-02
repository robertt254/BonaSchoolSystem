<template>
  <div class="fixed inset-0 bg-slate-900/50 flex items-center justify-center z-[200] p-4">
    <div class="bg-white rounded-xl shadow-2xl w-full max-w-sm border border-border">
      <div class="flex items-center justify-between p-6 border-b border-slate-100">
        <h2 class="text-lg font-bold text-slate-800">Change Password</h2>
        <button @click="$emit('close')" class="text-slate-400 hover:text-slate-600 transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <form @submit.prevent="submit" class="p-6 space-y-4">
        <div
          v-if="errorMsg"
          class="bg-red-50 border border-red-200 text-red-700 text-sm font-medium px-4 py-3 rounded-lg"
        >
          {{ errorMsg }}
        </div>
        <div
          v-if="successMsg"
          class="bg-emerald-50 border border-emerald-200 text-emerald-700 text-sm font-medium px-4 py-3 rounded-lg"
        >
          {{ successMsg }}
        </div>

        <div>
          <label class="block text-xs font-bold uppercase tracking-[0.07em] text-slate-500 mb-1.5">
            Current Password
          </label>
          <input
            v-model="form.current_password"
            type="password"
            required
            class="w-full border border-slate-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none text-sm"
          />
        </div>

        <div>
          <label class="block text-xs font-bold uppercase tracking-[0.07em] text-slate-500 mb-1.5">
            New Password
          </label>
          <input
            v-model="form.new_password"
            type="password"
            required
            minlength="8"
            class="w-full border border-slate-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none text-sm"
          />
        </div>

        <div>
          <label class="block text-xs font-bold uppercase tracking-[0.07em] text-slate-500 mb-1.5">
            Confirm New Password
          </label>
          <input
            v-model="form.confirm_password"
            type="password"
            required
            class="w-full border border-slate-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none text-sm"
          />
        </div>

        <div class="flex gap-3 pt-2">
          <button
            type="button"
            @click="$emit('close')"
            class="flex-1 px-4 py-3 text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg font-semibold text-sm transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="flex-1 px-4 py-3 bg-school-navy text-white rounded-lg font-semibold text-sm hover:bg-school-navy/90 disabled:opacity-50 transition-colors"
          >
            {{ loading ? 'Saving...' : 'Save' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { apiFetch } from '@/services/api'

const emit = defineEmits(['close'])

const form = reactive({ current_password: '', new_password: '', confirm_password: '' })
const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

const submit = async () => {
  errorMsg.value = ''
  successMsg.value = ''

  if (form.new_password !== form.confirm_password) {
    errorMsg.value = 'New passwords do not match.'
    return
  }

  loading.value = true
  try {
    await apiFetch('/api/auth/change-password', {
      method: 'POST',
      body: JSON.stringify({
        current_password: form.current_password,
        new_password: form.new_password,
      }),
    })
    successMsg.value = 'Password changed successfully.'
    form.current_password = ''
    form.new_password = ''
    form.confirm_password = ''
    setTimeout(() => emit('close'), 1500)
  } catch (err) {
    errorMsg.value = err.message || 'Failed to change password.'
  } finally {
    loading.value = false
  }
}
</script>
