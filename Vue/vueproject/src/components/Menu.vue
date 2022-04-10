<template>
  {{msg}}

  <button @click="myAdd">{{num}}</button>

<div class="menu">
  <a href="/" :class="{current:index===0}">站点首页</a>
  <a href="/register" :class="{current:index===1}">登陆/注册</a>
  <a href="" :class="{current:index===2}">会员中心</a>
</div>
</template>

<script>
export default {
  name: "Menu",
  props:{
    index:Number, // 变量： 数据类型
    msg:String,
    num:{
      type:Number,
      default:10
    }
    /*

    type:数据类型 Number   String   Boolean     Array 数组      Object 对象   函数 function   异步对象Promise
    default: 默认值 父组件没有对数据进行传递数据 默认使用该值

     */
  },
  methods:{
    myAdd(){
      // 往父组件 传递一个事件信号
      console.log("子组件被点击了")
      // this.$emit("add_num")
      // this.$emit("事件名","参数1","参数2","...")

      this.$emit("son_add",2)

    }
  }
}
</script>

<style scoped>
  .menu{
    height: 80px;
    overflow: hidden;
  }

  .menu a{
    float: left;
    height: 80px;
    line-height: 80px;
    text-align: center;
    width: 140px;
    background-color: blue;
    color: #eee;
  }

  .menu a.current{
    background-color: cadetblue;

  }

</style>