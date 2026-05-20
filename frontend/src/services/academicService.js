import { apiFetch } from './api'

export default {
  getReportCard: (studentId, term) =>
    apiFetch(`/api/academics/report-card/${studentId}/${encodeURIComponent(term)}`),
  saveScores: (scoresArray) =>
    apiFetch('/api/academics/scores', { method: 'POST', body: JSON.stringify(scoresArray) }),
}
