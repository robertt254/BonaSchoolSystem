<template>
  <div class="max-w-7xl mx-auto space-y-6">

    <!-- Grade overview cards -->
    <div v-if="loadingSummary" class="py-16 flex justify-center">
      <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
    </div>

    <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
      <button
        v-for="cls in summary"
        :key="cls.grade_level"
        @click="openClass(cls.grade_level)"
        :class="[
          'bg-white rounded-[12px] border p-4 text-left hover:shadow-md transition-all group',
          selectedGrade === cls.grade_level
            ? 'border-school-purple ring-2 ring-school-purple/20'
            : 'border-[#E2E8F0] hover:border-school-purple/40',
        ]"
      >
        <div class="flex items-center justify-between mb-3">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center font-black text-xs text-white"
            :style="{ background: gradeColor(cls.grade_level) }">
            {{ cls.grade_level.replace('Grade ', 'G').replace('Play Group', 'PG') }}
          </div>
          <span class="text-[10px] font-bold uppercase text-slate-400">{{ cls.total }} pupils</span>
        </div>
        <p class="font-bold text-slate-800 text-sm leading-tight">{{ cls.grade_level }}</p>
        <div class="mt-2 grid grid-cols-2 gap-1 text-[10px] text-slate-500">
          <span class="flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>{{ cls.male }}M</span>
          <span class="flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-pink-400"></span>{{ cls.female }}F</span>
        </div>
        <div class="mt-2 h-1.5 bg-slate-100 rounded-full overflow-hidden">
          <div
            class="h-full bg-emerald-400 rounded-full transition-all"
            :style="{ width: cls.total > 0 && cls.present_today > 0 ? `${Math.round(cls.present_today / cls.total * 100)}%` : '0%' }"
          ></div>
        </div>
        <p class="text-[10px] text-slate-400 mt-1">
          {{ cls.present_today }}/{{ cls.total }} present today
        </p>
      </button>
    </div>

    <!-- Class detail panel -->
    <div v-if="selectedGrade" class="bg-white rounded-[12px] border border-[#E2E8F0] overflow-hidden">

      <!-- Tab header -->
      <div class="border-b border-slate-100 bg-slate-50 px-6 flex items-center justify-between min-h-[56px]">
        <div class="flex">
          <button
            v-for="tab in TABS"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'px-5 py-[18px] text-sm font-bold border-b-2 transition-colors whitespace-nowrap',
              activeTab === tab.id
                ? 'border-school-purple text-school-purple'
                : 'border-transparent text-slate-400 hover:text-slate-600',
            ]"
          >
            {{ tab.label }}
            <span v-if="tab.id === 'subjects' && subjects.length" class="ml-1.5 text-[10px] font-bold bg-school-purple/10 text-school-purple rounded-full px-1.5 py-0.5">
              {{ subjects.length }}
            </span>
          </button>
        </div>

        <!-- Roster search -->
        <div v-if="activeTab === 'roster'" class="relative">
          <svg class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input v-model="rosterSearch" type="text" placeholder="Search…" class="pl-9 pr-3 py-2 border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple w-44" />
        </div>

        <!-- Subjects actions -->
        <div v-if="activeTab === 'subjects'" class="flex items-center gap-3 py-3">
          <button
            v-if="canManage && !subjects.length"
            @click="seedSubjects"
            :disabled="seeding"
            class="text-xs font-bold px-3 py-1.5 rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors flex items-center gap-1.5 disabled:opacity-50"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
            </svg>
            {{ seeding ? 'Seeding…' : 'Seed CBC Subjects' }}
          </button>
          <button
            v-if="canManage"
            @click="openAddSubject"
            class="text-xs font-bold px-3 py-1.5 rounded-lg bg-school-purple text-white hover:bg-school-purple/90 transition-colors flex items-center gap-1.5"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
            </svg>
            Add Subject
          </button>
        </div>
      </div>

      <!-- ── ROSTER TAB ──────────────────────────────────────────────────── -->
      <div v-if="activeTab === 'roster'">
        <div v-if="loadingRoster" class="py-12 flex justify-center">
          <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-[11px] font-bold uppercase tracking-wider text-slate-400">
                <th class="text-left px-6 py-3">#</th>
                <th class="text-left px-6 py-3">Student</th>
                <th class="text-left px-6 py-3">Adm No.</th>
                <th class="text-left px-6 py-3">Gender</th>
                <th class="text-left px-6 py-3">Age</th>
                <th class="text-center px-6 py-3">Attendance</th>
                <th class="text-right px-6 py-3">Fee Balance</th>
                <th class="text-right px-6 py-3">Status</th>
                <th class="text-right px-6 py-3"></th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr
                v-for="(s, i) in filteredRoster"
                :key="s.id"
                class="hover:bg-slate-50 transition-colors"
              >
                <td class="px-6 py-3.5 text-slate-400 text-xs">{{ i + 1 }}</td>
                <td class="px-6 py-3.5">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs shrink-0"
                      :class="s.gender === 'Female' ? 'bg-pink-100 text-pink-600' : 'bg-blue-100 text-blue-600'">
                      {{ s.first_name.charAt(0) }}{{ s.last_name.charAt(0) }}
                    </div>
                    <span class="font-semibold text-slate-800">{{ s.first_name }} {{ s.last_name }}</span>
                  </div>
                </td>
                <td class="px-6 py-3.5 font-mono text-xs text-school-navy">{{ s.admission_number }}</td>
                <td class="px-6 py-3.5">
                  <span v-if="s.gender" class="text-xs font-semibold px-2 py-0.5 rounded-full"
                    :class="s.gender === 'Female' ? 'bg-pink-50 text-pink-600' : 'bg-blue-50 text-blue-600'">
                    {{ s.gender }}
                  </span>
                  <span v-else class="text-slate-300">—</span>
                </td>
                <td class="px-6 py-3.5 text-slate-500 text-xs">
                  {{ s.date_of_birth ? calcAge(s.date_of_birth) + 'y' : '—' }}
                </td>
                <td class="px-6 py-3.5 text-center">
                  <template v-if="s.attendance_pct !== null">
                    <div class="flex items-center justify-center gap-2">
                      <div class="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                        <div class="h-full rounded-full transition-all"
                          :class="s.attendance_pct >= 80 ? 'bg-emerald-400' : s.attendance_pct >= 60 ? 'bg-amber-400' : 'bg-red-400'"
                          :style="{ width: s.attendance_pct + '%' }"></div>
                      </div>
                      <span class="text-xs font-bold" :class="s.attendance_pct >= 80 ? 'text-emerald-600' : s.attendance_pct >= 60 ? 'text-amber-600' : 'text-red-600'">
                        {{ s.attendance_pct }}%
                      </span>
                    </div>
                  </template>
                  <span v-else class="text-slate-300 text-xs">No data</span>
                </td>
                <td class="px-6 py-3.5 text-right font-bold" :class="s.fee_balance > 0 ? 'text-school-red' : 'text-emerald-600'">
                  {{ s.fee_balance > 0 ? formatCurrency(s.fee_balance) : 'Paid' }}
                </td>
                <td class="px-6 py-3.5 text-right">
                  <span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full"
                    :class="s.status === 'Active' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-500'">
                    {{ s.status }}
                  </span>
                </td>
                <td class="px-6 py-3.5 text-right">
                  <router-link :to="`/students/${s.id}`" class="text-xs font-semibold text-school-purple hover:text-school-purple-l transition">
                    Profile
                  </router-link>
                </td>
              </tr>
              <tr v-if="filteredRoster.length === 0">
                <td colspan="9" class="px-6 py-10 text-center text-slate-400 text-sm">No students found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ── SUBJECTS TAB ────────────────────────────────────────────────── -->
      <div v-if="activeTab === 'subjects'" class="p-6">

        <!-- Loading -->
        <div v-if="loadingSubjects" class="py-12 flex justify-center">
          <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
        </div>

        <!-- Empty state -->
        <div v-else-if="!subjects.length" class="py-12 text-center">
          <div class="w-14 h-14 bg-slate-100 rounded-2xl mx-auto flex items-center justify-center mb-4">
            <svg class="w-7 h-7 text-slate-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.966 8.966 0 00-6 2.292m0-14.25v14.25"/>
            </svg>
          </div>
          <p class="font-bold text-slate-700 mb-1">No subjects configured yet</p>
          <p class="text-sm text-slate-400 mb-5">{{ canManage ? 'Click "Seed CBC Subjects" to auto-populate from the national curriculum, or add subjects manually.' : 'Contact the admin to set up subjects for this class.' }}</p>
          <button v-if="canManage" @click="seedSubjects" :disabled="seeding"
            class="mx-auto inline-flex items-center gap-2 px-5 py-2.5 bg-school-purple text-white text-sm font-bold rounded-xl hover:bg-school-purple/90 transition-all disabled:opacity-50">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
            </svg>
            {{ seeding ? 'Seeding…' : 'Seed CBC Subjects for All Grades' }}
          </button>
        </div>

        <!-- Subject cards grid -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="subject in subjects"
            :key="subject.id"
            class="bg-white border border-slate-200 rounded-xl p-4 flex items-start gap-4 hover:shadow-sm transition-all group"
          >
            <!-- Color dot / initial -->
            <div
              class="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold text-sm shrink-0"
              :style="{ background: subject.color }"
            >
              {{ subject.name.charAt(0) }}
            </div>

            <div class="flex-1 min-w-0">
              <p class="font-bold text-slate-800 text-[14px] leading-tight truncate">{{ subject.name }}</p>
              <div class="mt-1 flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-slate-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
                </svg>
                <span v-if="subject.teacher_name" class="text-[12px] text-slate-600 font-medium truncate">{{ subject.teacher_name }}</span>
                <span v-else class="text-[12px] text-slate-400 italic">No teacher assigned</span>
              </div>
            </div>

            <!-- Edit button (admin/principal only) -->
            <button
              v-if="canManage"
              @click="openEditSubject(subject)"
              class="opacity-0 group-hover:opacity-100 transition-opacity w-7 h-7 rounded-lg bg-slate-100 hover:bg-school-purple/10 hover:text-school-purple text-slate-500 flex items-center justify-center shrink-0"
              title="Assign teacher / rename"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="!loadingSummary" class="bg-white rounded-[12px] border border-[#E2E8F0] py-16 text-center text-slate-400 text-sm">
      Select a class above to view the roster and subjects.
    </div>

    <!-- ── Add/Edit Subject Modal ─────────────────────────────────────── -->
    <div
      v-if="showSubjectModal"
      class="fixed inset-0 bg-slate-900/40 flex items-center justify-center p-4 z-50"
    >
      <div class="bg-white rounded-[14px] shadow-2xl w-full max-w-sm overflow-hidden border border-slate-200">
        <div class="px-6 py-4 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
          <h2 class="font-bold text-slate-800">{{ editingSubject ? 'Edit Subject' : 'Add Subject' }}</h2>
          <button @click="showSubjectModal = false" class="text-slate-400 hover:text-slate-600 w-7 h-7 rounded-full hover:bg-slate-100 flex items-center justify-center transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveSubject" class="p-6 space-y-4">
          <div v-if="!editingSubject">
            <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5">Subject Name</label>
            <input
              v-model="subjectForm.name"
              type="text"
              required
              placeholder="e.g. Mathematics"
              class="w-full border border-slate-200 rounded-xl px-3 py-2.5 text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple"
            />
          </div>

          <div v-else>
            <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5">Subject</label>
            <p class="font-bold text-slate-800">{{ editingSubject.name }}</p>
          </div>

          <div>
            <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5">Assigned Teacher</label>
            <select
              v-model="subjectForm.teacher_id"
              class="w-full border border-slate-200 rounded-xl px-3 py-2.5 text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple bg-white cursor-pointer"
            >
              <option :value="null">— No teacher assigned —</option>
              <option v-for="t in teachers" :key="t.id" :value="t.id">
                {{ t.name }} · {{ t.job_title || t.role }}
              </option>
            </select>
          </div>

          <div v-if="subjectModalError" class="rounded-xl bg-red-50 border border-red-200 px-4 py-3 text-[13px] font-medium text-red-700">
            {{ subjectModalError }}
          </div>

          <div class="flex justify-end gap-3 pt-2">
            <button type="button" @click="showSubjectModal = false" class="px-4 py-2 text-sm font-bold text-slate-600 hover:bg-slate-100 rounded-xl transition-colors">Cancel</button>
            <button
              v-if="canManage && editingSubject"
              type="button"
              @click="confirmDelete(editingSubject)"
              class="px-4 py-2 text-sm font-bold text-red-600 hover:bg-red-50 rounded-xl transition-colors"
            >
              Delete
            </button>
            <button type="submit" :disabled="savingSubject" class="px-5 py-2 text-sm font-bold bg-school-purple text-white rounded-xl hover:bg-school-purple/90 transition-all disabled:opacity-50">
              {{ savingSubject ? 'Saving…' : (editingSubject ? 'Save Changes' : 'Add Subject') }}
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const userRole = computed(() => authStore.user?.role || '')
const canManage = computed(() => ['admin', 'principal'].includes(userRole.value))

