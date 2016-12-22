<template>
    <div class="row" id="maintenance-info">
        <div class="col-md-12">
            <app-breadcrumb :breadcrumb="breadcrumb"></app-breadcrumb>
            <!--<div ui-include="'/static/views/htmls/detail-breadcrumb.html'"></div>-->
        </div>
        <div class="col-md-3 pull-right sidebar">
            <div class="b-t b-r b-b box store ">
                <div class="box-body text-center">
                    <div class="m-t-md m-b">
                        <span class="avatar w-96">
                            <img src="http://">
                            <i class="busy b-white right"></i>
                        </span>
                    </div>
                    <h6 v-text="store.name"></h6>
                    <p class="text-muted text-sm m-a">
                        编号&nbsp; <span v-text="store.no"></span>
                        <br>
                        <span v-text="store.mobile || store.phone || store.tel"></span>
                        <br>
                        <span v-text="store.address"></span>
                    </p>
                    <div class="form-group m-t-md">
                        <a class="btn form-control dark lt">查看详情</a>
                    </div>
                </div>
                <hr>
                <div class="box-body text-center">
                    <div class="m-t-md m-b">
                        <span class="avatar w-96">
                            <img v-bind:src="fixer.avatar_img">
                            <i class="busy b-white right"></i>
                        </span>
                    </div>
                    <h6><span v-text="fixer.screen_name"></span></h6>
                    <p class="m-a">
                    <div class="text-muted text-sm"><span v-text="fixer.title"></span></div>
                    <div class="text-muted text-sm"><span v-text="fixer.mobile"></span></div>
                    <div class="text-muted text-sm m-t-sm"><span class="" v-text="fixer.company"></span></div>
                    </p>
                    <div class="form-group m-t-md">
                        <a class="btn form-control dark"><span class="lt">转服务商</span></a>
                    </div>
                </div>
                <hr>
                <div class="box-body">
                    <com-maintenance-history :id="maintenance.id"></com-maintenance-history>
                </div>
            </div>
        </div>

        <div class="col-md-9 detail">
            <div class="box">
                <div class="box-header dker">
                    <h3>报修信息</h3>
                </div>
                <div class="box-body m-t clearfix">
                    <div class="row" v-for="row in infoTable">
                        <div class="col-md-4">
                            <div class="pull-right">
                                <p class="text-muted" v-text="row.label"></p>
                            </div>
                        </div>
                        <div class="col-md-8">
                            <div class="pull-left">
                                <p v-text="row.text"></p>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-8 col-md-push-4 m-t-sm m-b">
                        <div>
                            <span v-for="img in this.maintenance.logo">
                                <img class="img-rounded" alt="" src="" width="64" height="64"
                                     data-toggle="modal" data-target="#img-$index" ui-toggle-class="zoom"
                                     ui-target="#animate">
                                &nbsp;&nbsp;

                                <!-- .modal -->
                                <div id="img-$index" class="modal fade animate">
                                  <div class="modal-dialog" id="animate">
                                    <div class="modal-content">

                                      <div class="modal-body text-center p-lg">
                                        <img class="img-rounded" alt="" src="img">
                                      </div>
                                    </div><!-- /.modal-content -->
                                  </div>
                                </div>
                                <!-- / .modal -->
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="box">
                <div class="box-header dker">
                    <h3>维修情况</h3>
                </div>
                <div class="box-body">
                    <div id="fees">
                        <div class="row m-t-xs">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">零配件更换</p>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <p>￥<input type="number" v-model="spare_fee"></p>
                                </div>
                            </div>
                        </div>
                        <div class="row m-t-xs">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">人工费</p>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <p>￥<input type="number" v-model="labor_fee"></p>
                                </div>
                            </div>
                        </div>
                        <div class="row m-t-xs">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">交通费</p>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <p>￥<input type="number" v-model="transport_fee"></p>
                                </div>
                            </div>
                        </div>
                        <div class="row m-t-xs">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">住宿费</p>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <p>￥<input type="number" v-model="house_fee"></p>
                                </div>
                            </div>
                        </div>
                        <div class="row m-t-xs">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">快递费</p>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <p>￥<input type="number" v-model="delivery_fee"></p>
                                </div>
                            </div>
                        </div>

                        <div class="row m-t-xs">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <h5 class="text-muted">合计</h5>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <h5 class="text-orange" v-text="totalFee"></h5>
                                </div>
                            </div>
                        </div>
                    </div>
                    <hr>
                    <div class="row padding">
                        <div class="col-md-4">
                            <div class="pull-right">
                            <span class="avatar w-64">
                                <img src="fixer.avatar_img" alt="...">
                                <i class="busy b-white right"></i>
                            </span>
                            </div>
                        </div>
                        <div class="col-md-8">
                            <div class="pull-left">
                                <span>
                                    <h5 v-text="fixer.screen_name">
                                        &nbsp; &nbsp; &nbsp; &nbsp;
                                        <span class="text-muted">维修</span>
                                    </h5>
                                    <span class="text-muted p-t" v-text="fixer.mobile"></span>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="box">
                <div class="box-header dker">
                    <h3>商户</h3>
                </div>
                <div class="box-body">
                    <div class="row padding">
                        <div class="col-md-4">
                            <div class="pull-right">
                            <span class="avatar w-64">
                                <img src="reporter.avatar_img" alt="...">
                                <i class="busy b-white right"></i>
                            </span>
                            </div>
                        </div>
                        <div class="col-md-8">
                            <div class="pull-left">
                            <span>
                                <h5 v-text="reporter.screen_name">&nbsp; &nbsp; &nbsp; &nbsp;
                                    <span class="text-muted">报修</span>
                                </h5>
                                <span class="text-muted p-t" v-text="reporter.mobile">
                                </span>
                            </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="box" v-if="maintenance.status == 2">
                <div class="box-header dker">
                    <h3>审核结算</h3>
                </div>
                <div class="box-body">
                    <div class="row padding">
                        <div class="col-md-4"></div>
                        <div class="col-md-8">
                            <button class="b-a b-grey btn btn-xs rounded disabled" v-if="maintenance.settlement >= 1">
                                服务商审核
                            </button>
                            <button class="btn btn-xs rounded text-white opacity" v-else>服务商审核</button>
                            <span class="inline b-t b-t-dark"
                                  style="width: 15%; height: 4px; margin-left:-4px; margin-right:-4px;"></span>
                            <button class="b-a b-grey btn btn-xs rounded disabled" v-if="maintenance.settlement >= 2">
                                商户审核
                            </button>
                            <button class="btn btn-xs rounded text-white opacity" v-else>商户审核</button>
                            <span class="inline b-t b-t-dark"
                                  style="width: 15%; height: 4px; margin-left:-4px; margin-right:-4px;"></span>
                            <button class="b-a b-grey btn btn-xs rounded disabled" v-if="maintenance.settlement >= 3">
                                工单结算
                            </button>
                            <button class="btn btn-xs rounded text-white opacity" v-else>工单结算</button>
                        </div>
                    </div>
                    <div class="row padding">
                        <div class="col-md-4">
                            <div class="p-r text-right text-muted">服务商审核工单</div>
                        </div>
                        <div class="col-md-8" v-show="is_store && maintenance.settlement<1">
                            正在审核当前工单
                        </div>
                        <div class="col-md-8" v-show="is_repair && maintenance.settlement<1">
                            <label class="radio-inline">
                                <input type="radio" name="inlineRadioOptions" value="1"
                                       class="has-value" v-model="audit_repair_result"> 审核通过
                            </label>
                            <label class="radio-inline">
                                <input type="radio" name="inlineRadioOptions" value="0"
                                       v-model="audit_repair_result"> 审核不通过
                            </label>
                            <textarea class="form-control m-t" rows="2" placeholder="请填写备注信息"
                                      v-model="audit_repair_note"></textarea>
                            <div class="m-t-md p-t-xs">
                                <small class="text-muted">提示: 您可在当前页面保存审核结果, 再返回列表页选择多张工单批量审核</small>
                            </div>
                            <div class="m-t-sm">
                                <button class="btn btn-xs btn-fw dark" v-if="audit_repair_result"
                                        @click="save_repair_audit">仅保存结果
                                </button>
                                <button class="btn btn-xs btn-fw dark" disabled v-else>仅保存结果</button>
                                <button class="btn btn-xs btn-fw text-white p-x-md m-l-sm" @click="submit_repair_audit"
                                        v-if="audit_repair_result">提交审核
                                </button>
                                <button class="btn btn-xs btn-fw text-white p-x-md m-l-sm" disabled v-else>提交审核</button>
                            </div>
                        </div>
                        <div class="col-md-8" v-show="maintenance.settlement >= 1">
                            <div class="col-md-4">
                                <div>
                                    <span class="m-r"><i class="fa fa-check-circle text-orange m-r-xs"></i>服务商已审核
                                        <small class="text-success" v-if="maintenance.audit_repair_result">通过</small>
                                        <small class="text-danger" v-else>不通过</small>
                                    </span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <span v-text="maintenance.audit_repair_user.name"></span> /
                                <span class="text-muted" v-text="maintenance.audit_repair_user.mobile"></span>
                            </div>
                            <div class="col-md-4" v-text="maintenance.audit_repair_date"></div>
                            <div class="col-md-12" v-text="maintenance.audit_repair_note"></div>
                        </div>
                    </div>

                    <div class="row p-l p-r">
                        <hr>
                    </div>

                    <div class="row padding" v-if="maintenance.settlement >= 1">
                        <div class="col-md-4">
                            <div class="p-r text-right text-muted">商户审核工单</div>
                        </div>
                        <div class="col-md-8" v-show="is_repair && maintenance.settlement < 2">
                            正在审核当前工单
                        </div>
                        <div class="col-md-8" v-show="is_store && maintenance.settlement < 2">
                            <label class="radio-inline">
                                <input type="radio" name="inlineRadioOptions" value="1"
                                       class="has-value" v-model="audit_merchant_result"> 审核通过
                            </label>
                            <label class="radio-inline">
                                <input type="radio" name="inlineRadioOptions" value="0"
                                       v-model="audit_merchant_result"> 审核不通过
                            </label>
                            <textarea class="form-control m-t" rows="2" placeholder="请填写备注信息"
                                      v-model="audit_merchant_note"></textarea>
                            <div class="m-t-md p-t-xs">
                                <small class="text-muted">提示: 您可在当前页面保存审核结果, 再返回列表页选择多张工单批量审核</small>
                            </div>
                            <div class="m-t-sm">
                                <button class="btn btn-xs btn-fw dark" v-if="audit_merchant_result"
                                        @click="save_merchant_audit">仅保存结果
                                </button>
                                <button class="btn btn-xs btn-fw dark" disabled v-else>仅保存结果</button>
                                <button class="btn btn-xs btn-fw text-white p-x-md m-l-sm"
                                        @click="submit_merchant_audit" v-if="audit_merchant_result">提交审核
                                </button>
                                <button class="btn btn-xs btn-fw text-white p-x-md m-l-sm" disabled v-else>提交审核</button>
                            </div>
                        </div>
                        <div class="col-md-8" v-show="maintenance.settlement >= 2">
                            <div class="col-md-4">
                                <div>
                                    <span class="m-r"><i class="fa fa-check-circle text-orange m-r-xs"></i>商户已审核
                                        <small class="text-success" v-if="maintenance.audit_merchant_result">通过</small>
                                        <small class="text-danger" v-else>不通过</small>
                                    </span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <span v-text="maintenance.audit_merchant_user.name"></span> /
                                <span class="text-muted" v-text="maintenance.audit_merchant_user.mobile"></span>
                            </div>
                            <div class="col-md-4" v-text="maintenance.audit_merchant_date"></div>
                            <div class="col-md-12" v-text="maintenance.audit_merchant_note"></div>
                        </div>
                    </div>

                    <div class="row p-l p-r" v-if="maintenance.settlement >= 1">
                        <hr>
                    </div>

                    <div class="row padding" v-if='maintenance.settlement>=2'>
                        <div class="col-md-4">
                            <div class="p-r text-right text-muted">结算</div>
                        </div>
                        <div class="col-md-8">
                            <div class="row m-b" v-if="maintenance.settle_repair_result">
                                <div class="col-md-4">
                                    <span class="m-r"><i class="fa fa-check-circle text-orange m-r-xs"></i>服务商已结算</span>
                                </div>
                                <div class="col-md-4">
                                    <span v-text="maintenance.settle_repair_user.name"></span> /
                                    <span class="text-muted" v-text="maintenance.settle_repair_user.mobile"></span>
                                </div>
                                <div class="col-md-4" v-text="maintenance.settle_repair_date"></div>
                                <div class="col-md-12" v-text="maintenance.settle_repair_note"></div>
                            </div>
                            <div class="row m-b" v-if="maintenance.settle_merchant_result">
                                <div class="col-md-4">
                                    <span class="m-r"><i class="fa fa-check-circle text-orange m-r-xs"></i>商户已结算</span>
                                </div>
                                <div class="col-md-4">
                                    <span v-text="maintenance.settle_merchant_user.name"></span> /
                                    <span class="text-muted" v-text="maintenance.settle_merchant_user.mobile"></span>
                                </div>
                                <div class="col-md-4" v-text="maintenance.settle_merchant_date"></div>
                                <div class="col-md-12" v-text="maintenance.settle_merchant_note"></div>
                            </div>
                            <div v-if="(is_store && !maintenance.settle_merchant_result) || (is_repair && !maintenance.settle_repair_result)">
                                <div>
                                    <label class="md-check">
                                        <input type="checkbox" class="has-value" v-model="settle_result">
                                        <i class="indigo"></i>
                                        <span class="text-muted">本工单已结算</span>
                                    </label>
                                </div>
                                <textarea class="form-control m-t" rows="2" placeholder="请填写备注信息"
                                          v-model="settle_note"></textarea>
                                <div class="m-t-md p-t-xs">
                                    <small class="text-muted">提示: 您可在当前页面保存结算结果, 再返回列表页选择多张工单批量结算</small>
                                </div>
                                <div class="m-t-sm">
                                    <button class="btn btn-xs btn-fw dark" v-if="settle_result"
                                            @click="save_settlement">仅保存结果
                                    </button>
                                    <button class="btn btn-xs btn-fw dark" disabled v-else>仅保存结果</button>
                                    <button class="btn btn-xs btn-fw text-white p-x-md m-l-sm" @click="settle"
                                            v-if="settle_result">结算工单
                                    </button>
                                    <button class="btn btn-xs btn-fw text-white p-x-md m-l-sm" disabled v-else>结算工单
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapState} from 'vuex'
    import appBreadcrumb from '../../component/app-breadcrumb.vue'

    export default {
        computed: {
            infoTable: function () {
                return [
                    {'label': '资产', 'text': this.maintenance.device && this.maintenance.device.name},
                    {'label': '固定资产编号', 'text': this.maintenance.device && this.maintenance.device.uid},
                    {'label': '维修时效', 'text': this.maintenance && this.maintenance.must_time},
                    {'label': '故障现象', 'text': this.maintenance && this.maintenance.content},
                ]
            },
            fixer: function () {
                return {
                    'company': this.maintenance.grab_user && this.maintenance.grab_user.company,
                    'screen_name': this.maintenance.grab_user && this.maintenance.grab_user.name,
                    'mobile': this.maintenance.grab_user && this.maintenance.grab_user.mobile,
                }
            },
            reporter: function () {
                return {
                    'screen_name': this.maintenance.user && this.maintenance.user.name,
                    'mobile': this.maintenance.user && this.maintenance.user.mobile,
                }
            },
            totalFee: function () {
                return (this.spare_fee || 0) + (this.labor_fee || 0) + (this.transport_fee || 0) + (this.house_fee || 0) + (this.delivery_fee || 0);
            },
        },
        data () {
            return {
                breadcrumb: [
                    {'title': '首页'},
                    {'title': '维修'},
                    {'title': '维修工单'},
                ],
                store: {},
                maintenance: {},
                spare_fee: 0,
                labor_fee: 0,
                transport_fee: 0,
                house_fee: 0,
                delivery_fee: 0,
                user: JSON.parse(sessionStorage.getItem('user')) || {},
                audit_repair_result: null,
                audit_repair_note: '',
                audit_merchant_result: null,
                audit_merchant_note: '',
                settle_result: false,
                settle_note: '',
                is_store: false,
                is_repair: false,
            }
        },
        created: function () {
            this.is_store = ['1', '3', '4', '5', '7'].indexOf(this.user.category) > -1;
            this.is_repair = ['0', '2', '6', '7'].indexOf(this.user.category) > -1;

            var id = this.$route.params.id;
            var url = global.API_HOST + '/maintenance/' + id;
            var scope = this;
            $.getJSON(url, {}, function (data) {
                scope.maintenance = data;
                scope.store = scope.maintenance.store;

                scope.audit_repair_result = scope.maintenance['audit_repair_result_save'];
                scope.audit_repair_note = scope.maintenance['audit_repair_note_save'];
                scope.audit_merchant_result = scope.maintenance['audit_merchant_result_save'];
                scope.audit_merchant_note = scope.maintenance['audit_merchant_note_save'];

                if(scope.is_store) {
                    scope.settle_result = scope.maintenance['settle_merchant_result_save'];
                    scope.settle_note = scope.maintenance['settle_merchant_note_save'];
                }

                if(scope.is_repair) {
                    scope.settle_result = scope.maintenance['settle_repair_result_save'];
                    scope.settle_note = scope.maintenance['settle_repair_note_save'];
                }

            });
        },
        methods: {
            submit_repair_audit() {
                var scope = this;
                var data = {
                    audit_repair_result: this.audit_repair_result,
                    audit_repair_note: this.audit_repair_note,
                    user_id: this.user.id,
                };
                $.ajax({
                    type: 'POST',
                    url: global.API_HOST + '/maintenance/' + this.maintenance.id + '/audit/repair',
                    data: data,
                    crossDomain: true,
                }).done(function (data) {
                    if (data) {
                        scope.maintenance = data;
                    }
                });
            },
            submit_merchant_audit() {
                var scope = this;
                var data = {
                    audit_merchant_result: this.audit_merchant_result,
                    audit_merchant_note: this.audit_merchant_note,
                    user_id: this.user.id,
                };
                $.ajax({
                    type: 'POST',
                    url: global.API_HOST + '/maintenance/' + this.maintenance.id + '/audit/merchant',
                    data: data,
                    crossDomain: true,
                }).done(function (data) {
                    if (data) {
                        scope.maintenance = data;
                    }
                });
            },
            settle(){
                var scope = this;
                var data = {
                    settle_note: this.settle_note,
                    user_id: this.user.id,
                };
                $.ajax({
                    type: 'POST',
                    url: global.API_HOST + '/maintenance/' + this.maintenance.id + '/settlement',
                    data: data,
                    crossDomain: true,
                }).done(function (data) {
                    if (data) {
                        scope.maintenance = data;
                    }
                });
            },
            save_repair_audit(){
                var scope = this;
                var data = {
                    audit_repair_result: this.audit_repair_result,
                    audit_repair_note: this.audit_repair_note,
                    user_id: this.user.id,
                };
                $.ajax({
                    type: 'POST',
                    url: global.API_HOST + '/maintenance/' + this.maintenance.id + '/audit/repair/save',
                    data: data,
                    crossDomain: true,
                }).done(function (data) {
                    if (data) {
                        scope.maintenance = data;
                        toastr.info('保存成功');
                    }
                });
            },
            save_merchant_audit(){
                var scope = this;
                var data = {
                    audit_merchant_result: this.audit_merchant_result,
                    audit_merchant_note: this.audit_merchant_note,
                    user_id: this.user.id,
                };
                $.ajax({
                    type: 'POST',
                    url: global.API_HOST + '/maintenance/' + this.maintenance.id + '/audit/merchant/save',
                    data: data,
                    crossDomain: true,
                }).done(function (data) {
                    if (data) {
                        scope.maintenance = data;
                        toastr.info('保存成功');
                    }
                });

            },
            save_settlement(){
                var scope = this;
                var data = {
                    settle_note: this.settle_note,
                    user_id: this.user.id,
                };
                $.ajax({
                    type: 'POST',
                    url: global.API_HOST + '/maintenance/' + this.maintenance.id + '/settlement/save',
                    data: data,
                    crossDomain: true,
                }).done(function (data) {
                    if (data) {
                        scope.maintenance = data;
                        toastr.info('保存成功');
                    }
                });
            },
        },
        components: {
            appBreadcrumb,
        },
    }
</script>

<style>
    #maintenance-info .box {
        margin-bottom: 0;
    }

    #maintenance-info .detail {
        padding-right: 0;
    }

    #maintenance-info .sidebar {
        margin-top: 1px;
        padding-left: 0;
    }

    #maintenance-info #fees input {
        border: none;
    }
</style>