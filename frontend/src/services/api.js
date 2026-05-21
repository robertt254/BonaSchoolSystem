import { useAuthStore } from '@/stores/auth'

// ?? (not ||) so that VITE_API_URL="" (same-origin) is preserved and not
// replaced by the localhost fallback. Empty string means requests are relative
// to the current host — correct for the Docker/Render single-container deploy.
export const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000'

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
