import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'

Vue.config.debug = true;
Vue.use(VueRouter)

import overview from './components/overview.vue'
import MaintenanceList from './components/maintenance-list.vue'
import MaintenanceDetail from './components/maintenance-detail.vue'
import MaintenanceCall from './components/maintenance-call.vue'
import MaintenanceCallUsers from './components/maintenance-call-users.vue'

const routes = [
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
