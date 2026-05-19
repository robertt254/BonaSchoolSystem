<template>
  <div class="max-w-7xl mx-auto space-y-6 animate-fade-in pb-12">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-2">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
          Academics & Grading
        </h1>
        <p class="text-sm text-slate-500 mt-1 font-medium">{{ appStore.currentTerm }} Assesments</p>
      </div>
    </div>

    <!-- Flat Class Navigation Tabs -->
    <div
      class="bg-white p-2 rounded-[12px] shadow-sm border border-[#E2E8F0] overflow-x-auto flex gap-2"
    >
      <button
        v-for="grade in cbcGrades"
        :key="grade"
        @click="selectedGrade = grade"
        :class="[
          'px-5 py-2.5 rounded-[12px] text-sm font-bold whitespace-nowrap transition-all',
          selectedGrade === grade
            ? 'bg-school-navy text-white shadow-md'
            : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900',
        ]"
      >
        {{ grade }}
      </button>
    </div>

    <!-- Grade Content Area -->
    <div class="bg-white rounded-[12px] shadow-sm border border-[#E2E8F0] overflow-hidden mt-6">
      <!-- Content Header -->
      <div
        class="p-6 border-b border-slate-100 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-50/50"
      >
        <div>
          <h3 class="text-lg font-bold text-slate-800 tracking-tight">
            {{ selectedGrade }} Students
          </h3>
          <p class="text-xs text-slate-500 mt-0.5">Showing all students enrolled in this level.</p>
        </div>

        <div class="flex items-center gap-3 w-full sm:w-auto">
          <div class="relative w-full sm:w-64">
            <svg
              class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              ></path>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search student name..."
              class="w-full pl-9 pr-4 py-2 text-sm border border-[#E2E8F0] rounded-[12px] focus:outline-none focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy bg-white transition-all"
            />
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div
        v-if="loading"
        class="flex flex-col justify-center items-center py-20 text-slate-400 space-y-4"
      >
        <div
          class="w-8 h-8 border-4 border-[#E2E8F0] border-t-school-navy rounded-full animate-spin mx-auto"
        ></div>
        <span class="text-xs font-bold tracking-widest uppercase">Loading students...</span>
      </div>

      <!-- Students Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr
              class="bg-school-grey border-b border-[#E2E8F0] text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8]"
            >
              <th class="p-4 pl-6 font-bold w-12">#</th>
              <th class="p-4 font-bold">Student Name</th>
              <th class="p-4 font-bold">Admission No.</th>
              <th class="p-4 font-bold">Status</th>
              <th class="p-4 pr-6 font-bold text-right">Actions</th>
            </tr>
          </thead>

          <tbody class="text-sm">
            <tr
              v-for="(student, index) in filteredStudents"
              :key="student.id"
              class="border-b border-slate-50 hover:bg-slate-50/80 transition-colors group"
            >
              <td class="p-4 pl-6 text-slate-400 font-medium">{{ index + 1 }}</td>
              <td class="p-4 font-bold text-slate-800">
                <div class="flex items-center gap-3">
                  <div
                    class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 font-bold text-xs border border-[#E2E8F0]"
                  >
                    {{ student.first_name.charAt(0) }}
                  </div>
                  {{ student.first_name }} {{ student.last_name }}
                </div>
              </td>
              <td class="p-4 text-slate-500 font-medium">{{ student.admission_number }}</td>
              <td class="p-4">
                <span
                  class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-full border"
                  :class="
                    student.status === 'Active'
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      : 'bg-slate-50 text-slate-600 border-slate-200'
                  "
                >
                  {{ student.status }}
                </span>
              </td>
              <td class="p-4 pr-6 text-right flex gap-2 justify-end">
                <router-link
                  :to="`/students/${student.id}/profile`"
                  class="text-xs font-bold text-slate-500 bg-slate-50 hover:bg-slate-100 hover:text-slate-800 px-3 py-1.5 rounded-lg transition-colors border border-[#E2E8F0]"
                >
                  Profile
                </router-link>
                <button
                  @click="openGradingModal(student)"
                  class="text-xs font-bold text-school-navy bg-school-navy/5 hover:bg-school-navy hover:text-white px-3 py-1.5 rounded-lg transition-colors border border-school-navy/10 hover:border-school-navy"
                >
                  Enter Grades
                </button>
              </td>
            </tr>

            <tr v-if="filteredStudents.length === 0">
              <td colspan="5" class="p-12 text-center">
                <div class="flex flex-col items-center justify-center text-slate-400">
                  <span class="text-4xl mb-3"></span>
                  <p class="font-medium text-sm">No students found in {{ selectedGrade }}.</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Quick Entry Grade Form (Mockup for now) -->
    <div
      v-if="showGradeModal"
      class="fixed inset-0 bg-slate-900/40 flex items-center justify-center p-4 z-50 animate-fade-in"
    >
      <div
        class="bg-white rounded-[12px] shadow-2xl w-full max-w-lg overflow-hidden border border-[#E2E8F0]"
      >
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <div>
            <h2 class="font-heading text-[22px] font-bold text-[#0F172A] tracking-tight">
              Record Assessments
            </h2>
            <p class="text-xs text-slate-500 mt-0.5">
              {{ selectedStudent?.first_name }} {{ selectedStudent?.last_name }} -
              {{ appStore.currentTerm }}
            </p>
          </div>
          <button
            @click="showGradeModal = false"
            class="text-slate-400 hover:text-school-red hover:bg-school-red/10 h-8 w-8 rounded-full flex items-center justify-center transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
          </button>
        </div>

        <form @submit.prevent="submitScore" class="p-6 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label
                class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
                >Learning Area</label
              >
              <select
                v-model="gradeForm.learning_area"
                required
                class="w-full border border-[#E2E8F0] rounded-[12px] p-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
              >
                <option disabled value="">Select Area</option>
                <option>Mathematics Activities</option>
                <option>Language Activities</option>
                <option>Environmental Activities</option>
              </select>
            </div>
            <div>
              <label
                class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
                >Score (CBC)</label
              >
              <select
                v-model="gradeForm.score"
                required
                class="w-full border border-[#E2E8F0] rounded-[12px] p-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-bold text-school-navy"
              >
                <option disabled value="">Select Score</option>
                <option value="EE">Exceeding (EE)</option>
                <option value="ME">Meeting (ME)</option>
                <option value="AE">Approaching (AE)</option>
                <option value="BE">Below (BE)</option>
              </select>
            </div>
          </div>

          <div>
            <label
              class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
              >Teacher's Remarks</label
            >
            <textarea
              v-model="gradeForm.remarks"
              rows="2"
              class="w-full border border-[#E2E8F0] rounded-[12px] p-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm"
              placeholder="Enter optional comments..."
            ></textarea>
          </div>

          <div class="flex justify-end pt-4">
            <button
              type="submit"
              class="px-5 py-2.5 bg-school-navy text-white rounded-[12px] font-bold hover:bg-school-navy/90 hover:shadow-md transition-all text-sm w-full"
            >
              Submit Score
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useAppStore } from '@/stores/app'
import studentService from '@/services/studentService'
import academicService from '@/services/academicService'

