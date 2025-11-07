<template>
  <div :class="cls.tbody">
    <TableRow v-for="t in transactions" :key="t.id" :item="t" />
  </div>
</template>

<script setup lang="ts">
import cls from './Transactions.module.css'
import TableRow from './TableRow.vue'
defineProps<{ transactions: Array<any> }>()
</script>

<style scoped>
</style>


