<template>
  <div class="app">
    <router-view />
    <van-tabbar v-model="active" route>
      <van-tabbar-item icon="fire-o" to="/recommend">推荐</van-tabbar-item>
      <van-tabbar-item icon="add-o" to="/record">记录</van-tabbar-item>
      <van-tabbar-item icon="clock-o" to="/history">历史</van-tabbar-item>
      <van-tabbar-item icon="chart-trending-o" to="/statistics">统计</van-tabbar-item>
      <van-tabbar-item icon="contact" to="/profile">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const active = ref(0)
</script>

<style scoped>
.app {
  padding-bottom: 50px;
}
</style>
