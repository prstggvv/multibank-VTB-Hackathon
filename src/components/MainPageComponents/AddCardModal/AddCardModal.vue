<template>
  <div v-if="open" :class="cls.modalOverlay" @click.self="onClose">
    <div :class="cls.modal">
      <div :class="cls.modalTitle">Add new bank</div>
      <label :class="cls.modalRow">
        <span>Bank name</span>
        <input v-model.trim="local.name" :class="cls.modalInput" placeholder="Aurora Bank" />
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


