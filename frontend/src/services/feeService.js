import { apiFetch } from './api'

export default {
  getAllFees: () => apiFetch('/api/fees/'),
  recordFee: (data) => apiFetch('/api/fees/', { method: 'POST', body: JSON.stringify(data) }),
  getStudentBalance: (studentId, term) =>
    apiFetch(`/api/fees/balance/${studentId}/${encodeURIComponent(term)}`),
  getTermSummary: (term) =>
    apiFetch(`/api/fees/term-summary?term=${encodeURIComponent(term)}`),
  getMonthlyCollection: (year) =>
    apiFetch(`/api/fees/monthly-collection${year ? `?year=${year}` : ''}`),
  getDefaulters: (term) =>
    apiFetch(`/api/fees/defaulters?term=${encodeURIComponent(term)}`),
}
