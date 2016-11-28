//加载css
import "./assets/animate.css/animate.min.css"
import "./assets/glyphicons/glyphicons.css"
import "./assets/font-awesome/css/font-awesome.min.css"
import "./assets/material-design-icons/material-design-icons.css"
import "./assets/bootstrap/dist/css/bootstrap.min.css"
import "./libs/js/datetimepicker/css/bootstrap-datetimepicker.css"
import "./assets/styles/app.css"
import "./assets/styles/font.css"
import "./libs/jquery/toastr/toastr.min.css"
import "./libs/jquery/editable-select/source/jquery.editable-select.min.css"
import "./assets/styles/global.css"

import Vue from 'vue'
import VueRouter from 'vue-router'

import './libs/jquery/bootstrap/dist/js/bootstrap.js'
import './js/config.lazyload.js'
import './js/palette.js'
import './js/ui-load.js'
import './js/ui-jp.js'
import './js/ui-include.js'
import './js/ui-device.js'
import './js/ui-form.js'
import './js/ui-nav.js'
// import './js/ui-screenfull.js'
import './js/ui-scroll-to.js'
import './js/ui-toggle-class.js'
import './libs/jquery/toastr/toastr.min.js'
import './libs/jquery/editable-select/source/jquery.editable-select.js'
import './libs/jquery/fullscreen/screenfull.min.js'
import './libs/jquery/jquery.raty.min.js'

import './libs/js/datetimepicker/bootstrap-datetimepicker.js'
import './libs/js/datetimepicker/locales/bootstrap-datetimepicker.zh-CN.js'
// import './libs/jquery/jquery.twbsPagination.js'

import routes from './config/routes'
import store from './store/'
import com from './component/' //加载公共组件

Object.keys(com).forEach((key) => {
    var name = key.replace(/(\w)/, (v) => v.toUpperCase()) //首字母大写
    Vue.component(`com${name}`, com[key])
})

Vue.use(VueRouter)

const router = new VueRouter({
    routes
})
router.beforeEach(({meta, path}, from, next) => {
    var {auth = true} = meta
    var isLogin = Boolean(store.state.user && store.state.user.id) //true用户已登录， false用户未登录

    if (auth && !isLogin && path !== '/login') {
        return next({ path: '/login' })
    }
    next()
})

new Vue({ store, router }).$mount('#app')