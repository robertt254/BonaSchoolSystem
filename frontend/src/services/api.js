import { useAuthStore } from '@/stores/auth'

// Empty string = relative URLs, which the Vite dev proxy forwards to localhost:8000.
// The Dockerfile sets VITE_API_URL="" explicitly for the production build (same origin).
// Override with VITE_API_URL in .env.local only if you run frontend/backend on
// separate hosts (e.g. VITE_API_URL=http://localhost:8000).
export const BASE_URL = import.meta.env.VITE_API_URL ?? ''

export const getHeaders = () => {
  const token = useAuthStore().token || localStorage.getItem('access_token')
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  }
}

export async function apiFetch(path, options = {}) {
  const authStore = useAuthStore()
  if (authStore.isExpired()) {
    authStore.logout()
    window.location.href = '/login'
    throw new Error('Session expired. Please log in again.')
  }

  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: { ...getHeaders(), ...(options.headers || {}) },
  })

  // Session expired — clear local auth state and redirect to login
  if (res.status === 401) {
    const authStore = useAuthStore()
    authStore.logout()
    window.location.href = '/login'
    throw new Error('Session expired. Please log in again.')
  }

  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    // body.detail may be a string or a Pydantic error array
    const detail = typeof body.detail === 'string'
      ? body.detail
      : Array.isArray(body.detail)
        ? body.detail.map(e => e.msg || e.message || JSON.stringify(e)).join('; ')
        : `Request failed: ${res.status}`
    throw new Error(detail)
  }
  return res.json()
}
