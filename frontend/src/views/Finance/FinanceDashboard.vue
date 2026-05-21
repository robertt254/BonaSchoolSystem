<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="font-heading text-[22px] font-bold text-[#0F172A] tracking-tight">
          Finance Dashboard
        </h1>
        <p class="text-[13px] text-[#94A3B8] mt-1">
          Manage school collections, ledgers, and payroll.
        </p>
      </div>
    </div>

    <!-- Loading State -->
    <div
      v-if="loading"
      class="flex flex-col justify-center items-center py-20 text-slate-400 space-y-4"
    >
      <div
        class="w-8 h-8 border-4 border-[#E2E8F0] border-t-school-navy rounded-full animate-spin mx-auto"
      ></div>
      <span class="text-xs font-bold tracking-widest uppercase">Loading Finance Data...</span>
    </div>

    <div v-else class="space-y-8">
      <!-- Actions Section -->
      <div class="flex items-center gap-4">
        <button
          v-if="['accountant', 'admin', 'principal', 'secretary'].includes(authStore.user?.role)"
          @click="openFeeModal"
          class="bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded-[12px] font-bold transition-all shadow-sm text-sm flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          Record Fee Payment
        </button>
      </div>

      <!-- High-Level Metrics -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-8">
        <!-- Goal Progress -->
        <div
          class="bg-white p-8 rounded-[12px] border border-[#E2E8F0] shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] col-span-1 sm:col-span-2 relative overflow-hidden group"
        >
          <div
            class="absolute right-0 top-0 w-32 h-32 bg-blue-50 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-110"
          ></div>
          <div class="relative z-10">
            <div class="flex justify-between items-end mb-4">
              <div>
                <div class="text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1">
                  {{ appStore.currentTerm }} Collection
                </div>
                <div class="text-4xl font-extrabold text-slate-800">
                  {{ formatCurrency(termCollected) }}
                </div>
              </div>
              <div class="text-right">
                <div class="text-sm font-bold text-school-navy">{{ collectionPercentage }}%</div>
                <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Target: {{ formatCurrency(termGoal) }}
                </div>
              </div>
            </div>
            <!-- Progress Bar -->
            <div class="w-full bg-slate-100 rounded-full h-3 mb-2">
              <div
                class="bg-school-navy h-3 rounded-full transition-all duration-1000"
                :style="{ width: collectionPercentage + '%' }"
              ></div>
            </div>
          </div>
        </div>

        <!-- Total Revenue -->
        <div
          class="bg-white p-8 rounded-[12px] border border-[#E2E8F0] shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] relative overflow-hidden group"
        >
          <div
            class="absolute right-0 top-0 w-24 h-24 bg-emerald-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"
          ></div>
          <div class="relative z-10 flex flex-col justify-between h-full">
            <div>
              <div class="text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1">
                Total Revenue
              </div>
              <div class="text-3xl font-extrabold text-emerald-600">
                {{ formatCurrency(totalRevenue) }}
              </div>
            </div>
            <div class="mt-4 flex items-center text-xs text-slate-500 font-medium">
              Cumulative across all terms.
            </div>
          </div>
        </div>
      </div>

      <!-- Monthly Collection Chart -->
      <div class="bg-white rounded-[12px] border border-[#E2E8F0] shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] overflow-hidden">
        <div class="border-b border-slate-100 px-8 py-5 flex items-center justify-between bg-slate-50">
          <div>
            <h3 class="text-lg font-bold text-slate-800 tracking-tight">Monthly Collections</h3>
            <p class="text-xs text-slate-500 mt-0.5">Fee payments received per month · {{ new Date().getFullYear() }}</p>
          </div>
          <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">KES</span>
        </div>
        <div class="px-8 py-6">
          <div v-if="monthlyCollection.some(m => m.total > 0)" class="flex items-end gap-1.5 h-36">
            <div
              v-for="m in monthlyCollection"
              :key="m.month"
              class="flex-1 flex flex-col items-center gap-1 group"
            >
              <span class="text-[9px] font-bold text-slate-500 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                {{ m.total > 0 ? formatCurrencyShort(m.total) : '' }}
              </span>
              <div class="w-full flex flex-col justify-end rounded overflow-hidden bg-slate-100" style="height:88px">
                <div
                  class="w-full bg-school-navy/80 hover:bg-school-navy rounded transition-all duration-700"
                  :style="{ height: (m.total / maxMonthly * 88) + 'px' }"
                  :title="m.month + ': ' + formatCurrency(m.total)"
                ></div>
              </div>
              <span class="text-[9px] text-slate-400 font-semibold">{{ m.month }}</span>
            </div>
          </div>
          <div v-else class="h-36 flex items-center justify-center">
            <p class="text-sm text-slate-400">No payments recorded for {{ new Date().getFullYear() }}.</p>
          </div>
        </div>
      </div>

      <!-- Recent Fee Payments -->
      <div class="bg-white rounded-[12px] border border-[#E2E8F0] overflow-hidden">
        <div class="border-b border-slate-100 px-6 py-4 flex items-center justify-between bg-slate-50">
          <div>
            <h3 class="font-bold text-slate-800 text-sm">Recent Fee Payments</h3>
            <p class="text-xs text-slate-400 mt-0.5">Latest {{ recentFees.length }} transactions</p>
          </div>
          <router-link to="/finance/statements" class="text-xs font-semibold text-school-purple hover:text-school-purple-l transition-colors">
            View All Statements →
          </router-link>
        </div>
        <div class="divide-y divide-slate-50">
          <div
            v-for="fee in recentFees"
            :key="fee.id"
            class="flex items-center justify-between px-6 py-3 hover:bg-slate-50 transition-colors"
          >
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600 shrink-0">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>
                </svg>
              </div>
              <div>
                <p class="text-sm font-semibold text-slate-800">{{ getStudentName(fee.student_id) }}</p>
                <p class="text-xs text-slate-400">{{ fee.term }} · {{ fee.payment_type }}{{ fee.receipt_number ? ' · ' + fee.receipt_number : '' }}</p>
              </div>
            </div>
            <span class="text-sm font-bold text-emerald-700">{{ formatCurrency(fee.amount) }}</span>
          </div>
          <div v-if="!recentFees.length" class="px-6 py-8 text-center text-slate-400 text-sm">No payments recorded yet.</div>
        </div>
      </div>

      <!-- Payroll Module -->
      <div
        class="bg-white rounded-[12px] border border-[#E2E8F0] shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] overflow-hidden"
      >
        <div
          class="border-b border-slate-100 px-8 py-6 flex items-center justify-between bg-slate-50"
        >
          <div>
            <h3 class="text-lg font-bold text-slate-800 tracking-tight">Payroll Ledger</h3>
            <p class="text-xs text-slate-500 mt-0.5">Staff salaries and disbursements.</p>
          </div>
          <button
            @click="openPayrollModal"
            class="bg-school-navy hover:bg-school-navy/90 text-white px-4 py-2 rounded-[12px] font-bold transition-all shadow-sm text-sm flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4v16m8-8H4"
              ></path>
            </svg>
            Execute Payroll
          </button>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr
                class="bg-white text-slate-500 text-[11px] uppercase tracking-wider border-b border-slate-100"
              >
                <th class="py-5 px-8 font-bold">Month</th>
                <th class="py-5 px-8 font-bold">Staff Member</th>
                <th class="py-5 px-8 font-bold text-right">Basic</th>
                <th class="py-5 px-8 font-bold text-right text-emerald-600">Allowances</th>
                <th class="py-5 px-8 font-bold text-right text-school-red">Deductions</th>
                <th class="py-5 px-8 pr-6 font-bold text-right text-slate-800">Net Pay</th>
              </tr>
            </thead>
            <tbody class="text-sm">
              <tr
                v-for="pay in payrollLedger"
                :key="pay.id"
                class="border-b border-slate-50 hover:bg-slate-50/50 transition duration-150"
              >
                <td class="py-5 px-8 font-medium text-slate-500">{{ pay.payment_month }}</td>
                <td class="py-5 px-8 font-bold text-slate-800">{{ getStaffName(pay.staff_id) }}</td>
                <td class="py-5 px-8 text-right text-slate-600">
                  {{ formatCurrency(pay.basic_salary) }}
                </td>
                <td class="py-5 px-8 text-right text-emerald-600">
                  {{ formatCurrency(pay.allowances) }}
                </td>
                <td class="py-5 px-8 text-right text-school-red">{{ formatCurrency(pay.deductions) }}</td>
                <td class="py-5 px-8 pr-6 text-right font-bold text-slate-800">
                  {{ formatCurrency(pay.net_pay) }}
                </td>
              </tr>
              <tr v-if="payrollLedger.length === 0">
                <td colspan="6" class="py-6 px-8 text-center text-slate-400 text-sm font-medium">
                  No payroll records found.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Expenses Module -->
      <div
        class="bg-white rounded-[12px] border border-[#E2E8F0] shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] overflow-hidden"
      >
        <div
          class="border-b border-slate-100 px-6 py-5 flex items-center justify-between bg-slate-50"
        >
          <div>
            <h3 class="text-lg font-bold text-slate-800 tracking-tight">Expenses Ledger</h3>
            <p class="text-xs text-slate-500 mt-0.5">School operational expenses.</p>
          </div>
          <button
            v-if="['principal', 'admin'].includes(authStore.user?.role)"
            @click="openExpenseModal"
            class="bg-school-navy hover:bg-school-navy/90 text-white px-4 py-2 rounded-[12px] font-bold transition-all shadow-sm text-sm flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Add Expense
          </button>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-white text-slate-500 text-[11px] uppercase tracking-wider border-b border-slate-100">
                <th class="p-4 pl-6 font-bold">Date</th>
                <th class="p-4 font-bold">Category</th>
                <th class="p-4 font-bold">Justification</th>
                <th class="p-4 font-bold">Recorded By</th>
                <th class="p-4 pr-6 font-bold text-right text-school-red">Amount</th>
              </tr>
            </thead>
            <tbody class="text-sm">
              <tr
                v-for="expense in expenses"
                :key="expense.id"
                class="border-b border-slate-50 hover:bg-slate-50/50 transition duration-150"
              >
                <td class="p-4 pl-6 font-medium text-slate-500">{{ new Date(expense.expense_date).toLocaleDateString() }}</td>
                <td class="p-4 font-bold text-slate-800">{{ expense.category || 'N/A' }}</td>
                <td class="p-4 text-slate-600">{{ expense.justification }}</td>
                <td class="p-4 font-medium text-slate-500">{{ expense.recorded_by }}</td>
                <td class="p-4 pr-6 text-right font-bold text-school-red">
                  {{ formatCurrency(expense.amount) }}
                </td>
              </tr>
              <tr v-if="expenses.length === 0">
                <td colspan="5" class="p-8 text-center text-slate-400 text-sm font-medium">
                  No expenses recorded.
                </td>
              </tr>
              <tr v-if="expenses.length > 0" class="bg-slate-50 border-t-2 border-slate-200">
                <td class="p-4 pl-6 font-bold text-slate-700" colspan="3">Total ({{ expenses.length }} entries)</td>
                <td class="p-4 font-bold text-slate-500 text-right"></td>
                <td class="p-4 pr-6 text-right font-extrabold text-school-red">{{ formatCurrency(totalExpenses) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Payroll Modal -->
    <div
      v-if="showPayrollModal"
      class="fixed inset-0 bg-slate-900/40 flex items-center justify-center py-5 px-8 z-50 animate-fade-in"
    >
      <div
        class="bg-white rounded-[12px] shadow-2xl w-full max-w-md overflow-hidden border border-[#E2E8F0]"
      >
        <div class="p-8 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <h2 class="text-xl font-black text-slate-800 tracking-tight">Run Payroll</h2>
          <button
            @click="closePayrollModal"
            class="text-slate-400 hover:text-slate-600 hover:bg-slate-100 h-8 w-8 rounded-full flex items-center justify-center transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
          </button>
        </div>

        <form @submit.prevent="submitPayroll" class="p-8 space-y-6">
          <div>
            <label
              class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
              >Select Staff</label
            >
            <select
              v-model="payrollForm.staff_id"
              required
              class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all cursor-pointer"
            >
              <option disabled value="">-- Choose a staff member --</option>
              <option v-for="staff in activeStaff" :key="staff.id" :value="staff.id">
                {{ staff.name }} ({{ staff.job_title || staff.role }})
              </option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-8">
            <div>
              <label
                class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
                >Payment Month</label
              >
              <input
                v-model="payrollForm.payment_month"
                required
                type="month"
                class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all cursor-pointer"
              />
            </div>
            <div>
              <label
                class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
                >Basic Salary (Ksh)</label
              >
              <input
                v-model.number="payrollForm.basic_salary"
                type="number"
                min="0"
                required
                class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-bold text-slate-800 transition-all"
              />
            </div>
            <div>
              <label
                class="block text-xs font-bold text-emerald-600 uppercase tracking-widest mb-1.5"
                >Allowances (Ksh)</label
              >
              <input
                v-model.number="payrollForm.allowances"
                type="number"
                min="0"
                required
                class="w-full border border-emerald-200 rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none bg-emerald-50/50 font-bold text-emerald-700 transition-all"
              />
            </div>
            <div>
              <label
                class="block text-xs font-bold text-school-red uppercase tracking-widest mb-1.5"
                >Deductions (Ksh)</label
              >
              <input
                v-model.number="payrollForm.deductions"
                type="number"
                min="0"
                required
                class="w-full border border-red-200 rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-red/20 focus:border-school-red outline-none bg-red-50/50 font-bold text-school-red transition-all"
              />
            </div>
          </div>

          <!-- Net Pay Calculation -->
          <div
            class="py-5 px-8 bg-slate-50 rounded-[12px] border border-[#E2E8F0] flex justify-between items-center mt-2"
          >
            <span class="text-sm font-bold text-slate-500 uppercase tracking-widest"
              >Net Payable</span
            >
            <span class="text-xl font-black text-school-navy">{{
              formatCurrency(calculatedNetPay)
            }}</span>
          </div>

          <div
            v-if="payrollError"
            class="rounded-[10px] bg-red-50 border border-red-200 px-4 py-3 text-[13px] font-medium text-red-700"
          >
            {{ payrollError }}
          </div>

          <div class="flex justify-end gap-6 pt-4 mt-2">
            <button
              type="button"
              @click="closePayrollModal"
              class="px-8 py-4 text-slate-600 hover:bg-slate-100 rounded-[12px] font-bold transition-colors text-sm"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="calculatedNetPay < 0"
              class="px-8 py-4 bg-school-navy text-white rounded-[12px] font-bold hover:bg-school-navy/90 hover:shadow-md transition-all text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Disburse Funds
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Fee Payment Modal -->
    <div
      v-if="showFeeModal"
      class="fixed inset-0 bg-slate-900/40 flex items-center justify-center p-4 z-50 animate-fade-in"
    >
      <div
        class="bg-white rounded-[12px] shadow-2xl w-full max-w-md overflow-hidden border border-[#E2E8F0]"
      >
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <h2 class="text-xl font-black text-slate-800 tracking-tight">Record Fee Payment</h2>
          <button
            @click="closeFeeModal"
            class="text-slate-400 hover:text-slate-600 hover:bg-slate-100 h-8 w-8 rounded-full flex items-center justify-center transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <form @submit.prevent="submitFee" class="p-6 space-y-5">
          <div>
            <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5">
              Select Student
            </label>
            <select
              v-model="feeForm.student_id"
              required
              class="w-full border border-[#E2E8F0] rounded-[12px] p-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all cursor-pointer"
            >
              <option disabled value="">-- Choose a student --</option>
              <option v-for="student in students" :key="student.id" :value="student.id">
                {{ student.first_name }} {{ student.last_name }} ({{ student.admission_number }})
              </option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5">
                Term
              </label>
              <select
                v-model="feeForm.term"
                class="w-full border border-[#E2E8F0] rounded-[12px] p-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all cursor-pointer"
              >
                <option value="Term 1">Term 1</option>
                <option value="Term 2">Term 2</option>
                <option value="Term 3">Term 3</option>
              </select>
            </div>
            <div>
              <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5">
                Payment Type
              </label>
              <select
                v-model="feeForm.payment_type"
                class="w-full border border-[#E2E8F0] rounded-[12px] p-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all cursor-pointer"
              >
                <option value="Tuition">Tuition</option>
                <option value="Transport">Transport</option>
                <option value="Uniforms">Uniforms</option>
                <option value="Exam Fees">Exam Fees</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-school-red uppercase tracking-widest mb-1.5">
              Amount (Ksh)
            </label>
            <input
              v-model.number="feeForm.amount"
              type="number"
              min="1"
              required
              class="w-full border border-red-200 rounded-[12px] p-3 focus:ring-2 focus:ring-school-red/20 focus:border-school-red outline-none bg-red-50/50 font-bold text-school-red transition-all"
            />
          </div>

          <div class="flex justify-end space-x-3 pt-4 mt-2">
            <button
              type="button"
              @click="closeFeeModal"
              class="px-5 py-2.5 text-slate-600 hover:bg-slate-100 rounded-[12px] font-bold transition-colors text-sm"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-5 py-2.5 bg-school-navy text-white rounded-[12px] font-bold hover:bg-school-navy/90 hover:shadow-md transition-all text-sm"
            >
              Record Payment
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Expense Modal -->
    <div
      v-if="showExpenseModal"
      class="fixed inset-0 bg-slate-900/40 flex items-center justify-center p-4 z-50 animate-fade-in"
    >
      <div
        class="bg-white rounded-[12px] shadow-2xl w-full max-w-md overflow-hidden border border-[#E2E8F0]"
      >
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <h2 class="text-xl font-black text-slate-800 tracking-tight">Record Expense</h2>
          <button
            @click="closeExpenseModal"
            class="text-slate-400 hover:text-slate-600 hover:bg-slate-100 h-8 w-8 rounded-full flex items-center justify-center transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <form @submit.prevent="submitExpense" class="p-6 space-y-5">
          <div>
            <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5">
              Category
            </label>
            <input
              v-model="expenseForm.category"
              type="text"
              placeholder="e.g. Maintenance, Utilities, Supplies"
              class="w-full border border-[#E2E8F0] rounded-[12px] p-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all"
            />
          </div>

          <div>
            <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5">
              Justification (Required)
            </label>
            <textarea
              v-model="expenseForm.justification"
              required
              rows="3"
              placeholder="Explain why this expense is necessary..."
              class="w-full border border-[#E2E8F0] rounded-[12px] p-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all resize-none"
            ></textarea>
          </div>

          <div>
            <label class="block text-xs font-bold text-school-red uppercase tracking-widest mb-1.5">
              Amount (Ksh)
            </label>
            <input
              v-model.number="expenseForm.amount"
              type="number"
              min="1"
              required
              class="w-full border border-red-200 rounded-[12px] p-3 focus:ring-2 focus:ring-school-red/20 focus:border-school-red outline-none bg-red-50/50 font-bold text-school-red transition-all"
            />
          </div>

          <div class="flex justify-end space-x-3 pt-4 mt-2">
            <button
              type="button"
              @click="closeExpenseModal"
              class="px-5 py-2.5 text-slate-600 hover:bg-slate-100 rounded-[12px] font-bold transition-colors text-sm"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-5 py-2.5 bg-school-navy text-white rounded-[12px] font-bold hover:bg-school-navy/90 hover:shadow-md transition-all text-sm"
            >
              Save Expense
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import feeService from '@/services/feeService'
import studentService from '@/services/studentService'
import staffService from '@/services/staffService'
import financeService from '@/services/financeService'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'

const appStore = useAppStore()
const authStore = useAuthStore()

const fees = ref([])
const students = ref([])
const activeStaff = ref([])
const payrollLedger = ref([])
const expenses = ref([])
const loading = ref(true)
const termSummary = ref({ total_expected: 0, total_collected: 0, percentage: 0 })
const monthlyCollection = ref([])

const showPayrollModal = ref(false)
const showExpenseModal = ref(false)
const showFeeModal = ref(false)
const payrollError = ref('')

const feeForm = reactive({
  student_id: '',
  amount: 0,
  payment_type: 'Tuition',
  term: appStore.currentTerm,
})

const payrollForm = reactive({
  staff_id: '',
  payment_month: '',
  basic_salary: 0,
  allowances: 0,
  deductions: 0,
})

const expenseForm = reactive({
  amount: 0,
  justification: '',
  category: '',
})

const loadData = async () => {
  loading.value = true
  try {
    const [fetchedFees, fetchedStudents, fetchedStaff, fetchedPayroll, fetchedExpenses, fetchedSummary, fetchedMonthly] = await Promise.all([
      feeService.getAllFees().catch(() => []),
      studentService.getAllStudents().catch(() => []),
      staffService.getAllStaff().catch(() => []),
      financeService.getPayrollLedger().catch(() => []),
      financeService.getExpenses().catch(() => []),
      feeService.getTermSummary(appStore.currentTerm).catch(() => ({ total_expected: 0, total_collected: 0, percentage: 0 })),
      feeService.getMonthlyCollection().catch(() => []),
    ])
    fees.value = fetchedFees
    students.value = fetchedStudents
    activeStaff.value = fetchedStaff
    payrollLedger.value = fetchedPayroll.sort((a, b) => b.id - a.id)
    expenses.value = fetchedExpenses.sort((a, b) => b.id - a.id)
    termSummary.value = fetchedSummary
    monthlyCollection.value = fetchedMonthly
  } catch (error) {
    console.error('Error loading finance data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(loadData)

// --- COMPUTED FINANCE METRICS ---
const totalRevenue = computed(() =>
  fees.value.reduce((sum, fee) => sum + (fee.amount || 0), 0)
)

const termCollected = computed(() => termSummary.value.total_collected)
const termGoal      = computed(() => termSummary.value.total_expected)
const collectionPercentage = computed(() => Math.min(termSummary.value.percentage, 100))

const maxMonthly = computed(() =>
  Math.max(...monthlyCollection.value.map((m) => m.total), 1)
)

const totalExpenses = computed(() =>
  expenses.value.reduce((sum, e) => sum + (e.amount || 0), 0)
)

const recentFees = computed(() =>
  [...fees.value].sort((a, b) => b.id - a.id).slice(0, 10)
)

const getStudentName = (id) => {
  const s = students.value.find((st) => st.id === id)
  return s ? `${s.first_name} ${s.last_name}` : 'Unknown'
}

const formatCurrencyShort = (v) => {
  if (v >= 1_000_000) return `${(v / 1_000_000).toFixed(1)}M`
  if (v >= 1_000) return `${(v / 1_000).toFixed(0)}K`
  return String(v)
}

// --- FEE MODAL ---
const openFeeModal = () => {
  feeForm.student_id = ''
  feeForm.amount = 0
  feeForm.payment_type = 'Tuition'
  feeForm.term = appStore.currentTerm
  showFeeModal.value = true
}

const closeFeeModal = () => {
  showFeeModal.value = false
}

const submitFee = async () => {
  try {
    await feeService.recordFee(feeForm)
    closeFeeModal()
    await loadData()
  } catch (error) {
    alert(error.message || 'Failed to record fee.')
    console.error(error)
  }
}

// --- PAYROLL MODAL ---
const calculatedNetPay = computed(() => {
  return payrollForm.basic_salary + payrollForm.allowances - payrollForm.deductions
})

const openPayrollModal = () => {
  const date = new Date()
  const yyyy = date.getFullYear()
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  payrollForm.payment_month = `${yyyy}-${mm}`
  payrollForm.staff_id = ''
  payrollForm.basic_salary = 0
  payrollForm.allowances = 0
  payrollForm.deductions = 0
  payrollError.value = ''
  showPayrollModal.value = true
}

const closePayrollModal = () => {
  payrollError.value = ''
  showPayrollModal.value = false
}

const submitPayroll = async () => {
  payrollError.value = ''
  if (calculatedNetPay.value < 0) {
    payrollError.value = `Net pay cannot be negative. Deductions (${formatCurrency(payrollForm.deductions)}) exceed basic salary + allowances (${formatCurrency(payrollForm.basic_salary + payrollForm.allowances)}).`
    return
  }
  try {
    const payload = {
      ...payrollForm,
      net_pay: calculatedNetPay.value,
    }
    await financeService.executePayroll(payload)
    closePayrollModal()
    await loadData()
  } catch (error) {
    payrollError.value = error.message || 'Failed to execute payroll. Please try again.'
    console.error(error)
  }
}

// --- EXPENSE MODAL ---
const openExpenseModal = () => {
  expenseForm.amount = 0
  expenseForm.justification = ''
  expenseForm.category = ''
  showExpenseModal.value = true
}

const closeExpenseModal = () => {
  showExpenseModal.value = false
}

const submitExpense = async () => {
  try {
    await financeService.recordExpense(expenseForm)
    closeExpenseModal()
    await loadData()
  } catch (error) {
    alert(error.message || 'Failed to record expense.')
    console.error(error)
  }
}

// --- HELPER FUNCTIONS ---
const getStaffName = (id) => {
  const staff = activeStaff.value.find((s) => s.id === id)
  return staff ? staff.name : 'Unknown Staff'
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    maximumFractionDigits: 0,
  }).format(amount)
}
</script>
