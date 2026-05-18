import { useAuthStore } from '@/stores/auth'

const API_URL = `${import.meta.env.VITE_API_BASE_URL}/staff`

const getHeaders = () => {
  const token = useAuthStore().token || localStorage.getItem('access_token')
  return { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }
}

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
