import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import LoginView from '../views/LoginView.vue'
import DashboardHome from '../views/DashboardHome.vue'
import ForbiddenView from '../views/ForbiddenView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
    },
    {
      path: '/403',
      name: 'Forbidden',
      component: ForbiddenView,
    },
    {
      path: '/',
      component: AppLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: DashboardHome,
          meta: { requiresAuth: true },
        },
        {
          path: 'admin',
          name: 'admin-dash',
          component: () => import('../views/Admin/AdminDashboard.vue'),
          meta: { requiresAuth: true, roles: ['admin'] },
        },
        {
          path: 'admin/staff',
          name: 'staff-directory',
          component: () => import('../views/HRDashboard.vue'),
          meta: { requiresAuth: true, roles: ['admin', 'principal'] },
        },
        {
          path: 'principal',
          name: 'principal-dash',
          component: () => import('../views/Principal/PrincipalDashboard.vue'),
          meta: { requiresAuth: true, roles: ['principal', 'admin'] },
        },
        {
          path: 'office',
          name: 'secretary-dash',
          component: () => import('../views/Office/SecretaryDash.vue'),
          meta: { requiresAuth: true, roles: ['secretary', 'principal', 'admin'] },
        },
        {
          path: 'finance',
          name: 'accountant-dash',
          // AccountantDashboard.vue was replaced by FinanceDashboard.vue in upstream
          component: () => import('../views/Finance/FinanceDashboard.vue'),
          meta: { requiresAuth: true, roles: ['accountant', 'principal', 'admin'] },
        },
        {
          path: 'finance/statements',
          name: 'fee-statement',
          component: () => import('../views/FeeStatement.vue'),
          meta: { requiresAuth: true, roles: ['accountant', 'principal', 'admin'] },
        },
        {
          path: 'academics',
          name: 'teacher-dash',
          component: () => import('../views/Academics/SeniorTeacherDash.vue'),
          meta: { requiresAuth: true, roles: ['teacher', 'principal', 'admin'] },
        },
        {
          path: 'academics/report-card',
          name: 'report-card',
          component: () => import('../views/ReportCard.vue'),
          meta: { requiresAuth: true, roles: ['teacher', 'principal', 'admin'] },
        },
        {
          path: 'academics/attendance',
          name: 'attendance-page',
          component: () => import('../views/AttendancePage.vue'),
          meta: { requiresAuth: true, roles: ['teacher', 'principal', 'admin'] },
        },
        {
          path: 'students/:id',
          name: 'student-profile',
          component: () => import('../views/StudentProfile.vue'),
          meta: { requiresAuth: true },
        },
        {
          path: 'finance/defaulters',
          name: 'fee-defaulters',
          component: () => import('../views/Finance/FeeDefaulters.vue'),
          meta: { requiresAuth: true, roles: ['accountant', 'principal', 'admin'] },
        },
        {
          path: 'finance/fee-structure',
          name: 'fee-structure',
          component: () => import('../views/Finance/FeeStructureConfig.vue'),
          meta: { requiresAuth: true, roles: ['admin', 'principal'] },
        },
        {
          path: 'academics/timetable',
          name: 'timetable',
          component: () => import('../views/Academics/TimetablePage.vue'),
          meta: { requiresAuth: true, roles: ['teacher', 'principal', 'admin'] },
        },
        {
          path: 'academics/students',
          name: 'students-dashboard',
          component: () => import('../views/Academics/StudentsDashboard.vue'),
          meta: { requiresAuth: true },
        },
        {
          path: 'academics/classes',
          name: 'classes-dashboard',
          component: () => import('../views/Academics/ClassesDashboard.vue'),
          meta: { requiresAuth: true },
        },
        {
          path: 'admin/leave',
          name: 'leave-management',
          component: () => import('../views/Admin/LeaveManagement.vue'),
          meta: { requiresAuth: true },
        },
      ],
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('access_token')
  const isAuthenticated = !!token
  const userRole = localStorage.getItem('user_role')

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }

  if (to.name === 'Login' && isAuthenticated) {
    return next({ name: 'dashboard' })
  }

  const allowedRoles = to.meta.roles
  if (allowedRoles && allowedRoles.length > 0 && !allowedRoles.includes(userRole)) {
    return next({ name: 'Forbidden' })
  }

  next()
})

export default router
