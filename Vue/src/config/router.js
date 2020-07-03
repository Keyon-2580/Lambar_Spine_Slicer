import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from "../components/Login";
import Main from "../components/Main";
import Patient from "../components/Patient";
import Diagnosis from  "../components/Diagnosis"
import showImg from  "../components/showImg"
import STL from "../components/STL"


Vue.use(VueRouter)

const router = new VueRouter({
    routes:[
        {
            path:"/",
            name:"login",
            component:Login,
            meta: {
                requireAuth: true,
                keepAlive: true,
                title:'腰椎分割系统登录'
            }
        },
        {
            path:"/Main",
            name: 'main',
            component:Main,
            meta: {
                requireAuth: true,
                keepAlive: true,
                title:'腰椎分割系统主页'
            }
        },
        {
            path:"/Patient",
            name:"patient",
            component:Patient,
            meta: {
                requireAuth: true,
                keepAlive: true,
                title:'病人资料'
            }
        },
        {
            path:"/Diagnosis",
            name:"diagnosis",
            component:Diagnosis,
            meta: {
                requireAuth: true,
                keepAlive: false,
                title:'查看切片'
            }

        },
        {
            path:"/ImageShow",
            name:"ImageShow",
            component:showImg,
        },
        {
            path:"/STL",
            name:"STL",
            component:STL,
        },
    ]

})
router.beforeEach((to, from, next) => {

    /* 路由发生变化修改页面title */
    if (to.meta.title) {
        document.title = to.meta.title;
    }
    next();

});

export default router;


