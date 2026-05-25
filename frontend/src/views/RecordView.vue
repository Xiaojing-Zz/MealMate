<template>
  <div class="record-page">
    <van-nav-bar title="记录饮食" />

    <van-form @submit="onSubmit" class="record-form">
      <!-- 用餐类型 -->
      <van-field name="mealType" label="用餐类型">
        <template #input>
          <van-radio-group v-model="form.mealType" direction="horizontal">
            <van-radio v-for="item in mealTypes" :key="item" :name="item">{{ item }}</van-radio>
          </van-radio-group>
        </template>
      </van-field>

      <!-- 菜品名称 -->
      <van-field
        v-model="form.dishName"
        label="菜品名称"
        placeholder="吃了什么？"
        :rules="[{ required: true, message: '请填写菜品名称' }]"
      />

      <!-- 地点 -->
      <van-field
        v-model="form.locationName"
        label="地点"
        placeholder="在哪里吃的？（选填）"
      />

      <!-- 花费 -->
      <van-field
        v-model="form.cost"
        label="花费"
        type="number"
        placeholder="花了多少钱？（选填）"
      >
        <template #button>
          <span style="color: #999">元</span>
        </template>
      </van-field>

      <!-- 热量 -->
      <van-field
        v-model="form.calories"
        label="热量"
        type="number"
        placeholder="大约多少千卡？（选填）"
      >
        <template #button>
          <span style="color: #999">千卡</span>
        </template>
      </van-field>

      <!-- 满意度 -->
      <van-field label="满意度">
        <template #input>
          <van-rate v-model="form.rating" />
        </template>
      </van-field>

      <!-- 用餐日期 -->
      <van-field
        v-model="form.mealDate"
        label="日期"
        readonly
        clickable
        @click="showDatePicker = true"
        placeholder="选择日期"
        :rules="[{ required: true, message: '请选择日期' }]"
      />

      <!-- 备注 -->
      <van-field
        v-model="form.note"
        label="备注"
        type="textarea"
        placeholder="随便记点什么..."
        :autosize="{ minHeight: 60 }"
      />

      <div class="submit-area">
        <van-button type="primary" round block native-type="submit" :loading="submitting">
          保存记录
        </van-button>
      </div>
    </van-form>

    <van-date-picker
      v-model:show="showDatePicker"
      :min-date="new Date(2024, 0, 1)"
      :max-date="new Date()"
      @confirm="onDateConfirm"
    />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { showToast, showSuccessToast } from 'vant'
import dayjs from 'dayjs'

const submitting = ref(false)
const showDatePicker = ref(false)

const mealTypes = ['早餐', '午餐', '晚餐', '下午茶', '夜宵']

const form = reactive({
  mealType: '午餐',
  dishName: '',
  locationName: '',
  cost: '',
  calories: '',
  rating: 3,
  mealDate: dayjs().format('YYYY-MM-DD'),
  note: '',
})

function onDateConfirm({ selectedValues }) {
  form.mealDate = selectedValues.join('-')
  showDatePicker.value = false
}

async function onSubmit() {
  submitting.value = true
  // 模拟提交
  await new Promise(r => setTimeout(r, 600))
  showSuccessToast('记录成功！')
  // 重置表单
  form.dishName = ''
  form.locationName = ''
  form.cost = ''
  form.calories = ''
  form.rating = 3
  form.note = ''
  submitting.value = false
}
</script>

<style scoped>
.record-page {
  min-height: 100vh;
  background: #f7f8fa;
}

.record-form {
  margin-top: 8px;
}

.submit-area {
  padding: 16px;
  margin-top: 8px;
}
</style>
