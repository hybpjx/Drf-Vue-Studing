<template>
  <Menu :index="1" msg="注册"></Menu>
  <h1>注册页面</h1>


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
      <tr v-for="item in this.weathers">
        <td>{{item.date}}</td>
        <td>{{item.fengxiang}}——{{item.fengli}}</td>
        <td>{{item.low}}——{{item.high}}</td>
        <td>{{item.type}}</td>
      </tr>
    </table>
  </div>


</template>

<script>
import Menu from "@/components/Menu";
import http from "@/utils/http";

export default {
  name: "Register",
  components: {
    Menu,
    http,
  },
  data() {
    return {
      city: "苏州",
      // 声明一个变量存放天气
      weathers: []
    }
  },
  methods: {
    get_weather() {
      // 获取指定城市的天气
      // http.get(`http://wthrcdn.etouch.cn/weather_mini?city=${this.city}`).then(response => {
      http.get(`http://wthrcdn.etouch.cn/weather_mini`,{
        params:{
          city:this.city
        },
        headers:{
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
      }).catch(error=>{
        // ajax 在请求或者相应处理过程中出现异常，则自动调用这里
        console.log(error)// 打印错误信息
        console.log(error.response)// 打印来自服务端的报错
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