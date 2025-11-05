<template>
  <header :class="cls.header">
    <div :class="cls.container">
      <div :class="cls.logoContainer">
        <img 
          :class="cls.logo"
          src="../../../shared/assets/images/icons/Logo.svg"
        />
      </div>
      <div :class="cls.mainBlock">
        <h1 :class="cls.title">Транзакции</h1>
        <div :class="cls.mainInfo">
          <label :class="cls.label">
            <img 
              :class="cls.svgLoop"
              src="../../../shared/assets/images/icons/loop.svg"
            />
            <input 
              :class="cls.input"
              type="text"
              placeholder="Поиск"
            />
          </label>
          <div :class="cls.round">
            <img 
              :class="cls.svg"
              src="../../../shared/assets/images/icons/notification.svg"
            />
          </div>
          <div :class="cls.round">
            <img 
              :class="cls.svg"
              src="../../../shared/assets/images/icons/settings.svg"
            />
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import cls from './Header.module.css';

</script>