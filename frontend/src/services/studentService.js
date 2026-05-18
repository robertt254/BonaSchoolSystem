import { useAuthStore } from '@/stores/auth'

const API_URL = `${import.meta.env.VITE_API_BASE_URL}/students`

// Helper function to get the token securely
const getHeaders = () => {
  const authStore = useAuthStore()
  // Grab the token from Pinia (or localStorage as a fallback)
  const token = authStore.token || localStorage.getItem('access_token')

  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`, // This is our VIP pass for the FastAPI bouncer
  }
}

export default {
  // 1. READ: Fetch all students
  async getAllStudents() {
    const response = await fetch(`${API_URL}/`, {
      method: 'GET',
      headers: getHeaders(),
    })
    if (!response.ok) throw new Error('Failed to fetch students')
    return await response.json()
  },

  // 2. CREATE: Add a new student
  async createStudent(studentData) {
    const response = await fetch(`${API_URL}/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(studentData),
    })
    if (!response.ok) throw new Error('Failed to create student')
    return await response.json()
  },

  // 3. UPDATE: Edit a student
  async updateStudent(studentId, updateData) {
    const response = await fetch(`${API_URL}/${studentId}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(updateData),
    })
    if (!response.ok) throw new Error('Failed to update student')
    return await response.json()
  },

  // 4. DELETE: Remove a student
  async deleteStudent(studentId) {
    const response = await fetch(`${API_URL}/${studentId}`, {
      method: 'DELETE',
      headers: getHeaders(),
    })
    if (!response.ok) throw new Error('Failed to delete student')
    return await response.json()
  },
}
