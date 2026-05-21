import { apiFetch } from './api'

export default {
  getAllStudents: (params = {}) => {
    const qs = new URLSearchParams()
    if (params.search) qs.set('search', params.search)
    if (params.grade)  qs.set('grade', params.grade)
    if (params.skip  != null) qs.set('skip',  String(params.skip))
    if (params.limit != null) qs.set('limit', String(params.limit))
    const q = qs.toString()
    return apiFetch(`/api/students/${q ? '?' + q : ''}`)
  },

  getStudent: (id) => apiFetch(`/api/students/${id}`),

  getStudentProfile: (id) => apiFetch(`/api/students/${id}/profile`),

  createStudent: (data) =>
    apiFetch('/api/students/', { method: 'POST', body: JSON.stringify(data) }),

  updateStudent: (id, data) =>
    apiFetch(`/api/students/${id}`, { method: 'PUT', body: JSON.stringify(data) }),

  deleteStudent: (id) =>
    apiFetch(`/api/students/${id}`, { method: 'DELETE' }),
}
