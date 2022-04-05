// vue 的导包语句 只有工程化的项目才会使用到导包语句
// 这个表示 node_modules 里面的目录
import { createApp } from 'vue'
// 以. 开头的表示相对路径  没有. 开头的 表示绝对路径
import App from './App.vue'


createApp(App).mount('#app')

// 等于
// createApp({
//   name: 'App',
//   components: {
//     HelloWorld
//   }
// }).mount("#app")
