<template>
  <div class="login-wrap">
    <div class="login-bg"></div>
    <div class="login-card">
      <div class="brand">
        <el-icon size="40" color="#409eff"><Cpu /></el-icon>
        <h2>算法研发管理平台</h2>
        <p class="subtitle">数据 · 标注 · 训练 · 验证 · 推理 · 部署 一体化</p>
      </div>
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top" @submit.prevent>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" size="large" prefix-icon="User" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" size="large" prefix-icon="Lock" show-password @keyup.enter="onLogin" />
        </el-form-item>
        <el-button type="primary" size="large" :loading="loading" class="btn-login" @click="onLogin">登 录</el-button>
      </el-form>

      <el-divider><span style="color:#909399; font-size:12px">演示账号（点击可填充）</span></el-divider>
      <div class="demo-accounts">
        <el-tag v-for="a in accounts" :key="a.u" @click="fill(a)" effect="plain" class="demo-tag">
          {{ a.u }} / {{ a.p }} <span class="role">[{{ a.r }}]</span>
        </el-tag>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const user = useUserStore()
const formRef = ref()
const loading = ref(false)
const form = reactive({ username: 'admin', password: 'Admin@123' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}
const accounts = [
  { u: 'admin', p: 'Admin@123', r: '管理员' },
  { u: 'alice', p: 'Alice@123', r: '算法工程师' },
  { u: 'bob', p: 'Bob@123', r: '标注员' },
  { u: 'carol', p: 'Carol@123', r: '审核员' },
  { u: 'viewer', p: 'Viewer@123', r: '访客' }
]

function fill(a: any) { form.username = a.u; form.password = a.p }

async function onLogin() {
  await formRef.value.validate()
  loading.value = true
  try {
    await user.login(form.username, form.password)
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  height: 100vh;
  display: flex; justify-content: center; align-items: center;
  position: relative;
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
}
.login-bg {
  position: absolute; inset: 0;
  background-image:
    radial-gradient(circle at 20% 30%, rgba(255,255,255,0.15) 0, transparent 35%),
    radial-gradient(circle at 80% 70%, rgba(255,255,255,0.10) 0, transparent 35%);
}
.login-card {
  width: 420px;
  background: #fff;
  border-radius: 12px;
  padding: 40px 36px 28px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.2);
  z-index: 1;
}
.brand { text-align: center; margin-bottom: 24px; }
.brand h2 { margin: 8px 0 4px; color: #1f2329; }
.subtitle { color: #8a8f99; font-size: 13px; margin: 0; }
.btn-login { width: 100%; height: 44px; font-size: 15px; }
.demo-accounts { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; }
.demo-tag { cursor: pointer; font-size: 12px; }
.demo-tag .role { color: #909399; margin-left: 2px; }
</style>
