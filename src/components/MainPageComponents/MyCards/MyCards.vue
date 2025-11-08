<template>
  <section :class="cls['my-cards']">
    <h2 :class="cls.mainTitle">My Cards</h2>
    <div :class="cls.cards">
      <div v-for="c in cards" :key="c.id"
        :class="[cls.card, c.id === selectedId ? cls['card--primary'] : cls['card--light']]" role="button"
        @click="$emit('select', c.id)">
        <div :class="cls.mainInfo">
          <div :class="cls.mainRow">
            <div :class="cls.row">
              <p :class="cls.label">BALANCE</p>
              <p :class="cls.value">{{ c.balance }}</p>
            </div>
            <img :class="[cls.chip, c.id === selectedId ? '' : cls['chip--muted']]"
              src="/src/shared/assets/images/icons/Chip.svg" alt="chip" />
          </div>
          <div :class="cls.mainRow">
            <div :class="cls.row">
              <p :class="cls.label">
                CARD HOLDER
              </p>
              <p :class="[cls.value, cls.valueSum]">
                {{ c.holder }}
              </p>
            </div>
            <div :class="cls.row">
              <p :class="cls.label">
                VALID THRU
              </p>
              <p :class="[cls.value, cls.valueSum]">
                {{ c.validThru }}
              </p>
            </div>
          </div>
        </div>
        <div :class="cls.block">
          <p :class="cls.number">
            {{ c.number }}
          </p>
        </div>
      </div>
    </div>

    <div v-if="totalPages > 1" :class="cls.dots">
      <button v-for="p in totalPages" :key="p" :class="[cls.dot, p === page ? cls['dot--active'] : '']"
        @click="$emit('changePage', p)" />
    </div>
  </section>
</template>

<script setup lang="ts">
import cls from './MyCards.module.css'
defineProps<{ cards: Array<any>, page: number, totalPages: number, selectedId: string }>()
defineEmits<{ (e: 'changePage', page: number): void, (e: 'select', id: string): void }>()
</script>

<style scoped></style>
