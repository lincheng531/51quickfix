<style>
    .form-group-lg .select2-container--bootstrap .select2-selection--single, .input-group-lg .select2-container--bootstrap .select2-selection--single, .select2-container--bootstrap.input-lg .select2-selection--single {
        font-size: 14px;
        line-height: 2;
    }

    .select2 .select2-selection__placeholder {
        opacity: 0.5;
    }
</style>
<template>
    <div class="input-group select2-bootstrap-prepend select2-bootstrap-append"
         :class="{'input-group-lg': size=='lg', 'input-group-sm': size=='sm'}">
        <select class="select2 form-control"></select>
    </div>
</template>

<script>
    export default {
        data(){
            return {
                selectedVal: null,
                data: []
            }
        },
        props: {
            placeholder: {
                type: String,
                default: '请选择'
            },
            size: {
                size: String,
                default: 'lg'
            },
            keyName: {
                type: String,
                default: 'id',
            },
            valueName: {
                type: String,
                default: 'title',
            },
            type: null,
            value: null,
            dataSource: null,
            api: {
                default: null
            },
            width: {
                default: null
            }
        },
        watch: {
            selectedVal(val){
                this.$emit('input', val);
            },
            api(val){
                this.render();
            }
        },
        created(){
            var scope = this;
            this.selectedVal = this.value;

            if (this.type == 'gender') {
                this.data = [
                    {'id': 1, text: "男"},
                    {'id': 0, text: "女"},
                ];
            } else if (this.type == 'city') {
                this.data = [
                    {id: "", text: "全部"},
                    {id: "上海市", text: "上海"},
                    {id: "北京市", text: "北京"},
                    {id: "广州市", text: "广州"},
                    {id: "深圳市", text: "深圳"},
                    {id: "杭州市", text: "杭州"},
                    {id: "苏州市", text: "苏州"},
                ];
            } else if (this.type == 'state') {
                this.data = [
                    {id: "", text: "全部"},
                    {id: "1", text: "紧急"},
                    {id: "2", text: "非紧急"},
                ];
            } else if (this.type == 'head_type') {
                this.data = [
                    {id: "", text: "全部"},
                    {id: "2", text: "汉堡王"},
                    {id: "3", text: "达美乐"},
                    {id: "4", text: "永和大王"},
                ];
            } else if (this.type == 'category') {
                this.data = [
                    {id: "", text: "全部"},
                    {id: "设备", text: "设备类"},
                    {id: "工程", text: "工程类"},
                    {id: "IT", text: "IT类"},
                    {id: "其他", text: "其他"},
                ];
            }
        },
        mounted(){
            this.render();
        },
        methods: {
            _render_select(options){
                var scope = this;
                var select = $(".select2", this.$el).select2(options);
                select.on('select2:select', function (evt) {
                    scope.selectedVal = evt.target.value;
                });
                select.on('select2:unselect', function (evt) {
                    scope.selectedVal = null;
                });
                select.val(scope.selectedVal).trigger('change');
            },
            render(){
                var scope = this;
                var options = {
                    theme: 'bootstrap',
                    placeholder: this.placeholder,
                    allowClear: true,
                    width: this.width || '100%',
                };
                if (this.api) {
//                    $.getJSON(global.API_HOST + this.api, {}, function (res) {
//                        if (res.code == 0) {
//                            scope.data = res.data.map(function (e) {
//                                return {
//                                    id: e[scope.keyName],
//                                    text: e[scope.valueName],
//                                }
//                            });
//                            options.data = scope.data;
//                            scope._render_select(options);
//                        }
//                    });
                    options.ajax = {
                        url: global.API_HOST + this.api,
                        dataType: 'json',
                        processResults: function (res) {
                            var results = [];
                            if (res.status == 1) {
                                results = res.info.results.map(function (e) {
                                    return {
                                        id: e[scope.keyName],
                                        text: e[scope.valueName],
                                    }
                                });
                            }

                            return {
                                results: results
                            };
                        },
                        cache: true,
                    };
                } else {
                    if (this.dataSource && this.dataSource.length) {
                        options.data = this.dataSource.map(function (e) {
                            return {
                                id: e[scope.keyName],
                                text: e[scope.valueName],
                            }
                        });
                    } else {
                        options.data = this.data;
                    }
                }
                this._render_select(options);
            }
        }
    }
</script>