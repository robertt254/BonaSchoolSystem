/**
 * Download table data as a CSV file that Excel opens natively.
 * @param {string} filename  – e.g. "exam-rankings-2025.csv"
 * @param {Array}  headers   – [{key: 'name', label: 'Student Name'}, ...]
 * @param {Array}  rows      – array of objects
 */
export function downloadCsv(filename, headers, rows) {
  const escape = (val) => {
    const s = val === null || val === undefined ? '' : String(val)
    return s.includes(',') || s.includes('"') || s.includes('\n')
      ? `"${s.replace(/"/g, '""')}"`
      : s
  }
  const lines = [
    headers.map(h => escape(h.label)).join(','),
    ...rows.map(row => headers.map(h => escape(row[h.key])).join(',')),
  ]
  const bom = '﻿' // UTF-8 BOM so Excel reads Swahili/special chars correctly
  const blob = new Blob([bom + lines.join('\r\n')], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename.endsWith('.csv') ? filename : filename + '.csv'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
