<template>
  <div class="profile-page">
    <van-nav-bar title="个人中心" />

    <!-- 用户信息 -->
    <div class="user-card">
      <van-image round width="60" height="60" :src="avatar" />
      <div class="user-info">
        <h3>{{ nickname }}</h3>
        <span class="streak">已连续记录 {{ streak }} 天</span>
      </div>
    </div>

    <!-- 口味偏好 -->
    <van-cell-group inset title="口味偏好">
      <van-cell title="我的口味标签" is-link @click="showTastePicker = true">
        <template #value>
          <span v-if="tasteTags.length">{{ tasteTags.join('、') }}</span>
          <span v-else style="color: #ccc">未设置</span>
        </template>
      </van-cell>
    </van-cell-group>

    <!-- 数据管理 -->
    <van-cell-group inset title="数据管理">
      <van-cell title="导出数据" is-link @click="exportData" />
      <van-cell title="清除缓存" is-link @click="clearCache" />
    </van-cell-group>

    <!-- 关于 -->
    <van-cell-group inset title="关于">
      <van-cell title="版本" value="v0.1.0" />
      <van-cell title="反馈建议" is-link />
    </van-cell-group>

    <!-- 口味标签选择器 -->
    <van-popup v-model:show="showTastePicker" position="bottom" round>
      <div class="taste-picker">
        <h3>选择你的口味偏好</h3>
        <div class="taste-tags">
          <van-tag
            v-for="tag in allTasteTags"
            :key="tag"
            :type="tasteTags.includes(tag) ? 'primary' : 'default'"
            size="large"
            @click="toggleTaste(tag)"
          >
            {{ tag }}
          </van-tag>
        </div>
        <van-button type="primary" block round @click="showTastePicker = false" style="margin-top: 16px">
          确定
        </van-button>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { showToast, showConfirmDialog } from 'vant'

const nickname = ref('美食家')
const avatar = ref('https://picsum.photos/seed/avatar/100/100')
const streak = ref(7)
const showTastePicker = ref(false)

const tasteTags = ref(['辣', '下饭'])
const allTasteTags = ['辣', '不辣', '酸', '甜', '鲜', '清淡', '下饭', '低脂', '高蛋白', '素食']

function toggleTaste(tag) {
  const idx = tasteTags.value.indexOf(tag)
  if (idx > -1) {
    tasteTags.value.splice(idx, 1)
  } else {
    tasteTags.value.push(tag)
  }
}

function exportData() {
  showToast('数据导出功能开发中')
}

function clearCache() {
  showConfirmDialog({
    title: '提示',
    message: '确定要清除缓存吗？',
  }).then(() => {
    showToast('缓存已清除')
  }).catch(() => {})
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f7f8fa;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px 16px;
  background: linear-gradient(135deg, #1989fa, #6190ea);
  color: #fff;
}

.user-info h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}

.streak {
  font-size: 13px;
  opacity: 0.85;
}

.taste-picker {
  padding: 24px 16px;
}

.taste-picker h3 {
  font-size: 16px;
  margin-bottom: 16px;
  text-align: center;
}

.taste-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}
</style>
