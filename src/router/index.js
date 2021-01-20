import Vue from 'vue'
import Router from 'vue-router'
import Java from "../components/Java";
import Python from "../components/Python";
import Course from "../components/Course";

Vue.use(Router)

export default new Router({
    routes: [
        {path:'/data',component:Java},
        {path:'/python',component:Python},
        {path:'/course',component:Course},
    ]
})
