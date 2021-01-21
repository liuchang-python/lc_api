import Vue from 'vue'
import Router from 'vue-router'
import Java from "../components/Java";
import Python from "../components/Python";
import Course from "../components/Course";
import Home from "../components/Home";
import Login from "../components/Login";

Vue.use(Router)

export default new Router({
    routes: [
        {path: "/", component: Home},
        {path: "/login", component: Login},
        {path:'/data',component:Java},
        {path:'/python',component:Python},
        {path:'/course',component:Course},
    ]
})
