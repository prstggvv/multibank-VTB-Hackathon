<template>
  <button
    class="button"
    :class="className || ''"
    :type="type"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import './Button.css';

interface ButtonProps {
  className?: string
  type: 'button' | 'reset' | 'submit'
  disabled?: boolean
}

defineProps<ButtonProps>()
</script>