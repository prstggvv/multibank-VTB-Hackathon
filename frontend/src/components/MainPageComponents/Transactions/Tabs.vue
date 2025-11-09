<template>
  <div :class="cls.tabs">
    <button :class="[cls.tab, tab === 'bank' ? cls['tab--active'] : '']" type="button"
      @click="$emit('change', 'bank')">Bank accounts</button>
    <button :class="[cls.tab, tab === 'all' ? cls['tab--active'] : '']" type="button"
      @click="$emit('change', 'all')">All
      Transactions</button>
    <button :class="[cls.tab, tab === 'income' ? cls['tab--active'] : '']" type="button"
      @click="$emit('change', 'income')">Income</button>
    <button :class="[cls.tab, tab === 'expense' ? cls['tab--active'] : '']" type="button"
      @click="$emit('change', 'expense')">Expense</button>
  </div>
</template>

<script setup lang="ts">
import cls from './Transactions.module.css'
defineProps<{ tab: 'bank' | 'all' | 'income' | 'expense' }>()
defineEmits<{ (e: 'change', tab: 'bank' | 'all' | 'income' | 'expense'): void }>()
</script>

<style scoped></style>
