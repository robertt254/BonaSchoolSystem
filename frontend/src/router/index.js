import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import LoginView from '../views/LoginView.vue'
import DashboardHome from '../views/DashboardHome.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    },
    {
      path: '/',
      component: AppLayout,
      meta: { requiresAuth: true },
      children: [
        { path: '', name: 'dashboard', component: DashboardHome },
        { path: 'admin', name: 'admin-dash', component: () => import('../views/Admin/AdminDashboard.vue') },
        { path: 'admin/staff', name: 'staff-directory', component: () => import('../views/StaffDirectory.vue') },
        { path: 'principal', name: 'principal-dash', component: () => import('../views/Principal/PrincipalDashboard.vue') },
        { path: 'office', name: 'secretary-dash', component: () => import('../views/Office/SecretaryDash.vue') },
        { path: 'finance', name: 'accountant-dash', component: () => import('../views/Finance/AccountantDashboard.vue') },
        { path: 'finance/statements', name: 'fee-statement', component: () => import('../views/FeeStatement.vue') },
        { path: 'academics', name: 'teacher-dash', component: () => import('../views/Academics/SeniorTeacherDash.vue') },
        { path: 'academics/report-card', name: 'report-card', component: () => import('../views/ReportCard.vue') },
        { path: 'academics/attendance', name: 'attendance-page', component: () => import('../views/AttendancePage.vue') }
      ]
    }
  ]
})

// THE SECURITY GUARD
router.beforeEach((to, from, next) => {
  // Check if there is a token in the browser storage
  const isAuthenticated = !!localStorage.getItem('access_token')

  // If the route requires auth, and they don't have a token, kick them to login
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' })
  }
  // If they DO have a token, but they try to go to the login page, send them to the dashboard
  else if (to.name === 'Login' && isAuthenticated) {
    next({ name: 'dashboard' })
  }
  // Otherwise, let them proceed normally
  else {
    next()
  }
})

export default router