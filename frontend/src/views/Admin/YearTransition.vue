<template>
  <div class="max-w-3xl mx-auto space-y-5">

    <div>
      <h1 class="text-2xl font-extrabold text-slate-800">Academic Year Transition</h1>
      <p class="text-sm text-slate-400 mt-0.5">Advance all students to their next grade at the end of the year.</p>
    </div>

    <!-- Warning -->
    <div class="bg-amber-50 border border-amber-200 rounded-xl p-5 flex gap-4">
      <svg class="w-5 h-5 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
      </svg>
      <div>
        <p class="font-bold text-amber-800 text-sm">This action affects all students</p>
        <p class="text-amber-700 text-sm mt-1">Every active student will be moved to their next grade level. Grade 6 students will be marked as <strong>Graduated</strong>. This cannot be automatically undone — promote students individually if needed.</p>
      </div>
    </div>

    <!-- Grade summary -->
    <div v-if="summary.length > 0" class="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div class="px-5 py-3.5 border-b border-slate-100 bg-slate-50">
        <h3 class="font-bold text-sm text-slate-700">Current Enrollment by Grade</h3>
      </div>
      <table class="w-full text-sm">
        <thead>
          <tr class="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-100">
            <th class="px-5 py-3 text-left">Grade</th>
            <th class="px-5 py-3 text-center">Students</th>
            <th class="px-5 py-3 text-left">Promoted To</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in summary" :key="row.grade" class="border-b border-slate-50">
            <td class="px-5 py-3 font-semibold text-slate-800">{{ row.grade }}</td>
            <td class="px-5 py-3 text-center text-slate-600">{{ row.count }}</td>
            <td class="px-5 py-3">
              <span v-if="row.next" class="text-emerald-700 font-medium">{{ row.next }}</span>
              <span v-else class="text-slate-400 italic">Graduated</span>
            </td>
          </tr>
        </tbody>
        <tfoot>
          <tr class="border-t border-slate-200 bg-slate-50">
            <td class="px-5 py-3 font-bold text-slate-700">Total</td>
            <td class="px-5 py-3 text-center font-bold text-slate-700">{{ totalStudents }}</td>
            <td></td>
          </tr>
        </tfoot>
      </table>
    </div>

    <div v-if="!summaryLoaded" class="flex justify-center py-6">
      <button @click="loadSummary" :disabled="loadingSummary"
        class="bg-school-navy text-white px-6 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-navy/90 transition disabled:opacity-50">
        {{ loadingSummary ? 'Loading…' : 'Load Summary' }}
      </button>
    </div>

    <!-- Confirm action -->
    <div v-if="summaryLoaded && !done" class="bg-white rounded-xl border border-slate-200 p-5 space-y-4">
      <p class="text-sm text-slate-600">Type <strong>CONFIRM</strong> to proceed with the year transition.</p>
      <input v-model="confirmText" type="text" placeholder="Type CONFIRM"
        class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none w-full" />
      <div class="flex justify-end">
        <button @click="runTransition" :disabled="confirmText !== 'CONFIRM' || running"
          class="bg-red-600 text-white px-6 py-2.5 rounded-lg text-sm font-bold hover:bg-red-700 transition disabled:opacity-50">
          {{ running ? 'Processing…' : 'Run Year Transition' }}
        </button>
      </div>
    </div>

    <div v-if="done" class="bg-emerald-50 border border-emerald-200 rounded-xl px-5 py-4 text-emerald-700 font-semibold text-sm">
      Year transition complete. {{ result.promoted }} student(s) promoted, {{ result.graduated }} graduated.
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { apiFetch } from '@/services/api'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

const GRADE_PROGRESSION = {
  'Play Group': 'PP1', 'PP1': 'PP2', 'PP2': 'Grade 1',
  'Grade 1': 'Grade 2', 'Grade 2': 'Grade 3', 'Grade 3': 'Grade 4',
  'Grade 4': 'Grade 5', 'Grade 5': 'Grade 6', 'Grade 6': null,
}

const summary = ref([])
const summaryLoaded = ref(false)
const loadingSummary = ref(false)
const confirmText = ref('')
const running = ref(false)
const done = ref(false)
const result = ref({ promoted: 0, graduated: 0 })

const totalStudents = computed(() => summary.value.reduce((s, r) => s + r.count, 0))

const loadSummary = async () => {
  loadingSummary.value = true
  try {
    const data = await apiFetch(`/api/students/enrollment-summary?academic_year=${appStore.currentYear}`)
    summary.value = data.map(r => ({ grade: r.grade_level, count: r.count, next: GRADE_PROGRESSION[r.grade_level] }))
    summaryLoaded.value = true
  } catch { alert('Failed to load summary.') }
  finally { loadingSummary.value = false }
}

const runTransition = async () => {
  if (confirmText.value !== 'CONFIRM') return
  running.value = true
  try {
    const res = await apiFetch('/api/students/year-transition', { method: 'POST' })
    result.value = res
    done.value = true
  } catch (e) { alert(e?.message || 'Transition failed.') }
  finally { running.value = false }
}
</script>
