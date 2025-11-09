<template>
  <div :class="cls.pagination">
    <button :class="cls.link" type="button" @click="$emit('change', page - 1)">Предыдущая</button>
    <button v-for="p in totalPages" :key="p" :class="[cls.page, p === page ? cls['page--active'] : '']" type="button"
      @click="$emit('change', p)">{{ p }}</button>
    <button :class="cls.link" type="button" @click="$emit('change', page + 1)">Следующая</button>
  </div>
</template>

<script setup lang="ts">
import cls from './Transactions.module.css'
defineProps<{ page: number, totalPages: number }>()
defineEmits<{ (e: 'change', page: number): void }>()
</script>

<style scoped></style>
