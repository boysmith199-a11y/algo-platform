<template>
  <div class="page-container" v-loading="loading">
    <div class="card-wrap" v-if="project">
      <div class="header-row">
        <div>
          <el-button link @click="$router.back()" :icon="ArrowLeft">返回</el-button>
          <h2 class="title">{{ project.project_name }}</h2>
          <div class="meta">
            <el-tag effect="dark" :color="algoColor" style="border:none; margin-right:8px">
              {{ getLabel(ALGORITHM_TYPES, project.algorithm_type) }}
            </el-tag>
            <el-tag :type="getTag(PROJECT_STATUS, project.status).type as any">{{ getLabel(PROJECT_STATUS, project.status) }}</el-tag>
            <span class="leader">负责人: {{ project.leader || '-' }}</span>
          </div>
        </div>
      </div>
      <el-descriptions :column="2" border style="margin-top:12px">
        <el-descriptions-item label="项目ID">{{ project.id }}</el-descriptions-item>
        <el-descriptions-item label="创建人">{{ project.created_by }}</el-descriptions-item>
        <el-descriptions-item label="应用场景" :span="2">{{ project.scene_desc || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ project.remark || '-' }}</el-descriptions-item>
      </el-descriptions>
    </div>

    <el-tabs v-model="tab" class="card-wrap" style="margin-top:16px">
      <el-tab-pane label="数据集" name="dataset">
        <el-table :data="datasets" size="small">
          <el-table-column prop="dataset_name" label="数据集" />
          <el-table-column prop="source_type" label="来源" width="120" />
          <el-table-column prop="sample_count" label="样本数" width="100" />
          <el-table-column prop="storage_path" label="存储路径" show-overflow-tooltip />
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="标注任务" name="anno">
        <el-table :data="annos" size="small">
          <el-table-column prop="task_name" label="任务名称" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="{ row }">
              <el-tag :type="getTag(ANNO_STATUS, row.status).type as any" size="small">{{ getLabel(ANNO_STATUS, row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="完成进度" width="200">
            <template #default="{ row }">
              <el-progress :percentage="row.total_count ? Math.round(row.finished_count / row.total_count * 100) : 0" />
            </template>
          </el-table-column>
          <el-table-column prop="assignee" label="责任人" width="100" />
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="训练任务" name="train">
        <el-table :data="trainings" size="small">
          <el-table-column prop="job_name" label="任务名称" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getTag(TRAINING_STATUS, row.status).type as any" size="small">{{ getLabel(TRAINING_STATUS, row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="进度" width="180">
            <template #default="{ row }"><el-progress :percentage="row.progress" /></template>
          </el-table-column>
          <el-table-column prop="node_name" label="节点" width="120" />
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="模型版本" name="model">
        <el-table :data="models" size="small">
          <el-table-column prop="model_name" label="模型名" />
          <el-table-column prop="version_code" label="版本" width="100" />
          <el-table-column prop="export_format" label="格式" width="100" />
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getTag(MODEL_STATUS, row.status).type as any" size="small">{{ getLabel(MODEL_STATUS, row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="release_note" label="发布说明" show-overflow-tooltip />
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="部署记录" name="deploy">
        <el-table :data="deploys" size="small">
          <el-table-column prop="endpoint_url" label="服务地址" show-overflow-tooltip />
          <el-table-column prop="deploy_type" label="部署方式" width="100" />
          <el-table-column prop="env_template" label="环境模板" show-overflow-tooltip />
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getTag(DEPLOY_STATUS, row.release_status).type as any" size="small">{{ getLabel(DEPLOY_STATUS, row.release_status) }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { projectApi, datasetApi, annotationApi, trainingApi, modelApi, deployApi } from '@/api/modules'
import { ALGORITHM_TYPES, PROJECT_STATUS, ANNO_STATUS, TRAINING_STATUS, MODEL_STATUS, DEPLOY_STATUS, getLabel, getTag } from '@/utils/dict'

const route = useRoute()
const id = route.params.id as string
const loading = ref(false)
const tab = ref('dataset')
const project = ref<any>(null)
const datasets = ref<any[]>([])
const annos = ref<any[]>([])
const trainings = ref<any[]>([])
const models = ref<any[]>([])
const deploys = ref<any[]>([])

const algoColor = computed(() => ALGORITHM_TYPES.find(i => i.value === project.value?.algorithm_type)?.color || '#909399')

async function load() {
  loading.value = true
  try {
    const [p, d, a, t, m, dp]: any = await Promise.all([
      projectApi.get(id),
      datasetApi.list({ project_id: id, page_size: 100 }),
      annotationApi.list({ project_id: id, page_size: 100 }),
      trainingApi.list({ project_id: id, page_size: 100 }),
      modelApi.list({ project_id: id, page_size: 100 }),
      deployApi.list({ project_id: id, page_size: 100 })
    ])
    project.value = p.data
    datasets.value = d.data.list
    annos.value = a.data.list
    trainings.value = t.data.list
    models.value = m.data.list
    deploys.value = dp.data.list
  } finally { loading.value = false }
}
onMounted(load)
</script>

<style scoped>
.header-row { display: flex; justify-content: space-between; align-items: flex-start; }
.title { margin: 6px 0; font-size: 22px; font-weight: 600; color: #1f2329; }
.meta { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.leader { margin-left: 12px; color: #8a8f99; font-size: 13px; }
</style>
