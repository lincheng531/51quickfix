<template>
    <div class="padding">
        <div class="row">
            <div class="p-b-xs">
                <div class="pull-right">
                    <router-link to="/maintenance/call">
                        <a class="p-l-lg p-r-lg btn btn-sm theme-blue text-white">+ 报修</a>
                    </router-link>
                </div>
                <div style="width: 30%">
                    <form>
                        <div class="input-group input-group-sm b-a b-orange box-radius-2x" id="search">
                            <input type="text" class="form-control" placeholder="请输入编号、商户或资产等" v-model="search_q">
                            <span class="input-group-btn">
                                <a class="btn no-radius deep-orange-400 text-white b-a b-orange" type="button"
                                   @click="search(search_q)"><i class="fa fa-search"></i></a>
                            </span>
                        </div>
                    </form>
                </div>
            </div>
            <hr>
        </div>
        <div class="row">
            <div class="p-a p-t-xs p-b-sm b-b-2x b-primary nav-active-primary">
                <div class="row row-sm">
                    <form class="form-inline" role="form">
                        <div class="row m-b-sm">
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">城市</label>
                                </div>
                                <com-ui-single-select :size="'sm'" :type="'city'" :width="'118px'"
                                                      v-model="queryFilter.city"></com-ui-single-select>
                            </div>
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">餐厅</label>
                                </div>
                                <com-ui-single-select :size="'sm'" :width="'118px'"
                                                      v-model="queryFilter.city"></com-ui-single-select>
                            </div>
                            <div class="form-group col-xs-4" v-if="user_category=='merchant'">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">服务商</label>
                                </div>
                                <com-ui-single-select :size="'sm'" :width="'118px'"
                                                      v-model="queryFilter.city"></com-ui-single-select>
                            </div>
                            <div class="form-group col-xs-4" v-if="user_category=='service'">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">商家品牌</label>
                                </div>
                                <com-ui-single-select :size="'sm'" :type="'head_type'" :width="'118px'"
                                                      v-model="queryFilter.city"></com-ui-single-select>
                            </div>
                        </div>
                        <div class="row m-b-sm">
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">维修类别</label>
                                </div>
                                <com-ui-single-select :size="'sm'" :width="'118px'"
                                                      v-model="queryFilter.city"></com-ui-single-select>
                            </div>
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">设备品牌</label>
                                </div>
                                <com-ui-single-select :size="'sm'" :width="'118px'"
                                                      v-model="queryFilter.city"></com-ui-single-select>
                            </div>
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">资产</label>
                                </div>
                                <com-ui-single-select :size="'sm'" :width="'118px'"
                                                      v-model="queryFilter.city"></com-ui-single-select>
                            </div>
                        </div>
                        <div class="row m-b-sm">
                            <div class="form-group col-xs-4">
                                <div class="col-xs-4 text-right">
                                    <label class="m-r text-muted">维修时效</label>
                                </div>
                                <com-ui-single-select :size="'sm'" :type="'state'" :width="'118px'"
                                                      v-model="queryFilter.state"></com-ui-single-select>
                            </div>

                            <div class="form-group col-xs-8">
                                <div class="col-xs-2 text-right">
                                    <label class="m-r text-muted">报修时间</label>
                                </div>
                                <div class="col-xs-10" style="padding-left:0">
                                    <input type="datetime" class="fixTime" style="width:20%">
                                    <label> 至 </label><input type="datetime" class="fixTime" style="width:20%">
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <div class="row" v-if="list_type=='status'">
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
                           @click="getMaintenanceList('done')">维修结束</a>
                    </li>
                </ul>
            </div>
            <div class="tab-content">
                <div class="tab-pane animated fadeIn text-muted active" id="tab1" aria-expanded="true">
                    <com-maintenance-table :maintenances="maintenances" :list_type="list_type"></com-maintenance-table>
                </div>
                <div class="tab-pane animated fadeIn text-muted" id="tab2" aria-expanded="false">
                    <com-maintenance-table :maintenances="maintenances" :list_type="list_type"></com-maintenance-table>
                </div>
                <div class="tab-pane animated fadeIn text-muted" id="tab3" aria-expanded="false">
                    <com-maintenance-table :maintenances="maintenances" :list_type="list_type"></com-maintenance-table>
                </div>
            </div>
        </div>

        <div class="row" v-if="list_type=='audit'">
            <div class="b-b nav-active-orange">
                <ul class="nav nav-tabs" v-if="user_category=='merchant'">
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link active" data-toggle="tab" data-target="#tabAudit1" aria-expanded="true"
                           @click="getMaintenanceList('merchantAudit1')">待审核</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" data-toggle="tab" data-target="#tabAudit2" aria-expanded="false"
                           @click="getMaintenanceList('merchantAudit2')">审核未通过</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" data-toggle="tab" data-target="#tabAudit2" aria-expanded="false"
                           @click="getMaintenanceList('merchantAudit3')">审核失败</a>
                    </li>
                </ul>


                <ul class="nav nav-tabs" v-if="user_category=='service'">
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link active" data-toggle="tab" data-target="#tabAudit1" aria-expanded="true"
                           @click="getMaintenanceList('serviceAudit1')">待提交</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" data-toggle="tab" data-target="#tabAudit2" aria-expanded="true"
                           @click="getMaintenanceList('serviceAudit2')">等待对方审核</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" data-toggle="tab" data-target="#tabAudit3" aria-expanded="false"
                           @click="getMaintenanceList('serviceAudit3')">审核未通过</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" data-toggle="tab" data-target="#tabAudit4" aria-expanded="false"
                           @click="getMaintenanceList('serviceAudit4')">审核失败</a>
                    </li>
                </ul>
            </div>
            <div class="tab-content" v-if="user_category=='merchant'">
                <div class="tab-pane animated fadeIn text-muted active" id="tabAudit1" aria-expanded="true">
                    <com-maintenance-table :maintenances="maintenances" :list_type="list_type"></com-maintenance-table>
                    <!--
                    <button class="btn primary pull-left" v-if="list_type=='audit'" @click="batchOp('audit')">审核
                    </button>-->
                </div>
                <div class="tab-pane animated fadeIn text-muted" id="tabAudit2" aria-expanded="false">
                    <com-maintenance-table :maintenances="maintenances" :list_type="list_type"></com-maintenance-table>
                </div>
                <div class="tab-pane animated fadeIn text-muted" id="tabAudit3" aria-expanded="false">
                    <com-maintenance-table :maintenances="maintenances" :list_type="list_type"></com-maintenance-table>
                </div>
            </div>

            <div class="tab-content" v-if="user_category=='service'">
                <div class="tab-pane animated fadeIn text-muted active" id="tabAudit1" aria-expanded="true">
                    <com-maintenance-table :maintenances="maintenances" :list_type="list_type"></com-maintenance-table>
                    <button class="btn primary pull-left" v-if="list_type=='audit'" @click="batchOp('audit')">提交给商户
                    </button>
                </div>
                <div class="tab-pane animated fadeIn text-muted" id="tabAudit2" aria-expanded="false">
                    <com-maintenance-table :maintenances="maintenances" :list_type="list_type"></com-maintenance-table>
                </div>
                <div class="tab-pane animated fadeIn text-muted" id="tabAudit3" aria-expanded="false">
                    <com-maintenance-table :maintenances="maintenances" :list_type="list_type"></com-maintenance-table>
                </div>
                <div class="tab-pane animated fadeIn text-muted" id="tabAudit4" aria-expanded="false">
                    <com-maintenance-table :maintenances="maintenances" :list_type="list_type"></com-maintenance-table>
                </div>
            </div>
        </div>


        <div class="row" v-if="list_type=='settlement'">
            <div class="b-b nav-active-orange">
                <!--
                <ul class="nav nav-tabs" v-if="user_category=='merchant'">
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link active" data-toggle="tab" data-target="#tabSettlement1" aria-expanded="true"
                           @click="getMaintenanceList('settling')">待结算</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" data-toggle="tab" data-target="#tabSettlement2" aria-expanded="false"
                           @click="getMaintenanceList('settled')">结案</a>
                    </li>
                </ul>-->

                <ul class="nav nav-tabs" v-if="user_category=='merchant'">
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link active" data-toggle="tab" data-target="#tabSettlement1" aria-expanded="true"
                           @click="getMaintenanceList('merchantSettling')">待结算</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" data-toggle="tab" data-target="#tabSettlement2" aria-expanded="true"
                           @click="getMaintenanceList('merchantForSettling')">等待对方结算</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" data-toggle="tab" data-target="#tabSettlement3" aria-expanded="false"
                           @click="getMaintenanceList('settled')">结案</a>
                    </li>
                </ul>

                <ul class="nav nav-tabs" v-if="user_category=='service'">
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link active" data-toggle="tab" data-target="#tabSettlement1" aria-expanded="true"
                           @click="getMaintenanceList('repairSettling')">待结算</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" data-toggle="tab" data-target="#tabSettlement2" aria-expanded="true"
                           @click="getMaintenanceList('repairForSettling')">等待对方结算</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" data-toggle="tab" data-target="#tabSettlement3" aria-expanded="false"
                           @click="getMaintenanceList('settled')">结案</a>
                    </li>
                </ul>
            </div>
            <div class="tab-content">
                <div class="tab-pane animated fadeIn text-muted active" id="tabSettlement1" aria-expanded="true">
                    <com-maintenance-table :maintenances="maintenances" :list_type="list_type"></com-maintenance-table>
                    <button class="btn primary pull-left" v-if="list_type=='settlement'" @click="batchOp('settle')">提交
                    </button>
                </div>
                <div class="tab-pane animated fadeIn text-muted" id="tabSettlement2" aria-expanded="false">
                    <com-maintenance-table :maintenances="maintenances" :list_type="list_type"></com-maintenance-table>
                </div>
                <div class="tab-pane animated fadeIn text-muted" id="tabSettlement3" aria-expanded="false">
                    <com-maintenance-table :maintenances="maintenances" :list_type="list_type"></com-maintenance-table>
                </div>
            </div>
        </div>
        <div>
            <ul id="maintenance-pagination" class="pull-right"></ul>
        </div>
    </div>