const appStore = useAppStore()

// Strict CBC class structure (No streams/tracks)
const cbcGrades = [
  'Play Group',
  'PP1',
  'PP2',
  'Grade 1',
  'Grade 2',
  'Grade 3',
  'Grade 4',
  'Grade 5',
  'Grade 6',
]

const selectedGrade = ref('Grade 1')
const searchQuery = ref('')
const loading = ref(true)
const students = ref([])

// Modal state
const showGradeModal = ref(false)
const selectedStudent = ref(null)

const gradeForm = reactive({
  learning_area: '',
  score: '',
  remarks: '',
})

const loadStudents = async () => {
  loading.value = true
  try {
    students.value = await studentService.getAllStudents()
  } catch (error) {
    console.error('Failed to load students for academics dash', error)
  } finally {
    loading.value = false
  }
}

onMounted(loadStudents)

const filteredStudents = computed(() => {
  let result = students.value.filter((s) => s.grade_level === selectedGrade.value)

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(
      (s) =>
        s.first_name.toLowerCase().includes(query) ||
        s.last_name.toLowerCase().includes(query) ||
        s.admission_number.toLowerCase().includes(query),
    )
  }

  return result
})

const openGradingModal = (student) => {
  selectedStudent.value = student
  gradeForm.learning_area = ''
  gradeForm.score = ''
  gradeForm.remarks = ''
  showGradeModal.value = true
}

const submitScore = async () => {
  if (!selectedStudent.value) return

  const payload = {
    student_id: selectedStudent.value.id,
    term: appStore.currentTerm,
    learning_area: gradeForm.learning_area,
    score: gradeForm.score,
    remarks: gradeForm.remarks,
  }

  try {
    await academicService.saveScores([payload])
    showGradeModal.value = false
    gradeForm.learning_area = ''
    gradeForm.score = ''
    gradeForm.remarks = ''
    alert('Scores saved successfully!')
  } catch (error) {
    alert('Failed to save scores.')
    console.error(error)
  }
}
</script>
