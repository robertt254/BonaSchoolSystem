import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || null)
  const user = ref({
    name: localStorage.getItem('user_name') || null,
    role: localStorage.getItem('user_role') || null,
    username: localStorage.getItem('username') || null,
  })

  const login = async (username, password) => {
    // FastAPI's OAuth2 expects form data, NOT JSON
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)

    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    })

    if (!response.ok) {
      throw new Error('Invalid username or password')
    }

    const data = await response.json()

    // Save token
    token.value = data.access_token
    localStorage.setItem('access_token', data.access_token)

    // Decode the JWT token to find out who just logged in
    // A JWT has 3 parts separated by dots. The middle part is the data (payload).
    const payloadBase64 = data.access_token.split('.')[1]
    const decodedPayload = JSON.parse(atob(payloadBase64))

    // Update state (assuming your backend puts sub/role in the token)
    // If your backend doesn't put role in the token, we will map it temporarily
    const assignedRole = decodedPayload.role || determineRoleFromUsername(username)
    const assignedName = decodedPayload.name || username

    user.value = { username: decodedPayload.sub, role: assignedRole, name: assignedName }

    localStorage.setItem('user_role', assignedRole)
    localStorage.setItem('user_name', assignedName)
    localStorage.setItem('username', decodedPayload.sub)
  }

  // Fallback helper just in case your backend JWT doesn't contain the role yet
  const determineRoleFromUsername = (uname) => {
    if (uname.includes('admin')) return 'admin'
    if (uname.includes('principal')) return 'principal'
    if (uname.includes('finance') || uname.includes('account')) return 'accountant'
    if (uname.includes('secretary')) return 'secretary'
    return 'senior_teacher'
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
