import { getHeaders } from '../utils/api'

const API_URL = `/api/finance`

export default {
  async executePayroll(payrollData) {
    const res = await fetch(`${API_URL}/payroll`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(payrollData),
    })
    if (!res.ok) throw new Error('Failed to execute payroll')
    return await res.json()
  },

  async getPayrollLedger() {
    const res = await fetch(`${API_URL}/payroll`, {
      method: 'GET',
      headers: getHeaders(),
    })
    if (!res.ok) throw new Error('Failed to fetch payroll ledger')
    return await res.json()
  },
}
