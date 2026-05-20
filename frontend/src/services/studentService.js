import { apiFetch } from './api'

export default {
  getAllStudents: () => apiFetch('/api/students/'),
  createStudent: (data) => apiFetch('/api/students/', { method: 'POST', body: JSON.stringify(data) }),
  updateStudent: (id, data) => apiFetch(`/api/students/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteStudent: (id) => apiFetch(`/api/students/${id}`, { method: 'DELETE' }),
}
