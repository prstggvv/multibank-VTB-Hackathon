<template>
  <section :class="cls.transactions">
    <h2 :class="cls['section-title']">Recent Transactions</h2>

    <Tabs :tab="tab" @change="$emit('changeTab', $event)" />

    <div :class="cls.table">
      <TableHeader />
      <TableBody :transactions="transactions" />
    </div>

    <Pagination :page="page" :totalPages="totalPages" @change="$emit('changePage', $event)" />
  </section>
</template>

<script setup lang="ts">
import cls from './Transactions.module.css'
import Tabs from './Tabs.vue'
import TableHeader from './TableHeader.vue'
import TableBody from './TableBody.vue'
import Pagination from './Pagination.vue'
defineProps<{
  transactions: Array<any>,
  page: number,
  totalPages: number,
  tab: 'bank' | 'all' | 'income' | 'expense',
}>()
defineEmits<{
  (e: 'changePage', page: number): void,
  (e: 'changeTab', tab: 'bank' | 'all' | 'income' | 'expense'): void
}>()
</script>

<style scoped></style>
