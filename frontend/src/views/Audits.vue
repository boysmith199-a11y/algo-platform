<template>
  <div class="page-container">
    <div class="card-wrap">
      <div class="toolbar">
        <el-select v-model="query.action" placeholder="操作类型" clearable style="width:160px" @change="reload">
          <el-option v-for="a in actions" :key="a" :value="a" :label="a" />
        </el-select>
        <el-select v-model="query.target_type" placeholder="资源类型" clearable style="width:180px" @change="reload">
          <el-option v-for="t in targets" :key="t" :value="t" :label="t" />
        </el-select>
        <el-button :icon="Refresh" circle @click="reload" />
      </div>

      <el-table :data="list" v-loading="loading" border stripe>
        <el-table-column prop="username" label="用户" width="120" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-tag size="small" :type="actionColor(row.action) as any">{{ row.action }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="target_type" label="资源类型" width="140" />
        <el-table-column prop="detail_json" label="详情" />
        <el-table-column prop="ip" label="IP" width="130" />
        <el-table-column prop="created_at" label="时间" width="180">
          <template #default="{ row }">{{ fmt(row.created_at) }}</template>
        </el-table-column>
      </el-table>
      <el-pagination style="margin-top:12px; justify-content:flex-end"
        v-model:current-page="query.page" v-model:page-size="query.page_size"
        :total="total" :page-sizes="[20,50,100]"
        layout="total, sizes, prev, pager, next" @change="reload" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import { auditApi } from '@/api/modules'
import dayjs from 'dayjs'

const loading = ref(false)
const list = ref<any[]>([])
const total = ref(0)
const query = reactive<any>({ page: 1, page_size: 20, action: '', target_type: '' })

const actions = ['login', 'logout', 'create', 'update', 'delete', 'run', 'cancel', 'qc', 'release', 'publish', 'rollback', 'freeze', 'init']
const targets = ['user', 'project', 'dataset', 'dataset_version', 'annotation_task', 'training_job', 'model_version', 'deploy_record', 'system']

function fmt(t: string) { return t ? dayjs(t).format('YYYY-MM-DD HH:mm:ss') : '' }
function actionColor(a: string) {
  const m: Record<string, string> = { create: 'success', delete: 'danger', release: 'success', publish: 'success', rollback: 'warning' }
  return m[a] || ''
}

async function reload() {
  loading.value = true
  try {
    const params: any = { ...query }; Object.keys(params).forEach(k => params[k] === '' && delete params[k])
    const r: any = await auditApi.list(params); list.value = r.data.list; total.value = r.data.total
  } finally { loading.value = false }
}

onMounted(reload)
</script>
