// 业务字典与显示工具
export const ALGORITHM_TYPES = [
  { value: 'classification', label: '目标识别', color: '#409eff' },
  { value: 'detection', label: '目标检测', color: '#67c23a' },
  { value: 'segmentation', label: '目标分割', color: '#e6a23c' },
  { value: 'keypoint', label: '关键点回归', color: '#f56c6c' },
  { value: 'traditional', label: '传统算法', color: '#909399' },
  { value: 'other', label: '其它图像算法', color: '#b1b3b8' }
]

export const PROJECT_STATUS = [
  { value: 'planning', label: '资料梳理中', type: 'info' },
  { value: 'annotating', label: '标注中', type: 'warning' },
  { value: 'training', label: '训练中', type: 'primary' },
  { value: 'validating', label: '验证中', type: 'primary' },
  { value: 'deploying', label: '部署中', type: 'warning' },
  { value: 'online', label: '已上线', type: 'success' },
  { value: 'archived', label: '已归档', type: 'info' }
]

export const SOURCE_TYPES = [
  { value: 'realtime', label: '实时采集' },
  { value: 'archive', label: '存量归档' },
  { value: 'sensor', label: '传感器' },
  { value: 'opensource', label: '开源数据' },
  { value: 'simulation', label: '模拟仿真' },
  { value: 'purchase', label: '采购数据' }
]

export const TRAINING_STATUS = [
  { value: 'pending', label: '待启动', type: 'info' },
  { value: 'running', label: '运行中', type: 'primary' },
  { value: 'success', label: '成功', type: 'success' },
  { value: 'failed', label: '失败', type: 'danger' },
  { value: 'canceled', label: '已取消', type: 'info' }
]

export const ANNO_STATUS = [
  { value: 'pending', label: '待分配', type: 'info' },
  { value: 'running', label: '进行中', type: 'primary' },
  { value: 'qc', label: '待质检', type: 'warning' },
  { value: 'passed', label: '已通过', type: 'success' },
  { value: 'rework', label: '需返工', type: 'danger' },
  { value: 'closed', label: '已关闭', type: 'info' }
]

export const MODEL_STATUS = [
  { value: 'draft', label: '草稿', type: 'info' },
  { value: 'released', label: '已发布', type: 'success' },
  { value: 'deprecated', label: '已弃用', type: 'danger' }
]

export const DEPLOY_STATUS = [
  { value: 'pending', label: '待发布', type: 'info' },
  { value: 'deploying', label: '部署中', type: 'warning' },
  { value: 'online', label: '在线', type: 'success' },
  { value: 'failed', label: '失败', type: 'danger' },
  { value: 'rolled_back', label: '已回滚', type: 'info' }
]

export const EXPORT_FORMATS = [
  { value: 'pt', label: 'PyTorch (.pt)' },
  { value: 'onnx', label: 'ONNX' },
  { value: 'tensorrt', label: 'TensorRT' },
  { value: 'pb', label: 'TensorFlow (.pb)' },
  { value: 'coreml', label: 'CoreML' }
]

export function getLabel(dict: any[], value: string) {
  return dict.find(i => i.value === value)?.label || value
}

export function getTag(dict: any[], value: string) {
  return dict.find(i => i.value === value) || { label: value, type: '' }
}
