import { getHeaders } from '../utils/api'

const API_URL = `/api/staff`

export default {
  async getAllStaff() {
    const res = await fetch(`${API_URL}/`, { headers: getHeaders() })
    if (!res.ok) throw new Error('Failed to fetch staff')
    return await res.json()
  },
  async createStaff(staffData) {
    const res = await fetch(`${API_URL}/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(staffData),
    })
    if (!res.ok) throw new Error('Failed to create staff')
    return await res.json()
  },
  async updateStaff(id, staffData) {
    const res = await fetch(`${API_URL}/${id}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(staffData),
    })
    if (!res.ok) throw new Error('Failed to update staff')
    return await res.json()
  },
  async terminateStaff(id) {
    const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE', headers: getHeaders() })
    if (!res.ok) {
      const errorData = await res.json()
      throw new Error(errorData.detail || 'Failed to terminate staff')
    }
    return await res.json()
  },
}
