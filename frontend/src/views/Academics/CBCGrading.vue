<template>
  <div class="p-8 bg-gray-50 min-h-screen">
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-gray-800">CBC Grading</h1>
      <p class="text-gray-600 mt-1">Record academic assessments.</p>
    </div>

    <div
      class="flex space-x-4 mb-8 bg-white p-6 rounded-xl shadow-sm border border-gray-100 items-end"
    >
      <div class="flex-1">
        <label class="block text-sm font-medium text-gray-700 mb-1">Select Grade</label>
        <select
          v-model="selectedGrade"
          class="w-full border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-900 outline-none"
        >
          <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
        </select>
      </div>
      <div class="flex-1">
        <label class="block text-sm font-medium text-gray-700 mb-1">Select Term</label>
        <select
          v-model="selectedTerm"
          class="w-full border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-900 outline-none"
        >
          <option value="Term 1">Term 1</option>
          <option value="Term 2">Term 2</option>
          <option value="Term 3">Term 3</option>
        </select>
      </div>
      <div class="flex-1">
        <label class="block text-sm font-medium text-gray-700 mb-1">Learning Area</label>
        <select
          v-model="selectedLearningArea"
          class="w-full border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-900 outline-none"
        >
          <option value="Mathematics Activities">Mathematics Activities</option>
          <option value="Language Activities">Language Activities</option>
          <option value="Environmental Activities">Environmental Activities</option>
          <option value="Religious Education">Religious Education</option>
        </select>
      </div>

      <button
        @click="loadClassList"
        class="bg-blue-900 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-800 transition shadow"
      >
        Load Students
      </button>
    </div>

    <div
      v-if="classList.length > 0"
      class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden"
    >
      <div class="bg-blue-50 p-4 border-b border-blue-100 flex justify-between items-center">
        <h2 class="font-bold text-blue-900">{{ selectedGrade }} Roster</h2>
        <span class="text-sm font-medium text-blue-700 bg-blue-200 px-3 py-1 rounded-full"
          >{{ classList.length }} Students</span
        >
      </div>

      <table class="w-full text-left">
        <thead class="bg-gray-100 text-gray-600 text-sm uppercase tracking-wider">
          <tr>
            <th class="p-4 font-semibold w-1/3">Student Name</th>
            <th class="p-4 font-semibold w-1/4">Score</th>
            <th class="p-4 font-semibold">Remarks (Optional)</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="s in classList"
            :key="s.student_id"
            class="border-b border-gray-50 hover:bg-gray-50 transition"
          >
            <td class="p-4 font-medium text-gray-800">{{ s.name }}</td>
            <td class="p-4">
              <select
                v-model="s.score"
                class="w-full border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-900 outline-none"
              >
                <option value="EE">EE - Exceeding Expectations</option>
                <option value="ME">ME - Meeting Expectations</option>
                <option value="AE">AE - Approaching Expectations</option>
                <option value="BE">BE - Below Expectations</option>
              </select>
            </td>
            <td class="p-4">
              <input
                v-model="s.remarks"
                placeholder="Teacher's remark..."
                class="border border-gray-300 p-2 rounded-lg w-full text-sm focus:ring-2 focus:ring-blue-900 outline-none"
              />
            </td>
          </tr>
        </tbody>
      </table>

      <div class="p-6 bg-gray-50 text-right border-t border-gray-100">
        <button
          @click="saveGrades"
          class="bg-green-700 text-white px-8 py-3 rounded-lg font-bold shadow-lg hover:bg-green-600 transition flex items-center justify-center ml-auto"
        >
          Submit Grades
        </button>
      </div>
    </div>

    <div
      v-else-if="hasSearched"
      class="text-center py-12 text-gray-500 bg-white rounded-xl border border-gray-200 mt-8"
    >
      <p class="text-lg">No students found in {{ selectedGrade }}.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import academicService from '@/services/academicService'

const selectedGrade = ref('Grade 1')
const selectedTerm = ref('Term 1')
const selectedLearningArea = ref('Mathematics Activities')
const classList = ref([])
const hasSearched = ref(false)
const grades = [
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

const loadClassList = async () => {
  hasSearched.value = true
  const token = localStorage.getItem('access_token')
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_BASE_URL}/api/attendance/today/${selectedGrade.value}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    )
    if (!response.ok) throw new Error('Failed to fetch class list')
    const students = await response.json()
    classList.value = students.map((s) => ({
      student_id: s.student_id,
      name: s.name,
      term: selectedTerm.value,
      learning_area: selectedLearningArea.value,
      score: 'ME',
      remarks: '',
    }))
  } catch (error) {
    alert('Error loading class. Make sure backend is running.')
    console.error(error)
  }
}

const saveGrades = async () => {
  try {
    const records = classList.value.map((s) => ({
      student_id: s.student_id,
      term: selectedTerm.value,
      learning_area: selectedLearningArea.value,
      score: s.score,
      remarks: s.remarks,
    }))
    await academicService.saveScores(records)
    alert('✅ Grades submitted successfully!')
  } catch (error) {
    alert('Error saving grades')
    console.error(error)
  }
}
</script>
