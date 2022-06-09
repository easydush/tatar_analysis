<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <Header msg="tatar analysis"/>
</template>

<script>
import HeaderComponent from './components/Header'

export default {
  name: 'App',
  components: {
    Header: HeaderComponent
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
