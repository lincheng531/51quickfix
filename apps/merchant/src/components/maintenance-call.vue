<template>
    <div id="maintenance-call">
        <app-breadcrumb :breadcrumb="breadcrumb"></app-breadcrumb>

        <div class="theme-box p-b-lg">
            <div class="box theme-box theme-text-blue">
                <div class="box-header theme-grey-dark">
                    <h3>报修餐厅</h3>
                </div>
                <div class="box-body clearfix">
                    <div class="row text-right text-muted">
                        <div class="col-md-6">
                            <div class="col-md-2">连锁餐厅</div>
                            <div class="col-md-10"></div>
                        </div>
                        <div class="col-md-6">
                            <div class="col-md-2">餐厅名称</div>
                            <div class="col-md-10"></div>
                        </div>
                        <div class="col-md-6">
                            <div class="col-md-2">地址</div>
                            <div class="col-md-10"></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="box theme-box theme-text-blue">
                <div class="box-header theme-grey-dark">
                    <h3>报修人</h3>
                </div>
                <div class="box-body clearfix">
                    <div class="row text-right text-muted">
                        <div class="col-md-6">
                            <div class="col-md-2">连锁餐厅</div>
                            <div class="col-md-10"></div>
                        </div>
                        <div class="col-md-6">
                            <div class="col-md-2">餐厅名称</div>
                            <div class="col-md-10"></div>
                        </div>
                        <div class="col-md-6">
                            <div class="col-md-2">地址</div>
                            <div class="col-md-10"></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="box theme-box theme-text-blue">
                <div class="box-header theme-grey-dark">
                    <h3>报修信息</h3>
                </div>
                <div class="box-body clearfix">
                    <div class="row text-right text-muted">
                        <div class="col-md-6">
                            <div class="col-md-2">连锁餐厅</div>
                            <div class="col-md-10"></div>
                        </div>
                        <div class="col-md-6">
                            <div class="col-md-2">餐厅名称</div>
                            <div class="col-md-10"></div>
                        </div>
                        <div class="col-md-6">
                            <div class="col-md-2">地址</div>
                            <div class="col-md-10"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="m-a b-a b-dashed"></div>
            <div class="m-t-lg m-b-lg">
                <div class="row text-white">
                    <router-link to="/maintenances">
                        <div class="col-md-6 text-right">
                            <button class="btn btn-sm p-l-lg p-r-lg">取消报修</button>
                        </div>
                    </router-link>
                    <router-link to="/maintenance/call/users">
                        <div class="col-md-6">
                            <button class="btn btn-sm theme-blue p-l-lg p-r-lg">下一步</button>
                        </div>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import appBreadcrumb from './app-breadcrumb.vue'

    export default {
        data () {
            return {
                breadcrumb: [
                    {'title': '首页'},
                    {'title': '维修'},
                    {'title': '发布报修'},
                ],
            }
        },
        components: {
            appBreadcrumb,
        }
    }
</script>

<style>
    #maintenance-call .box {
        margin-bottom: 0;
    }
</style>