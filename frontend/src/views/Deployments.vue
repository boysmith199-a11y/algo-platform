<template>
  <div class="page-container">
    <div class="card-wrap">
      <div class="toolbar">
        <el-select v-model="query.project_id" placeholder="所属项目" clearable filterable style="width:240px" @change="reload">
          <el-option v-for="p in projects" :key="p.id" :value="p.id" :label="p.project_name" />
        </el-select>
        <el-button :icon="Refresh" circle @click="reload" />
      </div>

      <el-table :data="list" v-loading="loading" border stripe>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getTag(DEPLOY_STATUS, row.release_status).type as any" size="small">
              {{ getLabel(DEPLOY_STATUS, row.release_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="endpoint_url" label="服务地址" min-width="260" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link v-if="row.endpoint_url" type="primary" :href="row.endpoint_url" target="_blank">{{ row.endpoint_url }}</el-link>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="deploy_type" label="部署方式" width="110" />
        <el-table-column prop="env_template" label="环境模板" min-width="220" show-overflow-tooltip />
        <el-table-column prop="release_note" label="发布说明" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button link size="small" type="success"
              :disabled="row.release_status === 'online'" @click="onPublish(row)">发布上线</el-button>
            <el-button link size="small" type="warning"
              :disabled="row.release_status !== 'online'" @click="onRollback(row)">回滚</el-button>
            <el-popconfirm title="确定删除？" @confirm="onDel(row)">
              <template #reference><el-button link size="small" type="danger">删除</el-button></template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination style="margin-top:12px; justify-content:flex-end"
        v-model:current-page="query.page" v-model:page-size="query.page_size"
        :total="total" layout="total, sizes, prev, pager, next" @change="reload" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { deployApi, projectApi } from '@/api/modules'
import { DEPLOY_STATUS, getLabel, getTag } from '@/utils/dict'

const loading = ref(false)
const list = ref<any[]>([])
const total = ref(0)
const projects = ref<any[]>([])
const query = reactive<any>({ page: 1, page_size: 10, project_id: '' })

async function loadProjects() { const r: any = await projectApi.list({ page_size: 100 }); projects.value = r.data.list }
async function reload() {
  loading.value = true
  try {
    const params: any = { ...query }; Object.keys(params).forEach(k => params[k] === '' && delete params[k])
    const r: any = await deployApi.list(params); list.value = r.data.list; total.value = r.data.total
  } finally { loading.value = false }
}

async function onPublish(row: any) {
  await ElMessageBox.confirm('确定发布上线？此操作会创建对外服务地址', '发布确认', { type: 'warning' })
  await deployApi.publish(row.id); ElMessage.success('已上线'); reload()
}
async function onRollback(row: any) {
  await ElMessageBox.confirm('确定回滚？', '回滚确认', { type: 'warning' })
  await deployApi.rollback(row.id); ElMessage.success('已回滚'); reload()
}
async function onDel(row: any) { await deployApi.remove(row.id); ElMessage.success('已删除'); reload() }

onMounted(async () => { await loadProjects(); reload() })
</script>
