#!/bin/bash

FILES=$(find frontend/src/views -name "*.vue" ! -name "DashboardHome.vue" ! -name "LoginView.vue")

for file in $FILES; do
  # Cards
  sed -i 's/rounded-2xl/rounded-\[12px\]/g' "$file"
  sed -i 's/rounded-xl/rounded-\[12px\]/g' "$file"
  sed -i 's/shadow-sm border border-slate-200\/60/border border-\[\#E2E8F0\] shadow-none hover:shadow-\[0_8px_28px_rgba(0,0,0,0.06)\]/g' "$file"
  sed -i 's/border border-slate-200/border border-\[\#E2E8F0\]/g' "$file"
  sed -i 's/border border-slate-100/border border-\[\#E2E8F0\]/g' "$file"

  # Remove glassmorphism
  sed -i 's/bg-white\/80 backdrop-blur-xl/bg-white/g' "$file"
  sed -i 's/bg-white\/70 backdrop-blur-2xl/bg-white/g' "$file"
  sed -i 's/bg-white\/60 backdrop-blur-lg/bg-white/g' "$file"
  sed -i 's/backdrop-blur-xl//g' "$file"
  sed -i 's/backdrop-blur-2xl//g' "$file"
  sed -i 's/backdrop-blur-lg//g' "$file"
  sed -i 's/backdrop-blur-md//g' "$file"
  sed -i 's/backdrop-blur-sm//g' "$file"
  sed -i 's/bg-white\/90/bg-white/g' "$file"
  sed -i 's/bg-white\/80/bg-white/g' "$file"
  sed -i 's/bg-white\/70/bg-white/g' "$file"
  sed -i 's/bg-white\/60/bg-white/g' "$file"

  # Headings
  sed -i 's/text-3xl font-extrabold text-slate-900/font-heading text-\[22px\] font-bold text-\[\#0F172A\]/g' "$file"
  sed -i 's/text-2xl font-bold text-slate-800/font-heading text-\[22px\] font-bold text-\[\#0F172A\]/g' "$file"
  sed -i 's/text-lg font-black text-slate-800/font-heading text-\[22px\] font-bold text-\[\#0F172A\]/g' "$file"
  sed -i 's/text-slate-500 mt-2 text-lg/text-\[13px\] text-\[\#94A3B8\] mt-1/g' "$file"

  # Section labels
  sed -i 's/text-xs font-bold text-slate-400 uppercase tracking-widest/text-\[11px\] font-bold uppercase tracking-\[0.07em\] text-\[\#94A3B8\]/g' "$file"
  sed -i 's/text-xs font-bold text-slate-500 uppercase tracking-widest/text-\[11px\] font-bold uppercase tracking-\[0.07em\] text-\[\#94A3B8\]/g' "$file"

  # Forms
  sed -i 's/border border-slate-200 rounded-xl p-3 focus:ring-2 focus:ring-school-navy\/20 focus:border-school-navy outline-none bg-slate-50 text-sm/w-full px-\[14px\] py-\[9px\] rounded-\[9px\] border border-\[\#E2E8F0\] text-\[13px\] text-\[\#0F172A\] bg-white focus:outline-none focus:border-school-red focus:ring-2 focus:ring-school-red\/10 transition-all/g' "$file"
  sed -i 's/border border-slate-200 rounded-xl p-2.5 focus:ring-2 focus:ring-school-navy\/20 focus:border-school-navy outline-none bg-slate-50 text-sm/w-full px-\[14px\] py-\[9px\] rounded-\[9px\] border border-\[\#E2E8F0\] text-\[13px\] text-\[\#0F172A\] bg-white focus:outline-none focus:border-school-red focus:ring-2 focus:ring-school-red\/10 transition-all/g' "$file"
  sed -i 's/border border-slate-300 rounded-xl p-3 focus:ring-2 focus:ring-school-navy\/20 focus:border-school-navy outline-none bg-white text-sm/w-full px-\[14px\] py-\[9px\] rounded-\[9px\] border border-\[\#E2E8F0\] text-\[13px\] text-\[\#0F172A\] bg-white focus:outline-none focus:border-school-red focus:ring-2 focus:ring-school-red\/10 transition-all/g' "$file"

  # Remove animations
  sed -i 's/animate-pulse-glow//g' "$file"
  sed -i 's/animate-float//g' "$file"
  sed -i 's/animate-gradient-xy//g' "$file"
  sed -i 's/animate-spin-slow//g' "$file"
  sed -i 's/animate-bounce-slow//g' "$file"
  sed -i 's/animate-slide-up//g' "$file"
  sed -i 's/animate-bounce//g' "$file"

  # Clean up extra spaces
  sed -i 's/class=" /class="/g' "$file"
  sed -i 's/  "/ "/g' "$file"

done
