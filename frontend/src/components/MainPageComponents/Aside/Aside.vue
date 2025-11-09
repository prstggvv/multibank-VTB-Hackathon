<template>
  <aside :class="cls.aside">
    <button v-for="bank, index in banks" :key="index" type="button"
      :class="[cls.card, bank.id === selectedId ? cls.cardActive : '']" @click="setActive(bank.name)">
      <div :class="cls.imageWrapper">
        <div :class="cls.chip"></div>
      </div>
      <p :class="cls.title">{{ bank.name }}</p>
    </button>

    <button v-if="banks.length < 3" :class="cls.addCard" type="button" @click="$emit('add')">+
    </button>
  </aside>
</template>

<script setup>
import cls from './Aside.module.css'
import { useRootStore } from '../../../stores/root'
import { onMounted, computed,ref } from 'vue';
const rootStore = useRootStore();

const banks = computed(() => rootStore.getBanks);
const activeBank = ref('');

const setActive = (bank) => {
  activeBank.value = bank;
  
}


defineEmits(['add']);


onMounted(async () => {
  await rootStore.setBanks();
})
</script>

<style scoped></style>
