<template>
    <div class="input-group select2-bootstrap-append"
         :class="{'input-group-lg': size=='lg'}">
        <select class="select2 form-control" multiple="multiple">
            <option :value="item.id" v-for="item in data" v-text="item.title"></option>
        </select>
    </div>
</template>

<script>
    export default {
        data(){
            return {
                selectedVal: [],
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
            value: {
                type: Array,
                default: []
            },
            api: {
                default: null
            }
        },
        watch: {
            selectedVal(val){
                this.$emit('input', val);
            }
        },
        created(){
            var scope = this;
            this.selectedVal = this.value.map(function (e) {
                return String(e.id);
            });
            if (this.api) {
                $.getJSON(global.API_HOST + this.api, function (res) {
                    if (res.code == 0) {
                        scope.data = res.data;
                    }
                })
            }
        },
        mounted(){
            var scope = this;
            var select = $(".select2", this.$el).select2({
                theme: 'bootstrap',
                placeholder: this.placeholder,
                minimumResultsForSearch: Infinity,
                allowClear: true,
                data: this.data,
            });
            select.on('select2:select', function (evt) {
                scope.selectedVal.push(evt.target.value);
            });
            select.on('select2:unselect', function (evt) {
                var index = scope.selectedVal.indexOf(evt.target.value);
                scope.selectedVal.pop(index);
            });
            setTimeout(function () {
                select.val(scope.selectedVal).trigger('change');
            }, 500)
        },
    }
</script>