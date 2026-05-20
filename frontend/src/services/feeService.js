import { apiFetch } from './api'

export default {
  getAllFees: () => apiFetch('/api/fees/'),
  recordFee: (data) => apiFetch('/api/fees/', { method: 'POST', body: JSON.stringify(data) }),
  getStudentBalance: (studentId, term) =>
    apiFetch(`/api/fees/balance/${studentId}/${encodeURIComponent(term)}`),
}
