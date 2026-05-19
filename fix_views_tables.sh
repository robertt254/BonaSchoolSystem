#!/bin/bash

FILES=$(find frontend/src/views -name "*.vue" ! -name "DashboardHome.vue" ! -name "LoginView.vue")

for file in $FILES; do
  # Tables
  sed -i 's/class="bg-slate-50 text-slate-500 text-\[11px\] uppercase tracking-wider border-b border-slate-100"/class="bg-school-grey border-b border-\[\#E2E8F0\] text-\[11px\] font-bold uppercase tracking-\[0.07em\] text-\[\#94A3B8\]"/g' "$file"
  sed -i 's/class="bg-slate-50 text-slate-500 text-\[11px\] uppercase tracking-wider border-b border-slate-200"/class="bg-school-grey border-b border-\[\#E2E8F0\] text-\[11px\] font-bold uppercase tracking-\[0.07em\] text-\[\#94A3B8\]"/g' "$file"

done
