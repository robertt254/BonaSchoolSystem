<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="font-heading text-2xl font-bold text-text-primary tracking-tight">
          Finance Dashboard
        </h1>
        <p class="text-sm text-text-muted mt-1">
          Manage school collections, ledgers, and payroll.
        </p>
      </div>
    </div>

    <!-- Skeleton loading state -->
    <div v-if="loading" class="space-y-8">
      <SkeletonLoader type="stats" :count="3" />
      <div class="bg-white rounded border border-border p-8">
        <div class="skel h-3 w-44 mb-6" />
        <div class="flex items-end gap-2 h-36">
          <div v-for="n in 12" :key="n" class="flex-1 skel rounded" :style="{ height: (30 + Math.random() * 70) + 'px' }" />
        </div>
      </div>
    </div>

    <div v-else class="space-y-8">
      <!-- Actions Section -->
      <div class="flex items-center gap-4">
        <button
          v-if="['accountant', 'admin', 'principal', 'secretary'].includes(authStore.user?.role)"
          @click="openFeeModal"
          class="bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded font-bold transition-all shadow-sm text-sm flex items-center gap-2"
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
          class="bg-white p-8 rounded border border-border shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] col-span-1 sm:col-span-2 relative overflow-hidden group"
        >
          <div
            class="absolute right-0 top-0 w-32 h-32 bg-blue-50 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-110"
          ></div>
          <div class="relative z-10">
            <div class="flex justify-between items-end mb-4">
              <div>
                <div class="text-xs font-bold uppercase tracking-[0.07em] text-text-muted mb-1">
                  {{ appStore.currentTerm }} Collection
                </div>
                <div class="text-4xl font-extrabold text-slate-800">
                  {{ formatCurrency(termCollected) }}
                </div>
              </div>
              <div class="text-right">
                <div class="text-sm font-bold text-school-navy">{{ collectionPercentage }}%</div>
                <div class="text-xs font-bold text-slate-400 uppercase tracking-wider">
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
          class="bg-white p-8 rounded border border-border shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] relative overflow-hidden group"
        >
          <div
            class="absolute right-0 top-0 w-24 h-24 bg-emerald-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"
          ></div>
          <div class="relative z-10 flex flex-col justify-between h-full">
            <div>
              <div class="text-xs font-bold uppercase tracking-[0.07em] text-text-muted mb-1">
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

      <!-- Monthly Collection Chart (Chart.js) -->
      <div class="bg-white rounded border border-border hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] overflow-hidden transition-shadow">
        <div class="border-b border-slate-100 px-8 py-5 flex items-center justify-between bg-slate-50">
          <div>
            <h3 class="text-lg font-bold text-slate-800 tracking-tight">Monthly Collections</h3>
            <p class="text-xs text-slate-500 mt-0.5">Fee payments received per month · {{ new Date().getFullYear() }}</p>
          </div>
          <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">KES</span>
        </div>
        <div class="px-8 py-6" style="height:220px">
          <canvas ref="chartCanvas" />
        </div>
      </div>

      <!-- Three-column ledger row -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">

        <!-- Recent Fee Payments -->
        <div class="bg-white rounded border border-border overflow-hidden flex flex-col">
          <div class="border-b border-slate-100 px-4 py-4 flex items-center justify-between bg-slate-50 shrink-0">
            <div>
              <h3 class="font-bold text-slate-800 text-sm">Fee Payments</h3>
              <p class="text-xs text-slate-400 mt-0.5">Latest {{ recentFees.length }} transactions</p>
            </div>
            <router-link to="/finance/statements" class="text-xs font-semibold text-school-purple hover:underline">
              All →
            </router-link>
          </div>
          <div class="overflow-y-auto" style="max-height: 420px">
            <div
              v-for="fee in recentFees"
              :key="fee.id"
              class="flex items-center justify-between px-4 py-3 border-b border-slate-50 last:border-b-0 hover:bg-slate-50 transition-colors"
            >
              <div class="flex items-center gap-2.5 min-w-0">
                <div class="w-7 h-7 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600 shrink-0">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>
                  </svg>
                </div>
                <div class="min-w-0">
                  <p class="text-sm font-semibold text-slate-800 truncate">{{ getStudentName(fee.student_id) }}</p>
                  <p class="text-xs text-slate-400 truncate">{{ fee.term }} · {{ fee.payment_type }}</p>
                </div>
              </div>
              <div class="flex items-center gap-1.5 shrink-0 ml-2">
                <span class="text-sm font-bold text-emerald-700">{{ formatCurrency(fee.amount) }}</span>
                <button @click="openReceiptFor(fee)" title="View / print receipt"
                  class="w-7 h-7 flex items-center justify-center rounded text-slate-400 hover:text-school-navy hover:bg-slate-100 transition-colors">
                  <span class="material-symbols-outlined" style="font-size:18px">receipt_long</span>
                </button>
              </div>
            </div>
            <div v-if="!recentFees.length" class="px-4 py-8 text-center text-slate-400 text-sm">No payments yet.</div>
          </div>
        </div>

        <!-- Petty Cash -->
        <div class="bg-white rounded border border-border overflow-hidden flex flex-col">
          <div class="border-b border-slate-100 px-4 py-4 flex items-center justify-between bg-slate-50 shrink-0">
            <div>
              <h3 class="font-bold text-slate-800 text-sm">Petty Cash</h3>
              <p class="text-xs text-slate-400 mt-0.5">Imprest balance</p>
            </div>
            <router-link to="/finance/petty-cash"
              class="text-xs font-bold bg-school-navy text-white px-3 py-1.5 rounded hover:bg-school-navy/90 transition-all">
              Manage →
            </router-link>
          </div>
          <!-- Balance -->
          <div class="px-4 py-3 border-b border-slate-50 bg-slate-50/50">
            <div class="flex justify-between items-center">
              <span class="text-xs font-bold uppercase tracking-wide text-slate-400">Current Balance</span>
              <span class="text-base font-extrabold" :class="pettyCashBalance >= 0 ? 'text-emerald-600' : 'text-red-600'">
                KES {{ formatCurrencyShort(pettyCashBalance) }}
              </span>
            </div>
          </div>
          <div class="overflow-y-auto" style="max-height: 360px">
            <div
              v-for="tx in recentPettyCash"
              :key="tx.id"
              class="flex items-center justify-between px-4 py-3 border-b border-slate-50 last:border-b-0 hover:bg-slate-50 transition-colors"
            >
              <div class="flex items-center gap-2.5 min-w-0">
                <div class="w-7 h-7 rounded-full flex items-center justify-center shrink-0"
                  :class="tx.transaction_type === 'IN' ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-500'">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path v-if="tx.transaction_type === 'IN'" stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
                    <path v-else stroke-linecap="round" stroke-linejoin="round" d="M20 12H4"/>
                  </svg>
                </div>
                <div class="min-w-0">
                  <p class="text-sm font-semibold text-slate-800 truncate">{{ tx.description }}</p>
                  <p class="text-xs text-slate-400 truncate">{{ tx.category || 'General' }}</p>
                </div>
              </div>
              <span class="text-sm font-bold shrink-0 ml-2"
                :class="tx.transaction_type === 'IN' ? 'text-emerald-700' : 'text-red-500'">
                {{ tx.transaction_type === 'IN' ? '+' : '-' }}{{ formatCurrencyShort(tx.amount) }}
              </span>
            </div>
            <div v-if="!recentPettyCash.length" class="px-4 py-8 text-center text-slate-400 text-sm">No petty cash transactions yet.</div>
          </div>
        </div>

        <!-- Expenses Ledger -->
        <div class="bg-white rounded border border-border overflow-hidden flex flex-col">
          <div class="border-b border-slate-100 px-4 py-4 flex items-center justify-between bg-slate-50 shrink-0">
            <div>
              <h3 class="font-bold text-slate-800 text-sm">Expenses Ledger</h3>
              <p class="text-xs text-slate-400 mt-0.5">Operational costs</p>
            </div>
            <button
              v-if="['principal', 'admin'].includes(authStore.user?.role)"
              @click="openExpenseModal"
              class="text-xs font-bold bg-school-red text-white px-3 py-1.5 rounded hover:bg-school-red/90 transition-all flex items-center gap-1"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
              Add
            </button>
          </div>
          <div class="overflow-y-auto" style="max-height: 420px">
            <div
              v-for="expense in expenses"
              :key="expense.id"
              class="flex items-center justify-between px-4 py-3 border-b border-slate-50 last:border-b-0 hover:bg-slate-50 transition-colors"
            >
              <div class="flex items-center gap-2.5 min-w-0">
                <div class="w-7 h-7 rounded-full bg-red-50 flex items-center justify-center text-school-red shrink-0">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 14l-4-4 4-4m6 8l4-4-4-4"/>
                  </svg>
                </div>
                <div class="min-w-0">
                  <p class="text-sm font-semibold text-slate-800 truncate">{{ expense.category || 'General' }}</p>
                  <p class="text-xs text-slate-400 truncate">{{ new Date(expense.expense_date).toLocaleDateString('en-KE', { day: 'numeric', month: 'short', year: 'numeric' }) }} · {{ expense.recorded_by }}</p>
                </div>
              </div>
              <span class="text-sm font-bold text-school-red shrink-0 ml-2">{{ formatCurrency(expense.amount) }}</span>
            </div>
            <div v-if="!expenses.length" class="px-4 py-8 text-center text-slate-400 text-sm">No expenses recorded yet.</div>
          </div>
          <!-- Expenses total footer -->
          <div v-if="expenses.length" class="shrink-0 border-t border-slate-100 px-4 py-2.5 bg-slate-50 flex justify-between items-center">
            <span class="text-xs font-bold uppercase tracking-wide text-slate-400">Total Expenses</span>
            <span class="text-sm font-extrabold text-school-red">{{ formatCurrency(totalExpenses) }}</span>
          </div>
        </div>

      </div>
    </div>

    <!-- Fee Payment Modal -->
    <div
      v-if="showFeeModal"
      class="fixed inset-0 bg-slate-900/40 flex items-center justify-center p-4 z-50 animate-fade-in"
    >
      <div
        class="bg-white rounded shadow-2xl w-full max-w-md overflow-hidden border border-border"
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
            <label class="block text-xs font-bold uppercase tracking-[0.07em] text-text-muted mb-1.5">
              Select Student
            </label>
            <select
              v-model="feeForm.student_id"
              required
              @change="onFeeStudentChange"
              class="w-full border border-border rounded px-3 py-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all cursor-pointer"
            >
              <option disabled value="">-- Choose a student --</option>
              <option v-for="student in students" :key="student.id" :value="student.id">
                {{ student.first_name }} {{ student.last_name }} ({{ student.admission_number }})
              </option>
            </select>
          </div>

          <!-- Current term indicator -->
          <div class="flex items-center gap-2 text-xs text-text-muted bg-slate-50 border border-border rounded px-3 py-2.5">
            <span class="material-symbols-outlined" style="font-size:16px">event</span>
            <span>School is in <strong class="text-slate-700">{{ appStore.currentTerm }}</strong>. Payment auto-clears the oldest unpaid term first, then the current term.</span>
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-[0.07em] text-text-muted mb-1.5">
              Payment Type
            </label>
            <select
              v-model="feeForm.payment_type"
              class="w-full border border-border rounded px-3 py-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all cursor-pointer"
            >
              <option value="Tuition">Tuition</option>
              <option value="Transport">Transport</option>
              <option value="Uniforms">Uniforms</option>
              <option value="Exam Fees">Exam Fees</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-bold text-school-red uppercase tracking-widest mb-1.5">
              Amount (Ksh)
            </label>
            <input
              v-model.number="feeForm.amount"
              @input="loadAllocation"
              type="number"
              min="1"
              required
              class="w-full border border-red-200 rounded px-3 py-2.5 focus:ring-2 focus:ring-school-red/20 focus:border-school-red outline-none bg-red-50/50 font-bold text-school-red transition-all"
            />
          </div>

          <!-- Live allocation preview -->
          <div v-if="allocLoading" class="text-xs text-text-muted animate-pulse">Calculating allocation…</div>
          <div v-else-if="allocPreview && allocPreview.allocation.length"
            class="bg-slate-50 border border-border rounded p-4 space-y-2">
            <p class="text-xs font-bold uppercase tracking-widest text-slate-400">How this payment will be applied</p>
            <div v-for="(a, idx) in allocPreview.allocation" :key="idx" class="flex items-center justify-between text-sm">
              <span class="flex items-center gap-2">
                <span class="text-[10px] font-bold uppercase px-1.5 py-0.5 rounded-sm border" :class="allocBadge(a.kind)">
                  {{ allocLabel(a.kind) }}
                </span>
                <span class="text-slate-700 font-medium">{{ a.term }}</span>
              </span>
              <span class="font-bold text-slate-800">{{ formatCurrency(a.amount) }}</span>
            </div>
            <div class="flex items-center justify-between text-sm pt-1.5 border-t border-slate-200">
              <span class="font-bold text-slate-700">Total</span>
              <span class="font-black text-slate-800">{{ formatCurrency(allocPreview.amount) }}</span>
            </div>
          </div>

          <div class="flex justify-end space-x-3 pt-4 mt-2">
            <button
              type="button"
              @click="closeFeeModal"
              class="px-5 py-2.5 text-slate-600 hover:bg-slate-100 rounded font-bold transition-colors text-sm"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-5 py-2.5 bg-school-navy text-white rounded font-bold hover:bg-school-navy/90 hover:shadow-md transition-all text-sm"
            >
              Record Payment
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Payment Receipt Modal -->
    <div v-if="showReceiptModal && receiptData" class="fixed inset-0 bg-slate-900/40 flex items-center justify-center p-4 z-50 animate-fade-in print:bg-white print:p-0">
      <div id="receipt-print" class="bg-white rounded shadow-2xl w-full max-w-md overflow-hidden border border-border print:shadow-none print:border-none print:max-w-full">
        <div class="bg-school-navy text-white px-6 py-5 flex justify-between items-center">
          <div>
            <h2 class="text-lg font-black tracking-tight">Payment Receipt</h2>
            <p class="text-xs opacity-80 font-mono">{{ receiptData.receipt_number }}</p>
          </div>
          <span class="material-symbols-outlined">receipt_long</span>
        </div>
        <div class="p-6 space-y-3">
          <div class="flex justify-between text-sm">
            <span class="text-text-muted">Student</span>
            <span class="font-semibold text-slate-800">{{ receiptData.student_name }} <span class="text-text-muted">({{ receiptData.admission_number }})</span></span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-text-muted">Date</span>
            <span class="font-medium text-slate-700">{{ new Date(receiptData.payment_date).toLocaleString('en-KE') }}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-text-muted">Payment Type</span>
            <span class="font-medium text-slate-700">{{ receiptData.payment_type }}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-text-muted">Received By</span>
            <span class="font-medium text-slate-700">{{ receiptData.recorded_by }}</span>
          </div>
          <div class="border-t border-slate-100 pt-3">
            <p class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-2">Applied To</p>
            <div v-for="(a, idx) in (receiptData.allocation || [])" :key="idx" class="flex justify-between items-center text-sm py-1">
              <span class="flex items-center gap-2">
                <span class="text-[10px] font-bold uppercase px-1.5 py-0.5 rounded-sm border" :class="allocBadge(a.kind)">
                  {{ allocLabel(a.kind) }}
                </span>
                <span class="text-slate-700 font-medium">{{ a.term }}</span>
              </span>
              <span class="font-bold text-slate-800">{{ formatCurrency(a.amount) }}</span>
            </div>
            <p v-if="!receiptData.allocation || !receiptData.allocation.length" class="text-sm text-text-muted">{{ receiptData.term }} — {{ formatCurrency(receiptData.amount) }}</p>
          </div>
          <div class="flex justify-between items-center border-t border-slate-200 pt-3">
            <span class="font-bold text-slate-800">Total Paid</span>
            <span class="text-xl font-black text-emerald-600">{{ formatCurrency(receiptData.amount) }}</span>
          </div>
        </div>
        <div class="border-t border-slate-100 px-6 py-4 flex justify-end gap-3 print:hidden">
          <button @click="showReceiptModal = false" class="px-5 py-2.5 text-slate-600 hover:bg-slate-100 rounded font-bold transition-colors text-sm">Close</button>
          <button @click="printReceipt" class="px-5 py-2.5 bg-school-navy text-white rounded font-bold hover:bg-school-navy/90 transition-all text-sm">Print</button>
        </div>
      </div>
    </div>

    <!-- Expense Modal -->
    <div
      v-if="showExpenseModal"
      class="fixed inset-0 bg-slate-900/40 flex items-center justify-center p-4 z-50 animate-fade-in"
    >
      <div
        class="bg-white rounded shadow-2xl w-full max-w-md overflow-hidden border border-border"
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
            <label class="block text-xs font-bold uppercase tracking-[0.07em] text-text-muted mb-1.5">
              Category
            </label>
            <input
              v-model="expenseForm.category"
              type="text"
              placeholder="e.g. Maintenance, Utilities, Supplies"
              class="w-full border border-border rounded px-3 py-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all"
            />
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-[0.07em] text-text-muted mb-1.5">
              Justification (Required)
            </label>
            <textarea
              v-model="expenseForm.justification"
              required
              rows="3"
              placeholder="Explain why this expense is necessary..."
              class="w-full border border-border rounded px-3 py-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-medium text-slate-700 transition-all resize-none"
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
              class="w-full border border-red-200 rounded px-3 py-2.5 focus:ring-2 focus:ring-school-red/20 focus:border-school-red outline-none bg-red-50/50 font-bold text-school-red transition-all"
            />
          </div>

          <div class="flex justify-end space-x-3 pt-4 mt-2">
            <button
              type="button"
              @click="closeExpenseModal"
              class="px-5 py-2.5 text-slate-600 hover:bg-slate-100 rounded font-bold transition-colors text-sm"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-5 py-2.5 bg-school-navy text-white rounded font-bold hover:bg-school-navy/90 hover:shadow-md transition-all text-sm"
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
import { ref, reactive, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import { Chart, BarElement, BarController, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js'
import { apiFetch } from '@/services/api'
import feeService from '@/services/feeService'
import studentService from '@/services/studentService'
import staffService from '@/services/staffService'
import financeService from '@/services/financeService'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import SkeletonLoader from '@/components/ui/SkeletonLoader.vue'

Chart.register(BarElement, BarController, CategoryScale, LinearScale, Tooltip, Legend)

const toast = useToast()

const appStore = useAppStore()
const authStore = useAuthStore()

const fees = ref([])
const students = ref([])
const activeStaff = ref([])
const pettyCash = ref([])
const expenses = ref([])
const loading = ref(true)
const termSummary = ref({ total_expected: 0, total_collected: 0, percentage: 0 })
const monthlyCollection = ref([])

const showExpenseModal = ref(false)
const showFeeModal = ref(false)
const chartCanvas = ref(null)
let chartInstance = null

const feeForm = reactive({
  student_id: '',
  amount: 0,
  payment_type: 'Tuition',
  term: appStore.currentTerm,
})

const expenseForm = reactive({
  amount: 0,
  justification: '',
  category: '',
})

const loadData = async () => {
  loading.value = true
  try {
    const [fetchedFees, fetchedStudents, fetchedStaff, fetchedPettyCash, fetchedExpenses, fetchedSummary, fetchedMonthly] = await Promise.all([
      feeService.getAllFees().catch(() => []),
      studentService.getAllStudents().catch(() => []),
      staffService.getAllStaff().catch(() => []),
      financeService.getPettyCash().catch(() => []),
      financeService.getExpenses().catch(() => []),
      feeService.getTermSummary(appStore.currentTerm).catch(() => ({ total_expected: 0, total_collected: 0, percentage: 0 })),
      feeService.getMonthlyCollection().catch(() => []),
    ])
    fees.value = fetchedFees
    students.value = fetchedStudents
    activeStaff.value = fetchedStaff
    pettyCash.value = fetchedPettyCash
    expenses.value = fetchedExpenses.sort((a, b) => b.id - a.id)
    termSummary.value = fetchedSummary
    monthlyCollection.value = fetchedMonthly
  } catch (error) {
    console.error('Error loading finance data:', error)
  } finally {
    loading.value = false
  }
}

function buildChart() {
  if (!chartCanvas.value || !monthlyCollection.value.length) return
  const labels = monthlyCollection.value.map(m => m.month)
  const data   = monthlyCollection.value.map(m => m.total)
  if (chartInstance) { chartInstance.destroy(); chartInstance = null }
  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Collections (KES)',
        data,
        backgroundColor: 'rgba(10,15,30,0.70)',
        hoverBackgroundColor: 'rgba(10,15,30,0.90)',
        borderRadius: 6,
        borderSkipped: false,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => ' KES ' + ctx.parsed.y.toLocaleString('en-KE'),
          },
        },
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#94A3B8', font: { size: 11, weight: '600' } } },
        y: {
          grid: { color: '#F1F5F9' },
          ticks: {
            color: '#94A3B8',
            font: { size: 10 },
            callback: v => v >= 1000 ? (v / 1000).toFixed(0) + 'K' : v,
          },
        },
      },
    },
  })
}

