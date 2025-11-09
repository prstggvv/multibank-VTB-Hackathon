import { reactive, ref, watch } from 'vue'

interface InputItems {
  [key: string]: string
}

const validate = (values: InputItems) => {
  const errors: Record<string, string> = {}

  if (!values.email) {
    errors.email = 'Заполните поле E-mail'
  } else if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(values.email)) {
    errors.email = 'Введите корректный E-mail'
  }

  // if (!values.password) {
  //   errors.password = 'Заполните поле пароль'
  // } else if (values.password.length < 8) {
  //   errors.password = 'Пароль не может быть меньше 8 символов'
  // } else if (!/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$/.test(values.password)) {
  //   errors.password = 'Пароль должен состоять из строчных и прописных латинских букв, спецсимволов, цифр'
  // }

  return errors
}

export function useValidation(initialValues: InputItems) {
  const values = reactive({ ...initialValues })
  const errors = reactive<Record<string, string>>({})
  const isValid = ref(false)

  watch(values, (newValues) => {
    const newErrors = validate(newValues)
    Object.keys(errors).forEach((key) => delete errors[key])
    Object.assign(errors, newErrors)
    isValid.value = Object.keys(newErrors).length === 0
  }, { deep: true })

  const handleChange = (e: Event) => {
    const target = e.target as HTMLInputElement
    values[target.name] = target.value
  }

  return {
    values,
    errors,
    isValid,
    handleChange,
  }
}
