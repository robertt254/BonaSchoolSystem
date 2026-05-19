import { getHeaders } from '../utils/api'

const API_URL = `/api/students`

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

  async getStudentProfile(studentId) {
    const response = await fetch(`${API_URL}/${studentId}/profile`, {
      method: 'GET',
      headers: getHeaders(),
    })
    if (!response.ok) throw new Error('Failed to fetch student profile')
    return await response.json()
  },
}
