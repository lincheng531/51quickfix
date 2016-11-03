import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'

Vue.config.debug = true;
Vue.use(VueRouter)

import overview from './components/overview.vue'
import MaintenanceList from './components/maintenance-list.vue'
import MaintenanceDetail from './components/maintenance-detail.vue'

const routes = [
    {path: '/', component: overview},
    {path: '/maintenances', component: MaintenanceList},
    {path: '/maintenance/detail', component: MaintenanceDetail},
]

const router = new VueRouter({
    routes
})

new Vue({
    el: '#app',
    router,
    render: h=> h(App)
})