const TABS = [
  { id: 'roster', label: 'Roster' },
  { id: 'subjects', label: 'Subjects' },
]

const GRADE_COLORS = {
  'Play Group': '#F59E0B', 'PP1': '#8B5CF6', 'PP2': '#7C3AED',
  'Grade 1': '#3B82F6', 'Grade 2': '#06B6D4', 'Grade 3': '#10B981',
  'Grade 4': '#6366F1', 'Grade 5': '#EC4899', 'Grade 6': '#EF4444',
}

// ── State ─────────────────────────────────────────────────────────────────────
const summary = ref([])
const roster = ref([])
const subjects = ref([])
const teachers = ref([])
const loadingSummary = ref(false)
const loadingRoster = ref(false)
const loadingSubjects = ref(false)
const selectedGrade = ref('')
const activeTab = ref('roster')
const rosterSearch = ref('')
const seeding = ref(false)

const showSubjectModal = ref(false)
const editingSubject = ref(null)
const subjectForm = ref({ name: '', teacher_id: null })
const subjectModalError = ref('')
const savingSubject = ref(false)

// ── Computed ──────────────────────────────────────────────────────────────────
const gradeColor = (g) => GRADE_COLORS[g] || '#64748B'

const filteredRoster = computed(() => {
  const q = rosterSearch.value.toLowerCase()
  if (!q) return roster.value
  return roster.value.filter(s =>
    `${s.first_name} ${s.last_name}`.toLowerCase().includes(q) ||
    s.admission_number.toLowerCase().includes(q)
  )
})

