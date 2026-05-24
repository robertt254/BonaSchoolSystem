import { apiFetch } from '@/services/api'

export default {
  // Expenses
  recordExpense: (data) =>
    apiFetch('/api/finance/expenses', { method: 'POST', body: JSON.stringify(data) }),
  getExpenses: () => apiFetch('/api/finance/expenses'),

  // Payroll (accountant + admin only)
  getPayrollMonthly: (month) =>
    apiFetch(`/api/finance/payroll/monthly?month=${month}`),
  runMonthPayroll: (month, entries) =>
    apiFetch('/api/finance/payroll/run-month', { method: 'POST', body: JSON.stringify({ month, entries }) }),
  voidPayrollMonth: (month) =>
    apiFetch(`/api/finance/payroll/monthly?month=${month}`, { method: 'DELETE' }),

  // Petty cash
  getPettyCash: () => apiFetch('/api/finance/petty-cash'),
}
