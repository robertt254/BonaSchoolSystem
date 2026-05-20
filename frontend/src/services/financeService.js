import { apiFetch } from '@/services/api'

export default {
  executePayroll: (data) =>
    apiFetch('/api/finance/payroll', { method: 'POST', body: JSON.stringify(data) }),

  getPayrollLedger: () => apiFetch('/api/finance/payroll'),

  recordExpense: (data) =>
    apiFetch('/api/finance/expenses', { method: 'POST', body: JSON.stringify(data) }),

  getExpenses: () => apiFetch('/api/finance/expenses'),
}
