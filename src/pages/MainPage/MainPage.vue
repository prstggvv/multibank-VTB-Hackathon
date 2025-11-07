<template>
  <div :class="cls.main">
    <div :class="cls.container">
      <Header />
      <div :class="cls.layout">
        <Aside :banks="banks" :selected-id="selectedBankId" :max-banks="MAX_BANKS" @add="openAddModal"
          @select="selectBank" />
        <Main :cards="visibleCards" :page="currentPage" :totalPages="totalPages" :selectedId="selectedCardId"
          :transactions="visibleTransactions" :txPage="txPage" :txTotal="txTotal" :tab="tab" @changePage="setPage"
          @select="selectCard" @changeTxPage="setTxPage" @changeTab="setTab" />
      </div>
    </div>
  </div>
  <AddCardModal :open="isModalOpen" @close="closeModal" @submit="onSubmitBank" />
</template>

<script setup lang="ts">
import Header from '../../components/MainPageComponents/Header/Header.vue';
import Aside from '../../components/MainPageComponents/Aside/Aside.vue';
import Main from '../../components/MainPageComponents/Main/Main.vue';
import AddCardModal from '../../components/MainPageComponents/AddCardModal/AddCardModal.vue';
import cls from './MainPage.module.css'

import { computed, ref, watch } from 'vue'
import cardsData from '../../shared/lib/data/cards.json'

interface Transaction {
  id: string
  description: string
  type: string
  card: string
  date: string
  amount: number
}

interface Card {
  id: string
  balance: string
  holder: string
  validThru: string
  number: string
  primary?: boolean
  transactions: Transaction[]
}

interface Bank {
  id: string
  name: string
  cards: Card[]
}

const MAX_BANKS = 3
const banks = ref<Bank[]>((cardsData as { banks: Bank[] }).banks.slice(0, MAX_BANKS))
const selectedBankId = ref<string>(banks.value[0]?.id ?? '')

const perPage = 3
const currentPage = ref(1)

const currentBankCards = computed<Card[]>(() => {
  const bank = banks.value.find((item) => item.id === selectedBankId.value)
  return bank ? bank.cards : []
})

const totalPages = computed(() => Math.max(1, Math.ceil(currentBankCards.value.length / perPage)))
const visibleCards = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return currentBankCards.value.slice(start, start + perPage)
})

const selectedCardId = ref<string>(currentBankCards.value[0]?.id ?? '')

watch(currentBankCards, (value) => {
  const firstCard = value[0]
  if (!firstCard) {
    selectedCardId.value = ''
    return
  }
  if (!value.some((card) => card.id === selectedCardId.value)) {
    selectedCardId.value = firstCard.id
  }
})

watch(selectedBankId, () => {
  currentPage.value = 1
  const firstCard = currentBankCards.value[0]
  selectedCardId.value = firstCard ? firstCard.id : ''
  tab.value = 'bank'
  txPage.value = 1
})

watch(currentPage, () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value
  }
})

function setPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    const nextCard = visibleCards.value[0]
    if (nextCard) {
      selectedCardId.value = nextCard.id
    }
  }
}

function selectCard(id: string) {
  if (!currentBankCards.value.some((card) => card.id === id)) return
  selectedCardId.value = id
  txPage.value = 1
}

function selectBank(id: string) {
  if (id === selectedBankId.value) return
  selectedBankId.value = id
}

// Transactions logic
const tab = ref<'bank' | 'all' | 'income' | 'expense'>('bank')
const txPage = ref(1)
const txPerPage = 5

const filteredTransactions = computed<Transaction[]>(() => {
  const cards = currentBankCards.value
  if (!cards.length) {
    return []
  }

  if (tab.value === 'bank') {
    const target = cards.find((card) => card.id === selectedCardId.value)
    return target
      ? [...target.transactions].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
      : []
  }

  if (tab.value === 'all') {
    return cards.flatMap((card) => card.transactions)
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
  }

  if (tab.value === 'income') {
    return cards
      .flatMap((card) => card.transactions)
      .filter((transaction) => transaction.amount > 0)
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
  }

  return cards
    .flatMap((card) => card.transactions)
    .filter((transaction) => transaction.amount < 0)
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
})

const txTotal = computed(() => Math.max(1, Math.ceil(filteredTransactions.value.length / txPerPage)))
const visibleTransactions = computed(() => {
  const start = (txPage.value - 1) * txPerPage
  return filteredTransactions.value.slice(start, start + txPerPage)
})

function setTxPage(page: number) {
  if (page >= 1 && page <= txTotal.value) {
    txPage.value = page
  }
}

function setTab(next: 'bank' | 'all' | 'income' | 'expense') {
  tab.value = next
  txPage.value = 1
}

// Modal state and handlers
const isModalOpen = ref(false)

function openAddModal() {
  if (banks.value.length >= MAX_BANKS) return
  isModalOpen.value = true
}

function closeModal() {
  isModalOpen.value = false
}

function onSubmitBank(payload: { name: string }) {
  if (!payload.name || banks.value.length >= MAX_BANKS) {
    isModalOpen.value = false
    return
  }

  const newBank: Bank = {
    id: `bank-${Date.now()}`,
    name: payload.name,
    cards: []
  }

  banks.value.push(newBank)
  selectedBankId.value = newBank.id
  currentPage.value = 1
  isModalOpen.value = false
}
</script>

<style scoped></style>