import { defineStore } from 'pinia'
import { ref } from 'vue'
import { BASE_URL } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || null)
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

    // JWT payload contains sub, role, and name (all set by the backend)
    const payloadBase64 = data.access_token.split('.')[1]
    const payload = JSON.parse(atob(payloadBase64))

    if (!payload.role) {
      throw new Error('Malformed token: missing role claim')
    }

    user.value = { username: payload.sub, role: payload.role, name: payload.name || username }

    localStorage.setItem('user_role', user.value.role)
    localStorage.setItem('user_name', user.value.name)
    localStorage.setItem('username', user.value.username)
  }

  const logout = () => {
    token.value = null
    user.value = { name: null, role: null, username: null }
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_role')
    localStorage.removeItem('user_name')
    localStorage.removeItem('username')
  }

  return { token, user, login, logout }
})
