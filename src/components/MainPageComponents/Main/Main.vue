<template>
  <main :class="s.main">
    <MyCards :cards="cards" :page="page" :totalPages="totalPages" :selectedId="selectedId" @changePage="$emit('changePage', $event)" @select="$emit('select', $event)" />
    <Transactions :transactions="transactions" :page="txPage" :totalPages="txTotal" :tab="tab" @changePage="$emit('changeTxPage', $event)" @changeTab="$emit('changeTab', $event)" />
  </main>
</template>

<script setup lang="ts">
import MyCards from '../MyCards/MyCards.vue';
import Transactions from '../Transactions/Transactions.vue'
import s from './Main.module.css'
defineProps<{ cards: Array<any>, page: number, totalPages: number, selectedId: string, transactions: Array<any>, txPage: number, txTotal: number, tab: 'bank'|'all'|'income'|'expense' }>()
defineEmits<{(e:'changePage', page:number):void, (e:'select', id:string):void, (e:'changeTxPage', page:number):void, (e:'changeTab', tab:'bank'|'all'|'income'|'expense'):void}>()
</script>

<style scoped>
</style>


