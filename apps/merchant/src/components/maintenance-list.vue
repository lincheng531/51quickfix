<template>
    <div class="padding">
        <div class="row">
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
                                <div class="col-xs-3 text-right">
                                    <label class="m-r text-muted">城市</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                            <div class="form-group col-xs-4">
                                <div class="col-xs-3 text-right">
                                    <label class="m-r text-muted">餐厅</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                            <div class="form-group col-xs-4">
                                <div class="col-xs-3 text-right">
                                    <label class="m-r text-muted">服务商</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                        </div>
                        <div class="row m-b-sm">
                            <div class="form-group col-xs-4">
                                <div class="col-xs-3 text-right">
                                    <label class="m-r text-muted">维修类别</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                            <div class="form-group col-xs-4">
                                <div class="col-xs-3 text-right">
                                    <label class="m-r text-muted">品牌</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                            <div class="form-group col-xs-4">
                                <div class="col-xs-3 text-right">
                                    <label class="m-r text-muted">资产</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                        </div>
                        <div class="row m-b-sm">
                            <div class="form-group col-xs-4">
                                <div class="col-xs-3 text-right">
                                    <label class="m-r text-muted">维修时效</label>
                                </div>
                                <select class="form-control">
                                    <option value="">全部</option>
                                </select>
                            </div>
                            <div class="form-group col-xs-4">
                                <div class="col-xs-3 text-right">
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
                        <a class="nav-link active" href="" data-toggle="tab" data-target="#tab1" aria-expanded="true">最新报修</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" href="" data-toggle="tab" data-target="#tab2" aria-expanded="false">正在维修</a>
                    </li>
                    <li class="nav-item b-a box-radius-3x">
                        <a class="nav-link" href="" data-toggle="tab" data-target="#tab3" aria-expanded="false">维修完成</a>
                    </li>
                </ul>
            </div>
            <div class="tab-content p-a m-b-md">
                <div class="tab-pane animated fadeIn text-muted active" id="tab1" aria-expanded="true">
                    <router-link to="/maintenance/detail">ceshi</router-link>
                </div>
                <div class="tab-pane animated fadeIn text-muted" id="tab2" aria-expanded="false">
                    Components
                </div>
                <div class="tab-pane animated fadeIn text-muted" id="tab3" aria-expanded="false">
                    UI kits
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {}
</script>