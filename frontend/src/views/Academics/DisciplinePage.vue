<template>
  <div class="max-w-7xl mx-auto space-y-6">

    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-extrabold text-slate-800">Disciplinary Records</h1>
        <p class="text-sm text-slate-400 mt-0.5">Track and manage student disciplinary incidents.</p>
      </div>
      <button @click="showModal = true; resetForm()"
        class="bg-school-red text-white px-4 py-2.5 rounded-lg text-sm font-semibold hover:bg-red-700 transition flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Record Incident
      </button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div class="bg-white rounded-xl border border-slate-200 p-6">
        <p class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Total Records</p>
        <p class="text-3xl font-extrabold text-slate-800">{{ records.length }}</p>
      </div>
      <div class="bg-white rounded-xl border border-slate-200 p-6">
        <p class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Open</p>
        <p class="text-3xl font-extrabold text-red-500">{{ openCount }}</p>
      </div>
      <div class="bg-white rounded-xl border border-slate-200 p-6">
        <p class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Serious</p>
        <p class="text-3xl font-extrabold text-orange-500">{{ seriousCount }}</p>
      </div>
      <div class="bg-white rounded-xl border border-slate-200 p-6">
        <p class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Resolved</p>
        <p class="text-3xl font-extrabold text-emerald-600">{{ resolvedCount }}</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-slate-200 p-4 flex flex-wrap gap-3 items-end">
      <div class="flex-1 min-w-40">
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Search Student</label>
        <input v-model="searchQuery" type="text" placeholder="Name…"
          class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
      </div>
      <div>
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Grade</label>
        <select v-model="gradeFilter" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
          <option value="">All Grades</option>
          <option v-for="g in GRADES" :key="g" :value="g">{{ g }}</option>
        </select>
      </div>
      <div>
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Status</label>
        <select v-model="statusFilter" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
          <option value="">All</option>
          <option value="Open">Open</option>
          <option value="Resolved">Resolved</option>
        </select>
      </div>
      <div>
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Severity</label>
        <select v-model="severityFilter" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
          <option value="">All</option>
          <option value="Minor">Minor</option>
          <option value="Moderate">Moderate</option>
          <option value="Serious">Serious</option>
        </select>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div v-if="loading" class="py-16 flex justify-center">
        <div class="w-8 h-8 border-4 border-slate-200 border-t-red-400 rounded-full animate-spin"></div>
      </div>
      <div v-else-if="filtered.length === 0" class="py-12 text-center text-slate-400 text-sm">No records found.</div>
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200 text-xs font-bold uppercase tracking-wider text-slate-400">
              <th class="text-left px-6 py-4">Student</th>
              <th class="text-left px-6 py-4">Date</th>
              <th class="text-left px-6 py-4">Type</th>
              <th class="text-left px-6 py-4 hidden md:table-cell">Description</th>
              <th class="text-center px-6 py-4">Severity</th>
              <th class="text-center px-6 py-4">Status</th>
              <th class="text-right px-6 py-4">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="r in filtered" :key="r.id" class="hover:bg-slate-50 transition-colors">
              <td class="px-6 py-4">
                <p class="font-semibold text-slate-800">{{ r.student_name }}</p>
                <p class="text-xs text-slate-400">{{ r.grade_level }}</p>
              </td>
              <td class="px-6 py-4 text-slate-500 text-xs">{{ fmtDate(r.incident_date) }}</td>
              <td class="px-6 py-4 font-medium text-slate-700">{{ r.incident_type }}</td>
              <td class="px-6 py-4 text-slate-500 text-xs max-w-xs hidden md:table-cell">
                <p class="truncate">{{ r.description }}</p>
              </td>
              <td class="px-6 py-4 text-center">
                <span class="px-2 py-0.5 rounded-full text-xs font-bold"
                  :class="r.severity === 'Serious' ? 'bg-red-100 text-red-700' : r.severity === 'Moderate' ? 'bg-amber-100 text-amber-700' : 'bg-slate-100 text-slate-500'">
                  {{ r.severity }}
                </span>
              </td>
              <td class="px-6 py-4 text-center">
                <span class="px-2 py-0.5 rounded-full text-xs font-bold"
                  :class="r.status === 'Open' ? 'bg-red-50 text-red-600' : 'bg-emerald-50 text-emerald-700'">
                  {{ r.status }}
                </span>
              </td>
              <td class="px-6 py-4 text-right space-x-3">
                <button @click="viewRecord(r)" class="text-xs font-semibold text-school-purple hover:underline">View</button>
                <button v-if="r.status === 'Open'" @click="resolveRecord(r)" class="text-xs font-semibold text-emerald-600 hover:underline">Resolve</button>
                <button @click="deleteRecord(r.id)" class="text-xs font-semibold text-red-500 hover:underline">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- View/Resolve Modal -->
    <div v-if="showDetailModal && selectedRecord" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl w-full max-w-lg p-6 space-y-4 shadow-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-base font-bold text-slate-800">Incident Details</h3>
          <button @click="showDetailModal = false" class="text-slate-400 hover:text-slate-600 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-100">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="space-y-3 text-sm">
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-slate-50 rounded-lg p-3">
              <p class="text-xs text-slate-400 mb-0.5">Student</p>
              <p class="font-semibold text-slate-800">{{ selectedRecord.student_name }}</p>
              <p class="text-xs text-slate-500">{{ selectedRecord.grade_level }}</p>
            </div>
            <div class="bg-slate-50 rounded-lg p-3">
              <p class="text-xs text-slate-400 mb-0.5">Date</p>
              <p class="font-semibold text-slate-800">{{ fmtDate(selectedRecord.incident_date) }}</p>
            </div>
          </div>
          <div class="bg-slate-50 rounded-lg p-3">
            <p class="text-xs text-slate-400 mb-0.5">Incident</p>
            <p class="font-semibold text-slate-700">{{ selectedRecord.incident_type }}</p>
            <p class="text-slate-600 mt-1">{{ selectedRecord.description }}</p>
          </div>
          <div v-if="selectedRecord.status === 'Open'" class="space-y-2">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Action Taken</label>
              <textarea v-model="actionForm.action_taken" rows="2"
                class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none resize-none"></textarea>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Action Date</label>
              <input v-model="actionForm.action_date" type="date" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
            </div>
          </div>
          <div v-else class="bg-emerald-50 rounded-lg p-3">
            <p class="text-xs text-slate-400 mb-0.5">Action Taken</p>
            <p class="text-slate-700">{{ selectedRecord.action_taken || 'No action recorded.' }}</p>
          </div>
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button @click="showDetailModal = false" class="px-4 py-2 text-sm text-slate-600 hover:text-slate-800">Close</button>
          <button v-if="selectedRecord.status === 'Open'" @click="submitResolve" :disabled="savingAction"
            class="bg-emerald-600 text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-emerald-700 disabled:opacity-50">
            {{ savingAction ? 'Saving…' : 'Mark Resolved' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Add Incident Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl w-full max-w-lg p-6 space-y-4 shadow-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-base font-bold text-slate-800">Record Incident</h3>
          <button @click="showModal = false" class="text-slate-400 hover:text-slate-600 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-100">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="space-y-3">
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Student *</label>
            <input v-model="studentSearch" type="text" placeholder="Search student name…"
              @input="searchStudents"
              class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
            <div v-if="studentResults.length > 0" class="border border-slate-200 rounded-lg mt-1 divide-y divide-slate-50 max-h-40 overflow-y-auto">
              <button v-for="s in studentResults" :key="s.id" @click="selectStudent(s)"
                class="w-full text-left px-3 py-2 text-sm hover:bg-slate-50">
                {{ s.first_name }} {{ s.last_name }} — {{ s.grade_level }}
              </button>
            </div>
            <p v-if="form.student_id" class="text-xs text-emerald-600 mt-1">Selected: {{ form.student_name }}</p>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Date</label>
              <input v-model="form.incident_date" type="date" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Severity</label>
              <select v-model="form.severity" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
                <option value="Minor">Minor</option>
                <option value="Moderate">Moderate</option>
                <option value="Serious">Serious</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Incident Type</label>
            <input v-model="form.incident_type" type="text" placeholder="e.g. Misconduct, Absenteeism, Bullying…"
              class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none" />
          </div>
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Description</label>
            <textarea v-model="form.description" rows="2" class="w-full border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none resize-none"></textarea>
          </div>
        </div>
        <div class="flex justify-end gap-3 pt-2">
          <button @click="showModal = false" class="px-4 py-2 text-sm text-slate-600 hover:text-slate-800">Cancel</button>
          <button @click="saveRecord" :disabled="saving"
            class="bg-school-red text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-red-700 disabled:opacity-50">
            {{ saving ? 'Saving…' : 'Record Incident' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '@/services/api'
import studentService from '@/services/studentService'
import { useToast } from '@/composables/useToast'
const toast = useToast()


const GRADES = ['Play Group','PP1','PP2','Grade 1','Grade 2','Grade 3','Grade 4','Grade 5','Grade 6']

const records = ref([])
const loading = ref(false)
const searchQuery = ref('')
const gradeFilter = ref('')
const statusFilter = ref('')
const severityFilter = ref('')

const openCount = computed(() => records.value.filter(r => r.status === 'Open').length)
const seriousCount = computed(() => records.value.filter(r => r.severity === 'Serious').length)
const resolvedCount = computed(() => records.value.filter(r => r.status === 'Resolved').length)

const filtered = computed(() => {
  let list = records.value
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(r => r.student_name.toLowerCase().includes(q))
  }
  if (gradeFilter.value) list = list.filter(r => r.grade_level === gradeFilter.value)
  if (statusFilter.value) list = list.filter(r => r.status === statusFilter.value)
  if (severityFilter.value) list = list.filter(r => r.severity === severityFilter.value)
  return list
})

const loadRecords = async () => {
  loading.value = true
  try { records.value = await apiFetch('/api/discipline/') }
  catch { /* silent */ }
  finally { loading.value = false }
}

// Add modal
const showModal = ref(false)
const saving = ref(false)
const studentSearch = ref('')
const studentResults = ref([])
const form = ref({ student_id: null, student_name: '', incident_date: new Date().toISOString().split('T')[0], incident_type: '', description: '', severity: 'Minor' })

const resetForm = () => {
  form.value = { student_id: null, student_name: '', incident_date: new Date().toISOString().split('T')[0], incident_type: '', description: '', severity: 'Minor' }
  studentSearch.value = ''
  studentResults.value = []
}

let searchTimer = null
const searchStudents = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(async () => {
    if (studentSearch.value.length < 2) { studentResults.value = []; return }
    try {
      studentResults.value = await studentService.getAllStudents({ search: studentSearch.value, limit: 8 })
    } catch { studentResults.value = [] }
  }, 300)
}

const selectStudent = (s) => {
  form.value.student_id = s.id
  form.value.student_name = `${s.first_name} ${s.last_name}`
  studentSearch.value = ''
  studentResults.value = []
}

const saveRecord = async () => {
  if (!form.value.student_id || !form.value.incident_type || !form.value.description) return
  saving.value = true
  try {
    await apiFetch('/api/discipline/', { method: 'POST', body: JSON.stringify({
      student_id: form.value.student_id,
      incident_date: form.value.incident_date,
      incident_type: form.value.incident_type,
      description: form.value.description,
      severity: form.value.severity,
    }) })
    showModal.value = false
    await loadRecords()
  } catch (e) { toast.error(e?.message || 'Failed to record.') }
  finally { saving.value = false }
}

// Detail/resolve modal
const showDetailModal = ref(false)
const selectedRecord = ref(null)
const actionForm = ref({ action_taken: '', action_date: new Date().toISOString().split('T')[0] })
const savingAction = ref(false)

const viewRecord = (r) => {
  selectedRecord.value = r
  actionForm.value = { action_taken: r.action_taken || '', action_date: new Date().toISOString().split('T')[0] }
  showDetailModal.value = true
}

const resolveRecord = (r) => {
  viewRecord(r)
}

const submitResolve = async () => {
  savingAction.value = true
  try {
    await apiFetch(`/api/discipline/${selectedRecord.value.id}`, {
      method: 'PUT',
      body: JSON.stringify({ ...actionForm.value, status: 'Resolved' }),
    })
    showDetailModal.value = false
    await loadRecords()
  } catch { toast.error('Failed to update.') }
  finally { savingAction.value = false }
}

const deleteRecord = async (id) => {
  if (!confirm('Delete this record?')) return
  try {
    await apiFetch(`/api/discipline/${id}`, { method: 'DELETE' })
    await loadRecords()
  } catch { toast.error('Delete failed.') }
}

const fmtDate = (d) => d ? new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : '—'

onMounted(loadRecords)
</script>
