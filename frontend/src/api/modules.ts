import request from './request'

// ---- 认证 ----
export const authApi = {
  login: (username: string, password: string) =>
    request.post('/auth/login', { username, password }),
  me: () => request.get('/auth/me'),
  logout: () => request.post('/auth/logout')
}

// ---- 工作台 ----
export const dashboardApi = {
  overview: () => request.get('/dashboard/overview')
}

// ---- 项目 ----
export const projectApi = {
  list: (params: any) => request.get('/projects', { params }),
  get: (id: string) => request.get(`/projects/${id}`),
  create: (data: any) => request.post('/projects', data),
  update: (id: string, data: any) => request.put(`/projects/${id}`, data),
  remove: (id: string) => request.delete(`/projects/${id}`),
  stats: () => request.get('/projects/stats/overview')
}

// ---- 数据集 ----
export const datasetApi = {
  list: (params: any) => request.get('/datasets', { params }),
  get: (id: string) => request.get(`/datasets/${id}`),
  create: (data: any) => request.post('/datasets', data),
  update: (id: string, data: any) => request.put(`/datasets/${id}`, data),
  remove: (id: string) => request.delete(`/datasets/${id}`),
  versions: (id: string) => request.get(`/datasets/${id}/versions`),
  createVersion: (id: string, data: any) => request.post(`/datasets/${id}/versions`, data),
  freezeVersion: (vid: string) => request.post(`/datasets/versions/${vid}/freeze`)
}

// ---- 标注任务 ----
export const annotationApi = {
  list: (params: any) => request.get('/annotation-tasks', { params }),
  get: (id: string) => request.get(`/annotation-tasks/${id}`),
  create: (data: any) => request.post('/annotation-tasks', data),
  update: (id: string, data: any) => request.put(`/annotation-tasks/${id}`, data),
  remove: (id: string) => request.delete(`/annotation-tasks/${id}`),
  submitQc: (id: string, passed: number, total: number, comment = '') =>
    request.post(`/annotation-tasks/${id}/qc`, null, { params: { passed, total_qc: total, comment } })
}

// ---- 训练任务 ----
export const trainingApi = {
  list: (params: any) => request.get('/training-jobs', { params }),
  get: (id: string) => request.get(`/training-jobs/${id}`),
  create: (data: any) => request.post('/training-jobs', data),
  run: (id: string) => request.post(`/training-jobs/${id}/run`),
  cancel: (id: string) => request.post(`/training-jobs/${id}/cancel`),
  remove: (id: string) => request.delete(`/training-jobs/${id}`)
}

// ---- 模型版本 ----
export const modelApi = {
  list: (params: any) => request.get('/model-versions', { params }),
  get: (id: string) => request.get(`/model-versions/${id}`),
  create: (data: any) => request.post('/model-versions', data),
  update: (id: string, data: any) => request.put(`/model-versions/${id}`, data),
  release: (id: string) => request.post(`/model-versions/${id}/release`),
  remove: (id: string) => request.delete(`/model-versions/${id}`)
}

// ---- 部署 ----
export const deployApi = {
  list: (params: any) => request.get('/deploy-records', { params }),
  create: (data: any) => request.post('/deploy-records', data),
  update: (id: string, data: any) => request.put(`/deploy-records/${id}`, data),
  publish: (id: string) => request.post(`/deploy-records/${id}/publish`),
  rollback: (id: string) => request.post(`/deploy-records/${id}/rollback`),
  remove: (id: string) => request.delete(`/deploy-records/${id}`)
}

// ---- 审计 ----
export const auditApi = {
  list: (params: any) => request.get('/audit-logs', { params })
}
