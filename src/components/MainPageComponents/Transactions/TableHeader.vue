<template>
  <div :class="cls.thead">
    <div :class="cls.headCell">
      <p :class="cls.headerText">Description</p>
    </div>
    <div :class="cls.headCell">
      <p :class="cls.headerText">Transaction ID</p>
    </div>
    <div :class="cls.headCell">
      <p :class="cls.headerText">Type</p>
    </div>
    <div :class="cls.headCell">
      <p :class="cls.headerText">Card</p>
    </div>
    <div :class="cls.headCell">
      <p :class="cls.headerText">Date</p>
    </div>
    <div :class="cls.headCell">
      <p :class="cls.headerText">Amount</p>
    </div>
    <div :class="[cls.headCell, cls.headCellLast]">
      <p :class="cls.headerText">Receipt</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import cls from './Transactions.module.css';
</script>

<style scoped></style>
