<template>
  <h1>wifi例子</h1>

  <input :type="type" v-model="password">
  <button @click="change">{{text}}</button>
  <div><span>验证结果{{check}}</span></div>
</template>

<script setup>
  import {ref,watch} from "vue"


  let type =ref("password")
  let text=ref("显示密码")

  const change = () =>{
    if (type.value==="text"){
      type.value="password";
      text.value="显示密码";
    }else {
      type.value="text";
      text.value="隐藏密码";
    }
  }

  let password = ref("");
  let check = ref(false); // 密码是否通过
  // 监听数据
  watch(
      password,
      ()=>{
        let pl=password.value.length
        if(pl<6 || pl>16){
          check.value=false
        }else {
          check.value=true
        }
      }
  )

</script>


<style scoped>
input{
  border: 1px solid #333;
  outline: #333333;
}
</style>