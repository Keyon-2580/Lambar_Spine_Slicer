import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from "../components/Login";
import Main from "../components/Main";
import Patient from "../components/Patient";
import Diagnosis from  "../components/Diagnosis"
import showImg from  "../components/showImg"


Vue.use(VueRouter)

const router = new VueRouter({
    routes:[
        {
            path:"/",
            name:"login",
            component:Login
        },
        {
            path:"/Main",
            name: 'main',
            component:Main,
            // meta: {
            //     requireAuth: true,
            //     keepAlive: true
            // }
        },
        {
            path:"/Patient",
            name:"patient",
            component:Patient,
            meta: {
                requireAuth: true,
                keepAlive: true
            }
        },
        {
            path:"/Diagnosis",
            name:"diagnosis",
            component:Diagnosis,
            meta: {
                requireAuth: true,
                keepAlive: true
            }

        },
        {
            path:"/ImageShow",
            name:"ImageShow",
            component:showImg,


        },
    ]

})
export default router;


