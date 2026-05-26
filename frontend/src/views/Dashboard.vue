<template>
  <div class="page-container">
    <el-row :gutter="16">
      <el-col :span="4" v-for="c in stats" :key="c.label">
        <div class="stat-card">
          <div class="label">
            <el-icon><component :is="c.icon" /></el-icon>
            {{ c.label }}
          </div>
          <div class="value" :style="{ color: c.color }">{{ c.value }}</div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top:16px">
      <el-col :span="8">
        <div class="card-wrap">
          <h3 class="block-title">按算法类型分布</h3>
          <div ref="algoChart" style="height:280px"></div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="card-wrap">
          <h3 class="block-title">项目状态分布</h3>
          <div ref="statusChart" style="height:280px"></div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="card-wrap">
          <h3 class="block-title">训练任务状态</h3>
          <div ref="trainChart" style="height:280px"></div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top:16px">
      <el-col :span="12">
        <div class="card-wrap">
          <h3 class="block-title">运行中 / 待启动训练任务</h3>
          <el-table :data="data?.recent_running_jobs || []" size="small">
            <el-table-column prop="name" label="任务名称" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'running' ? 'primary' : 'info'" size="small">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="进度" width="180">
              <template #default="{ row }">
                <el-progress :percentage="row.progress" :stroke-width="10" />
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="card-wrap">
          <h3 class="block-title">最近操作审计</h3>
          <el-table :data="data?.recent_audits || []" size="small" max-height="280">
            <el-table-column prop="username" label="用户" width="100" />
            <el-table-column prop="action" label="操作" width="90">
              <template #default="{ row }">
                <el-tag size="small" :type="auditColor(row.action)">{{ row.action }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="detail" label="详情" />
            <el-table-column prop="time" label="时间" width="180">
              <template #default="{ row }">{{ fmtTime(row.time) }}</template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, nextTick } from 'vue'
import * as echarts from 'echarts'
import { dashboardApi } from '@/api/modules'
import { ALGORITHM_TYPES, PROJECT_STATUS, getLabel } from '@/utils/dict'
import dayjs from 'dayjs'

const data = ref<any>(null)
const algoChart = ref<HTMLElement>()
const statusChart = ref<HTMLElement>()
const trainChart = ref<HTMLElement>()

const stats = computed(() => {
  const s = data.value?.stats || {}
  return [
    { label: '项目', value: s.projects ?? 0, icon: 'Folder', color: '#409eff' },
    { label: '数据集', value: s.datasets ?? 0, icon: 'Coin', color: '#67c23a' },
    { label: '标注任务', value: s.annotation_tasks ?? 0, icon: 'EditPen', color: '#e6a23c' },
    { label: '训练任务', value: s.training_jobs ?? 0, icon: 'DataAnalysis', color: '#f56c6c' },
    { label: '模型版本', value: s.models ?? 0, icon: 'Box', color: '#909399' },
    { label: '部署记录', value: s.deployments ?? 0, icon: 'Connection', color: '#1ec3a5' }
  ]
})

function fmtTime(t: string) { return t ? dayjs(t).format('MM-DD HH:mm:ss') : '' }
function auditColor(a: string) {
  const map: Record<string, any> = { create: 'success', update: '', delete: 'danger', login: 'info', release: 'success', publish: 'success' }
  return map[a] || ''
}

function renderPie(el: HTMLElement, title: string, dataMap: Record<string, number>, dict: any[]) {
  const chart = echarts.init(el)
  const series = Object.entries(dataMap).map(([k, v]) => ({
    name: getLabel(dict, k), value: v
  }))
  chart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0, left: 'center', textStyle: { fontSize: 11 } },
    series: [{
      type: 'pie', radius: ['45%', '70%'], avoidLabelOverlap: true,
      label: { show: true, formatter: '{b}\n{c}', fontSize: 11 },
      data: series.length ? series : [{ name: '暂无数据', value: 0 }]
    }]
  })
  window.addEventListener('resize', () => chart.resize())
}

function renderBar(el: HTMLElement, dataMap: Record<string, number>) {
  const chart = echarts.init(el)
  const labels = Object.keys(dataMap)
  const values = Object.values(dataMap)
  chart.setOption({
    tooltip: {},
    grid: { left: 30, right: 20, top: 20, bottom: 30 },
    xAxis: { type: 'category', data: labels, axisLabel: { fontSize: 11 } },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: values, itemStyle: { color: '#409eff', borderRadius: [4, 4, 0, 0] }, barWidth: 30 }]
  })
  window.addEventListener('resize', () => chart.resize())
}

async function load() {
  const res: any = await dashboardApi.overview()
  data.value = res.data
  await nextTick()
  if (algoChart.value) renderPie(algoChart.value, '算法类型', data.value.project_by_algo || {}, ALGORITHM_TYPES)
  if (statusChart.value) renderPie(statusChart.value, '项目状态', data.value.project_by_status || {}, PROJECT_STATUS)
  if (trainChart.value) renderBar(trainChart.value, data.value.training_status || {})
}

onMounted(load)
</script>

<style scoped>
.stat-card .label {
  display: flex; align-items: center; gap: 6px;
}
.block-title {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: #1f2329;
  border-left: 3px solid #409eff;
  padding-left: 8px;
}
</style>
