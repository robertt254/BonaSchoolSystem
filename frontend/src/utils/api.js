import { useAuthStore } from '@/stores/auth'

export const getHeaders = () => {
  const authStore = useAuthStore()
  const token = authStore.token || localStorage.getItem('access_token')

  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  }
}
