import { apiFetch } from '@/services/api'

export default {
  // Expenses
  recordExpense: (data) =>
    apiFetch('/api/finance/expenses', { method: 'POST', body: JSON.stringify(data) }),
  getExpenses: () => apiFetch('/api/finance/expenses'),

  // Payroll (accountant + admin only)
  previewPayroll: (month) =>
    apiFetch(`/api/finance/payroll/preview?month=${month}`),
  runMonthPayroll: (month) =>
    apiFetch('/api/finance/payroll/run-month', { method: 'POST', body: JSON.stringify({ month }) }),
  getPayrollByMonth: (month) =>
    apiFetch(`/api/finance/payroll${month ? `?month=${month}` : ''}`),

  // Petty cash
  getPettyCash: () => apiFetch('/api/finance/petty-cash'),
}
