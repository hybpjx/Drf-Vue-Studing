<template>
  <Home></Home>
</template>

<script>
import Home from './views/Home.vue'

// 暴露语句
// 必须通过 export 导包过来
export default {
  name: 'App',
  data(){
    return {
      message:"hello,Python"
    }
  },
  components: {
    Home,
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
