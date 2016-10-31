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
                            <img v-bind:src="store.store_logo">
                            <i class="busy b-white right"></i>
                        </span>
                    </div>
                    <h6>{{store.title}}</h6>
                    <p class="text-muted text-sm m-a">
                        编号&nbsp; <span v-text="store.code"></span>
                        <br>
                        <span v-text="store.number"></span>
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
                <!--<div class="box-body">-->
                <!--<div ui-include="'/static/views/htmls/detail-timeline.html'"></div>-->
                <!--</div>-->
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
                            <span v-for="img in images">
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
                                <h5 v-text="reporter.screen_name">
                                    &nbsp; &nbsp; &nbsp; &nbsp;
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

            <div class="box">
                <div class="box-header dker">
                    <h3>审核结算</h3>
                </div>
                <div class="box-body">
                    <div class="row padding">
                        <div class="col-md-4"></div>
                        <div class="col-md-8">
                            <button class="b-a b-grey btn btn-xs rounded disabled">服务商审核</button>
                            <span class="inline b-t b-t-dark"
                                  style="width: 15%; height: 4px; margin-left:-4px; margin-right:-4px;"></span>
                            <button class="b-a b-grey btn btn-xs rounded disabled">我方审核</button>
                            <span class="inline b-t b-t-dark"
                                  style="width: 15%; height: 4px; margin-left:-4px; margin-right:-4px;"></span>
                            <button class="btn btn-xs rounded text-white opacity">工单结算</button>
                        </div>
                    </div>
                    <div class="row padding">
                        <div class="col-md-4">
                            <div class="p-r text-right text-muted">服务商审核工单</div>
                        </div>
                        <div class="col-md-8">
                            正在审核当前工单
                        </div>
                    </div>

                    <div class="row p-l p-r">
                        <hr>
                    </div>

                    <div class="row padding">
                        <div class="col-md-4">
                            <div class="p-r text-right text-muted">商户审核工单</div>
                        </div>
                        <div class="col-md-8">
                            <label class="radio-inline">
                                <input type="radio" name="inlineRadioOptions" id="inlineRadio1" value="option1"
                                       class="has-value"> 审核通过
                            </label>
                            <label class="radio-inline">
                                <input type="radio" name="inlineRadioOptions" id="inlineRadio2" value="option2"> 审核不通过
                            </label>
                            <textarea class="form-control m-t" rows="2" placeholder="请填写备注信息"></textarea>
                            <div class="m-t-md p-t-xs">
                                <small class="text-muted">提示: 您可在当前页面保存审核结果, 再返回列表页选择多张工单批量审核</small>
                            </div>
                            <div class="m-t-sm">
                                <button class="btn btn-xs btn-fw dark">仅保存结果</button>
                                <button class="btn btn-xs btn-fw text-white p-x-md m-l-sm">提交审核</button>
                            </div>
                        </div>
                    </div>

                    <div class="row p-l p-r">
                        <hr>
                    </div>

                    <div class="row padding">
                        <div class="col-md-4">
                            <div class="p-r text-right text-muted">结算</div>
                        </div>
                        <div class="col-md-8">
                            <div class="row">
                                <div class="col-md-4">
                                    <span class="m-r"><i class="fa fa-check-circle text-orange m-r-xs"></i>服务商已结算</span>
                                </div>
                                <div class="col-md-5">
                                    <span>张永生</span> /
                                    <span class="text-muted">13816903031</span>
                                </div>
                                <div class="col-md-3">2015年11月3日 15:16</div>
                            </div>
                            <div class="row">
                                <div class="col-md-4">
                                    <span class="m-r"><i class="fa fa-check-circle text-orange m-r-xs"></i>商户已结算</span>
                                </div>
                                <div class="col-md-5">
                                    <span>张永生</span> /
                                    <span class="text-muted">13816903031</span>
                                </div>
                                <div class="col-md-3">2015年11月3日 15:16</div>
                            </div>
                            <div class="m-t-md">
                                <label class="md-check">
                                    <input type="checkbox" checked class="has-value">
                                    <i class="indigo"></i>
                                    <span class="text-muted">本工单已结算</span>
                                </label>
                            </div>
                            <textarea class="form-control m-t" rows="2" placeholder="请填写备注信息"></textarea>
                            <div class="m-t-md p-t-xs">
                                <small class="text-muted">提示: 您可在当前页面保存结算结果, 再返回列表页选择多张工单批量结算</small>
                            </div>
                            <div class="m-t-sm">
                                <button class="btn btn-xs btn-fw dark">仅保存结果</button>
                                <button class="btn btn-xs btn-fw text-white p-x-md m-l-sm">结算工单</button>
                            </div>
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
                    {'title': '维修工单'},
                ],
                infoTable: [{'label': '资产', 'text': '三洋豆浆机'}],
                images: [],
                store: {},
                fixer: {
                    'screen_name': '张三',
                    'mobile': '13815903031'
                },
                reporter: {
                    'screen_name': '张三',
                    'mobile': '13815903031'
                }

            }
        },
        components: {
            appBreadcrumb,
        }
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
</style>