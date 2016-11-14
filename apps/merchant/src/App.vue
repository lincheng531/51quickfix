<template>
    <div id="app">
        <!--<app-nav></app-nav>-->
        <header class="app-header navbar-md white box-shadow">
            <nav class="navbar no-radius">
                <div class="container">
                    <a data-toggle="collapse" data-target="#navbar-left"
                       class="navbar-item pull-right hidden-md-up m-a-0 m-l">
                        <i class="material-icons"></i>
                    </a>
                    <ul class="nav navbar-nav pull-right m-r-md">
                        <!--<li class="nav-item"><a class="nav-link" ui-fullscreen=""><span><i-->
                        <!--class="fa fa-fw fa-arrows-v"></i></span></a></li>-->
                        <li class="nav-item dropdown">
                            <a href="" class="nav-link clear" data-toggle="dropdown">
                                <!--<span class="avatar w-32">-->
                                    <!--<img v-bind:src="USER_PROFILE.avatar_img">-->
                                <!--</span>-->
                                <!--<span v-text="USER_PROFILE.name"></span>-->
                            </a>
                            <div class="dropdown-menu pull-right dropdown-menu-scale">
                                <!--<a class="dropdown-item" ui-sref="app.page.setting" href="#/app/page/setting">-->
                                <!--<span>设置</span> <span class="label primary m-l-xs"></span>-->
                                <!--</a>-->
                                <!--<div class="dropdown-divider"></div>-->
                                <a class="dropdown-item" href="/admin/logout">退出</a>
                            </div>
                        </li>
                    </ul>
                    <div class="collapse navbar-toggleable-sm" id="navbar-left" data-pjax="">
                        <ul class="nav navbar-nav pull-left nav-active-border b-primary m-l-md">
                            <li class="nav-item">
                                <a class="nav-link" href="/">
                                    <h5 class="nav-text"><i class="material-icons md-24">&#xe88a;</i></h5>
                                </a>
                            </li>
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" data-toggle="dropdown" ui-sref-active="active">
                                    <span class="nav-text">维修</span>
                                </a>
                                <div class="dropdown-menu">
                                    <router-link to="/maintenances" class="dropdown-item">
                                        <span class="nav-text">维修跟踪</span>
                                    </router-link>
                                    <router-link to="/verify" class="dropdown-item hide show" :class="{'show': 1}">
                                        <span class="nav-text">费用审核</span>
                                    </router-link>
                                    <router-link to="/settlements" class="dropdown-item hide show" :class="{'show': 1}">
                                        <span class="nav-text">费用结算</span>
                                    </router-link>
                                </div>
                            </li>
                            <li class="nav-item">
                                <a href="#/app/assets" class="nav-link" ui-sref-active="active">
                                    <span class="nav-text">固定资产</span>
                                </a>
                            </li>
                            <li class="nav-item">
                                <a href="#/app/user-center" class="nav-link" ui-sref-active="active">
                                    <span class="nav-text">用户中心</span>
                                </a>
                            </li>
                            <li class="nav-item">
                                <a href="#/app/help" class="nav-link" ui-sref-active="active">
                                    <span class="nav-text">帮助</span>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
        <app-footer></app-footer>
        <div class="app-body" id="view">
            <div class="container">
                <router-view></router-view>
            </div>
        </div>
    </div>
</template>

<script>
    //    import appNav from './components/app-nav.vue'
    import appFooter from './components/app-footer.vue'

    export default {
        data () {
            return{
            }
        },
        components: {
//            appNav,
            appFooter,
        }
    }
</script>

<style>
    header {
        font-weight: 800;
        color: white;
    }

    .nav-active-orange .nav-link.active,
    .nav-active-orange .nav > li.active > a {
        color: rgba(255, 255, 255, 0.87) !important;
        background-color: #ff7315 !important;
    }

    .navbar {
        background-color: #374256;
    }

    #navbar-left .navbar-nav .nav-item + .nav-item {
        margin-left: 80px;
    }

    #navbar-left.navbar-nav > .nav-item > .nav-link {
        padding: 0 32px;
    }
</style>