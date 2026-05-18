import { useAuthStore } from '@/stores/auth'

const API_URL = `${import.meta.env.VITE_API_BASE_URL}/fees`

const getHeaders = () => {
  const authStore = useAuthStore()
  const token = authStore.token || localStorage.getItem('access_token')
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  }
}

export default {
  // Fetch the full ledger
  async getAllFees() {
    const response = await fetch(`${API_URL}/`, {
      method: 'GET',
      headers: getHeaders()
    })
    if (!response.ok) throw new Error('Failed to fetch fees')
    return await response.json()
  },

  // Log a new payment
  async recordFee(feeData) {
    const response = await fetch(`${API_URL}/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(feeData)
    })
    if (!response.ok) throw new Error('Failed to record fee')
    return await response.json()
  },

  // Fetch the calculated balance for a specific student and term
  async getStudentBalance(studentId, term) {
    const response = await fetch(`${API_URL}/balance/${studentId}/${term}`, {
      method: 'GET',
      headers: getHeaders()
    })
    if (!response.ok) throw new Error('Failed to fetch balance')
    return await response.json()
  }
}
