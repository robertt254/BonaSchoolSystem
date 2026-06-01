<template>
  <div class="max-w-5xl mx-auto space-y-6">

    <!-- Apply for leave -->
    <div v-if="!isReviewer" class="bg-white rounded-[12px] border border-[#E2E8F0] p-6">
      <h2 class="text-base font-bold text-slate-800 mb-5">Apply for Leave</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Leave Type</label>
          <select v-model="applyForm.leave_type" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple">
            <option value="Annual Leave">Annual Leave</option>
            <option value="Sick Leave">Sick Leave</option>
            <option value="Compassionate Leave">Compassionate Leave</option>
            <option value="Maternity Leave">Maternity Leave</option>
            <option value="Paternity Leave">Paternity Leave</option>
            <option value="Study Leave">Study Leave</option>
          </select>
        </div>
        <div></div>
        <div>
          <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Start Date</label>
          <input v-model="applyForm.start_date" type="date" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple" />
        </div>
        <div>
          <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">End Date</label>
          <input v-model="applyForm.end_date" type="date" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple" />
        </div>
        <div class="sm:col-span-2">
          <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Reason</label>
          <textarea
            v-model="applyForm.reason"
            rows="3"
            class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple resize-none"
            placeholder="Briefly explain the reason for leave…"
          ></textarea>
        </div>
      </div>
      <div class="mt-4 flex items-center gap-3">
        <button
          @click="submitLeave"
          :disabled="submitting"
          class="bg-school-purple text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition disabled:opacity-50"
        >{{ submitting ? 'Submitting…' : 'Submit Application' }}</button>
        <span v-if="applyMsg" class="text-sm font-medium" :class="applyError ? 'text-school-red' : 'text-emerald-600'">{{ applyMsg }}</span>
      </div>
    </div>

    <!-- Filter strip -->
    <div class="flex items-center gap-3 flex-wrap">
      <span class="text-xs font-bold uppercase tracking-widest text-slate-400">Filter:</span>
      <button
        v-for="s in ['all', 'pending', 'approved', 'rejected']"
        :key="s"
        @click="statusFilter = s"
        :class="statusFilter === s ? 'bg-school-purple text-white' : 'bg-white text-slate-600 border border-slate-200 hover:border-slate-300'"
        class="px-3 py-1.5 rounded-lg text-sm font-semibold capitalize transition"
      >{{ s }}</button>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-[12px] border border-[#E2E8F0] overflow-hidden">
      <div class="border-b border-slate-100 px-6 py-4 bg-slate-50">
        <h3 class="font-bold text-slate-800">{{ isReviewer ? 'All Leave Requests' : 'My Leave Requests' }}</h3>
      </div>

      <div v-if="loading" class="py-16 flex justify-center">
        <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
      </div>

      <div v-else-if="filteredRequests.length === 0" class="py-16 text-center text-slate-400 text-sm">
        No leave requests found.
      </div>

      <div v-else class="divide-y divide-slate-50">
        <div
          v-for="req in filteredRequests"
          :key="req.id"
          class="px-6 py-4 hover:bg-slate-50 transition-colors"
        >
          <div class="flex items-start justify-between gap-4">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="font-semibold text-slate-800">{{ req.staff_name }}</span>
                <span
                  class="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full"
                  :class="statusClass(req.status)"
                >{{ req.status }}</span>
                <span class="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded-full">{{ req.leave_type }}</span>
              </div>
              <p class="text-sm text-slate-600 mt-1">
                {{ formatDate(req.start_date) }} → {{ formatDate(req.end_date) }}
                <span class="text-slate-400 ml-2">({{ dayCount(req.start_date, req.end_date) }} day{{ dayCount(req.start_date, req.end_date) !== 1 ? 's' : '' }})</span>
              </p>
              <p class="text-xs text-slate-400 mt-1 italic">{{ req.reason }}</p>
            </div>

            <!-- Actions -->
            <div class="flex gap-2 shrink-0">
              <template v-if="isReviewer && req.status === 'pending'">
                <button
                  @click="reviewRequest(req.id, 'approve')"
                  class="text-xs font-bold px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-700 hover:bg-emerald-100 transition"
                >Approve</button>
                <button
                  @click="reviewRequest(req.id, 'reject')"
                  class="text-xs font-bold px-3 py-1.5 rounded-lg bg-red-50 text-school-red hover:bg-red-100 transition"
                >Reject</button>
              </template>
              <template v-if="!isReviewer && req.status === 'pending'">
                <button
                  @click="cancelRequest(req.id)"
                  class="text-xs font-bold px-3 py-1.5 rounded-lg bg-slate-100 text-slate-500 hover:bg-slate-200 transition"
                >Cancel</button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
const toast = useToast()


const authStore = useAuthStore()
const isReviewer = computed(() => ['admin', 'principal'].includes(authStore.user?.role))

const requests = ref([])
const loading = ref(false)
const statusFilter = ref('all')
const submitting = ref(false)
const applyMsg = ref('')
const applyError = ref(false)

const applyForm = ref({
  leave_type: 'Annual Leave',
  start_date: '',
  end_date: '',
  reason: '',
})

const filteredRequests = computed(() => {
  if (statusFilter.value === 'all') return requests.value
  return requests.value.filter(r => r.status === statusFilter.value)
})

const statusClass = (status) => ({
  pending: 'bg-amber-50 text-amber-700',
  approved: 'bg-emerald-50 text-emerald-700',
  rejected: 'bg-red-50 text-school-red',
}[status] || 'bg-slate-100 text-slate-500')

const formatDate = (d) => new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })

const dayCount = (start, end) => {
  const diff = new Date(end) - new Date(start)
  return Math.max(1, Math.round(diff / 86400000) + 1)
}

const loadRequests = async () => {
  loading.value = true
  try {
    requests.value = await apiFetch('/api/leave/')
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const submitLeave = async () => {
  applyMsg.value = ''
  applyError.value = false
  if (!applyForm.value.start_date || !applyForm.value.end_date || !applyForm.value.reason.trim()) {
    applyMsg.value = 'Please fill in all fields.'
    applyError.value = true
    return
  }
  submitting.value = true
  try {
    await apiFetch('/api/leave/', { method: 'POST', body: JSON.stringify(applyForm.value) })
    applyMsg.value = 'Application submitted.'
    applyForm.value = { leave_type: 'Annual Leave', start_date: '', end_date: '', reason: '' }
    await loadRequests()
    setTimeout(() => { applyMsg.value = '' }, 4000)
  } catch (e) {
    applyMsg.value = 'Submission failed: ' + (e?.message || '')
    applyError.value = true
  } finally {
    submitting.value = false
  }
}

const reviewRequest = async (id, action) => {
  try {
    await apiFetch(`/api/leave/${id}/review?action=${action}`, { method: 'PUT' })
    await loadRequests()
  } catch (e) {
    toast.error('Action failed: ' + (e?.message || ''))
  }
}

const cancelRequest = async (id) => {
  if (!confirm('Cancel this leave request?')) return
  try {
    await apiFetch(`/api/leave/${id}`, { method: 'DELETE' })
    await loadRequests()
  } catch (e) {
    toast.error('Cancel failed.')
  }
}

onMounted(loadRequests)
</script>
