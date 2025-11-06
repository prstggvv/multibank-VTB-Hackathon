<template>
  <aside :class="cls.aside">
    <div :class="cls.card">
      <div :class="cls.imageWrapper">
        <div :class="cls.chip"></div>
      </div>
      <p :class="cls.title">V-BANK</p>
    </div>

    <button :class="cls.button" type="button" @click="onAddClick">+</button>
  </aside>
</template>

<script setup lang="ts">
import cls from './Aside.module.css'
const emit = defineEmits<{ (e: 'add'): void }>()
function onAddClick() { emit('add') }
</script>

<style scoped></style>
