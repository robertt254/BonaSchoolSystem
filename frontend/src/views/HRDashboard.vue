<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-8 mb-8">
      <div>
        <h1 class="font-heading text-[22px] font-bold text-[#0F172A] tracking-tight">
          HR & Staff Management
        </h1>
        <p class="text-[13px] text-[#94A3B8] mt-1">
          Manage school personnel, compliance, and employment records.
        </p>
      </div>
      <button
        @click="openModal()"
        class="bg-school-navy hover:bg-school-navy/90 text-white px-8 py-4 rounded-[12px] font-bold transition-all shadow-sm hover:shadow flex items-center gap-6 text-sm"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 4v16m8-8H4"
          ></path>
        </svg>
        Hire New Staff
      </button>
    </div>

    <!-- Error Banner -->
    <div
      v-if="loadError"
      class="flex items-center gap-3 bg-red-50 border border-red-200 text-red-700 rounded-xl px-5 py-4 text-sm font-medium"
    >
      <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
      </svg>
      {{ loadError }}
      <button @click="loadStaff" class="ml-auto text-xs font-bold underline hover:no-underline">Retry</button>
    </div>

    <!-- Search bar -->
    <div class="bg-white rounded-[12px] border border-[#E2E8F0] p-4 flex flex-wrap gap-3 items-end">
      <div class="flex-1 min-w-56">
        <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Search Staff</label>
        <div class="relative">
          <svg class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Name, username, role, or job title…"
            class="w-full border border-slate-300 rounded-lg pl-9 pr-4 py-2.5 text-sm focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none"
          />
        </div>
      </div>
      <div>
        <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">Filter by Role</label>
        <select
          v-model="roleFilter"
          class="border border-slate-300 px-3 py-2.5 rounded-lg text-sm focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-white"
        >
          <option value="">All Roles</option>
          <option value="admin">Admin</option>
          <option value="principal">Principal</option>
          <option value="teacher">Teacher</option>
          <option value="accountant">Accountant</option>
          <option value="secretary">Secretary</option>
        </select>
      </div>
      <div class="text-sm text-slate-400 self-end pb-1">{{ filteredStaff.length }} member{{ filteredStaff.length !== 1 ? 's' : '' }}</div>
    </div>

    <!-- Loading State -->
    <div
      v-if="loading"
      class="flex flex-col justify-center items-center py-20 text-slate-400 space-y-4"
    >
      <div
        class="w-8 h-8 border-4 border-[#E2E8F0] border-t-school-navy rounded-full animate-spin mx-auto"
      ></div>
      <span class="text-xs font-bold tracking-widest uppercase">Loading Staff Records...</span>
    </div>

    <!-- Staff Table -->
    <div
      v-else
      class="bg-white rounded-[12px] border border-[#E2E8F0] shadow-none hover:shadow-[0_8px_28px_rgba(0,0,0,0.06)] overflow-hidden"
    >
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr
              class="bg-school-grey border-b border-[#E2E8F0] text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8]"
            >
              <th class="py-5 px-8 font-bold">Staff Member</th>
              <th class="py-5 px-8 font-bold">Role & Title</th>
              <th class="py-5 px-8 font-bold">Contract</th>
              <th class="py-5 px-8 font-bold">Compliance (KRA/NSSF/NHIF)</th>
              <th class="py-5 px-8 font-bold text-center">Leave Days</th>
              <th class="py-5 px-8 pr-6 font-bold text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="text-sm">
            <tr v-if="filteredStaff.length === 0">
              <td colspan="6" class="py-16 text-center text-slate-400 text-sm font-medium">
                {{ searchQuery || roleFilter ? 'No staff match your search.' : 'No staff records found.' }}
              </td>
            </tr>
            <tr
              v-for="staff in filteredStaff"
              :key="staff.id"
              class="border-b border-slate-50 hover:bg-slate-50/50 transition duration-150"
            >
              <td class="py-5 px-8">
                <div class="font-bold text-slate-800">{{ staff.name }}</div>
                <div class="text-xs text-slate-500 font-medium">{{ staff.can_login ? `@${staff.username}` : 'No portal account' }}</div>
              </td>
              <td class="py-5 px-8">
                <div class="flex items-center gap-2">
                  <span class="font-bold text-school-navy capitalize">{{ staff.role.replace('_', ' ') }}</span>
                  <span v-if="staff.can_login" class="text-[9px] font-bold uppercase tracking-widest bg-school-navy/10 text-school-navy px-1.5 py-0.5 rounded">Portal</span>
                  <span v-else class="text-[9px] font-bold uppercase tracking-widest bg-slate-100 text-slate-400 px-1.5 py-0.5 rounded">HR Only</span>
                </div>
                <div class="text-xs text-slate-500">{{ staff.job_title || 'N/A' }}</div>
              </td>
              <td class="py-5 px-8 text-slate-600 font-medium text-xs">
                <div>{{ staff.contract_type || 'N/A' }}</div>
                <div class="text-slate-400 mt-0.5">Hired: {{ staff.date_of_hire || 'N/A' }}</div>
              </td>
              <td class="py-5 px-8 text-xs text-slate-500 space-y-1.5">
                <div>
                  KRA:
                  <span class="font-bold text-slate-700">{{ staff.kra_pin || 'Pending' }}</span>
                </div>
                <div>
                  NSSF:
                  <span class="font-bold text-slate-700">{{ staff.nssf_number || 'Pending' }}</span>
                </div>
                <div>
                  NHIF:
                  <span class="font-bold text-slate-700">{{ staff.nhif_number || 'Pending' }}</span>
                </div>
              </td>
              <td class="py-5 px-8 text-center">
                <div class="text-xs font-bold text-slate-700">{{ staff.accrued_leave_days }} days</div>
                <div class="flex items-center justify-center gap-1 mt-1">
                  <div class="w-20 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div
                      class="h-full rounded-full transition-all"
                      :class="staff.leave_days_left > 7 ? 'bg-emerald-400' : staff.leave_days_left > 0 ? 'bg-amber-400' : 'bg-red-400'"
                      :style="{ width: staff.accrued_leave_days > 0 ? `${Math.round((staff.leave_days_used / staff.accrued_leave_days) * 100)}%` : '0%' }"
                    ></div>
                  </div>
                </div>
                <div class="text-[10px] text-slate-400 mt-0.5">
                  <span class="text-school-red font-semibold">{{ staff.leave_days_used }} used</span>
                  · <span class="text-emerald-600 font-semibold">{{ staff.leave_days_left }} left</span>
                </div>
              </td>
              <td class="py-5 px-8 pr-6 text-right space-x-3">
                <button
                  @click="openModal(staff)"
                  class="text-xs font-bold text-slate-500 hover:text-school-navy transition-colors"
                >
                  Edit
                </button>
                <button
                  v-if="authStore.user?.username !== staff.username && staff.can_login"
                  @click="openResetModal(staff)"
                  class="text-xs font-bold text-school-purple/70 hover:text-school-purple transition-colors"
                >
                  Reset PW
                </button>
                <button
                  v-if="authStore.user?.username !== staff.username"
                  @click="terminateStaff(staff.id)"
                  class="text-xs font-bold text-school-red/70 hover:text-school-red transition-colors"
                >
                  Terminate
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Hire / Edit Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-slate-900/40 flex items-center justify-center py-5 px-8 z-50 animate-fade-in overflow-y-auto"
    >
      <div class="bg-white rounded-[12px] shadow-2xl w-full max-w-2xl overflow-hidden my-8">
        <div
          class="p-8 border-b border-slate-100 flex justify-between items-center bg-slate-50 sticky top-0 z-10"
        >
          <h2 class="text-xl font-black text-slate-800 tracking-tight">
            {{ isEditing ? 'Edit Staff Profile' : 'Hire New Staff' }}
          </h2>
          <button
            @click="closeModal"
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

        <form @submit.prevent="saveStaff" class="p-8 space-y-6">
          <!-- Basic Info -->
          <div class="space-y-4">
            <h3 class="text-sm font-bold text-slate-800 border-b border-slate-100 pb-2">
              Basic Information
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-8">
              <div>
                <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5">Full Name</label>
                <input
                  v-model="formData.name"
                  required
                  type="text"
                  class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
              <div>
                <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5">Staff Role</label>
                <select
                  v-model="formData.role"
                  required
                  class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                >
                  <optgroup label="Portal Access (Login Required)">
                    <option value="accountant">Accountant / Finance Officer</option>
                    <option value="secretary">Secretary</option>
                    <option value="senior_teacher">Senior Teacher</option>
                    <option value="principal">Principal</option>
                    <option value="admin">System Admin</option>
                  </optgroup>
                  <optgroup label="HR Only (No Login)">
                    <option value="teacher">Teacher</option>
                    <option value="support_staff">Support Staff</option>
                  </optgroup>
                </select>
              </div>
            </div>

            <!-- Portal credentials — only shown for portal roles -->
            <div v-if="isPortalRole" class="grid grid-cols-1 sm:grid-cols-2 gap-8 pt-1">
              <div>
                <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5">Username</label>
                <input
                  v-model="formData.username"
                  :required="isPortalRole"
                  type="text"
                  :disabled="isEditing"
                  class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium disabled:opacity-50"
                />
              </div>
              <div v-if="!isEditing">
                <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5">Password</label>
                <input
                  v-model="formData.password"
                  :required="isPortalRole && !isEditing"
                  type="password"
                  class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
            </div>
            <div v-else class="flex items-center gap-2 text-xs text-slate-500 bg-slate-50 rounded-lg px-4 py-2.5">
              <svg class="w-4 h-4 text-slate-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              This staff member will be added to HR records only and will not have a system login account.
            </div>
          </div>

          <!-- Employment Details -->
          <div class="space-y-4">
            <h3 class="text-sm font-bold text-slate-800 border-b border-slate-100 pb-2">
              Employment Details
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-8">
              <div>
                <label
                  class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
                  >Job Title</label
                >
                <input
                  v-model="formData.job_title"
                  type="text"
                  class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
              <div>
                <label
                  class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
                  >Contract Type</label
                >
                <select
                  v-model="formData.contract_type"
                  class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                >
                  <option value="Permanent">Permanent & Pensionable</option>
                  <option value="Contract">Contract</option>
                  <option value="Temporary">Temporary</option>
                </select>
              </div>
              <div>
                <label
                  class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
                  >Date of Hire</label
                >
                <input
                  v-model="formData.date_of_hire"
                  type="date"
                  class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
              <div>
                <label
                  class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
                  >Leave Days</label
                >
                <input
                  v-model.number="formData.accrued_leave_days"
                  type="number"
                  min="0"
                  class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
            </div>
          </div>

          <!-- Compensation — accountant + admin only -->
          <div v-if="['accountant','admin'].includes(authStore.user?.role)" class="space-y-4">
            <h3 class="text-sm font-bold text-slate-800 border-b border-slate-100 pb-2 flex items-center gap-2">
              Compensation
              <span class="text-[10px] font-bold uppercase tracking-widest bg-amber-100 text-amber-700 px-2 py-0.5 rounded">Confidential</span>
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div>
                <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5">Basic Salary (KES/month)</label>
                <input
                  v-model.number="formData.basic_salary"
                  type="number"
                  min="0"
                  step="500"
                  class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 font-bold text-slate-800"
                />
              </div>
              <div>
                <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-emerald-600 mb-1.5">Allowances (KES/month)</label>
                <input
                  v-model.number="formData.allowances"
                  type="number"
                  min="0"
                  step="100"
                  class="w-full border border-emerald-200 rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-emerald-400/20 focus:border-emerald-400 outline-none bg-emerald-50/50 font-bold text-emerald-700"
                />
              </div>
              <div>
                <label class="block text-[11px] font-bold uppercase tracking-[0.07em] text-red-500 mb-1.5">Deductions (KES/month)</label>
                <input
                  v-model.number="formData.deductions"
                  type="number"
                  min="0"
                  step="100"
                  class="w-full border border-red-200 rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-red-400/20 focus:border-red-400 outline-none bg-red-50/50 font-bold text-red-600"
                />
              </div>
            </div>
            <p class="text-xs text-slate-400">Net pay = Basic + Allowances − Deductions. Deductions should include PAYE, NSSF, and NHIF.</p>
          </div>

          <!-- Compliance Details -->
          <div class="space-y-4">
            <h3 class="text-sm font-bold text-slate-800 border-b border-slate-100 pb-2">
              Compliance (Kenyan Law)
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-8">
              <div>
                <label
                  class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
                  >KRA PIN</label
                >
                <input
                  v-model="formData.kra_pin"
                  type="text"
                  class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium uppercase"
                />
              </div>
              <div>
                <label
                  class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
                  >NSSF Number</label
                >
                <input
                  v-model="formData.nssf_number"
                  type="text"
                  class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
              <div>
                <label
                  class="block text-[11px] font-bold uppercase tracking-[0.07em] text-[#94A3B8] mb-1.5"
                  >NHIF Number</label
                >
                <input
                  v-model="formData.nhif_number"
                  type="text"
                  class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
            </div>
          </div>

          <div class="flex justify-end pt-6 border-t border-slate-100 gap-3">
            <button
              type="button"
              @click="closeModal"
              class="px-8 py-4 text-slate-600 hover:bg-slate-100 rounded-[12px] font-bold transition-colors text-sm"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-8 py-4 bg-school-navy text-white rounded-[12px] font-bold hover:bg-school-navy/90 hover:shadow-md transition-all text-sm"
            >
              {{ isEditing ? 'Save Changes' : 'Hire Staff' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    <!-- Password Reset Modal -->
    <div
      v-if="showResetModal"
      class="fixed inset-0 bg-slate-900/40 flex items-center justify-center p-4 z-50 animate-fade-in"
    >
      <div class="bg-white rounded-[12px] shadow-2xl w-full max-w-sm overflow-hidden border border-[#E2E8F0]">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <div>
            <h2 class="text-lg font-black text-slate-800">Reset Password</h2>
            <p class="text-xs text-slate-400 mt-0.5">{{ resetTarget?.name }}</p>
          </div>
          <button
            @click="showResetModal = false"
            class="text-slate-400 hover:text-slate-600 hover:bg-slate-100 h-8 w-8 rounded-full flex items-center justify-center transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-1.5">New Password (min 8 characters)</label>
            <input
              v-model="newPassword"
              type="password"
              placeholder="Enter new password…"
              class="w-full border border-[#E2E8F0] rounded-[12px] px-4 py-3 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm"
            />
          </div>
          <p v-if="resetError" class="text-xs font-medium text-school-red">{{ resetError }}</p>
          <div class="flex gap-3 justify-end pt-2">
            <button
              @click="showResetModal = false"
              class="px-5 py-2.5 text-slate-600 hover:bg-slate-100 rounded-[12px] font-bold transition text-sm"
            >Cancel</button>
            <button
              @click="submitReset"
              :disabled="resetting"
              class="px-5 py-2.5 bg-school-navy text-white rounded-[12px] font-bold hover:bg-school-navy/90 transition text-sm disabled:opacity-50"
            >{{ resetting ? 'Resetting…' : 'Reset Password' }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import staffService from '@/services/staffService'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const PORTAL_ROLES = new Set(['principal', 'secretary', 'accountant', 'admin', 'senior_teacher'])
const staffList = ref([])
const loading = ref(true)
const loadError = ref('')
const showModal = ref(false)
const isEditing = ref(false)
const editId = ref(null)

const searchQuery = ref('')
const roleFilter = ref('')

const isPortalRole = computed(() => PORTAL_ROLES.has(formData.role))

const filteredStaff = computed(() => {
  let list = staffList.value
  if (roleFilter.value) {
    list = list.filter(s => s.role === roleFilter.value)
  }
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return list
  return list.filter(s =>
    s.name.toLowerCase().includes(q) ||
    s.username.toLowerCase().includes(q) ||
    s.role.toLowerCase().includes(q) ||
    (s.job_title || '').toLowerCase().includes(q)
  )
})

const showResetModal = ref(false)
const resetTarget = ref(null)
const newPassword = ref('')
const resetError = ref('')
const resetting = ref(false)

const BLANK_FORM = {
  name: '',
  username: '',
  password: '',
  role: 'teacher',
  job_title: '',
  contract_type: 'Permanent',
  date_of_hire: '',
  kra_pin: '',
  nssf_number: '',
  nhif_number: '',
  accrued_leave_days: 21,
  basic_salary: 0,
  allowances: 0,
  deductions: 0,
}

const formData = reactive({ ...BLANK_FORM })

const loadStaff = async () => {
  loading.value = true
  loadError.value = ''
  try {
    staffList.value = await staffService.getAllStaff()
  } catch (error) {
    loadError.value = error.message || 'Failed to load staff records. Please try again.'
  } finally {
    loading.value = false
  }
}

onMounted(loadStaff)

const openModal = (staff = null) => {
  if (staff) {
    isEditing.value = true
    editId.value = staff.id
    Object.assign(formData, staff)
    // Handle null dates for input type=date
    if (!formData.date_of_hire) formData.date_of_hire = ''
  } else {
    isEditing.value = false
    editId.value = null
    Object.assign(formData, { ...BLANK_FORM })
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveStaff = async () => {
  try {
    const payload = { ...formData }
    payload.basic_salary = Number(payload.basic_salary) || 0
    payload.allowances = Number(payload.allowances) || 0
    payload.deductions = Number(payload.deductions) || 0
    // Non-portal roles: strip username/password — backend auto-generates them
    if (!PORTAL_ROLES.has(payload.role)) {
      delete payload.username
      delete payload.password
    } else if (isEditing.value && !payload.password) {
      // Portal role edit: omit password if not being changed
      delete payload.password
    }
    const nullableFields = ['date_of_hire', 'job_title', 'contract_type', 'kra_pin', 'nssf_number', 'nhif_number']
    for (const f of nullableFields) {
      if (payload[f] === '') payload[f] = null
    }
    if (isEditing.value) {
      await staffService.updateStaff(editId.value, payload)
    } else {
      await staffService.createStaff(payload)
    }
    closeModal()
    await loadStaff()
  } catch (error) {
    alert(error.message || 'Failed to save staff record')
  }
}

const terminateStaff = async (id) => {
  if (
    confirm('Are you sure you want to terminate this staff member? This action cannot be undone.')
  ) {
    try {
      await staffService.terminateStaff(id)
      await loadStaff()
    } catch (error) {
      alert(error.message || 'Failed to terminate staff')
    }
  }
}

const openResetModal = (staff) => {
  resetTarget.value = staff
  newPassword.value = ''
  resetError.value = ''
  showResetModal.value = true
}

const submitReset = async () => {
  resetError.value = ''
  if (newPassword.value.length < 8) {
    resetError.value = 'Password must be at least 8 characters.'
    return
  }
  resetting.value = true
  try {
    await staffService.resetPassword(resetTarget.value.id, newPassword.value)
    showResetModal.value = false
    alert(`Password for ${resetTarget.value.name} has been reset successfully.`)
  } catch (e) {
    resetError.value = e.message || 'Password reset failed. Please try again.'
  } finally {
    resetting.value = false
  }
}
</script>
