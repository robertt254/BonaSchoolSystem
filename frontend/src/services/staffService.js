import { apiFetch } from './api'

export default {
  getAllStaff: () => apiFetch('/api/staff/'),
  createStaff: (data) => apiFetch('/api/staff/', { method: 'POST', body: JSON.stringify(data) }),
  updateStaff: (id, data) => apiFetch(`/api/staff/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  terminateStaff: (id) => apiFetch(`/api/staff/${id}`, { method: 'DELETE' }),
}
