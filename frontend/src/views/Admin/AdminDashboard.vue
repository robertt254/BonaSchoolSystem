<template>
  <div class="max-w-7xl mx-auto">
    <!-- Page Header -->
    <div class="mb-10">
      <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight">Administrator Dashboard</h1>
      <p class="text-slate-500 mt-2 text-lg">System overview and quick metrics.</p>
    </div>

    <!-- Quick Stat Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-10">
      <!-- Card 1 -->
      <div
        class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200/60 hover:shadow-md transition-shadow relative overflow-hidden group"
      >
        <div
          class="absolute right-0 top-0 w-24 h-24 bg-blue-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"
        ></div>
        <div class="flex justify-between items-start relative z-10">
          <div>
            <div class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">
              Total Students
            </div>
            <div class="text-4xl font-extrabold text-slate-800">{{ activeStudentsCount }}</div>
          </div>
          <div class="p-3 bg-blue-100/50 text-blue-600 rounded-xl">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
              ></path>
            </svg>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm relative z-10">
          <span class="text-emerald-500 font-semibold flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
              ></path>
            </svg>
            +2.5%
          </span>
          <span class="text-slate-400 ml-2">from last term</span>
        </div>
      </div>

      <!-- Card 2 -->
      <div
        class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200/60 hover:shadow-md transition-shadow relative overflow-hidden group"
      >
        <div
          class="absolute right-0 top-0 w-24 h-24 bg-purple-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"
        ></div>
        <div class="flex justify-between items-start relative z-10">
          <div>
            <div class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">
              Active Staff
            </div>
            <div class="text-4xl font-extrabold text-slate-800">{{ activeStaffCount }}</div>
          </div>
          <div class="p-3 bg-purple-100/50 text-purple-600 rounded-xl">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
              ></path>
            </svg>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm relative z-10">
          <span class="text-slate-400 font-semibold flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 12h14"
              ></path>
            </svg>
            No change
          </span>
          <span class="text-slate-400 ml-2">from last term</span>
        </div>
      </div>

      <!-- Card 3 -->
      <div
        class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200/60 hover:shadow-md transition-shadow relative overflow-hidden group"
      >
        <div
          class="absolute right-0 top-0 w-24 h-24 bg-emerald-50 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110"
        ></div>
        <div class="flex justify-between items-start relative z-10">
          <div>
            <div class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">
              System Status
            </div>
            <div class="text-2xl font-bold text-emerald-600 flex items-center gap-3 mt-3">
              <span class="relative flex h-3 w-3">
                <span
                  class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"
                ></span>
                <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
              </span>
              All Systems Operational
            </div>
          </div>
          <div class="p-3 bg-emerald-100/50 text-emerald-600 rounded-xl">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 13l4 4L19 7"
              ></path>
            </svg>
          </div>
        </div>
        <div class="mt-4 text-sm text-slate-400 relative z-10">Last checked: Just now</div>
      </div>
    </div>

    <!-- Main Data Area Placeholder (Skeleton Design) -->
    <div class="relative bg-white rounded-2xl shadow-sm border border-slate-200/60 overflow-hidden">
      <!-- Table Header Skeleton -->
      <div class="border-b border-slate-100 px-6 py-5 flex items-center justify-between">
        <h3 class="text-lg font-bold text-slate-800">Recent Activity</h3>
        <div class="h-8 w-24 bg-slate-100 rounded animate-pulse"></div>
      </div>
      <!-- Table Body Skeleton -->
      <div class="p-6">
        <div class="space-y-4">
          <div
            v-for="i in 4"
            :key="i"
            class="flex items-center justify-between py-3 border-b border-slate-50 last:border-0"
          >
            <div class="flex items-center gap-4">
              <div class="h-10 w-10 bg-slate-100 rounded-full animate-pulse"></div>
              <div>
                <div class="h-4 w-32 bg-slate-200 rounded animate-pulse mb-2"></div>
                <div class="h-3 w-20 bg-slate-100 rounded animate-pulse"></div>
              </div>
            </div>
            <div class="h-4 w-24 bg-slate-100 rounded animate-pulse"></div>
          </div>
        </div>
      </div>

      <!-- Overlay Empty State -->
      <div
        class="absolute inset-0 z-10 flex flex-col items-center justify-center bg-white/80 backdrop-blur-[1px]"
      >
        <div class="p-4 bg-slate-50 rounded-full mb-4">
          <svg class="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
            ></path>
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-slate-800 mb-1">Awaiting Data Connection</h3>
        <p class="text-sm text-slate-500 max-w-sm text-center">
          Backend connection is pending. Real-time metrics and activity logs will populate here once
          connected.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import studentService from '@/services/studentService'
import staffService from '@/services/staffService'

const activeStudentsCount = ref(0)
const activeStaffCount = ref(0)
const loading = ref(true)

const loadData = async () => {
  loading.value = true
  try {
    const [students, staff] = await Promise.all([
      studentService.getAllStudents(),
      staffService.getAllStaff(),
    ])

    // Calculate active students
    activeStudentsCount.value = students.filter((student) => student.status === 'Active').length

    // Calculate active staff
    activeStaffCount.value = staff.filter((s) => s.status === 'Active').length || staff.length
  } catch (error) {
    console.error('Failed to load dashboard metrics', error)
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>
