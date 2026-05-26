<template>
  <el-container class="layout">
    <el-aside width="220px" class="aside">
      <div class="logo">
        <el-icon size="22"><Cpu /></el-icon>
        <span>算法研发管理平台</span>
      </div>
      <el-menu :default-active="route.path" router class="menu" background-color="#001529" text-color="#cfd6e0" active-text-color="#fff">
        <el-menu-item index="/dashboard"><el-icon><Odometer /></el-icon><span>工作台</span></el-menu-item>
        <el-menu-item index="/projects"><el-icon><Folder /></el-icon><span>项目管理</span></el-menu-item>
        <el-menu-item index="/datasets"><el-icon><Coin /></el-icon><span>数据集管理</span></el-menu-item>
        <el-menu-item index="/annotations"><el-icon><EditPen /></el-icon><span>标注任务</span></el-menu-item>
        <el-menu-item index="/trainings"><el-icon><DataAnalysis /></el-icon><span>训练任务</span></el-menu-item>
        <el-menu-item index="/models"><el-icon><Box /></el-icon><span>模型仓库</span></el-menu-item>
        <el-menu-item index="/deployments"><el-icon><Connection /></el-icon><span>部署记录</span></el-menu-item>
        <el-menu-item index="/audits"><el-icon><Document /></el-icon><span>审计日志</span></el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="bread">{{ (route.meta as any).title || '工作台' }}</div>
        <div class="user-area">
          <el-dropdown @command="onCmd">
            <span class="user-info">
              <el-avatar :size="28" style="background:#409eff">{{ initial }}</el-avatar>
              <span class="uname">{{ user.userInfo?.real_name || user.userInfo?.username }}</span>
              <el-tag size="small">{{ roleText }}</el-tag>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const user = useUserStore()

const roleMap: Record<string, string> = {
  admin: '超级管理员', pm: '项目管理员', engineer: '算法工程师',
  annotator: '标注员', reviewer: '审核员', viewer: '只读访客'
}
const roleText = computed(() => roleMap[user.userInfo?.role_code] || '用户')
const initial = computed(() => (user.userInfo?.real_name || user.userInfo?.username || '?')[0]?.toUpperCase())

async function onCmd(cmd: string) {
  if (cmd === 'logout') {
    await user.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.layout { height: 100vh; }
.aside {
  background: #001529;
  color: #fff;
  overflow-x: hidden;
}
.logo {
  height: 56px;
  display: flex; align-items: center; gap: 8px;
  padding: 0 16px;
  color: #fff;
  font-size: 15px; font-weight: 600;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.menu { border-right: none; }
.menu :deep(.el-menu-item.is-active) { background: #1890ff !important; }

.header {
  background: #fff;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 20px;
  border-bottom: 1px solid #eaecef;
}
.bread { font-size: 15px; font-weight: 500; color: #1f2329; }
.user-info {
  display: flex; align-items: center; gap: 8px; cursor: pointer;
}
.uname { font-size: 14px; color: #1f2329; }
.main { padding: 0; background: #f5f7fa; overflow: auto; }
</style>
