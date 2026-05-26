<template>
  <div class="page-container">
    <div class="card-wrap">
      <div class="toolbar">
        <el-input v-model="query.keyword" placeholder="项目名 / 负责人" style="width:220px" clearable @change="reload" prefix-icon="Search" />
        <el-select v-model="query.algorithm_type" placeholder="算法类型" clearable style="width:160px" @change="reload">
          <el-option v-for="i in ALGORITHM_TYPES" :key="i.value" :value="i.value" :label="i.label" />
        </el-select>
        <el-select v-model="query.status" placeholder="项目状态" clearable style="width:140px" @change="reload">
          <el-option v-for="i in PROJECT_STATUS" :key="i.value" :value="i.value" :label="i.label" />
        </el-select>
        <div class="right">
          <el-button type="primary" :icon="Plus" @click="onAdd">新建项目</el-button>
        </div>
      </div>

      <el-table :data="list" v-loading="loading" border stripe>
        <el-table-column prop="project_name" label="项目名称" min-width="180">
          <template #default="{ row }">
            <el-link type="primary" @click="goDetail(row.id)">{{ row.project_name }}</el-link>
          </template>
        </el-table-column>
        <el-table-column label="算法类型" width="130">
          <template #default="{ row }">
            <el-tag effect="dark" :color="getAlgoColor(row.algorithm_type)" style="border:none">
              {{ getLabel(ALGORITHM_TYPES, row.algorithm_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="项目状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getTag(PROJECT_STATUS, row.status).type as any" size="small">{{ getLabel(PROJECT_STATUS, row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="leader" label="负责人" width="100" />
        <el-table-column prop="scene_desc" label="应用场景" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="170">
          <template #default="{ row }">{{ fmt(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button link size="small" type="primary" @click="goDetail(row.id)">详情</el-button>
            <el-button link size="small" @click="onEdit(row)">编辑</el-button>
            <el-popconfirm title="确定删除？" @confirm="onDel(row)">
              <template #reference><el-button link size="small" type="danger">删除</el-button></template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        style="margin-top:12px; justify-content:flex-end"
        v-model:current-page="query.page" v-model:page-size="query.page_size"
        :total="total" :page-sizes="[10,20,50]"
        layout="total, sizes, prev, pager, next, jumper" @change="reload" />
    </div>

    <el-dialog v-model="dialog.visible" :title="dialog.title" width="560px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="项目名称" prop="project_name">
          <el-input v-model="form.project_name" />
        </el-form-item>
        <el-form-item label="算法类型" prop="algorithm_type">
          <el-select v-model="form.algorithm_type" style="width:100%">
            <el-option v-for="i in ALGORITHM_TYPES" :key="i.value" :value="i.value" :label="i.label" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目状态">
          <el-select v-model="form.status" style="width:100%">
            <el-option v-for="i in PROJECT_STATUS" :key="i.value" :value="i.value" :label="i.label" />
          </el-select>
        </el-form-item>
        <el-form-item label="负责人"><el-input v-model="form.leader" /></el-form-item>
        <el-form-item label="应用场景"><el-input v-model="form.scene_desc" type="textarea" :rows="2" /></el-form-item>
        <el-form-item label="备注"><el-input v-model="form.remark" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog.visible=false">取消</el-button>
        <el-button type="primary" @click="onSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { projectApi } from '@/api/modules'
import { ALGORITHM_TYPES, PROJECT_STATUS, getLabel, getTag } from '@/utils/dict'
import dayjs from 'dayjs'

const router = useRouter()
const loading = ref(false)
const list = ref<any[]>([])
const total = ref(0)
const query = reactive<any>({ page: 1, page_size: 10, keyword: '', algorithm_type: '', status: '' })

const formRef = ref<FormInstance>()
const dialog = reactive({ visible: false, title: '', mode: 'add' as 'add' | 'edit', id: '' })
const form = reactive<any>({ project_name: '', algorithm_type: 'detection', status: 'planning', leader: '', scene_desc: '', remark: '' })
const rules = {
  project_name: [{ required: true, message: '请输入项目名称' }],
  algorithm_type: [{ required: true, message: '请选择算法类型' }]
}

function fmt(t: string) { return t ? dayjs(t).format('YYYY-MM-DD HH:mm') : '' }
function getAlgoColor(v: string) { return ALGORITHM_TYPES.find(i => i.value === v)?.color || '#909399' }
function goDetail(id: string) { router.push(`/projects/${id}`) }

async function reload() {
  loading.value = true
  try {
    const params: any = { ...query }
    Object.keys(params).forEach(k => params[k] === '' && delete params[k])
    const res: any = await projectApi.list(params)
    list.value = res.data.list
    total.value = res.data.total
  } finally { loading.value = false }
}

function onAdd() {
  dialog.mode = 'add'; dialog.title = '新建项目'; dialog.visible = true; dialog.id = ''
  Object.assign(form, { project_name: '', algorithm_type: 'detection', status: 'planning', leader: '', scene_desc: '', remark: '' })
}
function onEdit(row: any) {
  dialog.mode = 'edit'; dialog.title = '编辑项目'; dialog.visible = true; dialog.id = row.id
  Object.assign(form, row)
}
async function onSubmit() {
  await formRef.value?.validate()
  if (dialog.mode === 'add') await projectApi.create(form)
  else await projectApi.update(dialog.id, form)
  ElMessage.success('保存成功')
  dialog.visible = false
  reload()
}
async function onDel(row: any) {
  await projectApi.remove(row.id)
  ElMessage.success('删除成功')
  reload()
}

onMounted(reload)
</script>
