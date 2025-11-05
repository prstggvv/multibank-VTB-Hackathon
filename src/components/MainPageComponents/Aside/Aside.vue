<template>
  <aside :class="s.aside">
    <div :class="s['bank-card']">
      <div :class="s['bank-card__header']">
        <img :class="s['bank-card__icon']" src="/src/shared/assets/images/icons/Logo.svg" alt="bank" />
        <span :class="s['bank-card__chip']"></span>
      </div>
      <div :class="s['bank-card__title']">V-BANK</div>
    </div>

    <button :class="s['add-card']" type="button" @click="onAddClick">+</button>
  </aside>
 </template>

<script setup lang="ts">
import s from './Aside.module.css'
const emit = defineEmits<{(e:'add'):void}>()
function onAddClick() { emit('add') }
</script>

<style scoped>
</style>


