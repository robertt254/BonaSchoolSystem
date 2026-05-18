<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-slate-900">Teacher Dashboard</h1>
      <p class="text-slate-500 mt-1">Class management and academic records.</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
        <div class="text-sm font-semibold text-slate-500 uppercase">My Classes</div>
        <div class="mt-2 text-2xl font-bold text-bona-navy">Form 3A, 4B</div>
      </div>
      <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
        <div class="text-sm font-semibold text-slate-500 uppercase">Pending Grades</div>
        <div class="mt-2 text-2xl font-bold text-bona-red">2 Sets</div>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <h3 class="text-lg font-bold text-slate-800 mb-4">Today's Timetable</h3>
      <div class="text-slate-500 text-center py-8 border-2 border-dashed border-slate-200 rounded-lg">
        Timetable module loading...
      </div>
    </div>
  </div>
</template>