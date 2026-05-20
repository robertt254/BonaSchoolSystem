<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 bg-gray-50 min-h-screen">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-slate-900">Office Dashboard</h1>
      <p class="text-slate-500 mt-1">Daily operations and student management.</p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-8 mb-8">
      <div class="bg-white p-8 rounded-[12px] shadow-sm border border-[#E2E8F0]">
        <div class="text-sm font-semibold text-slate-500 uppercase">Total Students</div>
        <div class="mt-2 text-3xl font-bold text-school-navy">{{ students.length }}</div>
      </div>
      <div class="bg-white p-8 rounded-[12px] shadow-sm border border-[#E2E8F0]">
        <div class="text-sm font-semibold text-slate-500 uppercase">Active Students</div>
        <div class="mt-2 text-3xl font-bold text-emerald-600">
          {{ students.filter(s => s.status === 'Active').length }}
        </div>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mt-12">
      <h2 class="text-2xl font-bold text-gray-800">Student Directory</h2>
      <button
        @click="openAddModal"
        class="bg-school-navy text-white px-6 py-3.5 rounded shadow hover:bg-school-navy/90 transition shrink-0"
      >
        + Add New Student
      </button>
    </div>

    <!-- Search & Filter bar -->
    <div class="flex flex-col sm:flex-row gap-3">
      <div class="relative flex-1">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" />
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by name or admission number…"
          class="w-full border border-slate-300 rounded-lg pl-9 pr-4 py-2.5 text-sm focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none"
          @input="onSearchInput"
        />
      </div>
      <select
        v-model="gradeFilter"
        @change="fetchStudents"
        class="border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-white"
      >
        <option value="">All Grades</option>
        <option value="Play Group">Play Group</option>
        <option value="PP1">PP1</option>
        <option value="PP2">PP2</option>
        <option value="Grade 1">Grade 1</option>
        <option value="Grade 2">Grade 2</option>
        <option value="Grade 3">Grade 3</option>
        <option value="Grade 4">Grade 4</option>
        <option value="Grade 5">Grade 5</option>
        <option value="Grade 6">Grade 6</option>
      </select>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-12 text-gray-500">
      <span class="animate-pulse text-lg">Fetching student records...</span>
    </div>

    <div v-else class="bg-white rounded-[12px] shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-100 text-gray-600 text-sm uppercase tracking-wider border-b border-gray-200">
            <th class="py-5 px-6 font-semibold">Name</th>
            <th class="py-5 px-6 font-semibold">Admission No.</th>
            <th class="py-5 px-6 font-semibold">Grade</th>
            <th class="py-5 px-6 font-semibold hidden sm:table-cell">Guardian</th>
            <th class="py-5 px-6 font-semibold">Status</th>
            <th class="py-5 px-6 font-semibold text-right">Actions</th>
          </tr>
        </thead>

        <tbody class="text-gray-700">
          <tr
            v-for="student in students"
            :key="student.id"
            class="border-b border-gray-50 hover:bg-gray-50 transition duration-150"
          >
            <td class="py-4 px-6 font-medium">{{ student.first_name }} {{ student.last_name }}</td>
            <td class="py-4 px-6 text-gray-500 font-mono text-xs">{{ student.admission_number }}</td>
            <td class="py-4 px-6">{{ student.grade_level }}</td>
            <td class="py-4 px-6 hidden sm:table-cell text-sm text-slate-500">
              <span v-if="student.guardian_name">
                {{ student.guardian_name }}
                <span v-if="student.guardian_phone" class="block text-xs text-slate-400">{{ student.guardian_phone }}</span>
              </span>
              <span v-else class="text-slate-300">—</span>
            </td>
            <td class="py-4 px-6">
              <span
                class="px-3 py-1 text-xs font-bold rounded-full"
                :class="{
                  'bg-green-100 text-green-700': student.status === 'Active',
                  'bg-red-100 text-red-700': student.status !== 'Active',
                }"
              >{{ student.status }}</span>
            </td>
            <td class="py-4 px-6 text-right space-x-3">
              <router-link
                :to="`/students/${student.id}`"
                class="text-slate-500 hover:text-school-navy font-medium text-sm"
              >View</router-link>
              <button
                @click="openEditModal(student)"
                class="text-school-navy/70 hover:text-school-navy/90 font-medium text-sm"
              >Edit</button>
              <button
                @click="deleteStudent(student)"
                class="text-red-600 hover:text-red-800 font-medium text-sm"
              >Delete</button>
            </td>
          </tr>

          <tr v-if="students.length === 0">
            <td colspan="6" class="py-6 px-8 text-center text-gray-500 italic">
              {{ searchQuery || gradeFilter ? 'No students match your search.' : 'No students are currently enrolled in the system.' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Enroll / Edit Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
    >
      <div class="bg-white rounded-[12px] shadow-xl w-full max-w-lg overflow-hidden max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center sticky top-0 bg-white z-10">
          <h2 class="text-xl font-bold text-gray-800">
            {{ isEditing ? 'Edit Student' : 'Enroll New Student' }}
          </h2>
          <button @click="closeModal" class="text-gray-400 hover:text-gray-600 font-bold text-xl">
            &times;
          </button>
        </div>

        <form @submit.prevent="saveStudent" class="p-6 space-y-5">
          <!-- Name row -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
              <input
                v-model="formData.first_name"
                required
                type="text"
                class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-school-navy outline-none text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
              <input
                v-model="formData.last_name"
                required
                type="text"
                class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-school-navy outline-none text-sm"
              />
            </div>
          </div>

          <!-- Admission number -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Admission Number</label>
            <input
              v-model="formData.admission_number"
              :disabled="isEditing"
              required
              type="text"
              class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-school-navy outline-none text-sm"
              :class="isEditing ? 'bg-gray-100 text-gray-500' : ''"
            />
            <p v-if="isEditing" class="text-xs text-gray-500 mt-1">Admission numbers cannot be changed.</p>
          </div>

          <!-- Grade + Status -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Grade Level</label>
              <select
                v-model="formData.grade_level"
                required
                class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-school-navy outline-none text-sm"
              >
                <option value="Play Group">Play Group</option>
                <option value="PP1">PP1</option>
                <option value="PP2">PP2</option>
                <option value="Grade 1">Grade 1</option>
                <option value="Grade 2">Grade 2</option>
                <option value="Grade 3">Grade 3</option>
                <option value="Grade 4">Grade 4</option>
                <option value="Grade 5">Grade 5</option>
                <option value="Grade 6">Grade 6</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select
                v-model="formData.status"
                required
                class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-school-navy outline-none text-sm"
              >
                <option value="Active">Active</option>
                <option value="Graduated">Graduated</option>
                <option value="Transferred">Transferred</option>
              </select>
            </div>
          </div>

          <!-- Guardian section -->
          <div class="pt-2">
            <p class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-3">Guardian / Parent Info</p>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Guardian Name</label>
                <input
                  v-model="formData.guardian_name"
                  type="text"
                  placeholder="Optional"
                  class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-school-navy outline-none text-sm"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Guardian Phone</label>
                <input
                  v-model="formData.guardian_phone"
                  type="tel"
                  placeholder="Optional"
                  class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-school-navy outline-none text-sm"
                />
              </div>
            </div>
          </div>

          <div class="flex justify-end gap-4 pt-4 border-t border-gray-100 mt-2">
            <button
              type="button"
              @click="closeModal"
              class="px-5 py-3 text-gray-600 hover:bg-gray-100 rounded-lg font-medium transition text-sm"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="saving"
              class="px-5 py-3 bg-school-navy text-white rounded-lg font-medium hover:bg-school-navy/90 transition text-sm disabled:opacity-50"
            >
              {{ saving ? 'Saving…' : isEditing ? 'Save Changes' : 'Enroll Student' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import studentService from '@/services/studentService'

const students = ref([])
const loading = ref(true)
const saving = ref(false)

const showModal = ref(false)
const isEditing = ref(false)
const currentStudentId = ref(null)

const searchQuery = ref('')
const gradeFilter = ref('')
let searchTimer = null

const formData = reactive({
  first_name: '',
  last_name: '',
  admission_number: '',
  grade_level: 'Play Group',
  status: 'Active',
  guardian_name: '',
  guardian_phone: '',
})

const fetchStudents = async () => {
  loading.value = true
  try {
    students.value = await studentService.getAllStudents({
      search: searchQuery.value || undefined,
      grade: gradeFilter.value || undefined,
    })
  } catch (err) {
    console.error('Failed to load students:', err)
  } finally {
    loading.value = false
  }
}

const onSearchInput = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(fetchStudents, 350)
}

onMounted(fetchStudents)

const openAddModal = () => {
  isEditing.value = false
  currentStudentId.value = null

  let nextIdNum = 1
  if (students.value.length > 0) {
    const nums = students.value
      .map(s => { const m = s.admission_number.match(/^BONA-(\d+)$/); return m ? parseInt(m[1], 10) : 0 })
      .filter(n => n > 0)
    if (nums.length) nextIdNum = Math.max(...nums) + 1
  }

  Object.assign(formData, {
    first_name: '',
    last_name: '',
    admission_number: `BONA-${nextIdNum.toString().padStart(4, '0')}`,
    grade_level: 'Play Group',
    status: 'Active',
    guardian_name: '',
    guardian_phone: '',
  })
  showModal.value = true
}

const openEditModal = (student) => {
  isEditing.value = true
  currentStudentId.value = student.id
  Object.assign(formData, {
    first_name: student.first_name,
    last_name: student.last_name,
    admission_number: student.admission_number,
    grade_level: student.grade_level,
    status: student.status,
    guardian_name: student.guardian_name || '',
    guardian_phone: student.guardian_phone || '',
  })
  showModal.value = true
}

const closeModal = () => { showModal.value = false }

const saveStudent = async () => {
  saving.value = true
  try {
    const payload = { ...formData }
    if (!payload.guardian_name) payload.guardian_name = null
    if (!payload.guardian_phone) payload.guardian_phone = null

    if (isEditing.value) {
      await studentService.updateStudent(currentStudentId.value, payload)
    } else {
      await studentService.createStudent(payload)
    }
    closeModal()
    await fetchStudents()
  } catch (err) {
    alert("An error occurred. Check the admission number isn't a duplicate.")
    console.error(err)
  } finally {
    saving.value = false
  }
}

const deleteStudent = async (student) => {
  if (!window.confirm(`Delete ${student.first_name} ${student.last_name}? This cannot be undone.`)) return
  try {
    await studentService.deleteStudent(student.id)
    await fetchStudents()
  } catch (err) {
    alert('Failed to delete the student.')
    console.error(err)
  }
}
</script>
