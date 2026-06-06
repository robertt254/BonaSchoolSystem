<template>
  <div class="max-w-7xl mx-auto space-y-6">

    <!-- Page header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
      <div>
        <h2 class="text-2xl font-bold" style="color:#1c1b1d;letter-spacing:-0.01em">Student Directory</h2>
        <p class="text-sm mt-0.5" style="color:#46464c">Manage and track student enrollment across all academic levels.</p>
      </div>
    </div>

    <!-- Header stats -->
    <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div v-for="n in 4" :key="n" class="bg-white rounded border border-border p-6">
        <div class="skel h-2 w-24 rounded mb-3" />
        <div class="skel h-8 w-12 rounded" />
      </div>
    </div>
    <div v-else class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <!-- Total Students -->
      <div class="bg-white border border-slate-200 rounded p-6 flex flex-col justify-between hover:shadow-sm transition-all duration-200" style="min-height:130px;animation:slideIn 0.4s 0.04s ease both">
        <div class="flex justify-between items-start mb-4">
          <div class="p-2 rounded" style="background:rgba(113,46,221,0.1)">
            <span class="material-symbols-outlined" style="color:#712edd;font-size:22px">group</span>
          </div>
          <span class="text-xs font-semibold px-2 py-0.5 rounded" style="color:#64748b;background:#f1f5f9">All</span>
        </div>
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider" style="color:#64748b">Total Students</p>
          <h3 class="text-2xl font-bold mt-0.5" style="color:#1c1b1d">{{ displayTotal }}</h3>
        </div>
      </div>
      <!-- Active -->
      <div class="bg-white border border-slate-200 rounded p-6 flex flex-col justify-between hover:shadow-sm transition-all duration-200" style="min-height:130px;animation:slideIn 0.4s 0.12s ease both">
        <div class="flex justify-between items-start mb-4">
          <div class="p-2 rounded" style="background:#f0fdf4">
            <span class="material-symbols-outlined" style="color:#16a34a;font-size:22px">how_to_reg</span>
          </div>
          <span class="text-xs font-semibold px-2 py-0.5 rounded" style="color:#16a34a;background:#f0fdf4">Active</span>
        </div>
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider" style="color:#64748b">Active Enrollment</p>
          <h3 class="text-2xl font-bold mt-0.5" style="color:#1c1b1d">{{ displayActive }}</h3>
        </div>
      </div>
      <!-- Male -->
      <div class="bg-white border border-slate-200 rounded p-6 flex flex-col justify-between hover:shadow-sm transition-all duration-200" style="min-height:130px;animation:slideIn 0.4s 0.20s ease both">
        <div class="flex justify-between items-start mb-4">
          <div class="p-2 rounded" style="background:#eff6ff">
            <span class="material-symbols-outlined" style="color:#2563eb;font-size:22px">male</span>
          </div>
        </div>
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider" style="color:#64748b">Male</p>
          <h3 class="text-2xl font-bold mt-0.5" style="color:#1c1b1d">{{ displayMale }}</h3>
        </div>
      </div>
      <!-- Female -->
      <div class="bg-white border border-slate-200 rounded p-6 flex flex-col justify-between hover:shadow-sm transition-all duration-200" style="min-height:130px;animation:slideIn 0.4s 0.28s ease both">
        <div class="flex justify-between items-start mb-4">
          <div class="p-2 rounded" style="background:#fce7f3">
            <span class="material-symbols-outlined" style="color:#db2777;font-size:22px">female</span>
          </div>
        </div>
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider" style="color:#64748b">Female</p>
          <h3 class="text-2xl font-bold mt-0.5" style="color:#1c1b1d">{{ displayFemale }}</h3>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded border border-border p-4 flex flex-wrap gap-3 items-end">
      <div class="flex-1 min-w-48">
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Search</label>
        <div class="relative">
          <svg class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input
            v-model="search"
            type="text"
            placeholder="Name or admission number…"
            class="w-full pl-9 pr-4 py-2.5 border border-slate-300 rounded text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple"
          />
        </div>
      </div>
      <div>
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Grade</label>
        <select v-model="gradeFilter" class="border border-slate-300 px-3 py-2.5 rounded text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple">
          <option value="">All Grades</option>
          <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
        </select>
      </div>
      <div>
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Status</label>
        <select v-model="statusFilter" class="border border-slate-300 px-3 py-2.5 rounded text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple">
          <option value="">All</option>
          <option value="Active">Active</option>
          <option value="Graduated">Graduated</option>
          <option value="Transferred">Transferred</option>
        </select>
      </div>
      <div>
        <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Gender</label>
        <select v-model="genderFilter" class="border border-slate-300 px-3 py-2.5 rounded text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple">
          <option value="">All</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
        </select>
      </div>
      <div class="text-sm text-slate-400 self-end pb-1">{{ filtered.length }} result{{ filtered.length !== 1 ? 's' : '' }}</div>
    </div>

    <!-- Student table -->
    <div class="bg-white rounded border border-border overflow-hidden">
      <div v-if="loading" class="p-4 space-y-2">
        <SkeletonLoader type="table" :count="8" />
      </div>

      <div v-else-if="filtered.length === 0" class="py-16 text-center text-slate-400 text-sm">
        No students match the current filters.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-xs font-semibold uppercase tracking-wider text-white" style="background:#161b2b">
              <th class="text-left px-6 py-3">#</th>
              <th class="text-left px-6 py-3">Student</th>
              <th class="text-left px-6 py-3">Adm No.</th>
              <th class="text-left px-6 py-3">Grade</th>
              <th class="text-left px-6 py-3">Gender</th>
              <th class="text-left px-6 py-3">Date of Birth</th>
              <th class="text-left px-6 py-3">Guardian</th>
              <th class="text-left px-6 py-3">Status</th>
              <th class="text-right px-6 py-3">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr
              v-for="(s, i) in filtered"
              :key="s.id"
              class="hover:bg-slate-50 hover:border-l-2 hover:border-l-school-purple/30 transition-all duration-150"
              :style="{ animation: `slideIn 0.3s ${Math.min(i * 0.04, 0.4)}s ease both` }"
            >
              <td class="px-6 py-3.5 text-slate-400 text-xs">{{ i + 1 }}</td>
              <td class="px-6 py-3.5">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded flex items-center justify-center font-bold text-xs shrink-0"
                    :class="s.gender === 'Female' ? 'bg-pink-100 text-pink-600' : 'bg-blue-100 text-blue-600'">
                    {{ s.first_name.charAt(0) }}{{ s.last_name.charAt(0) }}
                  </div>
                  <div>
                    <p class="font-semibold text-slate-800">{{ s.first_name }} {{ s.last_name }}</p>
                    <p v-if="s.address" class="text-xs text-slate-400">{{ s.address }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-3.5 font-mono text-xs text-school-navy">{{ s.admission_number }}</td>
              <td class="px-6 py-3.5 text-slate-600">{{ s.grade_level }}</td>
              <td class="px-6 py-3.5">
                <span v-if="s.gender" class="text-[10px] font-bold uppercase tracking-tighter px-2 py-0.5 rounded-sm border"
                  :class="s.gender === 'Female' ? 'bg-pink-50 text-pink-700 border-pink-200' : 'bg-blue-50 text-blue-700 border-blue-200'">
                  {{ s.gender }}
                </span>
                <span v-else class="text-slate-300">—</span>
              </td>
              <td class="px-6 py-3.5 text-slate-500 text-xs">
                {{ s.date_of_birth ? formatDate(s.date_of_birth) : '—' }}
                <span v-if="s.date_of_birth" class="text-slate-300 ml-1">({{ calcAge(s.date_of_birth) }}y)</span>
              </td>
              <td class="px-6 py-3.5 text-slate-600 text-xs">
                <span v-if="s.guardian_name">{{ s.guardian_name }}</span>
                <span v-if="s.guardian_phone" class="text-slate-400 block">{{ s.guardian_phone }}</span>
                <span v-if="!s.guardian_name" class="text-slate-300">—</span>
              </td>
              <td class="px-6 py-3.5">
                <span class="text-[10px] font-bold uppercase tracking-tighter px-2 py-0.5 rounded-sm border"
                  :class="s.status === 'Active' ? 'bg-green-100 text-green-800 border-green-200' : 'bg-slate-100 text-slate-500 border-slate-200'">
                  {{ s.status }}
                </span>
              </td>
              <td class="px-6 py-3.5 text-right">
                <router-link :to="`/students/${s.id}`" class="text-xs font-semibold text-school-purple hover:text-school-purple-l transition">
                  View Profile
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import studentService from '@/services/studentService'
import { useCounter } from '@/composables/useCounter'
import SkeletonLoader from '@/components/ui/SkeletonLoader.vue'

const GRADES = ['Play Group', 'PP1', 'PP2', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6']

const students = ref([])
const loading = ref(false)
const search = ref('')
const gradeFilter = ref('')
const statusFilter = ref('')
const genderFilter = ref('')
const grades = ref(GRADES)

const filtered = computed(() => {
  let list = students.value
  const q = search.value.toLowerCase()
  if (q) list = list.filter(s =>
    `${s.first_name} ${s.last_name}`.toLowerCase().includes(q) ||
    s.admission_number.toLowerCase().includes(q)
  )
  if (gradeFilter.value) list = list.filter(s => s.grade_level === gradeFilter.value)
  if (statusFilter.value) list = list.filter(s => s.status === statusFilter.value)
  if (genderFilter.value) list = list.filter(s => s.gender === genderFilter.value)
  return list
})

const totalCount  = computed(() => students.value.length)
const activeCount = computed(() => students.value.filter(s => s.status === 'Active').length)
const maleCount   = computed(() => students.value.filter(s => s.gender === 'Male').length)
const femaleCount = computed(() => students.value.filter(s => s.gender === 'Female').length)

const displayTotal  = useCounter(totalCount)
const displayActive = useCounter(activeCount)
const displayMale   = useCounter(maleCount)
const displayFemale = useCounter(femaleCount)

const formatDate = (d) => new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
const calcAge = (dob) => {
  const diff = Date.now() - new Date(dob).getTime()
  return Math.floor(diff / (1000 * 60 * 60 * 24 * 365.25))
}

onMounted(async () => {
  loading.value = true
  try { students.value = await studentService.getAllStudents() }
  catch (e) { console.error(e) }
  finally { loading.value = false }
})
</script>

