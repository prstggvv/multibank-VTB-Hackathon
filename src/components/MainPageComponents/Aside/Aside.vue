<template>
  <aside :class="cls.aside">
    <button v-for="bank in banks" :key="bank.id" type="button"
      :class="[cls.card, bank.id === selectedId ? cls.cardActive : '']" @click="$emit('select', bank.id)">
      <div :class="cls.imageWrapper">
        <div :class="cls.chip"></div>
      </div>
      <p :class="cls.title">{{ bank.name }}</p>
    </button>

    <button v-if="banks.length < maxBanks" :class="cls.addCard" type="button" @click="$emit('add')">+
    </button>
  </aside>
</template>

<script setup lang="ts">
import cls from './Aside.module.css'

interface BankItem {
  id: string
  name: string
}

defineProps<{ banks: BankItem[]; selectedId: string; maxBanks: number }>()
defineEmits<{ (e: 'add'): void; (e: 'select', id: string): void }>()
</script>

<style scoped></style>
