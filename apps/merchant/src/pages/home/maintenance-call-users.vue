<template>
    <div id="call-users">
        <com-app-breadcrumb :breadcrumb="breadcrumb"></com-app-breadcrumb>
        <div class="box theme-box p-a">
            <div class="box-header text-center">
                <h2 class="p-a-md p-b-sm theme-text-blue">请选择维修员指派工单</h2>
                <h3 class="p-a">
                    <span class="text-muted">系统已为您找到以下</span>
                    <strong class="theme-text-blue"><span v-text="selectedCount"></span>位</strong>
                    <span class="text-muted">符合条件的维修工</span>
                </h3>
            </div>
            <div class="box-body">
                <div class="p-a-sm m-l-lg m-r-lg m-b-lg">
                    <table class="table table-striped">
                        <thead class="theme-title-grey text-white">
                        <tr>
                            <th><input class="m-r-xs" type="checkbox" @click="selectAll">全选</th>
                            <th>城市</th>
                            <th>区域</th>
                            <th>姓名</th>
                            <th>电话</th>
                            <th>维修资质</th>
                        </tr>
                        </thead>
                        <tbody class="theme-text-blue">
                        <tr v-for="item in grab_users">
                            <td :class="{'theme-table-selected': item.checked}"><input type="checkbox"
                                                                                       v-model="item.checked"></td>
                            <td :class="{'theme-table-selected': item.checked}" v-text="item.city"></td>
                            <td :class="{'theme-table-selected': item.checked}" v-text="item.area"></td>
                            <td :class="{'theme-table-selected': item.checked}" v-text="item.name">姓名</td>
                            <td :class="{'theme-table-selected': item.checked}" v-text="item.mobile">电话</td>
                            <td :class="{'theme-table-selected': item.checked}" v-text="item.certificates">维修资质</td>
                        </tr>
                        </tbody>
                    </table>
                </div>
                <div class="box-header text-center m-b-md">
                    <h3>
                        <span class="text-muted">已选择</span>
                        <strong class="text-orange"><span v-text="selectedCount"></span>位</strong>
                        <span class="text-muted">维修员</span>
                    </h3>
                    <div class="row m-t-md m-b" style="width: 35%; margin: 0 auto;">
                        <button class="btn btn-sm theme-blue text-white form-control" @click="call" v-if="canBePosted">
                            发布
                        </button>
                        <button class="btn btn-sm theme-blue text-white form-control" disabled v-else>发布</button>
                    </div>
                    <div class="row m-b" style="width: 35%; margin: 0 auto;">
                        <div class="col-md-6" style="padding: 0; padding-right:8px;">
                            <button class="btn btn-sm theme-title-grey text-white form-control" @click="stepBack">
                                返回上一步
                            </button>
                        </div>
                        <div class="col-md-6" style="padding: 0; padding-left: 8px;">
                            <button class="btn btn-sm theme-title-grey text-white form-control" @click="quitCall">
                                取消报修
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data () {
            return {
                breadcrumb: [
                    {'title': '首页'},
                    {'title': '维修'},
                    {'title': '发布报修'},
                    {'title': '选择维修工'},
                ],
                grab_users: [],
                selectAllStatus: false,
                canBePosted: false,
            }
        },
        computed: {
            selectedCount() {
                var count = 0;
                this.grab_users.map(function (e) {
                    if (e.checked) {
                        count++;
                    }
                });
                this.canBePosted = !!count;
                return count;
            }
        },
        created(){
            this.getRepairUsers();
        },
        methods: {
            selectAll(){
                var scope = this;
                this.selectAllStatus = !this.selectAllStatus;
                this.grab_users.map(function (e) {
                    e.checked = scope.selectAllStatus;
                });
            },
            getRepairUsers(){
                var scope = this;
                var url = global.API_HOST + '/repairs';
                var loc = this.$route.query.store_loc;
                if (loc) {
                    url += '?loc=' + loc[0] + ',' + loc[1]
                }
                $.ajax({
                    type: 'GET',
                    url: url,
                }).done(function (res) {
                    if (res.status == 1) {
                        var results = res.info.results;
                        results.map(function (e) {
                            e.checked = false;
                        });
                        scope.grab_users = results;
                    }
                    else {
                        toastr.warning(res.alert);
                    }
                });
            },
            call(){
                var user_ids = this.grab_users.filter(function (e) {
                    return e.checked;
                }).map(function (e) {
                    return e.id;
                });

                var scope = this;
                var device = this.$route.query.selectedDevice || this.$route.query.device;

                var data = this.$route.query;
                data.user_ids = user_ids.join(',');
                $.ajax({
                    type: 'POST',
                    url: global.API_HOST + '/maintenance/call',
                    data: data,
                }).done(function (res) {
                    if (res.status == 1) {
                        toastr.success('报修成功！', function () {
                            scope.$router.go(-2);
                        });
                    }
                    else {
                        toastr.warning(res.alert);
                    }
                });
            },
            stepBack() {
                this.$router.go(-1);
            },
            quitCall(){
                this.$router.go(-2);
            },
        },
    }
</script>