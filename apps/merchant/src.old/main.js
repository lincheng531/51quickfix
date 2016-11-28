import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'

Vue.config.debug = true;
Vue.use(VueRouter)

import overview from '../src/pages/home/overview.vue'
import MaintenanceList from '../src/pages/home/maintenance-list.vue'
import MaintenanceDetail from './components/maintenance-detail.vue'
import MaintenanceCall from '../src/pages/home/maintenance-call.vue'
import MaintenanceCallUsers from '../src/pages/home/maintenance-call-users.vue'
import Login from './components/login.vue'

const routes = [
    {
        path: '/login',
        meta: { auth: false },
        component: Login,
    },
    {path: '/', component: overview},
    {path: '/maintenances', component: MaintenanceList},
    {path: '/maintenance/detail', component: MaintenanceDetail},
    {path: '/maintenance/call', component: MaintenanceCall},
    {path: '/maintenance/call/users', component: MaintenanceCallUsers},
]

const router = new VueRouter({
    routes
})



new Vue({
    el: '#app',
    router,
    render: h => h(App)
})
