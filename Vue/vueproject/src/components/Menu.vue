<template>
<div class="menu">
  <a href="">首页</a>
  <a href="">列表页</a>
  <a href="">会员中心</a>
</div>
</template>

<script>
export default {
  name: "Menu"
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

</style>