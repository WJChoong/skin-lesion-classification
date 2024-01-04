<template>
  <div id="app" class="custom-dark-bg">
    <NavigationBar/>
    <router-view/>
  </div>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue';

export default {
  name: 'App',
  components: {
    NavigationBar
  }
};
</script>

<style>
.custom-dark-bg {
  background-color: #343a40; 
  min-height: 100vh;
}
</style>
