<template>
  <div class="p-8 bg-gray-50 min-h-screen">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">Student Directory</h1>
      <button
        @click="openAddModal"
        class="bg-school-navy text-white px-4 py-2 rounded shadow hover:bg-school-navy/90 transition"
      >
        + Add New Student
      </button>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-12 text-gray-500">
      <span class="animate-pulse text-lg">Fetching student records...</span>
    </div>

    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr
            class="bg-gray-100 text-gray-600 text-sm uppercase tracking-wider border-b border-gray-200"
          >
            <th class="p-4 font-semibold">Name</th>
            <th class="p-4 font-semibold">Admission No.</th>
            <th class="p-4 font-semibold">Grade</th>
            <th class="p-4 font-semibold">Status</th>
            <th class="p-4 font-semibold text-right">Actions</th>
          </tr>
        </thead>

        <tbody class="text-gray-700">
          <tr
            v-for="student in students"
            :key="student.id"
            class="border-b border-gray-50 hover:bg-gray-50 transition duration-150"
          >
            <td class="p-4 font-medium">{{ student.first_name }} {{ student.last_name }}</td>
            <td class="p-4 text-gray-500">{{ student.admission_number }}</td>
            <td class="p-4">{{ student.grade_level }}</td>
            <td class="p-4">
              <span
                class="px-3 py-1 text-xs font-bold rounded-full"
                :class="{
                  'bg-green-100 text-green-700': student.status === 'Active',
                  'bg-red-100 text-red-700': student.status !== 'Active',
                }"
              >
                {{ student.status }}
              </span>
            </td>
            <td class="p-4 text-right space-x-4">
              <button
                @click="openEditModal(student)"
                class="text-school-navy/70 hover:text-school-navy/90 font-medium"
              >
                Edit
              </button>
              <button
                @click="deleteStudent(student)"
                class="text-red-600 hover:text-red-800 font-medium"
              >
                Delete
              </button>
            </td>
          </tr>

          <tr v-if="students.length === 0">
            <td colspan="5" class="p-8 text-center text-gray-500 italic">
              No students are currently enrolled in the system.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
    >
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center">
          <h2 class="text-xl font-bold text-gray-800">
            {{ isEditing ? 'Edit Student' : 'Enroll New Student' }}
          </h2>
          <button @click="closeModal" class="text-gray-400 hover:text-gray-600 font-bold text-xl">
            &times;
          </button>
        </div>

        <form @submit.prevent="saveStudent" class="p-6 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
              <input
                v-model="formData.first_name"
                required
                type="text"
                class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-school-navy outline-none"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
              <input
                v-model="formData.last_name"
                required
                type="text"
                class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-school-navy outline-none"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Admission Number</label>
            <input
              v-model="formData.admission_number"
              :disabled="isEditing"
              required
              type="text"
              class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-school-navy outline-none disabled:bg-gray-100 disabled:text-gray-500"
            />
            <p v-if="isEditing" class="text-xs text-gray-500 mt-1">
              Admission numbers cannot be changed.
            </p>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Grade Level</label>
              <select
                v-model="formData.grade_level"
                required
                class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-school-navy outline-none"
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
                class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-school-navy outline-none"
              >
                <option value="Active">Active</option>
                <option value="Graduated">Graduated</option>
                <option value="Transferred">Transferred</option>
              </select>
            </div>
          </div>

          <div class="flex justify-end space-x-3 pt-4 border-t border-gray-100 mt-6">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg font-medium transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-school-navy text-white rounded-lg font-medium hover:bg-school-navy/90 transition"
            >
              {{ isEditing ? 'Save Changes' : 'Enroll Student' }}
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

// --- STATE ---
const students = ref([])
const loading = ref(true)

// Modal Controls
const showModal = ref(false)
const isEditing = ref(false)
const currentStudentId = ref(null)

// The Form Data
const formData = reactive({
  first_name: '',
  last_name: '',
  admission_number: '',
  grade_level: 'Play Group',
  status: 'Active',
})

// --- DATA FETCHING ---
const fetchStudents = async () => {
  loading.value = true
  try {
    students.value = await studentService.getAllStudents()
  } catch (error) {
    console.error('Failed to load students:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchStudents)

// --- MODAL LOGIC ---
const openAddModal = () => {
  isEditing.value = false
  currentStudentId.value = null
  // Reset form
  Object.assign(formData, {
    first_name: '',
    last_name: '',
    admission_number: '',
    grade_level: 'Play Group',
    status: 'Active',
  })
  showModal.value = true
}

const openEditModal = (student) => {
  isEditing.value = true
  currentStudentId.value = student.id
  // Pre-fill form with clicked student's data
  Object.assign(formData, {
    first_name: student.first_name,
    last_name: student.last_name,
    admission_number: student.admission_number,
    grade_level: student.grade_level,
    status: student.status,
  })
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

// --- CRUD ACTIONS ---
const saveStudent = async () => {
  try {
    if (isEditing.value) {
      await studentService.updateStudent(currentStudentId.value, formData)
    } else {
      await studentService.createStudent(formData)
    }
    closeModal()
    await fetchStudents() // Refresh the table automatically
  } catch (error) {
    alert("An error occurred. Check the admission number isn't a duplicate.")
    console.error(error)
  }
}

const deleteStudent = async (student) => {
  // Built-in browser safety check
  const isConfirmed = window.confirm(
    `Are you absolutely sure you want to delete ${student.first_name} ${student.last_name}? This cannot be undone.`,
  )

  if (isConfirmed) {
    try {
      await studentService.deleteStudent(student.id)
      await fetchStudents() // Refresh the table
    } catch (error) {
      alert('Failed to delete the student.')
      console.error(error)
    }
  }
}
</script>
