<template>
  <div class="max-w-3xl mx-auto space-y-6">
    <!-- Header -->
    <div>
      <h1 class="font-heading text-2xl font-bold text-text-primary tracking-tight">
        Parent Communications
      </h1>
      <p class="text-sm text-text-muted mt-1">
        Send bulk SMS notifications to parents and guardians.
      </p>
    </div>

    <!-- Compose Card -->
    <div class="bg-white border border-slate-200 rounded-xl overflow-hidden">
      <div class="px-6 py-4 border-b border-slate-100 bg-slate-50">
        <h2 class="font-heading text-sm font-bold text-text-primary">Compose Message</h2>
      </div>

      <form @submit.prevent="sendBroadcast" class="p-6 space-y-5">
        <!-- Audience -->
        <div>
          <label class="block text-xs font-bold uppercase tracking-[0.07em] text-text-muted mb-1.5">
            Recipients
          </label>
          <select
            v-model="form.grade"
            @change="fetchPreview"
            class="w-full border border-border rounded-xl p-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all cursor-pointer"
          >
            <option value="">All Parents / Guardians</option>
            <option v-for="g in GRADES" :key="g" :value="g">{{ g }} Parents</option>
          </select>
          <p class="mt-1.5 text-xs text-text-muted">
            <span v-if="previewLoading">Counting recipients…</span>
            <span v-else-if="recipientCount !== null">
              <span class="font-semibold text-slate-700">{{ recipientCount }}</span>
              guardian{{ recipientCount !== 1 ? 's' : '' }} will receive this message
            </span>
          </p>
        </div>

        <!-- Quick Templates -->
        <div>
          <label class="block text-xs font-bold uppercase tracking-[0.07em] text-text-muted mb-2">
            Quick Templates
          </label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="tpl in TEMPLATES"
              :key="tpl.label"
              type="button"
              @click="applyTemplate(tpl.text)"
              class="px-3 py-1.5 text-xs font-semibold rounded-full border border-slate-200 bg-slate-50 text-slate-600 hover:bg-school-purple/10 hover:border-school-purple/30 hover:text-school-purple transition-all"
            >
              {{ tpl.label }}
            </button>
          </div>
        </div>

        <!-- Message -->
        <div>
          <label class="block text-xs font-bold uppercase tracking-[0.07em] text-text-muted mb-1.5">
            Message
          </label>
          <textarea
            v-model="form.message"
            rows="5"
            maxlength="500"
            required
            placeholder="Type your message here…"
            class="w-full border border-border rounded-xl p-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-white font-medium text-slate-700 transition-all resize-none"
          ></textarea>
          <div class="flex justify-between mt-1">
            <span class="text-xs text-text-muted">Max 500 characters</span>
            <span
              class="text-xs font-semibold"
              :class="form.message.length > 450 ? 'text-school-red' : 'text-text-muted'"
            >
              {{ form.message.length }}/500
            </span>
          </div>
        </div>

        <!-- Error / Success -->
        <div v-if="errorMsg" class="rounded-xl bg-red-50 border border-red-200 px-4 py-3 text-sm font-medium text-red-700">
          {{ errorMsg }}
        </div>
        <div v-if="successMsg" class="rounded-xl bg-emerald-50 border border-emerald-200 px-4 py-3 text-sm font-medium text-emerald-700">
          {{ successMsg }}
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-3 pt-2">
          <button
            type="button"
            @click="resetForm"
            class="px-5 py-2.5 text-slate-600 hover:bg-slate-100 rounded-xl font-bold transition-colors text-sm"
          >
            Clear
          </button>
          <button
            type="submit"
            :disabled="sending || !form.message.trim() || recipientCount === 0"
            class="px-6 py-2.5 bg-school-navy text-white rounded-xl font-bold hover:bg-school-navy/90 hover:shadow-md transition-all text-sm flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg v-if="sending" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
            </svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
            {{ sending ? 'Sending…' : 'Send SMS' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Recent Broadcasts History (optional placeholder) -->
    <div class="bg-white border border-slate-200 rounded-xl overflow-hidden">
      <div class="px-6 py-4 border-b border-slate-100 bg-slate-50">
        <h2 class="font-heading text-sm font-bold text-text-primary">Tips</h2>
      </div>
      <ul class="p-6 space-y-2 text-sm text-slate-600">
        <li class="flex items-start gap-2">
          <span class="text-school-purple font-bold mt-0.5">•</span>
          Messages are sent from <span class="font-semibold">The Bona School</span> sender ID.
        </li>
        <li class="flex items-start gap-2">
          <span class="text-school-purple font-bold mt-0.5">•</span>
          Only guardians with a registered phone number will receive the SMS.
        </li>
        <li class="flex items-start gap-2">
          <span class="text-school-purple font-bold mt-0.5">•</span>
          Sending is queued in the background — it may take a minute for all messages to arrive.
        </li>
        <li class="flex items-start gap-2">
          <span class="text-school-purple font-bold mt-0.5">•</span>
          Keep messages under 160 characters to avoid being split into multiple SMS parts.
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { apiFetch } from '@/services/api'

const GRADES = [
  'Play Group', 'PP1', 'PP2',
  'Grade 1', 'Grade 2', 'Grade 3',
  'Grade 4', 'Grade 5', 'Grade 6',
]

const TEMPLATES = [
  {
    label: 'Term Dates',
    text: 'Dear Parent/Guardian, Term 2 begins on Monday 5th May 2025. Please ensure your child reports by 7:30 AM. — The Bona School.',
  },
  {
    label: 'Parents Meeting',
    text: "Dear Parent/Guardian, you are invited to a Parents' Meeting on Saturday 10th May 2025 at 9:00 AM. Your attendance is highly encouraged. — The Bona School.",
  },
  {
    label: 'Exam Notice',
    text: 'Dear Parent/Guardian, end-of-term examinations begin on Monday 2nd June 2025. Please ensure your child revises consistently. — The Bona School.',
  },
  {
    label: 'Fee Reminder',
    text: 'Dear Parent/Guardian, this is a reminder that school fees for Term 2 are due. Kindly clear the balance to avoid disruption. — The Bona School.',
  },
  {
    label: 'School Closed',
    text: 'Dear Parent/Guardian, the school will be CLOSED tomorrow due to a public holiday. Normal classes resume the following day. — The Bona School.',
  },
]

const form = reactive({ grade: '', message: '' })
const recipientCount = ref(null)
const previewLoading = ref(false)
const sending = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

const fetchPreview = async () => {
  previewLoading.value = true
  try {
    const qs = form.grade ? `?grade=${encodeURIComponent(form.grade)}` : ''
    const data = await apiFetch(`/api/sms/preview${qs}`)
    recipientCount.value = data.recipient_count
  } catch {
    recipientCount.value = null
  } finally {
    previewLoading.value = false
  }
}

const applyTemplate = (text) => {
  form.message = text
}

const resetForm = () => {
  form.grade = ''
  form.message = ''
  recipientCount.value = null
  errorMsg.value = ''
  successMsg.value = ''
  fetchPreview()
}

const sendBroadcast = async () => {
  errorMsg.value = ''
  successMsg.value = ''
  sending.value = true
  try {
    const payload = { message: form.message }
    if (form.grade) payload.grade = form.grade
    const res = await apiFetch('/api/sms/broadcast', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
    successMsg.value = res.message || `SMS queued for ${res.recipient_count} guardian(s).`
    form.message = ''
  } catch (err) {
    errorMsg.value = err.message || 'Failed to send broadcast. Please try again.'
  } finally {
    sending.value = false
  }
}

onMounted(fetchPreview)
</script>
