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

  async recordExpense(expenseData) {
    const res = await fetch(`${API_URL}/expenses`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(expenseData),
    })
    if (!res.ok) throw new Error('Failed to record expense')
    return await res.json()
  },

  async getExpenses() {
    const res = await fetch(`${API_URL}/expenses`, {
      method: 'GET',
      headers: getHeaders(),
    })
    if (!res.ok) throw new Error('Failed to fetch expenses')
    return await res.json()
  },
}
