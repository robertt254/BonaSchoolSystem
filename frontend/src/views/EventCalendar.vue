<template>
  <div class="max-w-6xl mx-auto space-y-6">

    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-extrabold text-slate-800">School Calendar</h1>
        <p class="text-sm text-slate-400 mt-0.5">Events, exams, holidays, and meetings.</p>
      </div>
      <button @click="showModal = true; resetForm()"
        class="bg-school-purple text-white px-4 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Add Event
      </button>
    </div>

    <!-- Month navigation -->
    <div class="bg-white rounded-xl border border-slate-200 p-4 flex items-center justify-between">
      <button @click="changeMonth(-1)" class="w-9 h-9 flex items-center justify-center rounded-lg hover:bg-slate-100 transition text-slate-600">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <h2 class="font-bold text-slate-800">{{ monthName }} {{ viewYear }}</h2>
      <button @click="changeMonth(1)" class="w-9 h-9 flex items-center justify-center rounded-lg hover:bg-slate-100 transition text-slate-600">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 18l6-6-6-6"/></svg>
      </button>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
      <!-- Calendar grid -->
      <div class="lg:col-span-2 bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div class="grid grid-cols-7 border-b border-slate-100">
          <div v-for="day in ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']" :key="day"
            class="px-2 py-3 text-center text-xs font-bold text-slate-400 uppercase tracking-wider">{{ day }}</div>
        </div>
        <div class="grid grid-cols-7">
          <div
            v-for="(cell, i) in calendarCells"
            :key="i"
            class="min-h-[72px] border-b border-r border-slate-50 p-1.5 cursor-pointer hover:bg-slate-50 transition-colors last:border-r-0"
            :class="cell.isToday ? 'bg-blue-50/50' : cell.otherMonth ? 'bg-slate-50/30' : ''"
            @click="cell.day && selectDay(cell)"
          >
            <span v-if="cell.day" class="block text-xs font-bold mb-1 w-6 h-6 flex items-center justify-center rounded-full"
              :class="cell.isToday ? 'bg-school-purple text-white' : 'text-slate-600'">
              {{ cell.day }}
            </span>
            <div v-for="ev in cell.events" :key="ev.id"
              class="text-xs font-semibold px-1.5 py-0.5 rounded mb-0.5 truncate cursor-pointer"
              :class="eventColor(ev.event_type)"
              @click.stop="selectedEvent = ev">
              {{ ev.title }}
            </div>
          </div>
        </div>
      </div>

      <!-- Event list + detail -->
      <div class="space-y-4">
        <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div class="px-4 py-3 border-b border-slate-100 bg-slate-50">
            <h3 class="font-bold text-sm text-slate-700">{{ monthName }} Events</h3>
          </div>
          <div v-if="monthEvents.length === 0" class="py-8 text-center text-sm text-slate-400">No events this month.</div>
          <div v-else class="divide-y divide-slate-50">
            <div v-for="ev in monthEvents" :key="ev.id"
              class="px-4 py-3 flex items-start gap-3 hover:bg-slate-50 cursor-pointer transition-colors"
              @click="selectedEvent = ev">
              <span class="mt-0.5 w-2.5 h-2.5 rounded-full shrink-0" :class="eventDot(ev.event_type)"></span>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-slate-800 truncate">{{ ev.title }}</p>
                <p class="text-xs text-slate-400">{{ fmtDate(ev.start_date) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Event detail panel -->
        <div v-if="selectedEvent" class="bg-white rounded-xl border border-slate-200 p-6">
          <div class="flex items-start justify-between mb-3">
            <div>
              <span class="text-xs font-bold uppercase tracking-wider px-2 py-0.5 rounded-full" :class="eventColor(selectedEvent.event_type)">
                {{ selectedEvent.event_type }}
              </span>
            </div>
            <div class="flex gap-2">
              <button @click="editEvent(selectedEvent)" class="text-xs font-semibold text-school-purple hover:underline">Edit</button>
              <button @click="deleteEvent(selectedEvent.id)" class="text-xs font-semibold text-red-500 hover:underline">Delete</button>
            </div>
          </div>
          <h4 class="font-bold text-slate-800 mb-1">{{ selectedEvent.title }}</h4>
          <p class="text-xs text-slate-500 mb-2">
            {{ fmtDate(selectedEvent.start_date) }}
            <span v-if="selectedEvent.end_date && selectedEvent.end_date !== selectedEvent.start_date">
              → {{ fmtDate(selectedEvent.end_date) }}
            </span>
          </p>
          <p v-if="selectedEvent.description" class="text-sm text-slate-600">{{ selectedEvent.description }}</p>
          <p class="text-xs text-slate-400 mt-2">Added by {{ selectedEvent.created_by }}</p>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-base font-bold text-slate-800">{{ editingId ? 'Edit Event' : 'New Event' }}</h3>
          <button @click="showModal = false" class="text-slate-400 hover:text-slate-600 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-100">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="space-y-3">
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Title *</label>
            <input v-model="form.title" type="text" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Type</label>
              <select v-model="form.event_type" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
                <option value="exam">Exam</option>
                <option value="holiday">Holiday</option>
                <option value="meeting">Meeting</option>
                <option value="sports">Sports</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Start Date</label>
              <input v-model="form.start_date" type="date" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
            </div>
          </div>
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">End Date (optional)</label>
            <input v-model="form.end_date" type="date" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
          </div>
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Description</label>
            <textarea v-model="form.description" rows="2" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none resize-none"></textarea>
          </div>
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button @click="showModal = false" class="px-4 py-2 text-sm text-slate-600 hover:text-slate-800">Cancel</button>
          <button @click="saveEvent" :disabled="saving"
            class="bg-school-purple text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-school-purple-l disabled:opacity-50">
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
import { useToast } from '@/composables/useToast'
const toast = useToast()


const today = new Date()
const viewYear = ref(today.getFullYear())
const viewMonth = ref(today.getMonth())

const events = ref([])
const selectedEvent = ref(null)
const showModal = ref(false)
const saving = ref(false)
const editingId = ref(null)
const form = ref({ title: '', event_type: 'other', start_date: '', end_date: '', description: '', all_day: true })

const MONTH_NAMES = ['January','February','March','April','May','June','July','August','September','October','November','December']
const monthName = computed(() => MONTH_NAMES[viewMonth.value])

const loadEvents = async () => {
  try {
    events.value = await apiFetch(`/api/events/?year=${viewYear.value}&month=${viewMonth.value + 1}`)
  } catch { /* silent */ }
}

const changeMonth = (dir) => {
  viewMonth.value += dir
  if (viewMonth.value > 11) { viewMonth.value = 0; viewYear.value++ }
  if (viewMonth.value < 0) { viewMonth.value = 11; viewYear.value-- }
  loadEvents()
}

const monthEvents = computed(() =>
  events.value.filter(e => {
    const d = new Date(e.start_date)
    return d.getFullYear() === viewYear.value && d.getMonth() === viewMonth.value
  }).sort((a, b) => new Date(a.start_date) - new Date(b.start_date))
)

const calendarCells = computed(() => {
  const year = viewYear.value
  const month = viewMonth.value
  const firstDay = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const todayStr = today.toISOString().split('T')[0]

  const cells = []
  for (let i = 0; i < firstDay; i++) cells.push({ day: null, events: [], otherMonth: true })

  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `${year}-${String(month + 1).padStart(2,'0')}-${String(d).padStart(2,'0')}`
    const dayEvents = events.value.filter(e => e.start_date === dateStr || e.end_date === dateStr || (e.start_date <= dateStr && e.end_date && e.end_date >= dateStr))
    cells.push({ day: d, events: dayEvents, isToday: dateStr === todayStr, otherMonth: false, dateStr })
  }
  return cells
})

const selectDay = (cell) => {
  if (!cell.events.length) {
    resetForm()
    form.value.start_date = cell.dateStr
    showModal.value = true
  } else {
    selectedEvent.value = cell.events[0]
  }
}

const eventColor = (type) => ({
  exam: 'bg-red-100 text-red-700',
  holiday: 'bg-emerald-100 text-emerald-700',
  meeting: 'bg-blue-100 text-blue-700',
  sports: 'bg-orange-100 text-orange-700',
  other: 'bg-slate-100 text-slate-600',
}[type] || 'bg-slate-100 text-slate-600')

const eventDot = (type) => ({
  exam: 'bg-red-400',
  holiday: 'bg-emerald-400',
  meeting: 'bg-blue-400',
  sports: 'bg-orange-400',
  other: 'bg-slate-400',
}[type] || 'bg-slate-400')

const resetForm = () => {
  form.value = { title: '', event_type: 'other', start_date: today.toISOString().split('T')[0], end_date: '', description: '', all_day: true }
  editingId.value = null
}

const editEvent = (ev) => {
  editingId.value = ev.id
  form.value = { title: ev.title, event_type: ev.event_type, start_date: ev.start_date, end_date: ev.end_date || '', description: ev.description || '', all_day: ev.all_day }
  showModal.value = true
}

const saveEvent = async () => {
  if (!form.value.title.trim() || !form.value.start_date) return
  saving.value = true
  try {
    const body = { ...form.value, end_date: form.value.end_date || null }
    if (editingId.value) {
      await apiFetch(`/api/events/${editingId.value}`, { method: 'PUT', body: JSON.stringify(body) })
    } else {
      await apiFetch('/api/events/', { method: 'POST', body: JSON.stringify(body) })
    }
    showModal.value = false
    selectedEvent.value = null
    await loadEvents()
  } catch (e) { toast.error(e?.message || 'Failed to save.') }
  finally { saving.value = false }
}

const deleteEvent = async (id) => {
  if (!confirm('Delete this event?')) return
  try {
    await apiFetch(`/api/events/${id}`, { method: 'DELETE' })
    selectedEvent.value = null
    await loadEvents()
  } catch { toast.error('Delete failed.') }
}

const fmtDate = (d) => d ? new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : ''

onMounted(loadEvents)
</script>
