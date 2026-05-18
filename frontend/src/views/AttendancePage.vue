<template>
  <div class="p-8 bg-gray-50 min-h-screen">
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-gray-800">Daily Roll Call</h1>
      <p class="text-gray-600 mt-1">Record attendance for the current school day.</p>
    </div>
    
    <div class="flex space-x-4 mb-8 bg-white p-6 rounded-xl shadow-sm border border-gray-100 items-end">
      <div class="flex-1 max-w-sm">
        <label class="block text-sm font-medium text-gray-700 mb-1">Select CBC Grade</label>
        <select v-model="selectedGrade" class="w-full border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-900 outline-none">
          <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
        </select>
      </div>
      
      <button @click="loadClassList" class="bg-blue-900 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-800 transition shadow">
        Load Students
      </button>
    </div>

    <div v-if="classList.length > 0" class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="bg-blue-50 p-4 border-b border-blue-100 flex justify-between items-center">
        <h2 class="font-bold text-blue-900">{{ selectedGrade }} Roster</h2>
        <span class="text-sm font-medium text-blue-700 bg-blue-200 px-3 py-1 rounded-full">{{ classList.length }} Students</span>
      </div>

      <table class="w-full text-left">
        <thead class="bg-gray-100 text-gray-600 text-sm uppercase tracking-wider">
          <tr>
            <th class="p-4 font-semibold w-1/3">Student Name</th>
            <th class="p-4 font-semibold w-1/4">Status</th>
            <th class="p-4 font-semibold">Remarks (Optional)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in classList" :key="s.student_id" class="border-b border-gray-50 hover:bg-gray-50 transition">
            <td class="p-4 font-medium text-gray-800">{{ s.name }}</td>
            <td class="p-4">
              <label class="inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="s.is_present" class="form-checkbox h-6 w-6 text-blue-900 rounded focus:ring-blue-900 cursor-pointer">
                <span class="ml-3 font-bold" :class="s.is_present ? 'text-green-700' : 'text-red-600'">
                  {{ s.is_present ? 'Present' : 'Absent' }}
                </span>
              </label>
            </td>
            <td class="p-4">
              <input v-model="s.remarks" placeholder="E.g., Sick, Sent home for fees..." class="border border-gray-300 p-2 rounded-lg w-full text-sm focus:ring-2 focus:ring-blue-900 outline-none">
            </td>
          </tr>
        </tbody>
      </table>
      
      <div class="p-6 bg-gray-50 text-right border-t border-gray-100">
        <button @click="saveAttendance" class="bg-green-700 text-white px-8 py-3 rounded-lg font-bold shadow-lg hover:bg-green-600 transition flex items-center justify-center ml-auto">
          Submit Roll Call
        </button>
      </div>
    </div>

    <div v-else-if="hasSearched" class="text-center py-12 text-gray-500 bg-white rounded-xl border border-gray-200 mt-8">
      <p class="text-lg">No students found in {{ selectedGrade }}.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selectedGrade = ref('Grade 1')
const classList = ref([])
const hasSearched = ref(false)
const grades = ["Play Group", "PP1", "PP2", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6"]

const loadClassList = async () => {
  hasSearched.value = true
  const token = localStorage.getItem('access_token')
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/attendance/today/${selectedGrade.value}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (!response.ok) throw new Error('Failed to fetch class list')
    classList.value = await response.json()
  } catch (error) {
    alert("Error loading class. Make sure backend is running.")
    console.error(error)
  }
}

const saveAttendance = async () => {
  const token = localStorage.getItem('access_token')
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/attendance/bulk`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}` 
      },
      body: JSON.stringify(classList.value)
    })
    if (!response.ok) throw new Error('Failed to save attendance')
    alert("✅ Roll Call submitted successfully for today!")
  } catch (error) {
    alert("Error saving attendance")
    console.error(error)
  }
}
</script>
