<template>
  <div class="max-w-5xl mx-auto space-y-6">

    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
      <div>
        <h2 class="text-2xl font-bold" style="color:#1c1b1d;letter-spacing:-0.01em">Fee Structure</h2>
        <p class="text-sm mt-0.5" style="color:#46464c">
          Termly tuition, admission and other charges
          <span v-if="!canEdit"> · <span class="font-semibold">view only</span></span>
        </p>
      </div>
      <div class="flex items-center gap-3">
        <select v-model.number="filterYear"
          class="border border-slate-300 rounded px-3 py-2 text-sm font-semibold outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple">
          <option v-for="y in appStore.years" :key="y" :value="y">{{ y }}</option>
        </select>
        <button v-if="canEdit" @click="save" :disabled="saving || loading"
          class="bg-school-navy text-white px-5 py-2 rounded text-sm font-semibold hover:bg-school-navy/90 disabled:opacity-50 transition">
          {{ saving ? 'Saving…' : 'Save Fee Structure' }}
        </button>
      </div>
    </div>

    <!-- Template / status banner -->
    <div v-if="isTemplate" class="flex items-start gap-2.5 bg-amber-50 border border-amber-200 rounded p-3 text-xs text-amber-800">
      <span class="material-symbols-outlined" style="font-size:16px">info</span>
      <span>
        No fee structure saved for <strong>{{ filterYear }}</strong> yet — showing the standard Bona School template.
        <template v-if="canEdit">Review the amounts and click <strong>Save Fee Structure</strong> to apply for {{ filterYear }}.</template>
        <template v-else>The principal has not set this year's fees yet.</template>
      </span>
    </div>

    <div v-if="loading" class="py-16 flex justify-center">
      <div class="w-8 h-8 border-4 border-slate-200 border-t-school-purple rounded-full animate-spin"></div>
    </div>

    <template v-else>
      <!-- 1. Admission & daily -->
      <div class="bg-white rounded border border-border overflow-hidden">
        <div class="px-6 py-3 border-b border-slate-100 bg-slate-50">
          <h3 class="font-bold text-sm text-slate-700">Admission &amp; Daily Costs</h3>
        </div>
        <div class="p-6 grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Admission (payable once)</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">Ksh</span>
              <input v-model.number="admission" type="number" min="0" :disabled="!canEdit"
                class="w-full border border-slate-300 rounded pl-12 pr-3 py-2.5 text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple disabled:bg-slate-50 disabled:text-slate-500" />
            </div>
          </div>
          <div>
            <label class="block text-xs font-bold uppercase tracking-widest text-slate-400 mb-1.5">Under 2 yrs · Daycare + Lifeskills (daily)</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">Ksh</span>
              <input v-model.number="daily" type="number" min="0" :disabled="!canEdit"
                class="w-full border border-slate-300 rounded pl-12 pr-3 py-2.5 text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple disabled:bg-slate-50 disabled:text-slate-500" />
            </div>
          </div>
        </div>
      </div>

      <!-- 2. Termly tuition -->
      <div class="bg-white rounded border border-border overflow-hidden">
        <div class="px-6 py-3 border-b border-slate-100 bg-slate-50">
          <h3 class="font-bold text-sm text-slate-700">Termly Payments (Tuition)</h3>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="text-xs font-semibold uppercase tracking-wider text-white" style="background:#161b2b">
                <th class="text-left px-6 py-3">Level / Grade</th>
                <th class="text-right px-6 py-3">Term 1</th>
                <th class="text-right px-6 py-3">Term 2</th>
                <th class="text-right px-6 py-3">Term 3</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="g in GRADES" :key="g" class="hover:bg-slate-50 transition-colors">
                <td class="px-6 py-2.5 font-semibold text-slate-800">{{ g }}</td>
                <td v-for="term in TERMS" :key="term" class="px-6 py-2 text-right">
                  <input v-model.number="termly[g][term]" type="number" min="0" :disabled="!canEdit"
                    class="w-28 text-right border border-slate-300 rounded px-2 py-1.5 text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple disabled:bg-slate-50 disabled:text-slate-500" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 3. Other payments -->
      <div class="bg-white rounded border border-border overflow-hidden">
        <div class="px-6 py-3 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
          <h3 class="font-bold text-sm text-slate-700">Other Payments</h3>
          <button v-if="canEdit" @click="addItem(other)" class="text-xs font-semibold text-school-purple hover:underline">+ Add item</button>
        </div>
        <div class="p-6 space-y-3">
          <div v-for="(item, i) in other" :key="i" class="flex items-center gap-3">
            <input v-model="item.name" type="text" placeholder="Item name" :disabled="!canEdit"
              class="flex-1 border border-slate-300 rounded px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple disabled:bg-slate-50 disabled:text-slate-500" />
            <div class="relative w-40">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">Ksh</span>
              <input v-model.number="item.amount" type="number" min="0" :disabled="!canEdit"
                class="w-full border border-slate-300 rounded pl-12 pr-3 py-2 text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple disabled:bg-slate-50 disabled:text-slate-500" />
            </div>
            <button v-if="canEdit" @click="other.splice(i, 1)" class="text-slate-300 hover:text-school-red transition shrink-0">
              <span class="material-symbols-outlined" style="font-size:20px">delete</span>
            </button>
          </div>
          <p v-if="!other.length" class="text-sm text-slate-400">No other payments configured.</p>
        </div>
      </div>

      <!-- 4. Co-curricular -->
      <div class="bg-white rounded border border-border overflow-hidden">
        <div class="px-6 py-3 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
          <h3 class="font-bold text-sm text-slate-700">Co-Curricular Activities (Optional)</h3>
          <button v-if="canEdit" @click="addItem(cocurricular)" class="text-xs font-semibold text-school-purple hover:underline">+ Add activity</button>
        </div>
        <div class="p-6 grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div v-for="(item, i) in cocurricular" :key="i" class="flex items-center gap-2">
            <input v-model="item.name" type="text" placeholder="Activity" :disabled="!canEdit"
              class="flex-1 border border-slate-300 rounded px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple disabled:bg-slate-50 disabled:text-slate-500" />
            <div class="relative w-32">
              <span class="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs">Ksh</span>
              <input v-model.number="item.amount" type="number" min="0" :disabled="!canEdit"
                class="w-full border border-slate-300 rounded pl-10 pr-2 py-2 text-sm outline-none focus:ring-2 focus:ring-school-purple/20 focus:border-school-purple disabled:bg-slate-50 disabled:text-slate-500" />
            </div>
            <button v-if="canEdit" @click="cocurricular.splice(i, 1)" class="text-slate-300 hover:text-school-red transition shrink-0">
              <span class="material-symbols-outlined" style="font-size:20px">delete</span>
            </button>
          </div>
          <p v-if="!cocurricular.length" class="text-sm text-slate-400">No activities configured.</p>
        </div>
      </div>

      <!-- Footer save (mirror of header for long pages) -->
      <div v-if="canEdit" class="flex justify-end">
        <button @click="save" :disabled="saving"
          class="bg-school-navy text-white px-6 py-2.5 rounded text-sm font-semibold hover:bg-school-navy/90 disabled:opacity-50 transition">
          {{ saving ? 'Saving…' : 'Save Fee Structure' }}
        </button>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { apiFetch } from '@/services/api'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const toast = useToast()
