<template>
  <div v-if="open" :class="s.modalOverlay" @click.self="onClose">
    <div :class="s.modal">
      <div :class="s.modalTitle">Add new card</div>
      <label :class="s.modalRow">
        <span>Balance</span>
        <input v-model="local.balance" :class="s.modalInput" placeholder="$5,756" />
      </label>
      <label :class="s.modalRow">
        <span>Card holder</span>
        <input v-model="local.holder" :class="s.modalInput" placeholder="Eddy Cusuma" />
      </label>
      <label :class="s.modalRow">
        <span>Valid thru</span>
        <input v-model="local.validThru" :class="s.modalInput" placeholder="12/22" />
      </label>
      <label :class="s.modalRow">
        <span>Card number</span>
        <input v-model="local.number" :class="s.modalInput" placeholder="3778 **** **** 1234" />
      </label>
      <div :class="s.modalActions">
        <button :class="[s.btn, s.btnGhost]" @click="onClose">Cancel</button>
        <button :class="[s.btn, s.btnPrimary]" @click="onSubmit">Add</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import s from './AddCardModal.module.css'

type Card = {
  balance: string
  holder: string
  validThru: string
  number: string
  primary?: boolean
}

const props = defineProps<{ open: boolean }>()
const emit = defineEmits<{(e:'close'):void, (e:'submit', card: Card):void}>()

const empty: Card = { balance: '', holder: '', validThru: '', number: '', primary: false }
const local = reactive<Card>({ ...empty })

function onClose() { emit('close') }
function onSubmit() {
  if (!local.balance || !local.holder || !local.validThru || !local.number) return
  emit('submit', { ...local })
  Object.assign(local, empty)
}

watch(() => props.open, (v) => {
  if (!v) Object.assign(local, empty)
})
</script>

<style scoped>
</style>


