<template>
    <div class="padding">
        <div class="row">
            <div class="pull-right" v-if="user.category=='7'">
                <router-link to="/maintenance/call">
                    <a class="p-l-lg p-r-lg btn btn-sm theme-blue text-white">+ 报修</a>
                </router-link>
            </div>
            <div style="width: 30%">
                <form>
                    <div class="input-group input-group-sm b-a b-orange box-radius-2x" id="search">
                        <input type="text" class="form-control" placeholder="请输入编号、商户等" v-model="search_q">
                        <span class="input-group-btn">
                                <a class="btn no-radius deep-orange-400 text-white b-a b-orange" type="button"
                                   ui-sref="app.store.search({search_q: search_q})"><i class="fa fa-search"></i></a>
                            </span>
                    </div>
                </form>
            </div>
            <hr>
        </div>
        <div class="row">
            <div class="p-a p-t-xs p-b-xs b-b-2x b-primary nav-active-primary">
                <div class="row row-sm">
                    <form class="form-inline" role="form">
                        <div class="row m-b-sm">
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">城市</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">餐厅</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">服务商</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                        </div>
                        <div class="row m-b-sm">
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">维修类别</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">品牌</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">资产</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                        </div>
                        <div class="row m-b-sm">
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">维修时效</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">维修状态</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                            <div class="col-xs-4" id="date-filter">
                                <label class="p-r-xs text-muted m-r-md">报修时间</label><input type="datetime"
                                                                                           style="width: 35%">
                                <label> 至 </label><input type="datetime" style="width: 35%">
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="b-b nav-active-orange">
                <ul class="nav nav-tabs">
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link active" data-toggle="tab" data-target="#tab1" aria-expanded="true"
                           @click="getMaintenanceList('new')">最新报修</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" data-toggle="tab" data-target="#tab2" aria-expanded="false"
                           @click="getMaintenanceList('fixing')">正在维修</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" data-toggle="tab" data-target="#tab3" aria-expanded="false"
                           @click="getMaintenanceList('done')">维修完成</a>
                    </li>
                </ul>
            </div>
            <div class="tab-content m-b-md">
                <div class="tab-pane animated fadeIn text-muted active" id="tab1" aria-expanded="true">
                    <com-maintenance-table :maintenances="maintenances"></com-maintenance-table>
                </div>
                <div class="tab-pane animated fadeIn text-muted" id="tab2" aria-expanded="false">
                    <com-maintenance-table :maintenances="maintenances"></com-maintenance-table>
                </div>
                <div class="tab-pane animated fadeIn text-muted" id="tab3" aria-expanded="false">
                    <com-maintenance-table :maintenances="maintenances"></com-maintenance-table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapState} from 'vuex'
    import {mapActions} from 'vuex'
    export default {
        data(){
            return {
                maintenances: [],
            }
        },
        computed: mapState({user: state => state.user}),
        created(){
            this.getMaintenanceList('new');
        },
        methods: {
            ...mapActions(['SIGNOUT']),
            getMaintenanceList(status){
                var parmas = {};
//                if (status == 'new') {
//                    this.maintenances = JSON.parse(sessionStorage.getItem('new'));
//                }
//                if (status == 'fixing') {
//                    this.maintenances = JSON.parse(sessionStorage.getItem('fixing'));
//                }
//                if (status == 'done') {
//                    this.maintenances = JSON.parse(sessionStorage.getItem('done'));
//                }
                //维修单状态 -1：取消 0：新维修单 1：接单或者出发中 2：已经完成  3:到店  4:维修失败 5:填写修单未确认 6:为暂停 7.被返修
                var statusChoiceDict = {
                    'new': '0',
                    'fixing': '1,3,5,6',
                    'done': '-1,2,4,7'
                };
                var statusText = {
                    '-1':'取消',
                    '0':'新维修单' ,
                    '1':'接单或者出发中',
                    '2':'已经完成',
                    '3':'到店',
                    '4':'维修失败',
                    '5':'填写修单未确认',
                    '6':'为暂停',
                    '7':'被返修',
                }
                var qs = {status: statusChoiceDict[status]};
                var scope = this;
                $.ajax({
                    type: 'GET',
                    url: global.API_HOST + '/maintenance/list',
                    data: qs,
                }).done(function (res) {
                    if (res.status == 1) {
                        scope.maintenances = res.info.results;
                        scope.maintenances.map(function (e) {
                            e.status = statusText[e.status];
                        });
                    }
                    else {
                        toastr.warning(res.alert);
                    }
                });
            }
        }
    }
</script>