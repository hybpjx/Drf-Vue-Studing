import {createRouter,createWebHistory} from "vue-router";
import wifi from '../views/wifi.vue'

const router=createRouter({
    history:createWebHistory(),
    routes:[
        {
            meta:{
                title:'wifi密码'
            },

            path:'/',
            name:'wifi',
            component:wifi
        }
    ]
})

export default router


router.beforeEach((to)=>{
    document.title=to.meta.title;
})