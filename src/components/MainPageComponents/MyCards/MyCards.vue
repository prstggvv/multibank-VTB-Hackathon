<template>
  <section :class="cls['my-cards']">
    <h2 :class="cls['section-title']">My Cards</h2>
    <div :class="cls.cards">
      <div v-for="(c, i) in cards" :key="i"
        :class="[cls.card, (c.id === selectedId || c.primary) ? cls['card--primary'] : cls['card--light']]"
        role="button" @click="$emit('select', c.id)">
        <div :class="cls['card__row']">
          <div>
            <div :class="cls.label">Balance</div>
            <div :class="cls.value">{{ c.balance }}</div>
          </div>
          <img :class="[cls.chip, !c.primary ? cls['chip--muted'] : '']" src="/src/shared/assets/images/icons/Chip.svg"
            alt="chip" />
        </div>
        <div :class="[cls['card__row'], cls['card__meta']]">
          <div>
            <div :class="cls.label">CARD HOLDER</div>
            <div :class="[cls.value, cls['value--sm']]">
              {{ c.holder }}
            </div>
          </div>
          <div>
            <div :class="cls.label">VALID THRU</div>
            <div :class="[cls.value, cls['value--sm']]">
              {{ c.validThru }}
            </div>
          </div>
        </div>
        <div :class="cls['card__number']">
          {{ c.number }}
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
