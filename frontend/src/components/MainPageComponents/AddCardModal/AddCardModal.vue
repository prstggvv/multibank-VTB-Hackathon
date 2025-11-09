<template>
  <div v-if="open" :class="cls.modalOverlay" @click.self="onClose">
    <div :class="cls.modal">
      <div :class="cls.modalTitle">Add new bank</div>
      <label :class="cls.modalRow">
        <span>Bank name</span>
        <select v-model="local.name" :class="cls.modalInput">
          <option value="" disabled>Select a bank</option>
          <option value="vbank">VBank</option>
          <option value="abank">Abank</option>
          <option value="sbank">Sbank</option>
        </select>
      </label>
      <div :class="cls.modalActions">
        <button :class="[cls.btn, cls.btnGhost]" @click="onClose">Cancel</button>
        <button :class="[cls.btn, cls.btnPrimary]" @click="onSubmit">Add</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import cls from './AddCardModal.module.css'
import { useRootStore } from '../../../stores/root';
const rootStore = useRootStore();

interface BankPayload {
  name: string
}

const props = defineProps<{ open: boolean }>()
const emit = defineEmits<{ (e: 'close'): void; (e: 'submit', bank: BankPayload): void }>()

const empty: BankPayload = { name: '' }
const local = reactive<BankPayload>({ ...empty })

function onClose() { emit('close') }
function onSubmit() {
  if (!local.name) return
  emit('submit', { ...local })
  Object.assign(local, empty)
}

watch(() => props.open, (value) => {
  if (!value) Object.assign(local, empty)
})
</script>

<style scoped>
</style>