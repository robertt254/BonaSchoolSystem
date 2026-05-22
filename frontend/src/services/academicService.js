import { apiFetch } from './api'

export default {
  getReportCard: (studentId, term, academicYear) =>
    apiFetch(`/api/academics/report-card/${studentId}/${encodeURIComponent(term)}${academicYear ? `?academic_year=${academicYear}` : ''}`),
  saveScores: (scoresArray) =>
    apiFetch('/api/academics/scores', { method: 'POST', body: JSON.stringify(scoresArray) }),
}