// ── Helpers ───────────────────────────────────────────────────────────────────
const formatCurrency = (v) =>
  new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 }).format(v)

const calcAge = (dob) => Math.floor((Date.now() - new Date(dob).getTime()) / (1000 * 60 * 60 * 24 * 365.25))

// ── Data fetching ─────────────────────────────────────────────────────────────
const loadRoster = async (grade) => {
  loadingRoster.value = true
  try {
    roster.value = await apiFetch(`/api/students/classes/${encodeURIComponent(grade)}`)
  } catch (e) {
    console.error(e)
    roster.value = []
  } finally {
    loadingRoster.value = false
  }
}

const loadSubjects = async (grade) => {
  loadingSubjects.value = true
  try {
    subjects.value = await apiFetch(`/api/subjects/?grade=${encodeURIComponent(grade)}`)
  } catch (e) {
    console.error(e)
    subjects.value = []
  } finally {
    loadingSubjects.value = false
  }
}

const loadTeachers = async () => {
  if (teachers.value.length) return
  try {
    const staff = await apiFetch('/api/staff/')
    teachers.value = staff.filter(s => ['teacher', 'principal', 'admin'].includes(s.role))
  } catch (e) {
    console.error(e)
  }
}

const openClass = async (grade) => {
  if (selectedGrade.value === grade) {
    selectedGrade.value = ''
    roster.value = []
    subjects.value = []
    return
  }
  selectedGrade.value = grade
  activeTab.value = 'roster'
  await Promise.all([loadRoster(grade), loadSubjects(grade)])
}

