#!/bin/bash

FILES=$(find frontend/src/views -name "*.vue" ! -name "DashboardHome.vue" ! -name "LoginView.vue")

for file in $FILES; do
  # Buttons Primary
  sed -i 's/bg-school-navy text-white rounded-xl font-bold hover:bg-school-navy\/90 hover:shadow-md transition-all text-sm/bg-school-red text-white font-semibold text-\[13px\] px-4 py-2 rounded-\[8px\] hover:bg-red-700 transition-colors/g' "$file"
  sed -i 's/bg-school-navy text-white px-5 py-2.5 rounded-xl font-bold text-sm hover:bg-school-navy\/90 shadow-md hover:shadow-lg transition-all/bg-school-red text-white font-semibold text-\[13px\] px-4 py-2 rounded-\[8px\] hover:bg-red-700 transition-colors/g' "$file"
  sed -i 's/bg-emerald-600 text-white rounded-xl font-bold hover:bg-emerald-700 hover:shadow-md transition-all text-sm/bg-school-red text-white font-semibold text-\[13px\] px-4 py-2 rounded-\[8px\] hover:bg-red-700 transition-colors/g' "$file"

  # Loading spinners
  sed -i 's/w-8 h-8 border-4 border-slate-200 border-t-school-navy rounded-full animate-spin/w-8 h-8 border-4 border-\[\#E2E8F0\] border-t-school-navy rounded-full animate-spin mx-auto/g' "$file"

  # remove emojis
  sed -i 's/👨‍🎓//g' "$file"
  sed -i 's/👩‍🏫//g' "$file"
  sed -i 's/📊//g' "$file"
  sed -i 's/💵//g' "$file"
  sed -i 's/📝//g' "$file"
  sed -i 's/✅//g' "$file"

done
