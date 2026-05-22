<template>
  <div class="max-w-7xl mx-auto space-y-6">

    <!-- Controls -->
    <div class="bg-white rounded-[12px] border border-[#E2E8F0] p-5 print:hidden">
      <div class="flex flex-wrap items-end gap-4">
        <div>
          <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Grade</label>
          <select v-model="selectedGrade" @change="loadTimetable" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple">
            <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
          </select>
        </div>
        <div>
          <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Term</label>
          <select v-model="selectedTerm" @change="loadTimetable" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple">
            <option value="Term 1">Term 1</option>
            <option value="Term 2">Term 2</option>
            <option value="Term 3">Term 3</option>
          </select>
        </div>
        <div class="ml-auto flex gap-2">
          <button v-if="canEdit" @click="showAddModal = true" class="bg-school-purple text-white px-4 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Add Period
          </button>
          <button @click="printPage()" class="border border-slate-200 text-slate-600 px-4 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-50 transition">Print</button>
        </div>
      </div>
    </div>

    <!-- Grid -->
    <div class="bg-white rounded-[12px] border border-[#E2E8F0] overflow-hidden">
      <div class="border-b border-slate-100 px-6 py-4 bg-slate-50">
        <h3 class="font-bold text-slate-800">{{ selectedGrade }} · {{ selectedTerm }} Timetable</h3>
      </div>

      <div v-if="loading" class="py-16 flex justify-center">
        <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-xs border-collapse">
          <thead>
            <tr>
              <th class="border border-slate-200 bg-slate-50 px-4 py-3 text-center font-bold text-slate-500 w-16">Period</th>
              <th
                v-for="day in days"
                :key="day"
                class="border border-slate-200 bg-slate-50 px-4 py-3 text-center font-bold text-slate-600 min-w-[140px]"
              >{{ day }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="period in periods" :key="period">
              <td class="border border-slate-200 bg-slate-50 px-4 py-3 text-center font-bold text-slate-400">{{ period }}</td>
              <td
                v-for="day in days"
                :key="day"
                class="border border-slate-200 px-4 py-3 align-top min-h-[72px] hover:bg-violet-50/30 transition-colors cursor-pointer"
                @click="canEdit && openEdit(day, period)"
              >
                <template v-if="grid[day]?.[period]">
                  <p class="font-bold text-slate-800 leading-tight">{{ grid[day][period].subject }}</p>
                  <p v-if="grid[day][period].teacher_name" class="text-slate-400 mt-0.5">{{ grid[day][period].teacher_name }}</p>
                  <p v-if="grid[day][period].start_time" class="text-slate-400 mt-0.5">
                    {{ grid[day][period].start_time }}–{{ grid[day][period].end_time }}
                  </p>
                  <button
                    v-if="canEdit"
                    @click.stop="deleteEntry(grid[day][period].id)"
                    class="mt-1 text-school-red text-[10px] hover:underline print:hidden"
                  >Remove</button>
                </template>
                <template v-else>
                  <span class="text-slate-200 text-[10px] print:hidden">+ Add</span>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-[16px] w-full max-w-md p-6 space-y-4 shadow-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-base font-bold text-slate-800">{{ editSlot ? 'Edit Period' : 'Add Period' }}</h3>
          <button @click="closeModal" class="w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1">Day</label>
            <select v-model="modalForm.day_of_week" class="w-full border border-slate-300 px-3 py-2 rounded-lg text-sm outline-none">
              <option v-for="d in days" :key="d" :value="d">{{ d }}</option>
            </select>
          </div>
          <div>
            <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1">Period</label>
            <select v-model.number="modalForm.period" class="w-full border border-slate-300 px-3 py-2 rounded-lg text-sm outline-none">
              <option v-for="p in periods" :key="p" :value="p">{{ p }}</option>
            </select>
          </div>
          <div class="col-span-2">
            <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1">Subject</label>
            <input v-model="modalForm.subject" type="text" class="w-full border border-slate-300 px-3 py-2 rounded-lg text-sm outline-none" placeholder="e.g. Mathematics" />
          </div>
          <div class="col-span-2">
            <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1">Teacher (optional)</label>
            <input v-model="modalForm.teacher_name" type="text" class="w-full border border-slate-300 px-3 py-2 rounded-lg text-sm outline-none" placeholder="Teacher name" />
          </div>
          <div>
            <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1">Start Time</label>
            <input v-model="modalForm.start_time" type="time" class="w-full border border-slate-300 px-3 py-2 rounded-lg text-sm outline-none" />
          </div>
          <div>
            <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1">End Time</label>
            <input v-model="modalForm.end_time" type="time" class="w-full border border-slate-300 px-3 py-2 rounded-lg text-sm outline-none" />
          </div>
        </div>

        <div class="flex justify-end gap-3 pt-2">
          <button @click="closeModal" class="px-4 py-2 text-sm text-slate-600 hover:text-slate-800 transition">Cancel</button>
          <button @click="savePeriod" :disabled="saving" class="bg-school-purple text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition disabled:opacity-50">
            {{ saving ? 'Saving…' : 'Save' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'

const authStore = useAuthStore()
const appStore = useAppStore()
const printPage = () => window.print()

const GRADES = ['Play Group', 'PP1', 'PP2', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6']
const grades = ref(GRADES)
const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
const periods = [1, 2, 3, 4, 5, 6, 7, 8]

const selectedGrade = ref('Grade 1')
const selectedTerm = ref(appStore.currentTerm)
const grid = ref({})
const loading = ref(false)
const saving = ref(false)
const showAddModal = ref(false)
const editSlot = ref(null)

const canEdit = computed(() => ['admin', 'principal', 'teacher'].includes(authStore.user?.role))

const modalForm = ref({
  day_of_week: 'Monday',
  period: 1,
  subject: '',
  teacher_name: '',
  start_time: '',
  end_time: '',
})

const loadTimetable = async () => {
  loading.value = true
  try {
    const data = await apiFetch(
      `/api/timetable/${encodeURIComponent(selectedGrade.value)}/${encodeURIComponent(selectedTerm.value)}?year=${appStore.currentYear}`
    )
    grid.value = data.grid
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const openEdit = (day, period) => {
  editSlot.value = { day, period }
  modalForm.value = {
    day_of_week: day,
    period,
    subject: grid.value[day]?.[period]?.subject || '',
    teacher_name: grid.value[day]?.[period]?.teacher_name || '',
    start_time: grid.value[day]?.[period]?.start_time || '',
    end_time: grid.value[day]?.[period]?.end_time || '',
  }
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  editSlot.value = null
  modalForm.value = { day_of_week: 'Monday', period: 1, subject: '', teacher_name: '', start_time: '', end_time: '' }
}

const savePeriod = async () => {
  if (!modalForm.value.subject.trim()) return
  saving.value = true
  try {
    await apiFetch('/api/timetable/', {
      method: 'POST',
      body: JSON.stringify({
        ...modalForm.value,
        grade_level: selectedGrade.value,
        term: selectedTerm.value,
        academic_year: appStore.currentYear,
      }),
    })
    await loadTimetable()
    closeModal()
  } catch (e) {
    alert('Failed to save: ' + (e?.message || ''))
  } finally {
    saving.value = false
  }
}

const deleteEntry = async (id) => {
  if (!confirm('Remove this period?')) return
  try {
    await apiFetch(`/api/timetable/${id}`, { method: 'DELETE' })
    await loadTimetable()
  } catch (e) {
    alert('Delete failed.')
  }
}

onMounted(loadTimetable)
</script>

<style>
@media print {
  .print\:hidden { display: none !important; }
}
</style>
