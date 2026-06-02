<template>
  <div class="max-w-7xl mx-auto space-y-6">

    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-extrabold text-slate-800">Office Dashboard</h1>
        <p class="text-sm text-slate-400 mt-0.5">Student admissions and daily operations.</p>
      </div>
      <button
        @click="openAddModal"
        class="inline-flex items-center gap-2 bg-school-purple text-white px-5 py-2.5 rounded-xl font-semibold text-sm hover:bg-school-purple-l transition-all shadow-sm"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
        </svg>
        Enroll New Student
      </button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div class="bg-white rounded-xl border border-border p-6">
        <p class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Total Students</p>
        <p class="text-3xl font-extrabold text-slate-800">{{ students.length }}</p>
      </div>
      <div class="bg-white rounded-xl border border-border p-6">
        <p class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Active</p>
        <p class="text-3xl font-extrabold text-emerald-600">{{ activeCount }}</p>
      </div>
      <div class="bg-white rounded-xl border border-border p-6">
        <p class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Male</p>
        <p class="text-3xl font-extrabold text-blue-600">{{ maleCount }}</p>
      </div>
      <div class="bg-white rounded-xl border border-border p-6">
        <p class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">Female</p>
        <p class="text-3xl font-extrabold text-pink-500">{{ femaleCount }}</p>
      </div>
    </div>

    <!-- Search & Filter bar -->
    <div class="bg-white rounded-xl border border-border p-4 flex flex-wrap gap-3 items-end">
      <div class="flex-1 min-w-48">
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Search</label>
        <div class="relative">
          <svg class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Name or admission number…"
            class="w-full border border-slate-300 rounded-lg pl-9 pr-4 py-2.5 text-sm focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none"
            @input="onSearchInput"
          />
        </div>
      </div>
      <div>
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Grade</label>
        <select
          v-model="gradeFilter"
          @change="() => { currentPage.value = 1; fetchStudents(1) }"
          class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none bg-white"
        >
          <option value="">All Grades</option>
          <option v-for="g in GRADES" :key="g" :value="g">{{ g }}</option>
        </select>
      </div>
      <div class="text-sm text-slate-400 self-end pb-1">{{ totalCount }} result{{ totalCount !== 1 ? 's' : '' }}</div>
    </div>

    <!-- Student table -->
    <div class="bg-white rounded-xl border border-border overflow-hidden">
      <div v-if="loading" class="py-16 flex justify-center">
        <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
      </div>

      <div v-else-if="students.length === 0" class="py-16 text-center text-slate-400 text-sm">
        {{ searchQuery || gradeFilter ? 'No students match your search.' : 'No students enrolled yet.' }}
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200 text-xs font-bold uppercase tracking-wider text-slate-400">
              <th class="text-left px-5 py-3">Student</th>
              <th class="text-left px-5 py-3">Adm No.</th>
              <th class="text-left px-5 py-3">Grade</th>
              <th class="text-left px-5 py-3 hidden sm:table-cell">Guardian</th>
              <th class="text-left px-5 py-3">Status</th>
              <th class="text-right px-5 py-3">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr
              v-for="student in students"
              :key="student.id"
              class="hover:bg-slate-50 transition-colors"
            >
              <td class="px-5 py-3">
                <div class="flex items-center gap-3">
                  <div
                    class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs shrink-0"
                    :class="student.gender === 'Female' ? 'bg-pink-100 text-pink-600' : 'bg-blue-100 text-blue-600'"
                  >
                    {{ student.first_name.charAt(0) }}{{ student.last_name.charAt(0) }}
                  </div>
                  <div>
                    <p class="font-semibold text-slate-800">{{ student.first_name }} {{ student.last_name }}</p>
                    <p v-if="student.date_of_birth" class="text-xs text-slate-400">{{ calcAge(student.date_of_birth) }}y old</p>
                  </div>
                </div>
              </td>
              <td class="px-5 py-3 font-mono text-xs text-school-navy font-semibold">{{ student.admission_number }}</td>
              <td class="px-5 py-3 text-slate-600">{{ student.grade_level }}</td>
              <td class="px-5 py-3 hidden sm:table-cell text-xs text-slate-600">
                <span v-if="student.guardian_name">
                  <p class="font-medium">{{ student.guardian_name }}</p>
                  <p v-if="student.guardian_phone" class="text-slate-400">{{ student.guardian_phone }}</p>
                </span>
                <span v-else class="text-slate-300">—</span>
              </td>
              <td class="px-5 py-3">
                <span
                  class="px-2 py-0.5 text-xs font-bold uppercase rounded-full"
                  :class="student.status === 'Active' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-500'"
                >{{ student.status }}</span>
              </td>
              <td class="px-5 py-3 text-right space-x-3">
                <router-link :to="`/students/${student.id}`" class="text-xs font-semibold text-school-purple hover:text-school-purple-l transition">View</router-link>
                <button @click="openEditModal(student)" class="text-xs font-semibold text-slate-500 hover:text-slate-700 transition">Edit</button>
                <button @click="deleteStudent(student)" class="text-xs font-semibold text-school-red hover:text-red-700 transition">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalCount > PAGE_SIZE" class="flex items-center justify-between bg-white rounded-xl border border-border px-5 py-3 text-sm">
      <span class="text-slate-400">Page {{ currentPage }} of {{ totalPages }}</span>
      <div class="flex gap-2">
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-3 py-1.5 rounded-lg border border-slate-200 text-slate-600 font-semibold hover:bg-slate-50 transition disabled:opacity-40"
        >Previous</button>
        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage >= totalPages"
          class="px-3 py-1.5 rounded-lg border border-slate-200 text-slate-600 font-semibold hover:bg-slate-50 transition disabled:opacity-40"
        >Next</button>
      </div>
    </div>

    <!-- Enroll / Edit Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-slate-900/50 flex items-center justify-center p-4 z-50 animate-fade-in"
    >
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-lg overflow-hidden max-h-[90vh] overflow-y-auto border border-border">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50 sticky top-0 z-10">
          <h2 class="text-lg font-extrabold text-slate-800">
            {{ isEditing ? 'Edit Student Record' : 'Enroll New Student' }}
          </h2>
          <button @click="closeModal" class="text-slate-400 hover:text-slate-600 hover:bg-slate-100 h-8 w-8 rounded-full flex items-center justify-center transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveStudent" class="p-6 space-y-5">

          <p class="text-xs font-bold uppercase tracking-widest text-slate-400">Student Details</p>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">First Name <span class="text-school-red">*</span></label>
              <input v-model="formData.first_name" required type="text" class="w-full border border-slate-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none text-sm" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Last Name <span class="text-school-red">*</span></label>
              <input v-model="formData.last_name" required type="text" class="w-full border border-slate-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none text-sm" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Date of Birth</label>
              <input v-model="formData.date_of_birth" type="date" class="w-full border border-slate-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none text-sm" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Gender</label>
              <select v-model="formData.gender" class="w-full border border-slate-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none text-sm">
                <option value="">— Select —</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Admission Number</label>
            <input
              v-model="formData.admission_number"
              :disabled="isEditing"
              type="text"
              :placeholder="isEditing ? '' : 'Leave blank to auto-generate (BNS/YYYY/NNNN)'"
              class="w-full border border-slate-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none text-sm"
              :class="isEditing ? 'bg-slate-50 text-slate-400 cursor-not-allowed' : ''"
            />
            <p class="text-xs text-slate-400 mt-1">{{ isEditing ? 'Admission numbers cannot be changed.' : 'Auto-generated if left blank.' }}</p>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Grade Level <span class="text-school-red">*</span></label>
              <select v-model="formData.grade_level" required class="w-full border border-slate-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none text-sm">
                <option v-for="g in GRADES" :key="g" :value="g">{{ g }}</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Status</label>
              <select v-model="formData.status" required class="w-full border border-slate-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none text-sm">
                <option value="Active">Active</option>
                <option value="Graduated">Graduated</option>
                <option value="Transferred">Transferred</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Home Address</label>
              <input v-model="formData.address" type="text" placeholder="e.g. Ruaka, Nairobi" class="w-full border border-slate-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none text-sm" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Previous School</label>
              <input v-model="formData.previous_school" type="text" placeholder="Transfer from (optional)" class="w-full border border-slate-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none text-sm" />
            </div>
          </div>

          <p class="text-xs font-bold uppercase tracking-widest text-slate-400 pt-2">Primary Guardian / Parent</p>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Name</label>
              <input v-model="formData.guardian_name" type="text" placeholder="Full name" class="w-full border border-slate-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none text-sm" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Phone</label>
              <input v-model="formData.guardian_phone" type="tel" placeholder="07XX XXX XXX" class="w-full border border-slate-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none text-sm" />
            </div>
          </div>

          <p class="text-xs font-bold uppercase tracking-widest text-slate-400 pt-2">Second Guardian / Parent <span class="normal-case font-normal text-slate-300">(optional)</span></p>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Name</label>
              <input v-model="formData.guardian2_name" type="text" placeholder="Full name" class="w-full border border-slate-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none text-sm" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Phone</label>
              <input v-model="formData.guardian2_phone" type="tel" placeholder="07XX XXX XXX" class="w-full border border-slate-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple outline-none text-sm" />
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              type="button"
              @click="closeModal"
              class="px-5 py-2.5 text-slate-600 hover:bg-slate-100 rounded-lg font-semibold transition text-sm"
            >Cancel</button>
            <button
              type="submit"
              :disabled="saving"
              class="px-5 py-2.5 bg-school-purple text-white rounded-lg font-semibold hover:bg-school-purple-l transition text-sm disabled:opacity-50"
            >{{ saving ? 'Saving…' : isEditing ? 'Save Changes' : 'Enroll Student' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import studentService from '@/services/studentService'
import { useToast } from '@/composables/useToast'
const toast = useToast()


const GRADES = ['Play Group', 'PP1', 'PP2', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6']
const PAGE_SIZE = 50

const students = ref([])
const loading = ref(true)
const saving = ref(false)
const totalCount = ref(0)
const currentPage = ref(1)

const totalPages = computed(() => Math.max(1, Math.ceil(totalCount.value / PAGE_SIZE)))

const showModal = ref(false)
const isEditing = ref(false)
const currentStudentId = ref(null)

const searchQuery = ref('')
const gradeFilter = ref('')
let searchTimer = null

// Stats use the current page data — counts from full list are now server-derived
const activeCount = computed(() => students.value.filter(s => s.status === 'Active').length)
const maleCount = computed(() => students.value.filter(s => s.gender === 'Male').length)
const femaleCount = computed(() => students.value.filter(s => s.gender === 'Female').length)

const calcAge = (dob) => Math.floor((Date.now() - new Date(dob).getTime()) / (1000 * 60 * 60 * 24 * 365.25))

const formData = reactive({
  first_name: '',
  last_name: '',
  admission_number: '',
  grade_level: 'Play Group',
  status: 'Active',
  date_of_birth: '',
  gender: '',
  guardian_name: '',
  guardian_phone: '',
  guardian2_name: '',
  guardian2_phone: '',
  address: '',
  previous_school: '',
})

const fetchStudents = async (page = currentPage.value) => {
  loading.value = true
  try {
    const skip = (page - 1) * PAGE_SIZE
    const data = await studentService.getAllStudents({
      search: searchQuery.value || undefined,
      grade: gradeFilter.value || undefined,
      skip,
      limit: PAGE_SIZE,
    })
    students.value = data
    // If the returned count equals PAGE_SIZE, there may be more pages
    if (data.length === PAGE_SIZE && page === currentPage.value) {
      // Fetch total count with same filters but limit=1000 for header count
      // Use a lightweight approach: if full page returned, estimate there's at least one more page
      totalCount.value = skip + data.length + (data.length === PAGE_SIZE ? PAGE_SIZE : 0)
    } else {
      totalCount.value = skip + data.length
    }
    currentPage.value = page
  } catch (err) {
    console.error('Failed to load students:', err)
  } finally {
    loading.value = false
  }
}

const goToPage = (page) => {
  if (page < 1 || page > totalPages.value) return
  fetchStudents(page)
}

const onSearchInput = () => {
  clearTimeout(searchTimer)
  currentPage.value = 1
  searchTimer = setTimeout(() => fetchStudents(1), 350)
}

onMounted(fetchStudents)

const openAddModal = () => {
  isEditing.value = false
  currentStudentId.value = null
  Object.assign(formData, {
    first_name: '', last_name: '', admission_number: '',
    grade_level: 'Play Group', status: 'Active',
    date_of_birth: '', gender: '',
    guardian_name: '', guardian_phone: '',
    guardian2_name: '', guardian2_phone: '',
    address: '', previous_school: '',
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
    date_of_birth: student.date_of_birth || '',
    gender: student.gender || '',
    guardian_name: student.guardian_name || '',
    guardian_phone: student.guardian_phone || '',
    guardian2_name: student.guardian2_name || '',
    guardian2_phone: student.guardian2_phone || '',
    address: student.address || '',
    previous_school: student.previous_school || '',
  })
  showModal.value = true
}

const closeModal = () => { showModal.value = false }

const saveStudent = async () => {
  saving.value = true
  try {
    const payload = { ...formData }
    if (!payload.admission_number) payload.admission_number = null
    if (!payload.date_of_birth) payload.date_of_birth = null
    if (!payload.gender) payload.gender = null
    if (!payload.guardian_name) payload.guardian_name = null
    if (!payload.guardian_phone) payload.guardian_phone = null
    if (!payload.guardian2_name) payload.guardian2_name = null
    if (!payload.guardian2_phone) payload.guardian2_phone = null
    if (!payload.address) payload.address = null
    if (!payload.previous_school) payload.previous_school = null

    if (isEditing.value) {
      await studentService.updateStudent(currentStudentId.value, payload)
    } else {
      await studentService.createStudent(payload)
    }
    closeModal()
    await fetchStudents()
  } catch (err) {
    toast.error("An error occurred. Check the admission number isn't a duplicate.")
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
    toast.error('Failed to delete the student.')
    console.error(err)
  }
}
</script>
