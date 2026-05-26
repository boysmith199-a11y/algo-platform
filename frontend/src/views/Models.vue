<template>
  <div class="page-container">
    <div class="card-wrap">
      <div class="toolbar">
        <el-select v-model="query.project_id" placeholder="所属项目" clearable filterable style="width:240px" @change="reload">
          <el-option v-for="p in projects" :key="p.id" :value="p.id" :label="p.project_name" />
        </el-select>
        <el-select v-model="query.status" placeholder="状态" clearable style="width:140px" @change="reload">
          <el-option v-for="i in MODEL_STATUS" :key="i.value" :value="i.value" :label="i.label" />
        </el-select>
        <div class="right"><el-button type="primary" :icon="Plus" @click="onAdd">登记模型</el-button></div>
      </div>
      <el-table :data="list" v-loading="loading" border stripe>
        <el-table-column prop="model_name" label="模型名称" min-width="180" />
        <el-table-column prop="version_code" label="版本" width="100" />
        <el-table-column label="格式" width="120">
          <template #default="{ row }">{{ getLabel(EXPORT_FORMATS, row.export_format) }}</template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getTag(MODEL_STATUS, row.status).type as any" size="small">{{ getLabel(MODEL_STATUS, row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="关键指标" min-width="260">
          <template #default="{ row }">
            <template v-for="(v, k) in parseMetric(row.metric_json)" :key="k">
              <el-tag size="small" effect="plain" style="margin-right:4px">{{ k }}: {{ v }}</el-tag>
            </template>
          </template>
        </el-table-column>
        <el-table-column prop="release_note" label="发布说明" show-overflow-tooltip />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button link size="small" type="success"
              :disabled="row.status === 'released'" @click="onRelease(row)">发布</el-button>
            <el-button link size="small" type="primary" @click="onDeploy(row)">部署</el-button>
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

    <el-dialog v-model="dialog.visible" title="登记模型版本" width="560px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="所属项目" prop="project_id">
          <el-select v-model="form.project_id" filterable style="width:100%">
            <el-option v-for="p in projects" :key="p.id" :value="p.id" :label="p.project_name" />
          </el-select>
        </el-form-item>
        <el-form-item label="模型名称" prop="model_name"><el-input v-model="form.model_name" /></el-form-item>
        <el-form-item label="版本号" prop="version_code"><el-input v-model="form.version_code" placeholder="v1.0.0" /></el-form-item>
        <el-form-item label="导出格式">
          <el-select v-model="form.export_format" style="width:100%">
            <el-option v-for="i in EXPORT_FORMATS" :key="i.value" :value="i.value" :label="i.label" />
          </el-select>
        </el-form-item>
        <el-form-item label="模型路径"><el-input v-model="form.artifact_path" /></el-form-item>
        <el-form-item label="发布说明"><el-input v-model="form.release_note" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog.visible=false">取消</el-button>
        <el-button type="primary" @click="onSubmit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { modelApi, projectApi, deployApi } from '@/api/modules'
import { MODEL_STATUS, EXPORT_FORMATS, getLabel, getTag } from '@/utils/dict'

const router = useRouter()
const loading = ref(false)
const list = ref<any[]>([])
const total = ref(0)
const projects = ref<any[]>([])
const query = reactive<any>({ page: 1, page_size: 10, project_id: '', status: '' })

const formRef = ref<FormInstance>()
const dialog = reactive({ visible: false })
const form = reactive<any>({ project_id: '', model_name: '', version_code: 'v1.0.0', export_format: 'pt', artifact_path: '', release_note: '' })
const rules = { project_id: [{ required: true }], model_name: [{ required: true }], version_code: [{ required: true }] }

function parseMetric(s: string) { try { return JSON.parse(s || '{}') } catch { return {} } }

async function loadProjects() { const r: any = await projectApi.list({ page_size: 100 }); projects.value = r.data.list }
async function reload() {
  loading.value = true
  try {
    const params: any = { ...query }; Object.keys(params).forEach(k => params[k] === '' && delete params[k])
    const r: any = await modelApi.list(params); list.value = r.data.list; total.value = r.data.total
  } finally { loading.value = false }
}

function onAdd() {
  dialog.visible = true
  Object.assign(form, { project_id: projects.value[0]?.id || '', model_name: '', version_code: 'v1.0.0', export_format: 'pt', artifact_path: '', release_note: '' })
}
async function onSubmit() {
  await formRef.value?.validate()
  await modelApi.create(form); ElMessage.success('已登记'); dialog.visible = false; reload()
}
async function onRelease(row: any) {
  await ElMessageBox.confirm(`确定将 ${row.model_name} ${row.version_code} 发布？`, '发布确认')
  await modelApi.release(row.id); ElMessage.success('已发布'); reload()
}
async function onDel(row: any) { await modelApi.remove(row.id); ElMessage.success('已删除'); reload() }

async function onDeploy(row: any) {
  await ElMessageBox.confirm(`将为 ${row.model_name}@${row.version_code} 创建部署记录`, '创建部署')
  await deployApi.create({
    project_id: row.project_id, model_version_id: row.id,
    env_template: 'CUDA11.8 + Python3.10', deploy_type: 'python',
    release_status: 'pending', release_note: `部署 ${row.model_name}@${row.version_code}`
  })
  ElMessage.success('已创建部署记录')
  router.push('/deployments')
}

onMounted(async () => { await loadProjects(); reload() })
</script>
