<template>
  <form 
    :class="['form', className]"
    @submit.prevent="onSubmit"
    novalidate
  >
    <div class="container">
      <router-link
        class="li"
        to="/"
      >
        <!-- <img 
          class="svg"
          src="/vite.svg"
          alt="логотип"
        /> -->
      </router-link>
      <h1 class="title">
        {{ textTitle }}
      </h1>
      <slot />
    </div>
    <p class="text">
      {{ subtitle }}
      <router-link
        :to="to"
        class="link"
      >
        {{ auth }}
      </router-link>
    </p>
  </form>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import './Form.css'

interface FormProps {
  className?: string
  textSendButton: string
  textTitle: string
  subtitle: string
  auth: string
  to: string
}

defineProps<FormProps>()
const emit = defineEmits<{
  (e: 'submit', event: Event): void
}>()

function onSubmit(event: Event) {
  emit('submit', event)
}
</script>

