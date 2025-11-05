<template>
  <div :class="cls.main">
    <div :class="cls.container">
      <Header />
      <div :class="cls.layout">
        <Aside @add="openAddModal" />
        <Main :cards="visibleCards" :page="currentPage" :totalPages="totalPages" :selectedId="selectedCardId"
          :transactions="visibleTransactions" :txPage="txPage" :txTotal="txTotal" :tab="tab" @changePage="setPage"
          @select="selectCard" @changeTxPage="setTxPage" @changeTab="setTab" />
      </div>
    </div>
  </div>
  <AddCardModal :open="isModalOpen" @close="closeModal" @submit="onSubmitCard" />
</template>

<script setup lang="ts">
import Header from '../../components/MainPageComponents/Header/Header.vue';
import Aside from '../../components/MainPageComponents/Aside/Aside.vue';
import Main from '../../components/MainPageComponents/Main/Main.vue';
import AddCardModal from '../../components/MainPageComponents/AddCardModal/AddCardModal.vue';
import cls from './MainPage.module.css'

import { ref, computed } from 'vue'
import cardsData from '../../shared/lib/data/cards.json'

type Card = {
  balance: string
  holder: string
  validThru: string
  number: string
  primary?: boolean
}

type Tx = {
  id: string,
  description: string,
  type: string,
  card: string,
  date: string,
  amount: number
}
const cards = ref<any[]>((cardsData as any).cards)
const selectedCardId = ref<string>(cards.value[0]?.id || '')

const perPage = 3
const currentPage = ref(1)
const totalPages = computed(() => Math.max(1, Math.ceil(cards.value.length / perPage)))
const visibleCards = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return cards.value.slice(start, start + perPage)
})

function setPage(p: number) {
  if (p >= 1 && p <= totalPages.value) currentPage.value = p
}

function selectCard(id: string) {
  selectedCardId.value = id
}

// Transactions logic
const tab = ref<'bank' | 'all' | 'income' | 'expense'>('bank')
const txPage = ref(1);
const txPerPage = 5;
const filteredTransactions = computed<Tx[]>(() => {
  let all: Tx[] = [];

  if (tab.value === 'bank') {
    const target = cards.value.find(c => c.id === selectedCardId.value)
    all = target ? target.transactions : []
  } else if (tab.value === 'all') {
    all = cards.value.flatMap(c => c.transactions)
  } else if (tab.value === 'income') {
    all = cards.value.flatMap(c => c.transactions).filter(t => t.amount > 0)
  } else if (tab.value === 'expense') {
    all = cards.value.flatMap(c => c.transactions).filter(t => t.amount < 0)
  }
  return all.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
})

const txTotal = computed(() => Math.max(1, Math.ceil(filteredTransactions.value.length / txPerPage)))
const visibleTransactions = computed(() => {
  const start = (txPage.value - 1) * txPerPage
  return filteredTransactions.value.slice(start, start + txPerPage)
})

function setTxPage(p: number) {
  if (p >= 1 && p <= txTotal.value) txPage.value = p

}
function setTab(t: 'bank' | 'all' | 'income' | 'expense') {
  tab.value = t; txPage.value = 1
}

// Modal state and handlers
const isModalOpen = ref(false)
function openAddModal() { isModalOpen.value = true }
function closeModal() { isModalOpen.value = false }
function onSubmitCard(card: Card) {
  cards.value.push({ ...card })
  isModalOpen.value = false
  currentPage.value = totalPages.value
}
</script>

<style scoped></style>