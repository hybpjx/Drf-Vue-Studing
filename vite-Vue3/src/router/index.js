import {createRouter,createWebHistory} from "vue-router";


const router=createRouter({
    history:createWebHistory(),
    routes:[
        {
            meta:{
                title:'wifi密码'
            },

            path:'/wifi',
            name:'wifi',
            component:import('../views/wifi.vue')
        }
    ]
})

export default router


router.beforeEach(()=>{
    document.title=to.meta.title;
})