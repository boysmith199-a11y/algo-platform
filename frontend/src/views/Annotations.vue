<template>
  <div class="page-container">
    <div class="card-wrap">
      <div class="toolbar">
        <el-select v-model="query.project_id" placeholder="所属项目" clearable filterable style="width:240px" @change="reload">
          <el-option v-for="p in projects" :key="p.id" :value="p.id" :label="p.project_name" />
        </el-select>
        <el-select v-model="query.status" placeholder="状态" clearable style="width:140px" @change="reload">
          <el-option v-for="i in ANNO_STATUS" :key="i.value" :value="i.value" :label="i.label" />
        </el-select>
        <div class="right"><el-button type="primary" :icon="Plus" @click="onAdd">新建标注任务</el-button></div>
      </div>
      <el-table :data="list" v-loading="loading" border stripe>
        <el-table-column prop="task_name" label="任务名称" min-width="200" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getTag(ANNO_STATUS, row.status).type as any" size="small">{{ getLabel(ANNO_STATUS, row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="完成进度" width="200">
          <template #default="{ row }">
            <el-progress :percentage="row.total_count ? Math.round(row.finished_count / row.total_count * 100) : 0" />
            <span style="font-size:12px;color:#909399">{{ row.finished_count }}/{{ row.total_count }}</span>
          </template>
        </el-table-column>
        <el-table-column label="质检通过率" width="160">
          <template #default="{ row }">
            <span v-if="row.finished_count">{{ Math.round(row.qc_passed_count / row.finished_count * 100) }}%</span>
            <span v-else>-</span>
            <span style="font-size:12px;color:#909399; margin-left:6px">{{ row.qc_passed_count }}/{{ row.finished_count }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="assignee" label="责任人" width="100" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button link size="small" type="primary" @click="openQc(row)">提交质检</el-button>
            <el-button link size="small" @click="onEdit(row)">编辑</el-button>
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

    <el-dialog v-model="dialog.visible" :title="dialog.title" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="所属项目" prop="project_id">
          <el-select v-model="form.project_id" filterable style="width:100%">
            <el-option v-for="p in projects" :key="p.id" :value="p.id" :label="p.project_name" />
          </el-select>
        </el-form-item>
        <el-form-item label="任务名称" prop="task_name"><el-input v-model="form.task_name" /></el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status" style="width:100%">
            <el-option v-for="i in ANNO_STATUS" :key="i.value" :value="i.value" :label="i.label" />
          </el-select>
        </el-form-item>
        <el-form-item label="责任人"><el-input v-model="form.assignee" /></el-form-item>
        <el-form-item label="总样本数"><el-input-number v-model="form.total_count" :min="0" /></el-form-item>
        <el-form-item label="规范说明"><el-input v-model="form.spec_doc" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog.visible=false">取消</el-button>
        <el-button type="primary" @click="onSubmit">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="qcDialog.visible" title="提交质检结果" width="440px">
      <el-form label-width="100px">
        <el-form-item label="任务名称"><span>{{ qcDialog.taskName }}</span></el-form-item>
        <el-form-item label="质检数量"><el-input-number v-model="qcDialog.total" :min="0" /></el-form-item>
        <el-form-item label="通过数量"><el-input-number v-model="qcDialog.passed" :min="0" :max="qcDialog.total" /></el-form-item>
        <el-form-item label="备注"><el-input v-model="qcDialog.comment" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="qcDialog.visible=false">取消</el-button>
        <el-button type="primary" @click="submitQc">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, type FormInstance } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { annotationApi, projectApi } from '@/api/modules'
import { ANNO_STATUS, getLabel, getTag } from '@/utils/dict'

const loading = ref(false)
const list = ref<any[]>([])
const total = ref(0)
const projects = ref<any[]>([])
const query = reactive<any>({ page: 1, page_size: 10, project_id: '', status: '' })

const formRef = ref<FormInstance>()
const dialog = reactive({ visible: false, title: '', mode: 'add' as 'add' | 'edit', id: '' })
const form = reactive<any>({ project_id: '', task_name: '', assignee: '', total_count: 100, spec_doc: '', status: 'pending' })
const rules = { project_id: [{ required: true }], task_name: [{ required: true }] }

const qcDialog = reactive({ visible: false, id: '', taskName: '', total: 0, passed: 0, comment: '' })

async function loadProjects() { const res: any = await projectApi.list({ page_size: 100 }); projects.value = res.data.list }

async function reload() {
  loading.value = true
  try {
    const params: any = { ...query }; Object.keys(params).forEach(k => params[k] === '' && delete params[k])
    const res: any = await annotationApi.list(params)
    list.value = res.data.list; total.value = res.data.total
  } finally { loading.value = false }
}

function onAdd() {
  dialog.mode = 'add'; dialog.title = '新建标注任务'; dialog.visible = true; dialog.id = ''
  Object.assign(form, { project_id: projects.value[0]?.id || '', task_name: '', assignee: '', total_count: 100, spec_doc: '', status: 'pending' })
}
function onEdit(row: any) { dialog.mode = 'edit'; dialog.title = '编辑标注任务'; dialog.visible = true; dialog.id = row.id; Object.assign(form, row) }
async function onSubmit() {
  await formRef.value?.validate()
  if (dialog.mode === 'add') await annotationApi.create(form); else await annotationApi.update(dialog.id, form)
  ElMessage.success('保存成功'); dialog.visible = false; reload()
}
async function onDel(row: any) { await annotationApi.remove(row.id); ElMessage.success('删除成功'); reload() }

function openQc(row: any) {
  qcDialog.visible = true; qcDialog.id = row.id; qcDialog.taskName = row.task_name
  qcDialog.total = row.finished_count || row.total_count; qcDialog.passed = row.qc_passed_count || row.finished_count
  qcDialog.comment = ''
}
async function submitQc() {
  await annotationApi.submitQc(qcDialog.id, qcDialog.passed, qcDialog.total, qcDialog.comment)
  ElMessage.success('质检已提交'); qcDialog.visible = false; reload()
}

onMounted(async () => { await loadProjects(); reload() })
</script>