const appStore = useAppStore()
const authStore = useAuthStore()

const GRADES = ['Play Group', 'PP1', 'PP2', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6']
const TERMS = ['Term 1', 'Term 2', 'Term 3']

const canEdit = computed(() => ['admin', 'principal'].includes(authStore.user?.role))
const filterYear = ref(appStore.currentYear)

const loading = ref(false)
const saving = ref(false)
const isTemplate = ref(false)

const termly = ref({})
const admission = ref(0)
const daily = ref(0)
const other = ref([])
const cocurricular = ref([])

// Convert flat FeeStructure rows into the sectioned editor model.
const organize = (rows) => {
  const t = {}
  GRADES.forEach(g => { t[g] = { 'Term 1': 0, 'Term 2': 0, 'Term 3': 0 } })
  let adm = 0, day = 0
  const oth = [], cocur = []
  for (const r of rows) {
    const amt = Number(r.amount) || 0
    if (r.grade_level !== 'General') {
      if (t[r.grade_level] && TERMS.includes(r.term)) t[r.grade_level][r.term] = amt
    } else if (r.term === 'Once') {
      adm = amt
    } else if (r.term === 'Daily') {
      day = amt
    } else if (r.term === 'Termly') {
      oth.push({ name: r.fee_type, amount: amt })
    } else if (r.term === 'Optional') {
      cocur.push({ name: r.fee_type, amount: amt })
    }
  }
  termly.value = t
  admission.value = adm
  daily.value = day
  other.value = oth
  cocurricular.value = cocur
}

// Flatten the editor model back into FeeStructure rows for bulk save.
const flatten = () => {
  const y = filterYear.value
  const rows = []
  for (const g of GRADES) {
    for (const term of TERMS) {
      rows.push({ grade_level: g, term, fee_type: 'Tuition', amount: Number(termly.value[g]?.[term]) || 0, academic_year: y })
    }
  }
  rows.push({ grade_level: 'General', term: 'Once', fee_type: 'Admission', amount: Number(admission.value) || 0, academic_year: y })
  rows.push({ grade_level: 'General', term: 'Daily', fee_type: 'Daycare (Under 2)', amount: Number(daily.value) || 0, academic_year: y })
  for (const o of other.value) if (o.name?.trim()) rows.push({ grade_level: 'General', term: 'Termly', fee_type: o.name.trim(), amount: Number(o.amount) || 0, academic_year: y })
  for (const c of cocurricular.value) if (c.name?.trim()) rows.push({ grade_level: 'General', term: 'Optional', fee_type: c.name.trim(), amount: Number(c.amount) || 0, academic_year: y })
  return rows
}

const load = async () => {
  loading.value = true
  try {
    const all = await apiFetch('/api/fees/structure')
    const yearRows = (all || []).filter(r => r.academic_year === filterYear.value)
    if (yearRows.length === 0) {
      const tmpl = await apiFetch(`/api/fees/structure/template?year=${filterYear.value}`)
      organize(tmpl)
      isTemplate.value = true
    } else {
      organize(yearRows)
      isTemplate.value = false
    }
  } catch (e) {
    toast.error(e?.message || 'Failed to load fee structure.')
  } finally {
    loading.value = false
  }
}

const save = async () => {
  if (!canEdit.value) return
  saving.value = true
  try {
    const res = await apiFetch('/api/fees/structure/bulk', { method: 'POST', body: JSON.stringify(flatten()) })
    isTemplate.value = false
    toast.success(`Fee structure saved for ${filterYear.value} (${res.saved} items).`)
    await load()
  } catch (e) {
    toast.error(e?.message || 'Failed to save fee structure.')
  } finally {
    saving.value = false
  }
}

const addItem = (list) => { list.push({ name: '', amount: 0 }) }

watch(filterYear, load)
onMounted(load)
</script>
