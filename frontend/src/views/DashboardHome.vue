<template>
  <div class="p-8 bg-slate-50 min-h-screen">

    <div class="bg-blue-900 rounded-2xl p-8 text-white shadow-lg mb-8 flex justify-between items-center bg-opacity-95">
      <div>
        <h1 class="text-3xl font-black tracking-wide mb-2">Welcome to The Bona School</h1>
        <p class="text-blue-200 text-lg">Competency-Based Curriculum (CBC) Management System</p>
      </div>
      <div class="hidden md:block text-5xl">
        🎓
      </div>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-12 text-slate-500">
      <span class="animate-pulse text-lg font-medium">Compiling school analytics...</span>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">

      <div class="bg-white rounded-xl p-6 shadow-sm border border-slate-200 border-t-4 border-t-blue-500">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-sm font-bold text-slate-500 uppercase tracking-wider mb-1">Total Enrolled</p>
            <h2 class="text-4xl font-black text-slate-800">{{ totalStudents }}</h2>
          </div>
          <div class="p-3 bg-blue-50 rounded-lg text-blue-600 text-xl">👨‍🎓</div>
        </div>
        <p class="text-sm text-slate-500 mt-4 font-medium">Across all CBC grades</p>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm border border-slate-200 border-t-4 border-t-emerald-500">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-sm font-bold text-slate-500 uppercase tracking-wider mb-1">Total Revenue</p>
            <h2 class="text-3xl font-black text-slate-800">{{ formatCurrency(totalRevenue) }}</h2>
          </div>
          <div class="p-3 bg-emerald-50 rounded-lg text-emerald-600 text-xl">💰</div>
        </div>
        <p class="text-sm text-slate-500 mt-4 font-medium">All historical payments</p>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm border border-slate-200 border-t-4 border-t-indigo-500">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-sm font-bold text-slate-500 uppercase tracking-wider mb-1">Active Staff</p>
            <h2 class="text-4xl font-black text-slate-800">{{ totalStaff }}</h2>
          </div>
          <div class="p-3 bg-indigo-50 rounded-lg text-indigo-600 text-xl">🧑‍🏫</div>
        </div>
        <p class="text-sm text-slate-500 mt-4 font-medium">Teachers & Administrators</p>
      </div>

    </div>

    <div v-if="!loading" class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h3 class="text-lg font-bold text-slate-800 mb-4">Quick Actions</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <router-link to="/academics/attendance" class="p-4 border border-slate-100 rounded-lg hover:bg-slate-50 transition text-center group">
          <div class="text-2xl mb-2 group-hover:scale-110 transition-transform">📋</div>
          <p class="font-medium text-slate-700">Roll Call</p>
        </router-link>
        <router-link to="/finance" class="p-4 border border-slate-100 rounded-lg hover:bg-slate-50 transition text-center group">
          <div class="text-2xl mb-2 group-hover:scale-110 transition-transform">💵</div>
          <p class="font-medium text-slate-700">Log Payment</p>
        </router-link>
        <router-link to="/academics" class="p-4 border border-slate-100 rounded-lg hover:bg-slate-50 transition text-center group">
          <div class="text-2xl mb-2 group-hover:scale-110 transition-transform">📝</div>
          <p class="font-medium text-slate-700">Enter Grades</p>
        </router-link>
        <router-link to="/office" class="p-4 border border-slate-100 rounded-lg hover:bg-slate-50 transition text-center group">
          <div class="text-2xl mb-2 group-hover:scale-110 transition-transform">➕</div>
          <p class="font-medium text-slate-700">Admit Student</p>
        </router-link>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import studentService from '@/services/studentService'
import feeService from '@/services/feeService'
import staffService from '@/services/staffService'

const loading = ref(true)
const totalStudents = ref(0)
const totalRevenue = ref(0)
const totalStaff = ref(0)

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 }).format(amount)
}

onMounted(async () => {
  try {
    // We use Promise.all to fetch everything at the exact same time
    const [students, fees, staff] = await Promise.all([
      studentService.getAllStudents().catch(() => []),
      feeService.getAllFees().catch(() => []),
      staffService.getAllStaff().catch(() => [])
    ])

    // Calculate the totals
    totalStudents.value = students.length
    totalStaff.value = staff.length

    // Add up every single payment in the ledger
    totalRevenue.value = fees.reduce((sum, fee) => sum + (fee.amount || 0), 0)

  } catch (error) {
    console.error("Failed to load dashboard analytics", error)
  } finally {
    loading.value = false
  }
})
</script>
