import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/login', component: () => import('@/views/Login.vue'), meta: { public: true } },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'dashboard', component: () => import('@/views/Dashboard.vue'), meta: { title: '工作台' } },
      { path: 'projects', name: 'projects', component: () => import('@/views/Projects.vue'), meta: { title: '项目管理' } },
      { path: 'projects/:id', name: 'project-detail', component: () => import('@/views/ProjectDetail.vue'), meta: { title: '项目详情' } },
      { path: 'datasets', name: 'datasets', component: () => import('@/views/Datasets.vue'), meta: { title: '数据集管理' } },
      { path: 'annotations', name: 'annotations', component: () => import('@/views/Annotations.vue'), meta: { title: '标注任务' } },
      { path: 'trainings', name: 'trainings', component: () => import('@/views/Trainings.vue'), meta: { title: '训练任务' } },
      { path: 'models', name: 'models', component: () => import('@/views/Models.vue'), meta: { title: '模型仓库' } },
      { path: 'deployments', name: 'deployments', component: () => import('@/views/Deployments.vue'), meta: { title: '部署记录' } },
      { path: 'audits', name: 'audits', component: () => import('@/views/Audits.vue'), meta: { title: '审计日志' } }
    ]
  }
]

const router = createRouter({ history: createWebHashHistory(), routes })

router.beforeEach((to, _, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.public) return next()
  if (!token) return next('/login')
  next()
})

export default router
