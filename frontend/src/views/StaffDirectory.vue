<template>
  <div class="p-8 bg-slate-50 min-h-screen">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-3xl font-bold text-slate-800">Staff & HR Directory</h1>
        <p class="text-slate-500 mt-1">System Administrator Access Only</p>
      </div>
      <button
        @click="openAddModal"
        class="bg-school-navy text-white px-5 py-2 rounded-lg shadow hover:bg-school-navy/80 transition font-medium"
      >
        + Hire New Staff
      </button>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr
            class="bg-slate-100 text-slate-600 text-sm uppercase tracking-wider border-b border-slate-200"
          >
            <th class="p-4 font-semibold">Employee Name</th>
            <th class="p-4 font-semibold">System Username</th>
            <th class="p-4 font-semibold">Access Role</th>
            <th class="p-4 font-semibold text-right">Admin Actions</th>
          </tr>
        </thead>
        <tbody class="text-slate-700">
          <tr
            v-for="user in staff"
            :key="user.id"
            class="border-b border-slate-50 hover:bg-slate-50 transition"
          >
            <td class="p-4 font-medium">{{ user.name }}</td>
            <td class="p-4 text-slate-500 font-mono text-sm">{{ user.username }}</td>
            <td class="p-4">
              <span
                class="px-3 py-1 text-xs font-bold rounded-full uppercase tracking-wide"
                :class="{
                  'bg-purple-100 text-purple-700': user.role === 'admin',
                  'bg-school-grey/80 text-blue-700': user.role === 'principal',
                  'bg-emerald-100 text-emerald-700': user.role === 'accountant',
                  'bg-orange-100 text-orange-700': user.role === 'teacher',
                }"
              >
                {{ user.role }}
              </span>
            </td>
            <td class="p-4 text-right space-x-4">
              <button
                @click="openEditModal(user)"
                class="text-school-navy/80 hover:text-indigo-800 font-medium"
              >
                Edit
              </button>
              <button
                @click="deleteStaff(user)"
                class="text-red-600 hover:text-red-800 font-medium"
              >
                Revoke Access
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div
      v-if="showModal"
      class="fixed inset-0 bg-slate-900 bg-opacity-60 flex items-center justify-center p-4 z-50"
    >
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <h2 class="text-xl font-bold text-slate-800">
            {{ isEditing ? 'Edit Employee Access' : 'Create Staff Account' }}
          </h2>
          <button @click="closeModal" class="text-slate-400 hover:text-slate-600 font-bold text-xl">
            &times;
          </button>
        </div>

        <form @submit.prevent="saveStaff" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
            <input
              v-model="formData.name"
              required
              type="text"
              class="w-full border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-school-navy/80 outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Username</label>
              <input
                v-model="formData.username"
                required
                type="text"
                class="w-full border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-school-navy/80 outline-none font-mono text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">System Role</label>
              <select
                v-model="formData.role"
                required
                class="w-full border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-school-navy/80 outline-none"
              >
                <option value="teacher">Teacher</option>
                <option value="accountant">Accountant</option>
                <option value="principal">Principal</option>
                <option value="admin">Admin</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">
              {{ isEditing ? 'New Password (Leave blank to keep current)' : 'Temporary Password' }}
            </label>
            <input
              v-model="formData.password"
              :required="!isEditing"
              type="password"
              class="w-full border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-school-navy/80 outline-none"
            />
          </div>

          <div class="flex justify-end space-x-3 pt-4 border-t border-slate-100 mt-6">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-lg font-medium transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-school-navy text-white rounded-lg font-medium hover:bg-school-navy/80 transition"
            >
              {{ isEditing ? 'Update Access' : 'Create Account' }}
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

const staff = ref([])
const showModal = ref(false)
const isEditing = ref(false)
const currentUserId = ref(null)

const formData = reactive({
  name: '',
  username: '',
  role: 'teacher',
  password: '',
})

const fetchStaff = async () => {
  try {
    staff.value = await staffService.getAllStaff()
  } catch (error) {
    console.error(error)
  }
}

onMounted(fetchStaff)

const openAddModal = () => {
  isEditing.value = false
  currentUserId.value = null
  Object.assign(formData, { name: '', username: '', role: 'teacher', password: '' })
  showModal.value = true
}

const openEditModal = (user) => {
  isEditing.value = true
  currentUserId.value = user.id
  Object.assign(formData, {
    name: user.name,
    username: user.username,
    role: user.role,
    password: '',
  })
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveStaff = async () => {
  try {
    // If editing, and they left password blank, don't send it to the backend
    const payload = { ...formData }
    if (isEditing.value && !payload.password) {
      delete payload.password
    }

    if (isEditing.value) {
      await staffService.updateStaff(currentUserId.value, payload)
    } else {
      await staffService.createStaff(payload)
    }
    closeModal()
    await fetchStaff()
  } catch {
    alert('Error saving staff. Username might be taken.')
  }
}

const deleteStaff = async (user) => {
  if (
    window.confirm(`Are you sure you want to completely revoke system access for ${user.name}?`)
  ) {
    try {
      await staffService.terminateStaff(user.id)
      await fetchStaff()
    } catch (error) {
      alert(error.message) // Will show our "Cannot delete your own admin account" error!
    }
  }
}
</script>
