import { getHeaders } from '../utils/api'

const API_URL = 'http://127.0.0.1:8000/api/fees'

export default {
  // Fetch the full ledger
  async getAllFees() {
    const response = await fetch(`${API_URL}/`, {
      method: 'GET',
      headers: getHeaders(),
    })
    if (!response.ok) throw new Error('Failed to fetch fees')
    return await response.json()
  },

  // Log a new payment
  async recordFee(feeData) {
    const response = await fetch(`${API_URL}/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(feeData),
    })
    if (!response.ok) throw new Error('Failed to record fee')
    return await response.json()
  },

  // Fetch the calculated balance for a specific student and term
  async getStudentBalance(studentId, term) {
    const response = await fetch(`${API_URL}/balance/${studentId}/${term}`, {
      method: 'GET',
      headers: getHeaders(),
    })
    if (!response.ok) throw new Error('Failed to fetch balance')
    return await response.json()
  },
}
