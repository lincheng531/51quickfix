<template>
    <div id="call-users">
        <app-breadcrumb :breadcrumb="breadcrumb"></app-breadcrumb>
        <div class="box theme-box p-a">
            <div class="box-header text-center">
                <h2 class="p-a-md p-b-sm theme-text-blue">请选择维修员指派工单</h2>
                <h3 class="p-a">
                    <span class="text-muted">系统已为您找到以下</span>
                    <strong class="theme-text-blue">5位</strong>
                    <span class="text-muted">符合条件的维修工</span>
                </h3>
            </div>
            <div class="box-body">
                <div class="p-a-sm m-l-lg m-r-lg m-b-lg">
                    <table class="table table-striped">
                        <thead class="theme-title-grey text-white">
                        <tr>
                            <th><input class="m-r-xs" type="checkbox">全选</th>
                            <th>城市</th>
                            <th>区域</th>
                            <th>姓名</th>
                            <th>电话</th>
                            <th>维修资质</th>
                        </tr>
                        </thead>
                        <tbody class="theme-text-blue">
                        <tr>
                            <td><input type="checkbox"></td>
                            <td>城市</td>
                            <td>区域</td>
                            <td>姓名</td>
                            <td>电话</td>
                            <td>维修资质</td>
                        </tr>
                        <tr>
                            <td><input type="checkbox"></td>
                            <td>城市</td>
                            <td>区域</td>
                            <td>姓名</td>
                            <td>电话</td>
                            <td>维修资质</td>
                        </tr>
                        <tr>
                            <td><input type="checkbox"></td>
                            <td>城市</td>
                            <td>区域</td>
                            <td>姓名</td>
                            <td>电话</td>
                            <td>维修资质</td>
                        </tr>
                        <tr>
                            <td><input type="checkbox"></td>
                            <td>城市</td>
                            <td>区域</td>
                            <td>姓名</td>
                            <td>电话</td>
                            <td>维修资质</td>
                        </tr>

                        <tr class="theme-table-selected" style="background-color: rgb(255, 241, 232);">
                            <td><input type="checkbox"></td>
                            <td>城市</td>
                            <td>区域</td>
                            <td>姓名</td>
                            <td>电话</td>
                            <td>维修资质</td>
                        </tr>
                        </tbody>
                    </table>
                </div>
                <div class="box-header text-center m-b-md">
                    <h3>
                        <span class="text-muted">已选择</span>
                        <strong class="text-orange">1位</strong>
                        <span class="text-muted">维修员</span>
                    </h3>
                    <div class="row m-t-md m-b" style="width: 35%; margin: 0 auto;">
                        <router-link to="/maintenances">
                            <button class="btn btn-sm theme-blue text-white form-control">发布</button>
                        </router-link>
                    </div>
                    <div class="row m-b" style="width: 35%; margin: 0 auto;">
                        <div class="col-md-6" style="padding: 0; padding-right:8px;">
                            <button class="btn btn-sm theme-title-grey text-white form-control">返回上一步</button>
                        </div>
                        <div class="col-md-6" style="padding: 0; padding-left: 8px;">
                            <router-link to="/maintenances">
                                <button class="btn btn-sm theme-title-grey text-white form-control">取消报修</button>
                            </router-link>
                        </div>
                    </div>
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
                    {'title': '选择维修工'},
                ],
            }
        },
        components: {
            appBreadcrumb,
        }
    }
</script>