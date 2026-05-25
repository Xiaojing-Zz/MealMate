<template>
  <div class="history-page">
    <van-nav-bar title="历史回顾" />

    <!-- 切换视图 -->
    <van-tabs v-model:active="viewMode">
      <van-tab title="日历">
        <div class="calendar-view">
          <van-calendar
            :poppable="false"
            :show-confirm="false"
            :min-date="new Date(2024, 0, 1)"
            :max-date="new Date()"
            :style="{ height: '350px' }"
            @month-change="onMonthChange"
          />
          <div class="day-records" v-if="selectedDate">
            <h3>{{ selectedDate }} 的饮食记录</h3>
            <div v-if="dayRecords.length" class="record-list">
              <van-card
                v-for="record in dayRecords"
                :key="record.id"
                :title="record.dishName"
                :desc="record.locationName || '未知地点'"
              >
                <template #tags>
                  <van-tag type="primary">{{ record.mealType }}</van-tag>
                  <van-rate v-model="record.rating" :size="12" readonly />
                </template>
                <template #price>
                  <span v-if="record.cost">¥{{ record.cost }}</span>
                </template>
              </van-card>
            </div>
            <van-empty v-else description="这天没有记录" />
          </div>
        </div>
      </van-tab>

      <van-tab title="时间轴">
        <div class="timeline-view">
          <van-list
            v-model:loading="loading"
            :finished="finished"
            finished-text="没有更多了"
            @load="loadMore"
          >
            <div class="timeline">
              <div v-for="group in groupedRecords" :key="group.date" class="timeline-group">
                <div class="timeline-date">{{ group.date }}</div>
                <div v-for="record in group.records" :key="record.id" class="timeline-item">
                  <div class="timeline-dot"></div>
                  <div class="timeline-content">
                    <div class="record-header">
                      <span class="dish-name">{{ record.dishName }}</span>
                      <van-rate v-model="record.rating" :size="10" readonly />
                    </div>
                    <div class="record-meta">
                      <van-tag size="small" type="primary">{{ record.mealType }}</van-tag>
                      <span v-if="record.locationName" class="location">{{ record.locationName }}</span>
                      <span v-if="record.cost" class="cost">¥{{ record.cost }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </van-list>
        </div>
      </van-tab>
    </van-tabs>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const viewMode = ref(0)
const loading = ref(false)
const finished = ref(false)
const selectedDate = ref('')

// 模拟数据
const mockRecords = [
  { id: 1, dishName: '宫保鸡丁', mealType: '午餐', locationName: '川味小馆', cost: 28, rating: 4, mealDate: '2024-01-15' },
  { id: 2, dishName: '皮蛋瘦肉粥', mealType: '早餐', locationName: '永和豆浆', cost: 12, rating: 5, mealDate: '2024-01-15' },
  { id: 3, dishName: '日式拉面', mealType: '晚餐', locationName: '一兰拉面', cost: 58, rating: 4, mealDate: '2024-01-14' },
  { id: 4, dishName: '煎饼果子', mealType: '早餐', locationName: '街边小摊', cost: 8, rating: 3, mealDate: '2024-01-14' },
  { id: 5, dishName: '黄焖鸡米饭', mealType: '午餐', locationName: '杨铭宇', cost: 22, rating: 4, mealDate: '2024-01-13' },
]

const dayRecords = computed(() => {
  if (!selectedDate.value) return []
  return mockRecords.filter(r => r.mealDate === selectedDate.value)
})

const groupedRecords = computed(() => {
  const groups = {}
  mockRecords.forEach(r => {
    if (!groups[r.mealDate]) groups[r.mealDate] = { date: r.mealDate, records: [] }
    groups[r.mealDate].records.push(r)
  })
  return Object.values(groups).sort((a, b) => b.date.localeCompare(a.date))
})

function onMonthChange(date) {
  // 加载该月数据
}

function loadMore() {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    finished.value = true
  }, 500)
}
</script>

<style scoped>
.history-page {
  min-height: 100vh;
  background: #f7f8fa;
}

.day-records {
  padding: 12px 16px;
}

.day-records h3 {
  font-size: 16px;
  margin-bottom: 12px;
}

.record-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.timeline-view {
  padding: 16px;
}

.timeline-group {
  margin-bottom: 16px;
}

.timeline-date {
  font-size: 14px;
  color: #999;
  margin-bottom: 8px;
  padding-left: 16px;
}

.timeline-item {
  display: flex;
  align-items: flex-start;
  padding: 8px 0 8px 16px;
  border-left: 2px solid #e5e5e5;
  margin-left: 8px;
}

.timeline-dot {
  width: 10px;
  height: 10px;
  background: #1989fa;
  border-radius: 50%;
  margin-left: -21px;
  margin-right: 12px;
  margin-top: 4px;
  flex-shrink: 0;
}

.timeline-content {
  flex: 1;
  background: #fff;
  padding: 12px;
  border-radius: 8px;
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.dish-name {
  font-weight: 500;
  font-size: 15px;
}

.record-meta {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 13px;
  color: #999;
}

.location, .cost {
  font-size: 13px;
}
</style>
