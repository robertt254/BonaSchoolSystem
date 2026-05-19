<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight">HR & Staff Management</h1>
        <p class="text-slate-500 mt-2 text-lg">
          Manage school personnel, compliance, and employment records.
        </p>
      </div>
      <button
        @click="openModal()"
        class="bg-school-navy hover:bg-school-navy/90 text-white px-5 py-2.5 rounded-xl font-bold transition-all shadow-sm hover:shadow flex items-center gap-2 text-sm"
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

    <!-- Loading State -->
    <div
      v-if="loading"
      class="flex flex-col justify-center items-center py-20 text-slate-400 space-y-4"
    >
      <div
        class="w-8 h-8 border-4 border-slate-200 border-t-school-navy rounded-full animate-spin"
      ></div>
      <span class="text-xs font-bold tracking-widest uppercase">Loading Staff Records...</span>
    </div>

    <!-- Staff Table -->
    <div v-else class="bg-white rounded-2xl shadow-sm border border-slate-200/60 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr
              class="bg-slate-50 text-slate-500 text-[11px] uppercase tracking-wider border-b border-slate-100"
            >
              <th class="p-4 pl-6 font-bold">Staff Member</th>
              <th class="p-4 font-bold">Role & Title</th>
              <th class="p-4 font-bold">Contract</th>
              <th class="p-4 font-bold">Compliance (KRA/NSSF/NHIF)</th>
              <th class="p-4 font-bold">Leave Days</th>
              <th class="p-4 pr-6 font-bold text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="text-sm">
            <tr
              v-for="staff in staffList"
              :key="staff.id"
              class="border-b border-slate-50 hover:bg-slate-50/50 transition duration-150"
            >
              <td class="p-4 pl-6">
                <div class="font-bold text-slate-800">{{ staff.name }}</div>
                <div class="text-xs text-slate-500 font-medium">Username: {{ staff.username }}</div>
              </td>
              <td class="p-4">
                <div class="font-bold text-school-navy capitalize">{{ staff.role }}</div>
                <div class="text-xs text-slate-500">{{ staff.job_title || 'N/A' }}</div>
              </td>
              <td class="p-4 text-slate-600 font-medium text-xs">
                <div>{{ staff.contract_type || 'N/A' }}</div>
                <div class="text-slate-400 mt-0.5">Hired: {{ staff.date_of_hire || 'N/A' }}</div>
              </td>
              <td class="p-4 text-[10px] text-slate-500 font-mono space-y-1">
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
              <td class="p-4 font-bold text-slate-700">{{ staff.accrued_leave_days }}</td>
              <td class="p-4 pr-6 text-right">
                <button
                  @click="openModal(staff)"
                  class="text-xs font-bold text-slate-500 hover:text-school-navy mr-3 transition-colors"
                >
                  Edit
                </button>
                <button
                  v-if="appStore.user?.username !== staff.username"
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
      class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in overflow-y-auto"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden my-8">
        <div
          class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50 sticky top-0 z-10"
        >
          <h2 class="text-xl font-black text-slate-800 tracking-tight">
            {{ isEditing ? 'Edit Staff Profile' : 'Hire New Staff' }}
          </h2>
          <button
            @click="closeModal"
            class="text-slate-400 hover:text-school-red hover:bg-school-red/10 h-8 w-8 rounded-full flex items-center justify-center transition-colors"
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

        <form @submit.prevent="saveStaff" class="p-6 space-y-6">
          <!-- Basic Info -->
          <div class="space-y-4">
            <h3 class="text-sm font-bold text-slate-800 border-b border-slate-100 pb-2">
              Basic Information
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label
                  class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
                  >Full Name</label
                >
                <input
                  v-model="formData.name"
                  required
                  type="text"
                  class="w-full border border-slate-200 rounded-xl p-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
              <div>
                <label
                  class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
                  >Username</label
                >
                <input
                  v-model="formData.username"
                  required
                  type="text"
                  :disabled="isEditing"
                  class="w-full border border-slate-200 rounded-xl p-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium disabled:opacity-50"
                />
              </div>
              <div v-if="!isEditing">
                <label
                  class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
                  >Password</label
                >
                <input
                  v-model="formData.password"
                  required
                  type="password"
                  class="w-full border border-slate-200 rounded-xl p-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
              <div>
                <label
                  class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
                  >System Role</label
                >
                <select
                  v-model="formData.role"
                  required
                  class="w-full border border-slate-200 rounded-xl p-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                >
                  <option value="teacher">Teacher</option>
                  <option value="finance">Finance Officer</option>
                  <option value="secretary">Secretary</option>
                  <option value="principal">Principal</option>
                  <option value="admin">System Admin</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Employment Details -->
          <div class="space-y-4">
            <h3 class="text-sm font-bold text-slate-800 border-b border-slate-100 pb-2">
              Employment Details
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label
                  class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
                  >Job Title</label
                >
                <input
                  v-model="formData.job_title"
                  type="text"
                  class="w-full border border-slate-200 rounded-xl p-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
              <div>
                <label
                  class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
                  >Contract Type</label
                >
                <select
                  v-model="formData.contract_type"
                  class="w-full border border-slate-200 rounded-xl p-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                >
                  <option value="Permanent">Permanent & Pensionable</option>
                  <option value="Contract">Contract</option>
                  <option value="Temporary">Temporary</option>
                </select>
              </div>
              <div>
                <label
                  class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
                  >Date of Hire</label
                >
                <input
                  v-model="formData.date_of_hire"
                  type="date"
                  class="w-full border border-slate-200 rounded-xl p-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
              <div>
                <label
                  class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
                  >Leave Days</label
                >
                <input
                  v-model.number="formData.accrued_leave_days"
                  type="number"
                  min="0"
                  class="w-full border border-slate-200 rounded-xl p-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
            </div>
          </div>

          <!-- Compliance Details -->
          <div class="space-y-4">
            <h3 class="text-sm font-bold text-slate-800 border-b border-slate-100 pb-2">
              Compliance (Kenyan Law)
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label
                  class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
                  >KRA PIN</label
                >
                <input
                  v-model="formData.kra_pin"
                  type="text"
                  class="w-full border border-slate-200 rounded-xl p-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium uppercase"
                />
              </div>
              <div>
                <label
                  class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
                  >NSSF Number</label
                >
                <input
                  v-model="formData.nssf_number"
                  type="text"
                  class="w-full border border-slate-200 rounded-xl p-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
              <div>
                <label
                  class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5"
                  >NHIF Number</label
                >
                <input
                  v-model="formData.nhif_number"
                  type="text"
                  class="w-full border border-slate-200 rounded-xl p-2.5 focus:ring-2 focus:ring-school-navy/20 focus:border-school-navy outline-none bg-slate-50 text-sm font-medium"
                />
              </div>
            </div>
          </div>

          <div class="flex justify-end pt-6 border-t border-slate-100 gap-3">
            <button
              type="button"
              @click="closeModal"
              class="px-5 py-2.5 text-slate-600 hover:bg-slate-100 rounded-xl font-bold transition-colors text-sm"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-5 py-2.5 bg-school-navy text-white rounded-xl font-bold hover:bg-school-navy/90 hover:shadow-md transition-all text-sm"
            >
              {{ isEditing ? 'Save Changes' : 'Hire Staff' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import staffService from '@/services/staffService'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()
const staffList = ref([])
const loading = ref(true)
const showModal = ref(false)
const isEditing = ref(false)
const editId = ref(null)

const formData = reactive({
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
  accrued_leave_days: 0,
})

const loadStaff = async () => {
  loading.value = true
  try {
    staffList.value = await staffService.getAllStaff()
  } catch (error) {
    console.error(error)
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
    Object.assign(formData, {
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
      accrued_leave_days: 0,
    })
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveStaff = async () => {
  try {
    if (isEditing.value) {
      await staffService.updateStaff(editId.value, formData)
    } else {
      await staffService.createStaff(formData)
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
</script>
