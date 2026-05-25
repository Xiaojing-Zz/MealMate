<template>
  <div class="recommend-page">
    <van-nav-bar title="今天吃什么" />

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <van-dropdown-menu>
        <van-dropdown-item v-model="filters.taste" :options="tasteOptions" />
        <van-dropdown-item v-model="filters.cuisine" :options="cuisineOptions" />
        <van-dropdown-item v-model="filters.priceRange" :options="priceOptions" />
      </van-dropdown-menu>
    </div>

    <!-- 场景快捷入口 -->
    <div class="quick-scenarios">
      <van-button size="small" type="primary" plain @click="quickRecommend('hungry')">我超饿</van-button>
      <van-button size="small" type="primary" plain @click="quickRecommend('casual')">随便就行</van-button>
      <van-button size="small" type="primary" plain @click="quickRecommend('fridge')">清理冰箱</van-button>
    </div>

    <!-- 推荐结果卡片 -->
    <div class="result-card" v-if="result">
      <div class="dish-image">
        <van-image :src="result.dish.image_url || defaultImage" fit="cover" radius="12" />
      </div>
      <div class="dish-info">
        <h2 class="dish-name">{{ result.dish.name }}</h2>
        <div class="dish-meta">
          <van-tag v-if="result.dish.cuisine" type="primary">{{ result.dish.cuisine }}</van-tag>
          <van-tag v-for="tag in (result.dish.tags || [])" :key="tag" plain type="success">{{ tag }}</van-tag>
        </div>
        <div class="dish-details">
          <span v-if="result.dish.reference_price">¥{{ result.dish.reference_price }}</span>
          <span v-if="result.dish.calories">{{ result.dish.calories }}千卡</span>
          <span v-if="result.dish.prep_time">{{ result.dish.prep_time }}分钟</span>
        </div>
        <p class="recommend-reason">{{ result.reason }}</p>
      </div>
      <div class="action-buttons">
        <van-button type="primary" block @click="goRecord">就吃这个！去记录</van-button>
        <van-button plain block @click="recommend" style="margin-top: 8px">换一个</van-button>
      </div>
    </div>

    <!-- 空状态 -->
    <div class="empty-state" v-else>
      <van-empty description="点击下方按钮，帮你决定吃什么">
        <van-button type="primary" round @click="recommend" :loading="loading">
          随机一下
        </van-button>
      </van-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { showToast } from 'vant'

const loading = ref(false)
const result = ref(null)
const defaultImage = 'https://picsum.photos/seed/food/400/300'

const filters = reactive({
  taste: '',
  cuisine: '',
  priceRange: '',
})

const tasteOptions = [
  { text: '口味', value: '' },
  { text: '辣', value: '辣' },
  { text: '不辣', value: '不辣' },
  { text: '酸', value: '酸' },
  { text: '甜', value: '甜' },
  { text: '鲜', value: '鲜' },
]

const cuisineOptions = [
  { text: '菜系', value: '' },
  { text: '川菜', value: '川菜' },
  { text: '粤菜', value: '粤菜' },
  { text: '湘菜', value: '湘菜' },
  { text: '日料', value: '日料' },
  { text: '西餐', value: '西餐' },
  { text: '东南亚', value: '东南亚' },
]

const priceOptions = [
  { text: '价格', value: '' },
  { text: '¥20以下', value: '¥20以下' },
  { text: '¥20-50', value: '¥20-50' },
  { text: '¥50-100', value: '¥50-100' },
]

// 模拟推荐（后续替换为真实API调用）
const mockDishes = [
  { id: 1, name: '宫保鸡丁', cuisine: '川菜', tags: ['辣', '下饭'], reference_price: 28, calories: 450, prep_time: 20, image_url: 'https://picsum.photos/seed/kungpao/400/300' },
  { id: 2, name: '白切鸡', cuisine: '粤菜', tags: ['清淡', '鲜'], reference_price: 45, calories: 320, prep_time: 30, image_url: 'https://picsum.photos/seed/chicken/400/300' },
  { id: 3, name: '日式咖喱饭', cuisine: '日料', tags: ['微辣', '快捷'], reference_price: 35, calories: 580, prep_time: 25, image_url: 'https://picsum.photos/seed/curry/400/300' },
  { id: 4, name: '番茄牛腩', cuisine: '粤菜', tags: ['酸甜', '营养'], reference_price: 55, calories: 520, prep_time: 40, image_url: 'https://picsum.photos/seed/beef/400/300' },
  { id: 5, name: '冬阴功汤', cuisine: '东南亚', tags: ['酸辣', '鲜'], reference_price: 38, calories: 280, prep_time: 20, image_url: 'https://picsum.photos/seed/tomyum/400/300' },
]

const reasons = [
  '今天天气适合来点这个！',
  '你已经好久没吃这个了',
  '根据你的口味偏好推荐',
  '营养均衡的好选择',
  '大家都说这家很好吃',
]

async function recommend() {
  loading.value = true
  // 模拟API延迟
  await new Promise(r => setTimeout(r, 800))
  const dish = mockDishes[Math.floor(Math.random() * mockDishes.length)]
  result.value = {
    dish,
    reason: reasons[Math.floor(Math.random() * reasons.length)],
  }
  loading.value = false
}

function quickRecommend(scenario) {
  recommend()
}

function goRecord() {
  showToast('跳转到记录页')
}
</script>

<style scoped>
.recommend-page {
  min-height: 100vh;
  background: #f7f8fa;
}

.filter-bar {
  background: #fff;
}

.quick-scenarios {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  background: #fff;
  margin-bottom: 8px;
}

.result-card {
  margin: 12px;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
}

.dish-image {
  height: 200px;
}

.dish-info {
  padding: 16px;
}

.dish-name {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 8px;
}

.dish-meta {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.dish-details {
  display: flex;
  gap: 16px;
  color: #999;
  font-size: 14px;
  margin-bottom: 12px;
}

.recommend-reason {
  color: #666;
  font-size: 14px;
  padding: 8px 12px;
  background: #f5f5f5;
  border-radius: 8px;
}

.action-buttons {
  padding: 0 16px 16px;
}

.empty-state {
  padding-top: 60px;
}
</style>
