<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <!-- RouterView is the dynamic placeholder. 
       If the URL is '/', it injects Login.vue here. 
       If the URL is '/admin', it injects AdminDashboard.vue here. -->
  <RouterView />
</template>

<style>
/* Global reset to ensure no unwanted margins cause laggy scrolling */
body,
html {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>
