<style>
    .form-control {
        display: inline-block
    }

    select.form-control {
        width: 24%;
        height: 27px;
    }

    select.form-control.lg {
        width: 100%;
    }

    .asterisk {
        vertical-align: -webkit-baseline-middle;
    }
</style>
<template>
    <div id="maintenance-call">
        <com-app-breadcrumb :breadcrumb="breadcrumb"></com-app-breadcrumb>

        <div class="theme-box p-b-lg">
            <div class="box theme-box theme-text-blue">
                <div class="box-header theme-grey-dark">
                    <h3>报修餐厅</h3>
                </div>
                <div class="box-body clearfix">
                    <div class="row text-muted">
                        <div class="col-md-6">
                            <div class="col-md-12">
                                <div class="col-md-2 text-right">连锁餐厅</div>
                                <div class="col-md-10">
                                    <div>
                                        <select class="form-control" placeholder="品牌" v-model="form.head_type">
                                            <option value='2'>汉堡王</option>
                                            <option value='3'>达美乐</option>
                                            <option value='4'>永和大王</option>
                                        </select>
                                        <input type="text" placeholder="门店编号" v-model="form.store_no"
                                               @change="changeStore">
                                    </div>
                                    <div class="p-a-xs">非连锁餐厅无需输入</div>
                                </div>
                            </div>
                            <div class="col-md-12 text-muted m-t">
                                <div class="col-md-2" text-right>餐厅名称</div>
                                <div class="col-md-9">
                                    <div class="col-md-11" style="padding:0;">
                                        <input type="text" class="form-control" placeholder="请输入"
                                               v-model="form.store_name">
                                    </div>
                                    <div class="col-md-1">
                                        <span class="text-orange text-md asterisk">*</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12 text-muted m-t">
                                <div class="col-md-2 text-right">地址</div>
                                <div class="col-md-9">
                                <textarea cols="45" class="form-control" placeholder="请输入" v-model="form.address"
                                          @change="codeAddress(form.address)"></textarea>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div id="map" style="width:100%px;height:160px"></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="box theme-box theme-text-blue">
                <div class="box-header theme-grey-dark">
                    <h3>报修人</h3>
                </div>
                <div class="box-body clearfix">
                    <div class="row text-muted">
                        <div class="col-md-6">
                            <div class="col-md-2 text-right">手机号</div>
                            <div class="col-md-10">
                                <input type="tel" placeholder="请输入" v-model="form.mobile" @change="changeUser">
                                <span class="text-orange">*</span>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="col-md-2 text-right">姓名</div>
                            <div class="col-md-10">
                                <input type="text" placeholder="请输入" v-model="form.name">
                                <span class="text-orange text-md asterisk">*</span>
                            </div>
                        </div>
                    </div>
                    <div class="row text-muted m-t">
                        <div class="col-md-6">
                            <div class="col-md-2 text-right">职务</div>
                            <div class="col-md-10">
                                <select class="form-control" style="width: 36%;" v-model="form.user_category">
                                    <option value="1">商户店员</option>
                                    <option value="3">商户区域经理</option>
                                    <option value="4">商户OC</option>
                                    <option value="5">商户管理员</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="box theme-box theme-text-blue">
                <div class="box-header theme-grey-dark">
                    <h3>报修信息</h3>
                </div>
                <div class="box-body clearfix" v-if="!toCreateDevice">
                    <div class="row text-muted m-t">
                        <div class="col-md-6">
                            <div class="col-md-2 text-right">请选资产</div>
                            <div class="col-md-10">
                                <select name="" class="form-control lg" v-model="form.selectedDevice"
                                        id="selectedDevice">
                                    <option value='冰箱 wise'>冰箱
                                        <small class="text-muted">wise</small>
                                    </option>
                                    <option value='双边调理台 WISE'>双边调理台
                                        <small class="text-muted">WISE</small>
                                    </option>
                                    <option value='员工冰箱 Haier'>员工冰箱
                                        <small class="text-muted">Haier</small>
                                    </option>
                                    <option value='冷库库板 HairCarrier'>冷库库板
                                        <small class="text-muted">HairCarrier</small>
                                    </option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="col-md-2 text-right">
                                <a class="text-dark" @click="toCreateDevice=true">
                                    <small><i class="fa fa-plus"></i> 新添资产</small>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="box-body clearfix" v-else>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="col-md-2 text-right">
                                <a class="text-dark" @click="toCreateDevice=false">
                                    <small><i class="fa fa-minus"></i> 取消添加</small>
                                </a>
                            </div>
                        </div>
                    </div>
                    <div class="row text-muted m-t">
                        <div class="col-md-6">
                            <div class="col-md-2 text-right">设备</div>
                            <div class="col-md-10">
                                <select name="" class="form-control" v-model="form.category" style="width: 23%"
                                        @change="changeCategory">
                                    <option :value="item" v-for="item in categories">{{ item }}</option>
                                </select>
                                <select name="" class="form-control" v-model="form.efcategory" style="width: 23%"
                                        @change="changeEfCategory">
                                    <option :value="item" v-for="item in efcategories">{{ item }}</option>
                                </select>

                                <select name="" class="form-control" v-model="form.ecategory" style="width: 23%"
                                        @change="changeECategory">
                                    <option :value="item" v-for="item in ecategories">{{ item }}</option>
                                </select>
                                <select name="" class="form-control" v-model="form.brand" style="width: 23%" id="brand">
                                    <option :value="item" v-for="item in brands">{{ item }}</option>
                                </select>
                                <span class="text-orange">*</span>
                            </div>
                        </div>
                    </div>

                    <div class="row text-muted m-t">
                        <div class="col-md-6">
                            <div class="col-md-2 text-right">设备名</div>
                            <div class="col-md-10">
                                <input type="input" v-model="form.device">
                            </div>
                        </div>
                    </div>

                    <div class="row text-muted m-t">
                        <div class="col-md-6">
                            <div class="col-md-2 text-right">型号</div>
                            <div class="col-md-10">
                                <select name="" class="form-control">
                                    <option value=""></option>
                                </select>
                                <input type="text" v-model="form.model">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="col-md-2 text-right">规格</div>
                            <div class="col-md-10">
                                <select name="" class="form-control">
                                    <option value=""></option>
                                </select>
                                <input type="text" v-model="form.specifications">
                            </div>
                        </div>
                    </div>

                    <div class="row text-muted m-t">
                        <div class="col-md-6">
                            <div class="col-md-2 text-right">序列号</div>
                            <div class="col-md-10">
                                <textarea cols="45" placeholder="请输入" v-model="form.psnumber"></textarea>
                            </div>
                        </div>
                    </div>

                    <div class="row text-muted m-t">
                        <div class="col-md-6">
                            <div class="col-md-2 text-right">过保日期</div>
                            <div class="col-md-10">
                                <input type="datetime">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="m-a b-a b-dashed"></div>
            <div class="row text-muted m-t-md m-b-md">
                <div class="col-md-6">
                    <div class="col-md-2 text-right">上门时间</div>
                    <div class="col-md-10">
                        <input type="datetime" id="must_time" v-model="form.must_time">
                        <span class="text-orange">*</span>
                    </div>
                </div>
            </div>
            <div class="m-a b-a b-dashed"></div>
            <div class="row text-muted m-t-md m-b-md">
                <div class="col-md-6">
                    <div class="col-md-2 text-right">故障描述</div>
                    <div class="col-md-10">
                        <textarea cols="45" rows="6" v-model="form.content"></textarea>
                    </div>
                </div>
            </div>

            <div class="m-a b-a b-dashed"></div>

            <div class="m-t-lg m-b-lg">
                <div class="row text-white">
                    <a @click="quitCall">
                        <div class="col-md-6 text-right">
                            <button class="btn btn-sm p-l-lg p-r-lg">取消报修</button>
                        </div>
                    </a>
                    <a @click="stepNext">
                        <div class="col-md-6">
                            <button class="btn btn-sm theme-blue p-l-lg p-r-lg">下一步</button>
                        </div>
                    </a>
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
                ],
                form: {
                    head_type: 2,
                    user_category: '1',
                    store_name: '',
                    address: '',
                    name: '',
                    category: null,
                    efcategory: null,
                    ecategory: null,
                    brand: null,
                    device: null,
                },
                categories: [],
                efcategories: [],
                ecategories: [],
                brands: [],
                toCreateDevice: false,
            }
        },
        created(){
            $('#must_time').datetimepicker({
                language: 'zh-CN',
                format: 'yyyy-mm-dd',
                minView: 'month',
                autoclose: true,
                todayHighlight: true,
            });
            this.getCategories();
        },
        mounted(){
            window.initialize = this.initMap();
            var script = document.createElement('script');
            script.src = 'http://api.map.baidu.com/api?v=1.4&callback=initialize';
            document.body.appendChild(script);
        },
        methods: {
            initMap() {
                var mp = new BMap.Map('map');
                mp.centerAndZoom(new BMap.Point(121.491, 31.233), 11);
            },
            codeAddress(address) {
                console.log('encoding address...');
                var map = new BMap.Map("map");
                var geo = new BMap.Geocoder();
                geo.getPoint(address, function (point) {
                    console.log(point);
                    if (point) {
                        map.centerAndZoom(point, 16);
                        map.addOverlay(new BMap.Marker(point));
                    }
                }, "上海市");
            },
            stepNext(){
                var scope = this;
                var selectedDevice = $('#selectedDevice').val();
                if (selectedDevice) {
                    var splitdevice = selectedDevice.split(' ')
                    scope.form['selectedDevice'] = splitdevice[0];
                    scope.form['brand'] = splitdevice[1];
                }
                else {
                    scope.form['brand'] = $('#brand').val();
                }
                this.$router.push({
                    path: '/maintenance/call/users',
                    query: scope.form,
                })
            },
            quitCall(){
                this.$router.go(-1);
            },
            changeStore(){
                var scope = this;
                var data = {head_type: this.form.head_type, no: this.form.store_no}
                $.ajax({
                    type: 'POST',
                    url: global.API_HOST + '/store',
                    data: data,
                }).done(function (res) {
                    if (res.status == 1) {
                        var store = res.info.results;
                        if (store) {
                            scope.form.store_name = store.name;
                            scope.form.address = store.address;
                            scope.codeAddress(scope.form.address);
                        }
                    }
                    else {
                        toastr.warning(res.alert);
                    }
                });
            },
            changeUser() {
                var scope = this;
                var data = {mobile: this.form.mobile};
                $.ajax({
                    type: 'POST',
                    url: global.API_HOST + '/user',
                    data: data,
                }).done(function (res) {
                    if (res.status == 1) {
                        var user = res.info.results;
                        if (user) {
                            scope.form.name = user.name;
                            scope.form.user_category = user.category;
                        }
                    }
                    else {
                        toastr.warning(res.alert);
                    }
                });
            },
            getCategories(options) {
                var scope = this;
                var data = options || {};
                $.ajax({
                    type: 'GET',
                    url: global.API_HOST + '/categories',
                    data: data,
                }).done(function (res) {
                    if (res.status == 1) {
                        var results = res.info.results;
                        scope.categories = results;
                    }
                    else {
                        toastr.warning(res.alert);
                    }
                });
            },
            changeCategory() {
                var scope = this;
                $.ajax({
                    type: 'GET',
                    url: global.API_HOST + '/categories',
                    data: {parent: this.form.category, level: 2},
                }).done(function (res) {
                    if (res.status == 1) {
                        var results = res.info.results;
                        scope.efcategories = results;
                        scope.form.efcategory = scope.efcategories[0];
                    }
                    else {
                        toastr.warning(res.alert);
                    }
                });
            },
            changeEfCategory() {
                var scope = this;
                $.ajax({
                    type: 'GET',
                    url: global.API_HOST + '/categories',
                    data: {parent: this.form.efcategory, level: 3},
                }).done(function (res) {
                    if (res.status == 1) {
                        var results = res.info.results;
                        scope.ecategories = results;
                        scope.form.ecategory = scope.ecategories[0];
                    }
                    else {
                        toastr.warning(res.alert);
                    }
                });
            },
            changeECategory() {
                var scope = this;
                $.ajax({
                    type: 'GET',
                    url: global.API_HOST + '/categories',
                    data: {parent: this.form.ecategory, level: 4},
                }).done(function (res) {
                    if (res.status == 1) {
                        var results = res.info.results;
                        scope.brands = results;
                        scope.form.brand = scope.brands[0];
                    }
                    else {
                        toastr.warning(res.alert);
                    }
                });
            }
        }
    }
</script>

<style>
    #maintenance-call .box {
        margin-bottom: 0;
    }
</style>