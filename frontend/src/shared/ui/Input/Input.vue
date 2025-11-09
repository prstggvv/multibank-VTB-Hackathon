<template>
  <label class="label" :class="className">
    <div class="inputWrapper">
      <input
        ref="inputRef"
        :class="['input', { errorInput: error }]"
        :type="type"
        :placeholder="placeholder"
        :name="name"
        :value="modelValue"
        @input="onInput"
      />
      <button
        v-if="icon"
        type="button"
        class="iconButton"
        @click="handleIconClick"
      >
        <span v-if="icon === 'HideIcon'">👁️</span>
        <span v-else-if="icon === 'ShowIcon'">🙈</span>
      </button>
    </div>
    <span v-if="error" class="errorText">{{ errorText }}</span>
  </label>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'
import './Input.css'

interface InputProps {
  className?: string
  type: 'text' | 'password' | 'email'
  placeholder: string
  name: string
  modelValue: string
  error?: boolean
  errorText?: string
  icon?: 'HideIcon' | 'ShowIcon'
}

defineProps<InputProps>()
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'icon-click'): void
}>()

const inputRef = ref<HTMLInputElement | null>(null)

function onInput(evt: Event) {
  const target = evt.target as HTMLInputElement
  emit('update:modelValue', target.value)
}

function handleIconClick() {
  emit('icon-click')
}
</script>