// ── Subject management ────────────────────────────────────────────────────────
const seedSubjects = async () => {
  seeding.value = true
  try {
    await apiFetch('/api/subjects/seed', { method: 'POST' })
    await loadSubjects(selectedGrade.value)
  } catch (e) {
    console.error(e)
  } finally {
    seeding.value = false
  }
}

const openAddSubject = async () => {
  await loadTeachers()
  editingSubject.value = null
  subjectForm.value = { name: '', teacher_id: null }
  subjectModalError.value = ''
  showSubjectModal.value = true
}

const openEditSubject = async (subject) => {
  await loadTeachers()
  editingSubject.value = subject
  subjectForm.value = { name: subject.name, teacher_id: subject.teacher_id }
  subjectModalError.value = ''
  showSubjectModal.value = true
}

const saveSubject = async () => {
  subjectModalError.value = ''
  savingSubject.value = true
  try {
    if (editingSubject.value) {
      await apiFetch(`/api/subjects/${editingSubject.value.id}`, {
        method: 'PUT',
        body: JSON.stringify({ teacher_id: subjectForm.value.teacher_id ?? 0 }),
      })
    } else {
      if (!subjectForm.value.name.trim()) {
        subjectModalError.value = 'Subject name is required.'
        return
      }
      await apiFetch('/api/subjects/', {
        method: 'POST',
        body: JSON.stringify({
          name: subjectForm.value.name.trim(),
          grade_level: selectedGrade.value,
          teacher_id: subjectForm.value.teacher_id,
        }),
      })
    }
    showSubjectModal.value = false
    await loadSubjects(selectedGrade.value)
  } catch (e) {
    subjectModalError.value = e.message || 'Failed to save subject.'
  } finally {
    savingSubject.value = false
  }
}

const confirmDelete = async (subject) => {
  if (!confirm(`Delete "${subject.name}" from ${selectedGrade.value}? This cannot be undone.`)) return
  try {
    await apiFetch(`/api/subjects/${subject.id}`, { method: 'DELETE' })
    showSubjectModal.value = false
    await loadSubjects(selectedGrade.value)
  } catch (e) {
    subjectModalError.value = e.message || 'Failed to delete subject.'
  }
}

// ── Init ──────────────────────────────────────────────────────────────────────
onMounted(async () => {
  loadingSummary.value = true
  try {
    summary.value = await apiFetch('/api/students/classes/summary')
  } catch (e) {
    console.error(e)
  } finally {
    loadingSummary.value = false
  }
})
</script>
