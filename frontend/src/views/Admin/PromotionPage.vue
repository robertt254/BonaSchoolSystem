<template>
  <div class="max-w-5xl mx-auto space-y-6">

    <div>
      <h1 class="text-2xl font-extrabold text-slate-800">Student Promotion</h1>
      <p class="text-sm text-slate-400 mt-0.5">Advance selected students to the next grade level.</p>
    </div>

    <!-- Controls -->
    <div class="bg-white rounded-lg border border-slate-200 p-6 flex flex-wrap gap-4 items-end">
      <div>
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Current Grade</label>
        <select v-model="selectedGrade" class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm outline-none">
          <option v-for="g in GRADES" :key="g" :value="g">{{ g }}</option>
        </select>
      </div>
      <div class="flex-1 min-w-0">
        <p v-if="nextGrade" class="text-sm text-slate-500">
          Will promote to: <span class="font-bold text-school-purple">{{ nextGrade }}</span>
        </p>
        <p v-else class="text-sm text-amber-600 font-medium">Grade 6 students will be marked as Graduated.</p>
      </div>
      <button @click="loadStudents" :disabled="loading"
        class="bg-school-purple text-white px-5 py-2.5 rounded-lg text-sm font-semibold hover:bg-school-purple-l transition disabled:opacity-50">
        {{ loading ? 'Loading…' : 'Load Class' }}
      </button>
    </div>

    <!-- Student table -->
    <div v-if="students.length > 0" class="bg-white rounded-lg border border-slate-200 overflow-hidden">
      <div class="flex items-center justify-between px-5 py-3.5 border-b border-slate-100 bg-slate-50">
        <div class="flex items-center gap-3">
          <input type="checkbox" :checked="allSelected" @change="toggleAll"
            class="w-4 h-4 rounded border-slate-300 accent-school-purple cursor-pointer" />
          <span class="text-sm font-semibold text-slate-700">{{ selectedIds.length }} of {{ students.length }} selected</span>
        </div>
        <button @click="promote" :disabled="selectedIds.length === 0 || promoting"
          class="bg-emerald-600 text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-emerald-700 transition disabled:opacity-50">
          {{ promoting ? 'Promoting…' : `Promote Selected (${selectedIds.length})` }}
        </button>
      </div>
      <table class="w-full text-sm">
        <thead>
          <tr class="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-100">
            <th class="px-5 py-3 text-left w-10"></th>
            <th class="px-5 py-3 text-left">Name</th>
            <th class="px-5 py-3 text-left">Adm No.</th>
            <th class="px-5 py-3 text-left">Guardian</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in students" :key="s.id" class="border-b border-slate-50 hover:bg-slate-50 cursor-pointer"
            @click="toggleStudent(s.id)">
            <td class="px-5 py-3">
              <input type="checkbox" :checked="selectedIds.includes(s.id)" @click.stop="toggleStudent(s.id)"
                class="w-4 h-4 rounded border-slate-300 accent-school-purple cursor-pointer" />
            </td>
            <td class="px-5 py-3 font-medium text-slate-800">{{ s.name }}</td>
            <td class="px-5 py-3 font-mono text-xs text-slate-500">{{ s.admission_number }}</td>
            <td class="px-5 py-3 text-slate-500 text-xs">{{ s.guardian_name || '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else-if="loaded" class="bg-white rounded-lg border border-slate-200 py-12 text-center text-slate-400 text-sm">
      No active students found in {{ selectedGrade }}.
    </div>

    <!-- Success banner -->
    <div v-if="successMsg" class="bg-emerald-50 border border-emerald-200 rounded-xl px-5 py-4 text-emerald-700 text-sm font-semibold">
      {{ successMsg }}
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { apiFetch } from '@/services/api'
import { useAppStore } from '@/stores/app'
import { useToast } from '@/composables/useToast'
const toast = useToast()


const appStore = useAppStore()

const GRADES = ['Play Group','PP1','PP2','Grade 1','Grade 2','Grade 3','Grade 4','Grade 5','Grade 6']
const GRADE_PROGRESSION = {
  'Play Group': 'PP1', 'PP1': 'PP2', 'PP2': 'Grade 1',
  'Grade 1': 'Grade 2', 'Grade 2': 'Grade 3', 'Grade 3': 'Grade 4',
  'Grade 4': 'Grade 5', 'Grade 5': 'Grade 6', 'Grade 6': null,
}

const selectedGrade = ref('Grade 1')
const students = ref([])
const selectedIds = ref([])
const loading = ref(false)
const promoting = ref(false)
const loaded = ref(false)
const successMsg = ref('')

const nextGrade = computed(() => GRADE_PROGRESSION[selectedGrade.value])
const allSelected = computed(() => students.value.length > 0 && selectedIds.value.length === students.value.length)

const loadStudents = async () => {
  loading.value = true
  loaded.value = false
  selectedIds.value = []
  successMsg.value = ''
  try {
    const data = await apiFetch(
      `/api/students/?grade_level=${encodeURIComponent(selectedGrade.value)}&academic_year=${appStore.currentYear}&per_page=300`
    )
    students.value = data.students || data
  } catch { toast.error('Failed to load students.') }
  finally { loading.value = false; loaded.value = true }
}

const toggleAll = () => {
  selectedIds.value = allSelected.value ? [] : students.value.map(s => s.id)
}

const toggleStudent = (id) => {
  const idx = selectedIds.value.indexOf(id)
  if (idx === -1) selectedIds.value.push(id)
  else selectedIds.value.splice(idx, 1)
}

const promote = async () => {
  if (!selectedIds.value.length) return
  const toGrade = nextGrade.value || 'Graduated'
  if (!confirm(`Promote ${selectedIds.value.length} student(s) to ${toGrade}?`)) return
  promoting.value = true
  try {
    const res = await apiFetch('/api/students/promote', {
      method: 'POST',
      body: JSON.stringify({ student_ids: selectedIds.value, to_grade: toGrade }),
    })
    successMsg.value = `${res.promoted ?? selectedIds.value.length} student(s) promoted to ${toGrade}.`
    await loadStudents()
  } catch (e) { toast.error(e?.message || 'Promotion failed.') }
  finally { promoting.value = false }
}
</script>
