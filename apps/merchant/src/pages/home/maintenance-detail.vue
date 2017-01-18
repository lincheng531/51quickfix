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

    #maintenance-info #fees .input-group-addon {
        border-right: none;
    }

    #maintenance-info #fees .input-group input {
        border-left: none;
    }
</style>
<template>
    <div class="row" id="maintenance-info">
        <div class="col-md-12">
            <div class="pull-right m-t-md text-muted">编号：<span v-text="maintenance.code"></span></div>
            <app-breadcrumb class="w-lg" :breadcrumb="breadcrumb"></app-breadcrumb>
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
                    <com-maintenance-history :status_list="status_list"></com-maintenance-history>
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
                            <span v-for="img in maintenance.logo">
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
                    <div id="fees" v-if="billEdit">
                        <div class="row m-t-xs">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">上门费</p>
                                </div>
                            </div>
                            <div class="col-md-5">
                                <div class="pull-left">
                                    <div class="input-group m-b w-sm">
                                        <span class="input-group-addon">￥</span>
                                        <input type="number" class="form-control" placeholder="0.00"
                                               @keyup="changeBill(billForm.visit)" v-model="billForm.visit">
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <a class="pull-right text-muted m-r-sm" @click="addFeeItem">
                                    <i class="fa fa-plus m-r-xs opacity"></i>添加其他费用
                                </a>
                            </div>
                        </div>

                        <div class="row m-t-xs">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">零配件更换</p>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <p>￥<span type="number"
                                              v-text="billForm.spare_total"></span></p>
                                </div>
                            </div>
                        </div>
                        <div class="row m-t-xs" v-if="billForm.labor">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">人工费</p>
                                </div>
                            </div>
                            <div class="col-md-5">
                                <div class="pull-left">
                                    <div class="input-group m-b">
                                        <span class="input-group-addon">￥</span>
                                        <input type="number" class="form-control" placeholder="0.00"
                                               @keyup="changeBill(billForm.labor)" v-model="billForm.labor">
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="row m-t-xs" v-if="billForm.travel">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">交通费</p>
                                </div>
                            </div>
                            <div class="col-md-5">
                                <div class="pull-left">
                                    <div class="input-group m-b">
                                        <span class="input-group-addon">￥</span>
                                        <input type="number" class="form-control" placeholder="0.00"
                                               @keyup="changeBill(billForm.travel)" v-model="billForm.travel">
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="row m-t-xs" v-if="billForm.stay_total">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">住宿费</p>
                                </div>
                            </div>
                            <div class="col-md-5">
                                <div class="pull-left">
                                    <div class="input-group m-b">
                                        <span class="input-group-addon">￥</span>
                                        <input type="number" class="form-control" placeholder="0.00"
                                               @keyup="changeBill(billForm.stay_total)" v-model="billForm.stay_total">
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="row m-t-xs" v-for="(item, index) in otherFees">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <input type="text text-right" class="form-control w r text-muted"
                                           placeholder="请输入花费原因" v-model="item.key" @keyup="changeBill(item.value)">
                                </div>
                            </div>
                            <div class="col-md-5">
                                <div class="pull-left">
                                    <div class="input-group m-b">
                                        <span class="input-group-addon">￥</span>
                                        <input type="number" class="form-control" placeholder="0.00"
                                               v-model="item.value"
                                               @keyup="changeBill(item.value)">
                                    </div>
                                </div>
                            </div>

                            <div class="col-md-3">
                                <a class="pull-right text-muted m-r-lg m-t-sm" @click="removeFeeItem(index)"><i
                                        class="fa fa-remove"></i></a>
                            </div>
                        </div>


                        <div class="row m-t-xs">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">优惠金额</p>
                                </div>
                            </div>
                            <div class="col-md-5">
                                <div class="pull-left">
                                    <div class="input-group m-b">
                                        <span class="input-group-addon">-￥</span>
                                        <input type="number" class="form-control" placeholder="0.00"
                                               @keyup="changeBill(billForm.discount)" v-model="billForm.discount">
                                    </div>
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
                                    <h5 class="text-orange" v-text="billFormTotal"></h5>
                                </div>
                            </div>
                        </div>

                        <div class="row m-t-md"
                             v-if="maintenance.bill && maintenance.bill.spare && maintenance.bill.spare.length">
                            <div id="spare-specifications" class="p-a-sm">
                                <table class="table table-striped table-hover b-a">
                                    <thead class="text-white" style="background-color: #374256;">
                                    <tr>
                                        <th>零配件</th>
                                        <th>编号</th>
                                        <th>损坏类型</th>
                                        <th>保固截止日期</th>
                                        <th>状态</th>
                                        <th>单价</th>
                                        <th>数量</th>
                                        <th>费用</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr v-for="item in ((maintenance.bill || {}).spare || [])">
                                        <td v-text="item.name"></td>
                                        <td v-text="item.no"></td>

                                        <td v-text="item.no"></td>
                                        <td v-text="item.no"></td>
                                        <td v-text="item.no"></td>

                                        <td v-text="item.price"></td>
                                        <td v-text="item.count"></td>
                                        <td v-text="item.total"></td>
                                    </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <!-- ---------------------------------- 以上是费用编辑 ----------------------------------------->
                    <div id="fees" v-else>
                        <div class="row m-t-xs">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">上门费</p>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <p>￥<span v-text="maintenance.bill && maintenance.bill.visit"></span></p>
                                </div>
                                <a class="pull-right text-muted m-r-sm" @click="billEdit=true" v-if="is_repair">
                                    <i class="fa fa-edit m-r-xs opacity"></i>编辑
                                </a>
                            </div>
                        </div>
                        <div class="row m-t-xs">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">零配件更换</p>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <p>￥<span v-text="maintenance.bill && maintenance.bill.spare_total"></span></p>
                                </div>
                            </div>
                        </div>
                        <div class="row m-t-xs" v-if="maintenance.bill && maintenance.bill.labor">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">人工费</p>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <p>￥<span v-text="maintenance.bill && maintenance.bill.labor"></span>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="row m-t-xs" v-if="maintenance.bill && maintenance.bill.travel">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">交通费</p>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <p>￥<span v-text="maintenance.bill && maintenance.bill.travel"></span>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="row m-t-xs" v-if="maintenance.bill && maintenance.bill.stay_total">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">住宿费</p>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <p>￥<span v-text="maintenance.bill && maintenance.bill.stay_total"></span></p>
                                </div>
                            </div>
                        </div>

                        <div class="row m-t-xs" v-for="item in ((maintenance.bill || {}).others || [])">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted" v-text="item.msg"></p>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <p>￥<span v-text="item.total"></span></p>
                                </div>
                            </div>
                        </div>

                        <div class="row m-t-xs" v-if="maintenance.bill && maintenance.bill.discount">
                            <div class="col-md-4">
                                <div class="pull-right">
                                    <p class="text-muted">优惠金额</p>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="pull-left">
                                    <p>-￥<span v-text="maintenance.bill && maintenance.bill.discount"></span></p>
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
                                    <h5 class="text-orange"
                                        v-text="maintenance.bill && maintenance.bill.total"></h5>
                                </div>
                            </div>
                        </div>

                        <div class="row m-t-md"
                             v-if="maintenance.bill && maintenance.bill.spare && maintenance.bill.spare.length">
                            <div id="spare-specifications" class="p-a-sm">
                                <table class="table table-striped table-hover b-a">
                                    <thead class="text-white" style="background-color: #374256;">
                                    <tr>
                                        <th>零配件</th>
                                        <th>编号</th>
                                        <th>损坏类型</th>
                                        <th>保固截止日期</th>
                                        <th>状态</th>
                                        <th>单价</th>
                                        <th>数量</th>
                                        <th>费用</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr v-for="item in ((maintenance.bill || {}).spare || [])">
                                        <td v-text="item.name"></td>
                                        <td v-text="item.no"></td>
                                        <td>
                                            <span v-if="item.category==1">自然</span>
                                            <span v-if="item.category==0">人为</span>
                                        </td>

                                        <td v-text="item.guarantee_time"></td>
                                        <td>
                                            <span v-if="item.status">保固</span>
                                            <span v-else>非保固</span>
                                        </td>

                                        <td v-text="item.price"></td>
                                        <td v-text="item.count"></td>
                                        <td v-text="item.total"></td>
                                    </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <div class="row p-t p-b" v-if="billEdit">
                        <div class="text-center">
                            <button class="btn btn-xs btn-fw dark m-r-sm" @click="updateBill">保存修改</button>
                            <button class="btn btn-xs btn-fw dark m-l-sm" @click="billEdit=false">取消</button>
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
                            <button class="b-a b-grey btn btn-xs rounded disabled"
                                    v-if="maintenance.settlement >= 1">
                                服务商审核
                            </button>
                            <button class="btn btn-xs rounded text-white opacity" v-else>服务商审核</button>
                            <span class="inline b-t b-t-dark"
                                  style="width: 15%; height: 4px; margin-left:-4px; margin-right:-4px;"></span>
                            <button class="b-a b-grey btn btn-xs rounded disabled"
                                    v-if="maintenance.settlement >= 2">
                                商户审核
                            </button>
                            <button class="btn btn-xs rounded text-white opacity" v-else>商户审核</button>
                            <span class="inline b-t b-t-dark"
                                  style="width: 15%; height: 4px; margin-left:-4px; margin-right:-4px;"></span>
                            <button class="b-a b-grey btn btn-xs rounded disabled"
                                    v-if="maintenance.settlement >= 3">
                                工单结算
                            </button>
                            <button class="btn btn-xs rounded text-white opacity" v-else>工单结算</button>
                        </div>
                    </div>
                    <div class="row padding">
                        <div class="col-md-4">
                            <div class="p-r text-right text-muted">服务商审核工单</div>
                        </div>
                        <div class="col-md-8"
                             v-show="is_store && (!maintenance.settlement || maintenance.settlement<1)">
                            正在审核当前工单
                        </div>
                        <div class="col-md-8"
                             v-show="is_repair && (!maintenance.settlement || maintenance.settlement<1)">
                            <label class="radio-inline">
                                <input type="radio" name="inlineRadioOptions" value="1"
                                       class="has-value" v-model="audit_repair_result"> 核对无误，审核通过
                            </label>
                            <label class="radio-inline">
                                <input type="radio" name="inlineRadioOptions" value="0"
                                       v-model="audit_repair_result"> 工单有争议，审核失败
                            </label>
                            <textarea class="form-control m-t" rows="2" placeholder="请填写备注信息"
                                      v-model="audit_repair_note"></textarea>
                            <div class="m-t-md p-t-xs">
                                <small class="text-muted">提示: 确定审核结果后，工单将进入"<strong
                                        class="text-orange">维修/费用审核/待提交列表</strong>"，可批量提交至商户。
                                </small>
                            </div>
                            <div class="m-t-sm">
                                <button class="btn btn-xs btn-fw dark" v-if="audit_repair_result"
                                        @click="save_repair_audit">确定
                                </button>
                                <button class="btn btn-xs btn-fw dark" disabled v-else>确定</button>
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
                            <!--
                            <div class="m-t-md p-t-xs">
                                <small class="text-muted">提示: 您可在当前页面保存审核结果, 再返回列表页选择多张工单批量审核</small>
                            </div>-->
                            <div class="m-t-sm">
                                <!--
                                <button class="btn btn-xs btn-fw dark" v-if="audit_merchant_result"
                                        @click="save_merchant_audit">仅保存结果
                                </button>
                                <button class="btn btn-xs btn-fw dark" disabled v-else>仅保存结果</button>
                                <button class="btn btn-xs btn-fw text-white p-x-md m-l-sm"
                                        @click="submit_merchant_audit" v-if="audit_merchant_result">提交
                                </button>
                                <button class="btn btn-xs btn-fw text-white p-x-md m-l-sm" disabled v-else>提交</button>-->
                                <button class="btn btn-xs btn-fw dark" v-if="audit_merchant_result"
                                        @click="submit_merchant_audit">提交
                                </button>
                                <button class="btn btn-xs btn-fw dark" disabled v-else>提交</button>
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

                    <div class="row padding"
                         v-if='maintenance.settlement>=2 && maintenance.audit_repair_result && maintenance.audit_merchant_result'>
                        <div class="col-md-4">
                            <div class="p-r text-right text-muted">结算</div>
                        </div>
                        <div class="col-md-8">
                            <div class="row m-b" v-if="maintenance.settle_repair_result">
                                <div class="col-md-4">
                                        <span class="m-r"><i
                                                class="fa fa-check-circle text-orange m-r-xs"></i>服务商已结算</span>
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
                                        <span class="m-r"><i
                                                class="fa fa-check-circle text-orange m-r-xs"></i>商户已结算</span>
                                </div>
                                <div class="col-md-4">
                                    <span v-text="maintenance.settle_merchant_user.name"></span> /
                                    <span class="text-muted"
                                          v-text="maintenance.settle_merchant_user.mobile"></span>
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
                                <!--
                                <div class="m-t-md p-t-xs">
                                    <small class="text-muted">提示: 您可在当前页面保存结算结果, 再返回列表页选择多张工单批量结算</small>
                                </div>-->
                                <div class="m-t-sm">
                                    <!--
                                    <button class="btn btn-xs btn-fw dark" v-if="settle_result"
                                            @click="save_settlement">仅保存结果
                                    </button>
                                    <button class="btn btn-xs btn-fw dark" disabled v-else>仅保存结果</button>
                                    <button class="btn btn-xs btn-fw text-white p-x-md m-l-sm" @click="settle"
                                            v-if="settle_result">结算工单
                                    </button>
                                    <button class="btn btn-xs btn-fw text-white p-x-md m-l-sm" disabled v-else>结算工单
                                    </button>-->
                                    <button class="btn btn-xs btn-fw dark" v-if="settle_result"
                                            @click="settle">提交
                                    </button>
                                    <button class="btn btn-xs btn-fw dark" disabled v-else>提交</button>
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
            _billFormTotal(){
                return (this.billForm.visit || 0) +
                        (this.billForm.spare_total || 0) +
                        (this.billForm.labor || 0) +
                        (this.billForm.travel || 0) +
                        (this.billForm.stay_total || 0);
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
                status_list: [],
                spare_fee: 0,
                labor_fee: 0,
                transport_fee: 0,
                house_fee: 0,
                user: JSON.parse(sessionStorage.getItem('user')) || {},
                audit_repair_result: null,
                audit_repair_note: '',
                audit_merchant_result: null,
                audit_merchant_note: '',
                settle_result: false,
                settle_note: '',
                is_store: false,
                is_repair: false,
                billEdit: false,
                billForm: {},
                otherFees: [],
                billFormTotal: 0,
            }
        },
        created: function () {
            this.is_store = ['1', '3', '4', '5', '7'].indexOf(this.user.category) > -1;
            this.is_repair = ['0', '2', '6', '7'].indexOf(this.user.category) > -1;
            this.getDetail();
        },
        methods: {
            getDetail(){
                var id = this.$route.params.id;
                var url = global.API_HOST + '/maintenance/' + id;
                var scope = this;
                $.getJSON(url, {}, function (data) {
                    scope.status_list = data.status_list;
                    scope.maintenance = data;
                    scope.store = scope.maintenance.store;

                    scope.audit_repair_result = scope.maintenance['audit_repair_result_save'];
                    scope.audit_repair_note = scope.maintenance['audit_repair_note_save'];
                    scope.audit_merchant_result = scope.maintenance['audit_merchant_result_save'];
                    scope.audit_merchant_note = scope.maintenance['audit_merchant_note_save'];

                    if (scope.is_store) {
                        scope.settle_result = scope.maintenance['settle_merchant_result_save'];
                        scope.settle_note = scope.maintenance['settle_merchant_note_save'];
                    }

                    if (scope.is_repair) {
                        scope.settle_result = scope.maintenance['settle_repair_result_save'];
                        scope.settle_note = scope.maintenance['settle_repair_note_save'];
                    }

                    scope.initBillForm();

                });
            },
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
            initBillForm(){
                this.billForm = this.maintenance.bill;
                this.billFormTotal = this.billForm.total;
                this.otherFees = (this.maintenance.bill.others || []).map(function (e) {
                    return {key: e.msg, value: e.total}
                });
            },
            addFeeItem(){
                this.otherFees.push({key: '', total: 0});
            },
            removeFeeItem(index){
                this.otherFees.splice(index, 1);
                this.changeBill();
            },
            changeBill(val){
                if (val && isNaN(val)) {
                    toastr.error('金额 ' + val + ' 不正确');
                    return
                }
                this.billFormTotal = parseFloat(this.billForm.visit || 0) +
                        parseFloat(this.billForm.spare_total || 0) +
                        parseFloat(this.billForm.labor || 0) +
                        parseFloat(this.billForm.travel || 0) +
                        parseFloat(this.billForm.stay_total || 0) -
                        parseFloat(this.billForm.discount || 0);

                for (var i in this.otherFees) {
                    var item = this.otherFees[i];
                    if (item.key && item.value && !isNaN(item.value)) {
                        this.billFormTotal += parseFloat(item.value);
                    }
                }
            },
            updateBill() {
                this.billForm.total = this.billFormTotal;
                this.billForm.others = JSON.stringify(this.otherFees || []);
                var scope = this;

                $.ajax({
                    type: 'POST',
                    url: global.API_HOST + '/bill/' + this.billForm.id + '/update',
                    data: this.billForm,
                    crossDomain: true,
                }).done(function (data) {
                    scope.billEdit = false;
                    scope.getDetail();
                });
            },
        },
        components: {
            appBreadcrumb,
        },
    }
</script>