</template>

<script>
    import {mapState} from 'vuex'
    export default {
        data(){
            return {
                list_type: null,
                queryFilter: {},
                maintenances: [],
                user: JSON.parse(sessionStorage.getItem('user')) || {},
                user_category: null,
            }
        },
        computed: {
            list_type(){
                return this.$route.params.type;
            }
        },
        mounted(){
            if (['1', '3', '4', '5'].indexOf(this.user.category) > -1) {
                this.user_category = 'merchant';
            } else if (['0', '2', '6'].indexOf(this.user.category) > -1) {
                this.user_category = 'service';
            }
            $('.fixTime').datetimepicker({
                language: 'zh-CN',
                format: 'yyyy-mm-dd hh:ii',
                autoclose: true,
                clearBtn: true,
                minView: 0,
                todayHighlight: true,
            });
            this.maintenances = [];
        },
        methods: {
            setPagination(currentPage, totalPage) {
                var scope = this;
                var $pagination = $('#maintenance-pagination');
                $pagination.twbsPagination('destroy');
                $pagination.twbsPagination({
                    first: "第一页",
                    prev: "上一页",
                    next: "下一页",
                    last: "最后一页",
                    totalPages: totalPage,
                    visiblePages: 10,
                    startPage: currentPage,
                    initiateStartPageClick: false,
                    onPageClick: function (event, page) {
                        scope.queryFilter.page = page;
                        scope.getMaintenanceList();
                    }
                });
            },
            search(q){
                this.maintenances = [];
                this.queryFilter.page = 1;
                this.queryFilter.q = q;
                this.getMaintenanceList()
            },
            getMaintenanceList(status){
                var scope = this;
                //维修单状态 -1：取消 0：新维修单 1：接单或者出发中 2：已经完成  3:到店  4:维修失败 5:填写修单未确认 6:为暂停 7.被返修
                var statusChoiceDict = {
                    'new': '0',
                    'fixing': '1,3,5,6',
                    'done': '-1,2,4,7'
                };
                var statusText = {
                    '-1': '取消',
                    '0': '新维修单',
                    '1': '接单或者出发中',
                    '2': '已经完成',
                    '3': '到店',
                    '4': '维修失败',
                    '5': '填写修单未确认',
                    '6': '为暂停',
                    '7': '被返修',
                }
                if (status) {
                    this.maintenances = [];
                    this.queryFilter.page = 1;
                    this.queryFilter.status = statusChoiceDict[status] || status;
                }
                $.ajax({
                    type: 'GET',
                    url: global.API_HOST + '/maintenance/list',
                    data: this.queryFilter,
                }).done(function (res) {
                    if (res.status == 1) {
                        var results = res.info.results;
                        var meta = res.info.meta;
                        results = results.map(function (e) {
                            e.checked = false;
                            return e;
                        });
                        if (results.length) {
                            scope.setPagination(meta.currentPage, meta.totalPage);
                        }
                        scope.maintenances = results;
                        scope.maintenances.map(function (e) {
                            e.status = statusText[e.status];
                        });
                    }
                    else {
                        toastr.warning(res.alert);
                    }
                });
            },
            batchOp(item) {
                var scope = this;
                var ids = this.maintenances.filter(function (e) {
                    return e.checked;
                }).map(function (e) {
                    return e.id;
                });

                if (!ids.length) {
                    return;
                }

                $.ajax({
                    type: 'POST',
                    url: global.API_HOST + '/maintenance/batchOp',
                    data: {ids: ids.join(','), type: item, user_id: this.user.id},
                }).done(function (res) {
                    if (res.status == 1) {
                        scope.getMaintenanceList();
                        toastr.info('操作成功');
                    }
                    else {
                        toastr.warning(res.alert);
                    }
                });

            }
        }
    }
</script>