<template>
  <div class="max-w-7xl mx-auto">
    <!-- Page Header -->
    <div class="mb-10">
      <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight">Administrator Dashboard</h1>
      <p class="text-slate-500 mt-2 text-lg">System overview and quick metrics.</p>
    </div>

    <!-- Quick Stat Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <!-- Card 1 -->
      <div
        class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200/60 hover:shadow-md transition-shadow"
      >
        <div class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">
          Total Students
        </div>
        <div class="text-4xl font-extrabold text-slate-800">1,248</div>
      </div>

      <!-- Card 2 -->
      <div
        class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200/60 hover:shadow-md transition-shadow"
      >
        <div class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">
          Active Staff
        </div>
        <div class="text-4xl font-extrabold text-slate-800">84</div>
      </div>

      <!-- Card 3 -->
      <div
        class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200/60 hover:shadow-md transition-shadow"
      >
        <div class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">
          System Status
        </div>
        <div class="text-2xl font-bold text-green-600 flex items-center gap-3 mt-2">
          <span class="relative flex h-4 w-4">
            <span
              class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"
            ></span>
            <span class="relative inline-flex rounded-full h-4 w-4 bg-green-500"></span>
          </span>
          Online
        </div>
      </div>
    </div>

    <!-- Main Data Area Placeholder -->
    <div
      class="bg-white rounded-2xl shadow-sm border border-slate-200/60 p-12 text-center text-slate-500 flex flex-col items-center justify-center min-h-[300px]"
    >
      <svg
        class="w-16 h-16 text-slate-300 mb-4"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="1.5"
          d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
        ></path>
      </svg>
      <h3 class="text-lg font-semibold text-slate-700 mb-2">Awaiting Data Connection</h3>
      <p>Backend connection pending. Database metrics will populate here.</p>
    </div>
  </div>
</template>
