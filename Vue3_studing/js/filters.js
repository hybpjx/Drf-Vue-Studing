// 定义全局范围的过滤器
Vue.filter("money1", function (v) {
    // 就是用来格式化这个数据的
    if (v === 0) {
        return v
    }
    return v.toFixed(2) + "元"
})