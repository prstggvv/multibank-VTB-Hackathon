<template>
  <main class="section" :class="className">
    <section class="container">
      <Form
        @submit="handleSubmit"
        text-send-button="Войти в аккаунт"
        text-title="Вход в аккаунт"
        subtitle="Ещё не зарегистрированы?"
        auth="Регистрация"
        to="/signup"
      >
        <Input
          type="email"
          placeholder="E-mail"
          :model-value="values.email || ''"
          name="email"
          :error="Object.prototype.hasOwnProperty.call(errors, 'email')"
          :error-text="errors.email || ''"
          @update:model-value="handleInputChange('email', $event)"
        />

        <Input 
          :type="passwordType"
          placeholder="Пароль"
          :model-value="values.password || ''"
          name="password"
          :error="Object.prototype.hasOwnProperty.call(errors, 'password')"
          :error-text="errors.password || ''"
          :icon="passwordIcon"
          @update:model-value="handleInputChange('password', $event)"
          @icon-click="handleClickIcon"
        />

        <Button
          type="submit"
          :disabled="!isValid"
          :class-name="isValid ? 'formButton formButtonActive' : 'formButton'"
        >
          Войти в аккаунт
        </Button>
      </Form>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Form from '../../components/Form/Form.vue'
import Input from '../../shared/ui/Input/Input.vue'
import Button from '../../shared/ui/Button/Button.vue'
import { useValidation } from '../../shared/lib/hooks/useValidation'
import './LoginPage.css'

interface LoginPageProps {
  className?: string
}

defineProps<LoginPageProps>()

const emit = defineEmits<{
  login: [email: string, password: string]
}>()

const {
  values,
  errors,
  isValid,
  handleChange,
} = useValidation({})

const passwordIcon = ref<'HideIcon' | 'ShowIcon'>('HideIcon')
const passwordType = ref<'text' | 'password'>('password')

const handleInputChange = (name: string, value: string) => {
  const event = {
    target: {
      name,
      value
    }
  } as Event & { target: { name: string; value: string } }
  handleChange(event)
}

const handleClickIcon = () => {
  if (passwordType.value === 'password') {
    passwordType.value = 'text'
    passwordIcon.value = 'ShowIcon'
  } else {
    passwordType.value = 'password'
    passwordIcon.value = 'HideIcon'
  }
}

const handleSubmit = (e: Event) => {
  e.preventDefault()
  const email = values.email || ''
  const password = values.password || ''
  if (email && password) {
    emit('login', email, password)
  }
}
</script>

