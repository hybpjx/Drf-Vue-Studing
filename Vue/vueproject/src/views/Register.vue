<template>
  <Menu :index="1" msg="注册"></Menu>
  <h1>注册页面</h1>
  <button @click="user_register"> 用户注册</button>
  <hr>

  <input type="text" v-model="city">
  <button @click="get_weather"> 获取数据</button>

  <div class="weather">
    <table>
      <tr>
        <td>data</td>
        <td>fengxiang——fengli</td>
        <td>low——high</td>
        <td>type</td>
      </tr>
      <tr v-for="(item,key) in this.weathers" :key="key">
        <td>{{ item.date }}</td>
        <td>{{ item.fengxiang }}——{{ item.fengli }}</td>
        <td>{{ item.low }}——{{ item.high }}</td>
        <td>{{ item.type }}</td>
      </tr>
    </table>
  </div>


</template>

<script>
import Menu from "@/components/Menu";
import http from "@/utils/http";

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  "name": "Register",
  "components": {
    Menu,
    // eslint-disable-next-line vue/no-unused-components
    http,
  },
  "data"() {
    return {
      "city": "苏州",
      // 声明一个变量存放天气
      "weathers": []
    }
  },
  "methods": {
    "get_weather"() {
      // 获取指定城市的天气
      // http.get(`http://wthrcdn.etouch.cn/weather_mini?city=${this.city}`).then(response => {
      http.get(`http://wthrcdn.etouch.cn/weather_mini`, {
        "params": {
          "city": this.city
        },
        "headers": {
          // 自定义请求头
        }
      }).then(response => {
        if (response.status === 200) {
          // console.log(response?.data?.data?.forecast);
          let weatherData = response?.data?.data?.forecast
          if (weatherData) {
            this.weathers = weatherData;
          }
        }
      }).catch(error => {
        // ajax 在请求或者相应处理过程中出现异常，则自动调用这里
        console.log(error)// 打印错误信息
        console.log(error.response)// 打印来自服务端的报错
      })
    },

    "user_register"() {
      // 使用post请求数据 也可以使用put 和patch来获取数据参数与配置与post相同
      // 参数1 url
      // 参数2 data 请求体数据
      // 参数3 config 与get中相同
      http.post(`http://127.0.0.1:8000/api/stu/`, {
        "name": "小王八",
        "gender": false,
        "age": 25,
        "classNum": "301",
        "description": "巴拉巴拉"
      }, {
        "headers": {
          // 自定义请求头
        }
      }).then(response=>{
        console.log(response.data)
      }).catch(error=>{
        console.log(error)
        console.log(error.response)
      })
    }
  }
}
</script>

<style scoped>
.weather table {
  width: 800px;
  border-collapse: collapse;
}

.weather table td {
  width: 120px;
  height: 40px;
  line-height: 40px;
  border: 1px solid red;
  text-align: center;
}

</style>