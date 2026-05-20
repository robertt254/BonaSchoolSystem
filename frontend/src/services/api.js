import { useAuthStore } from '@/stores/auth'

export const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export const getHeaders = () => {
  const token = useAuthStore().token || localStorage.getItem('access_token')
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  }
}

export async function apiFetch(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: { ...getHeaders(), ...(options.headers || {}) },
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed: ${res.status}`)
  }
  return res.json()
}
