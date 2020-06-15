import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from "../components/Login";
import Main from "../components/Main";
import Patient from "../components/Patient";


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
            meta: {
                requireAuth: true,
                keepAlive: true
            }
        },
        {
            path:"/Patient",
            name:"patient",
            component:Patient,
            meta: {
                requireAuth: true,
                keepAlive: true
            }
        }
    ]

})
export default router;