watch(monthlyCollection, async () => {
  await nextTick()
  buildChart()
})

let refreshTimer = null
onMounted(() => {
  loadData()
  refreshTimer = setInterval(loadData, 60_000)
})
onUnmounted(() => {
  clearInterval(refreshTimer)
  if (chartInstance) chartInstance.destroy()
})

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

const pettyCashBalance = computed(() =>
  pettyCash.value.length ? (pettyCash.value[0]?.running_balance ?? 0) : 0
)

const recentPettyCash = computed(() =>
  pettyCash.value.slice(0, 8)
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
const allocPreview  = ref(null)
const allocLoading  = ref(false)
let   allocTimer    = null

const showReceiptModal = ref(false)
const receiptData      = ref(null)

const openFeeModal = () => {
  feeForm.student_id = ''
  feeForm.amount = 0
  feeForm.payment_type = 'Tuition'
  feeForm.term = appStore.currentTerm
  allocPreview.value = null
  showFeeModal.value = true
}

const closeFeeModal = () => {
  showFeeModal.value = false
  allocPreview.value = null
}

// Debounced waterfall-allocation preview (oldest arrears first, then current term).
const loadAllocation = () => {
  clearTimeout(allocTimer)
  if (!feeForm.student_id || !feeForm.amount || feeForm.amount <= 0) {
    allocPreview.value = null
    return
  }
  allocLoading.value = true
  allocTimer = setTimeout(async () => {
    try {
      allocPreview.value = await feeService.previewAllocation(
        feeForm.student_id, feeForm.amount, appStore.currentTerm,
      )
    } catch {
      allocPreview.value = null
    } finally {
      allocLoading.value = false
    }
  }, 300)
}

const onFeeStudentChange = () => {
  feeForm.term = appStore.currentTerm
  loadAllocation()
}

const submitFee = async () => {
  try {
    const res = await feeService.recordFee({ ...feeForm, current_term: appStore.currentTerm })
    const student = students.value.find(s => s.id === feeForm.student_id)
    receiptData.value = {
      ...res,
      student_name: student ? `${student.first_name} ${student.last_name}` : '',
      admission_number: student?.admission_number || '',
    }
    closeFeeModal()
    showReceiptModal.value = true
    toast.success('Fee payment recorded successfully.')
    await loadData()
  } catch (error) {
    toast.error(error.message || 'Failed to record fee.')
  }
}

const printReceipt = () => window.print()

// Re-open a printable receipt for an already-recorded payment.
const openReceiptFor = (fee) => {
  const student = students.value.find(s => s.id === fee.student_id)
  receiptData.value = {
    ...fee,
    student_name: student ? `${student.first_name} ${student.last_name}` : getStudentName(fee.student_id),
    admission_number: student?.admission_number || '',
  }
  showReceiptModal.value = true
}

const allocLabel = (k) => (k === 'arrears' ? 'Arrears' : k === 'advance' ? 'Advance' : 'Current')
const allocBadge = (k) =>
  k === 'arrears'
    ? 'bg-amber-50 text-amber-700 border-amber-200'
    : k === 'advance'
      ? 'bg-blue-50 text-blue-700 border-blue-200'
      : 'bg-emerald-50 text-emerald-700 border-emerald-200'

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
    toast.success('Expense recorded.')
    await loadData()
  } catch (error) {
    toast.error(error.message || 'Failed to record expense.')
  }
}

// --- HELPER FUNCTIONS ---
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    maximumFractionDigits: 0,
  }).format(amount)
}
</script>

