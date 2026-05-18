import { getHeaders } from '../utils/api'

const API_URL = 'http://127.0.0.1:8000/api/academics'

export default {
  // To fetch the report card data
  async getReportCard(studentId, term) {
    const res = await fetch(`${API_URL}/report-card/${studentId}/${term}`, {
      headers: getHeaders(),
    })
    if (!res.ok) throw new Error('Failed to fetch report card')
    return await res.json()
  },

  // For the teacher's grading page
  async saveScores(scoresArray) {
    const res = await fetch(`${API_URL}/scores`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(scoresArray),
    })
    if (!res.ok) throw new Error('Failed to save scores')
    return await res.json()
  },
}
