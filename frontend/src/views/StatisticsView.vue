<template>
  <div class="statistics-page">
    <van-nav-bar title="统计分析" />

    <!-- 周期切换 -->
    <div class="period-selector">
      <van-button
        v-for="p in periods"
        :key="p.value"
        :type="period === p.value ? 'primary' : 'default'"
        size="small"
        @click="period = p.value"
      >
        {{ p.label }}
      </van-button>
    </div>

    <div class="charts-container">
      <!-- 本周花费趋势 -->
      <div class="chart-card">
        <h3>花费趋势</h3>
        <div class="chart-placeholder">
          <div class="bar-chart">
            <div v-for="(item, idx) in costData" :key="idx" class="bar-item">
              <div class="bar" :style="{ height: (item.cost / maxCost * 120) + 'px' }"></div>
              <span class="bar-label">{{ item.date }}</span>
              <span class="bar-value">¥{{ item.cost }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 品类分布 -->
      <div class="chart-card">
        <h3>品类分布</h3>
        <div class="pie-list">
          <div v-for="(item, idx) in categoryData" :key="idx" class="pie-item">
            <span class="pie-name">{{ item.cuisine }}</span>
            <van-progress :percentage="item.percentage" :color="pieColors[idx % pieColors.length]" />
            <span class="pie-value">{{ item.count }}次</span>
          </div>
        </div>
      </div>

      <!-- 常去地点TOP -->
      <div class="chart-card">
        <h3>常去地点 TOP</h3>
        <van-cell-group inset>
          <van-cell
            v-for="(item, idx) in locationData"
            :key="idx"
            :title="item.location_name"
            :value="item.visit_count + '次'"
            :label="'第' + (idx + 1) + '名'"
          />
        </van-cell-group>
      </div>

      <!-- 最爱菜品排行 -->
      <div class="chart-card">
        <h3>最爱菜品</h3>
        <van-cell-group inset>
          <van-cell
            v-for="(item, idx) in favoriteData"
            :key="idx"
            :title="item.dish_name"
            :value="'⭐ ' + item.avg_rating.toFixed(1)"
            :label="item.count + '次'"
          >
            <template #icon>
              <span class="rank-badge">{{ idx + 1 }}</span>
            </template>
          </van-cell>
        </van-cell-group>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const period = ref('week')

const periods = [
  { label: '本周', value: 'week' },
  { label: '本月', value: 'month' },
  { label: '自定义', value: 'custom' },
]

const pieColors = ['#1989fa', '#07c160', '#ff976a', '#ed4014', '#9c26b0']

// 模拟数据
const costData = [
  { date: '周一', cost: 45 },
  { date: '周二', cost: 68 },
  { date: '周三', cost: 32 },
  { date: '周四', cost: 55 },
  { date: '周五', cost: 82 },
  { date: '周六', cost: 120 },
  { date: '周日', cost: 95 },
]

const maxCost = computed(() => Math.max(...costData.map(i => i.cost)))

const categoryData = [
  { cuisine: '川菜', count: 5, percentage: 35 },
  { cuisine: '粤菜', count: 3, percentage: 21 },
  { cuisine: '日料', count: 2, percentage: 14 },
  { cuisine: '西餐', count: 2, percentage: 14 },
  { cuisine: '其他', count: 2, percentage: 16 },
]

const locationData = [
  { location_name: '川味小馆', visit_count: 5 },
  { location_name: '永和豆浆', visit_count: 3 },
  { location_name: '一兰拉面', visit_count: 2 },
]

const favoriteData = [
  { dish_name: '宫保鸡丁', avg_rating: 4.5, count: 3 },
  { dish_name: '日式拉面', avg_rating: 4.0, count: 2 },
  { dish_name: '煎饼果子', avg_rating: 3.5, count: 2 },
]
</script>

<style scoped>
.statistics-page {
  min-height: 100vh;
  background: #f7f8fa;
}

.period-selector {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  background: #fff;
}

.charts-container {
  padding: 8px 12px;
}

.chart-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
}

.chart-card h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.bar-chart {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 160px;
  padding-top: 10px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.bar {
  width: 24px;
  background: linear-gradient(180deg, #1989fa, #6190ea);
  border-radius: 4px 4px 0 0;
  transition: height 0.3s;
}

.bar-label {
  font-size: 11px;
  color: #999;
}

.bar-value {
  font-size: 11px;
  color: #666;
}

.pie-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.pie-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pie-name {
  width: 50px;
  font-size: 14px;
}

.pie-value {
  width: 40px;
  text-align: right;
  font-size: 13px;
  color: #999;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background: #1989fa;
  color: #fff;
  border-radius: 50%;
  font-size: 12px;
  margin-right: 8px;
}
</style>
