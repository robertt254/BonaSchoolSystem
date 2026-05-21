import { defineStore } from 'pinia'
import { ref } from 'vue'
import { BASE_URL } from '@/services/api'

function parseTokenExpiry(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp ? payload.exp * 1000 : null
  } catch {
    return null
  }
}

export const useAuthStore = defineStore('auth', () => {
  const storedToken = localStorage.getItem('access_token')
  const token = ref(storedToken || null)
  const tokenExpiresAt = ref(storedToken ? parseTokenExpiry(storedToken) : null)
  const user = ref({
    name: localStorage.getItem('user_name') || null,
    role: localStorage.getItem('user_role') || null,
    username: localStorage.getItem('username') || null,
  })

  const login = async (username, password) => {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)

    const response = await fetch(`${BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    })

    if (!response.ok) {
      const body = await response.json().catch(() => ({}))
      throw new Error(body.detail || 'Invalid username or password')
    }

    const data = await response.json()

    token.value = data.access_token
    localStorage.setItem('access_token', data.access_token)

    const payload = JSON.parse(atob(data.access_token.split('.')[1]))

    if (!payload.role) {
      throw new Error('Malformed token: missing role claim')
    }

    user.value = { username: payload.sub, role: payload.role, name: payload.name || username }
    tokenExpiresAt.value = payload.exp ? payload.exp * 1000 : null

    localStorage.setItem('user_role', user.value.role)
    localStorage.setItem('user_name', user.value.name)
    localStorage.setItem('username', user.value.username)
  }

  const logout = () => {
    token.value = null
    tokenExpiresAt.value = null
    user.value = { name: null, role: null, username: null }
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_role')
    localStorage.removeItem('user_name')
    localStorage.removeItem('username')
  }

  return { token, tokenExpiresAt, user, login, logout }
})
