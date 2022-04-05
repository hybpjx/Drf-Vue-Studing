
<template>
  <div>
    <Menu></Menu>
    <h1>Home.vue</h1>
    <button @click="sub" class="sub">-</button>
    <input type="text" size="1px" v-model="num">
    <button @click="add" class="add">+</button>
  </div>
</template>


<script>

import Menu from "@/components/Menu";

export default {
  name: "Home",
  data() {
    return {
      num: 0
    }
  },
  methods: {
    add() {
      this.num++;
    },
    sub(){
      this.num--;
    }
  },
  watch: {
    num() {
      if (this.num > 20) {
        this.num = 10;
      }
    }
  },

  components:{
    Menu,
  }
}
</script>

<style scoped>
  h1{
    color: red;
  }
</style>