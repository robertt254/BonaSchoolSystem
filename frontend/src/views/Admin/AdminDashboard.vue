<template>
  <div>
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-slate-900">Administrator Dashboard</h1>
      <p class="text-slate-500 mt-1">System overview and quick metrics.</p>
    </div>

    <!-- Quick Stat Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">

      <!-- Card 1 -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
        <div class="text-sm font-semibold text-slate-500 uppercase tracking-wider">Total Students</div>
        <div class="mt-2 text-3xl font-bold text-bona-navy">1,248</div>
      </div>

      <!-- Card 2 -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
        <div class="text-sm font-semibold text-slate-500 uppercase tracking-wider">Active Staff</div>
        <div class="mt-2 text-3xl font-bold text-bona-navy">84</div>
      </div>

      <!-- Card 3 -->
      <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
        <div class="text-sm font-semibold text-slate-500 uppercase tracking-wider">System Status</div>
        <div class="mt-2 text-xl font-bold text-green-600 flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-green-500 animate-pulse"></span>
          Online
        </div>
      </div>

    </div>

    <!-- Main Data Area Placeholder -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-8 text-center text-slate-500">
      Backend connection pending. Database metrics will populate here.
    </div>

  </div>
</template>