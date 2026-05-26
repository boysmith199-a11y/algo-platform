import { defineStore } from 'pinia'
import { authApi } from '@/api/modules'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    userInfo: JSON.parse(localStorage.getItem('user_info') || 'null') as any
  }),
  actions: {
    async login(username: string, password: string) {
      const res: any = await authApi.login(username, password)
      this.token = res.data.access_token
      this.userInfo = res.data.user_info
      localStorage.setItem('access_token', this.token)
      localStorage.setItem('user_info', JSON.stringify(this.userInfo))
      return res
    },
    async logout() {
      try { await authApi.logout() } catch (e) { /* ignore */ }
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_info')
    }
  }
})
