<template>
  <div class="page-container">
    <div class="card-wrap">
      <div class="toolbar">
        <el-select v-model="query.project_id" placeholder="所属项目" clearable filterable style="width:240px" @change="reload">
          <el-option v-for="p in projects" :key="p.id" :value="p.id" :label="p.project_name" />
        </el-select>
        <el-input v-model="query.keyword" placeholder="数据集名称" style="width:200px" clearable @change="reload" prefix-icon="Search" />
        <div class="right"><el-button type="primary" :icon="Plus" @click="onAdd">新建数据集</el-button></div>
      </div>

      <el-table :data="list" v-loading="loading" border stripe>
        <el-table-column prop="dataset_name" label="数据集名称" min-width="180" />
        <el-table-column label="来源" width="120">
          <template #default="{ row }">{{ getLabel(SOURCE_TYPES, row.source_type) }}</template>
        </el-table-column>
        <el-table-column prop="sample_count" label="样本数" width="100" />
        <el-table-column prop="storage_path" label="存储路径" show-overflow-tooltip />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button link size="small" type="primary" @click="onVersion(row)">版本管理</el-button>
            <el-button link size="small" @click="onEdit(row)">编辑</el-button>
            <el-popconfirm title="确定删除？" @confirm="onDel(row)">
              <template #reference><el-button link size="small" type="danger">删除</el-button></template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination style="margin-top:12px; justify-content:flex-end"
        v-model:current-page="query.page" v-model:page-size="query.page_size"
        :total="total" :page-sizes="[10,20,50]"
        layout="total, sizes, prev, pager, next" @change="reload" />
    </div>

    <!-- 新增/编辑 -->
    <el-dialog v-model="dialog.visible" :title="dialog.title" width="560px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="所属项目" prop="project_id">
          <el-select v-model="form.project_id" filterable style="width:100%">
            <el-option v-for="p in projects" :key="p.id" :value="p.id" :label="p.project_name" />
          </el-select>
        </el-form-item>
        <el-form-item label="数据集名" prop="dataset_name"><el-input v-model="form.dataset_name" /></el-form-item>
        <el-form-item label="来源" prop="source_type">
          <el-select v-model="form.source_type" style="width:100%">
            <el-option v-for="i in SOURCE_TYPES" :key="i.value" :value="i.value" :label="i.label" />
          </el-select>
        </el-form-item>
        <el-form-item label="样本数"><el-input-number v-model="form.sample_count" :min="0" /></el-form-item>
        <el-form-item label="存储路径"><el-input v-model="form.storage_path" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog.visible=false">取消</el-button>
        <el-button type="primary" @click="onSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 版本管理 -->
    <el-dialog v-model="verDialog.visible" :title="`版本管理 - ${verDialog.dsName}`" width="780px">
      <el-button type="primary" size="small" :icon="Plus" @click="addVer">新建版本</el-button>
      <el-table :data="versions" size="small" style="margin-top:10px">
        <el-table-column prop="version_code" label="版本号" width="100" />
        <el-table-column prop="sample_count" label="样本数" width="90" />
        <el-table-column label="划分比例" width="160">
          <template #default="{ row }">{{ row.train_ratio }} / {{ row.val_ratio }} / {{ row.test_ratio }}</template>
        </el-table-column>
        <el-table-column label="冻结" width="80">
          <template #default="{ row }">
            <el-tag :type="row.frozen_flag ? 'success' : 'info'" size="small">{{ row.frozen_flag ? '已冻结' : '可变更' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="change_log" label="变更说明" show-overflow-tooltip />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button link size="small" :disabled="row.frozen_flag" @click="freeze(row)">冻结</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 新增版本 -->
    <el-dialog v-model="newVer.visible" title="新建数据版本" width="500px">
      <el-form :model="newVer.form" label-width="100px">
        <el-form-item label="版本号"><el-input v-model="newVer.form.version_code" placeholder="v1.0" /></el-form-item>
        <el-form-item label="样本数"><el-input-number v-model="newVer.form.sample_count" :min="0" /></el-form-item>
        <el-form-item label="训练比"><el-input-number v-model="newVer.form.train_ratio" :step="0.1" :min="0" :max="1" /></el-form-item>
        <el-form-item label="验证比"><el-input-number v-model="newVer.form.val_ratio" :step="0.1" :min="0" :max="1" /></el-form-item>
        <el-form-item label="测试比"><el-input-number v-model="newVer.form.test_ratio" :step="0.1" :min="0" :max="1" /></el-form-item>
        <el-form-item label="变更说明"><el-input v-model="newVer.form.change_log" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="newVer.visible=false">取消</el-button>
        <el-button type="primary" @click="submitVer">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, type FormInstance } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { datasetApi, projectApi } from '@/api/modules'
import { SOURCE_TYPES, getLabel } from '@/utils/dict'

const loading = ref(false)
const list = ref<any[]>([])
const total = ref(0)
const projects = ref<any[]>([])
const query = reactive<any>({ page: 1, page_size: 10, keyword: '', project_id: '' })

const formRef = ref<FormInstance>()
const dialog = reactive({ visible: false, title: '', mode: 'add' as 'add' | 'edit', id: '' })
const form = reactive<any>({ project_id: '', dataset_name: '', source_type: 'archive', sample_count: 0, storage_path: '', description: '' })
const rules = {
  project_id: [{ required: true, message: '请选择项目' }],
  dataset_name: [{ required: true, message: '请输入数据集名称' }]
}

const verDialog = reactive({ visible: false, dsId: '', dsName: '' })
const versions = ref<any[]>([])
const newVer = reactive({ visible: false, form: { version_code: '', sample_count: 0, train_ratio: 0.8, val_ratio: 0.1, test_ratio: 0.1, change_log: '' } as any })

async function loadProjects() {
  const res: any = await projectApi.list({ page: 1, page_size: 100 })
  projects.value = res.data.list
}

async function reload() {
  loading.value = true
  try {
    const params: any = { ...query }
    Object.keys(params).forEach(k => params[k] === '' && delete params[k])
    const res: any = await datasetApi.list(params)
    list.value = res.data.list
    total.value = res.data.total
  } finally { loading.value = false }
}

function onAdd() {
  dialog.mode = 'add'; dialog.title = '新建数据集'; dialog.visible = true; dialog.id = ''
  Object.assign(form, { project_id: projects.value[0]?.id || '', dataset_name: '', source_type: 'archive', sample_count: 0, storage_path: '', description: '' })
}
function onEdit(row: any) {
  dialog.mode = 'edit'; dialog.title = '编辑数据集'; dialog.visible = true; dialog.id = row.id
  Object.assign(form, row)
}
async function onSubmit() {
  await formRef.value?.validate()
  if (dialog.mode === 'add') await datasetApi.create(form)
  else await datasetApi.update(dialog.id, form)
  ElMessage.success('保存成功')
  dialog.visible = false
  reload()
}
async function onDel(row: any) {
  await datasetApi.remove(row.id); ElMessage.success('删除成功'); reload()
}

async function onVersion(row: any) {
  verDialog.visible = true; verDialog.dsId = row.id; verDialog.dsName = row.dataset_name
  const res: any = await datasetApi.versions(row.id)
  versions.value = res.data
}
function addVer() {
  newVer.visible = true
  newVer.form = { version_code: '', sample_count: 0, train_ratio: 0.8, val_ratio: 0.1, test_ratio: 0.1, change_log: '' }
}
async function submitVer() {
  await datasetApi.createVersion(verDialog.dsId, { ...newVer.form, dataset_id: verDialog.dsId })
  ElMessage.success('已新建版本'); newVer.visible = false
  const res: any = await datasetApi.versions(verDialog.dsId); versions.value = res.data
}
async function freeze(row: any) {
  await datasetApi.freezeVersion(row.id); ElMessage.success('已冻结')
  const res: any = await datasetApi.versions(verDialog.dsId); versions.value = res.data
}

onMounted(async () => { await loadProjects(); reload() })
</script>
