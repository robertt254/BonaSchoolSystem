import { apiFetch } from './api'

export default {
  getAllFees: () => apiFetch('/api/fees/'),
  recordFee: (data) => apiFetch('/api/fees/', { method: 'POST', body: JSON.stringify(data) }),
  getStudentBalance: (studentId, term, academicYear) => {
    const qs = academicYear ? `?academic_year=${academicYear}` : ''
    return apiFetch(`/api/fees/balance/${studentId}/${encodeURIComponent(term)}${qs}`)
  },
  getTermSummary: (term) =>
    apiFetch(`/api/fees/term-summary?term=${encodeURIComponent(term)}`),
  getMonthlyCollection: (year) =>
    apiFetch(`/api/fees/monthly-collection${year ? `?year=${year}` : ''}`),
  getDefaulters: (term) =>
    apiFetch(`/api/fees/defaulters?term=${encodeURIComponent(term)}`),
  getCarryForwards: (studentId) =>
    apiFetch(`/api/fees/carry-forward/${studentId}`),
  addCarryForward: (data) =>
    apiFetch('/api/fees/carry-forward', { method: 'POST', body: JSON.stringify(data) }),
  deleteCarryForward: (id) =>
    apiFetch(`/api/fees/carry-forward/${id}`, { method: 'DELETE' }),
}
