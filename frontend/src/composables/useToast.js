import { ref } from 'vue'

const toasts = ref([])
let _id = 0

function add(message, type = 'info', duration = 3500) {
  const id = ++_id
  toasts.value.push({ id, message, type })
  setTimeout(() => remove(id), duration)
}

function remove(id) {
  const i = toasts.value.findIndex(t => t.id === id)
  if (i !== -1) toasts.value.splice(i, 1)
}

export function useToast() {
  return {
    toasts,
    success: (msg, dur) => add(msg, 'success', dur),
    error:   (msg, dur) => add(msg, 'error', dur ?? 5000),
    info:    (msg, dur) => add(msg, 'info', dur),
    warning: (msg, dur) => add(msg, 'warning', dur),
    remove,
  }
}
