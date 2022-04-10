
<template>
  <div>
    <Menu :index="0" msg="首页" :num="num" @son_add="son_add"></Menu>
    <!--  父组件要发送数据给子组件，通过组件的属性传递，属性名就是将来的变量名，传递数据如果是个变量，则需要在左边加上英文冒号  -->
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
    },
    son_add(args1){
      console.log(`父组件接受的变量${args1}`)
      this.num+=args1
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