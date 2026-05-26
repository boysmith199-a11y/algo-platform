<template>
  <div class="page-container">
    <div class="card-wrap">
      <div class="toolbar">
        <el-select v-model="query.project_id" placeholder="所属项目" clearable filterable style="width:240px" @change="reload">
          <el-option v-for="p in projects" :key="p.id" :value="p.id" :label="p.project_name" />
        </el-select>
        <el-select v-model="query.status" placeholder="状态" clearable style="width:140px" @change="reload">
          <el-option v-for="i in TRAINING_STATUS" :key="i.value" :value="i.value" :label="i.label" />
        </el-select>
        <el-button :icon="Refresh" circle @click="reload" />
        <div class="right"><el-button type="primary" :icon="Plus" @click="onAdd">新建训练任务</el-button></div>
      </div>

      <el-table :data="list" v-loading="loading" border stripe>
        <el-table-column prop="job_name" label="任务名称" min-width="200" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getTag(TRAINING_STATUS, row.status).type as any" size="small">{{ getLabel(TRAINING_STATUS, row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="进度" width="200">
          <template #default="{ row }">
            <el-progress :percentage="row.progress" :status="row.status === 'success' ? 'success' : (row.status === 'failed' ? 'exception' : undefined)" />
          </template>
        </el-table-column>
        <el-table-column prop="node_name" label="节点" width="120" />
        <el-table-column label="关键指标" min-width="240">
          <template #default="{ row }">
            <div v-if="row.metric_json" style="font-size:12px;color:#606266">
              <template v-for="(v, k) in parseMetric(row.metric_json)" :key="k">
                <el-tag size="small" effect="plain" style="margin-right:4px">{{ k }}: {{ v }}</el-tag>
              </template>
            </div>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button link size="small" type="primary"
              :disabled="['running','success'].includes(row.status)" @click="onRun(row)">▶ 启动</el-button>
            <el-button link size="small" type="warning"
              :disabled="row.status !== 'running'" @click="onCancel(row)">取消</el-button>
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

    <el-dialog v-model="dialog.visible" title="新建训练任务" width="540px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="所属项目" prop="project_id">
          <el-select v-model="form.project_id" filterable style="width:100%">
            <el-option v-for="p in projects" :key="p.id" :value="p.id" :label="p.project_name" />
          </el-select>
        </el-form-item>
        <el-form-item label="任务名称" prop="job_name"><el-input v-model="form.job_name" /></el-form-item>
        <el-form-item label="GPU节点"><el-input v-model="form.node_name" placeholder="gpu-node-1" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog.visible=false">取消</el-button>
        <el-button type="primary" @click="onSubmit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage, type FormInstance } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import { trainingApi, projectApi } from '@/api/modules'
import { TRAINING_STATUS, getLabel, getTag } from '@/utils/dict'

const loading = ref(false)
const list = ref<any[]>([])
const total = ref(0)
const projects = ref<any[]>([])
const query = reactive<any>({ page: 1, page_size: 10, project_id: '', status: '' })

const formRef = ref<FormInstance>()
const dialog = reactive({ visible: false })
const form = reactive<any>({ project_id: '', job_name: '', node_name: 'gpu-node-1' })
const rules = { project_id: [{ required: true }], job_name: [{ required: true }] }

let timer: any = null

function parseMetric(s: string) { try { return JSON.parse(s) } catch { return {} } }

async function loadProjects() { const r: any = await projectApi.list({ page_size: 100 }); projects.value = r.data.list }

async function reload() {
  loading.value = true
  try {
    const params: any = { ...query }; Object.keys(params).forEach(k => params[k] === '' && delete params[k])
    const r: any = await trainingApi.list(params)
    list.value = r.data.list; total.value = r.data.total
  } finally { loading.value = false }
}

function onAdd() {
  dialog.visible = true
  Object.assign(form, { project_id: projects.value[0]?.id || '', job_name: `train-${Date.now().toString().slice(-6)}`, node_name: 'gpu-node-1' })
}
async function onSubmit() {
  await formRef.value?.validate()
  await trainingApi.create(form); ElMessage.success('已创建'); dialog.visible = false; reload()
}
async function onRun(row: any) { await trainingApi.run(row.id); ElMessage.success('任务已启动'); reload() }
async function onCancel(row: any) { await trainingApi.cancel(row.id); ElMessage.success('已取消'); reload() }
async function onDel(row: any) { await trainingApi.remove(row.id); ElMessage.success('已删除'); reload() }

onMounted(async () => {
  await loadProjects(); reload()
  // 自动轮询进度（每3秒）
  timer = setInterval(() => {
    if (list.value.some(i => i.status === 'running')) reload()
  }, 3000)
})
onBeforeUnmount(() => { if (timer) clearInterval(timer) })
</script>
