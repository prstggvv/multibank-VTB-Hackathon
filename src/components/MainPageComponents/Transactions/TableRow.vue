<template>
  <div :class="cls.row">
    <div :class="[cls.cell, cls.desc]">
      <div :class="cls.imageWrapper">
        <img :class="cls.dir" :style="item.amount > 0 ? 'transform: rotate(180deg)' : ''"
          src="/src/shared/assets/images/icons/arrow.svg" alt="dir" />
      </div>
      <p :class="cls.cellText">{{ item.description }}</p>
    </div>
    <div :class="cls.cell">
      <p :class="cls.cellText">#{{ item.id }}</p>
    </div>
    <div :class="cls.cell">
      <p :class="cls.cellText">{{ item.type }}</p>
    </div>
    <div :class="cls.cell">
      <p :class="cls.cellText">{{ item.card }}</p>
    </div>
    <div :class="cls.cell">
      <p :class="cls.cellText">
        {{ new Date(item.date).toLocaleString() }}
      </p>
    </div>
    <div :class="[cls.cell, cls.amount, item.amount > 0 ? cls['amount--pos'] : cls['amount--neg']]">
      <p :class="cls.cellText">
        {{ item.amount > 0 ? '+' : '-' }}${{ Math.abs(item.amount) }}
      </p>
    </div>
    <div :class="[cls.cell, cls.cellLast]">
      <button :class="cls['btn-outlined']" type="button">
        Скачать
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import cls from './Transactions.module.css'
defineProps<{
  item: {
    id: string,
    description: string,
    type: string,
    card: string,
    date: string,
    amount: number,
  }
}>()
</script>

<style scoped></style>
