<style>
    .table td {
        vertical-align: middle;
    }
</style>
<template>
    <div>
        <table class="table table-striped table-hover">
            <thead class="theme-title-grey text-white">
            <tr>
                <th width="5%"><input type="checkbox" v-model="selectedAll"></th>
                <th width="10%">报修</th>
                <th width="8%">城市</th>
                <th width="9%">餐厅</th>
                <th width="7%">类别</th>
                <th width="8%">资产</th>
                <th width="8%">时效</th>
                <th width="13%">故障描述</th>
                <th width="11%">维修员</th>
                <th width="9%">状态</th>
                <th width="13%"></th>
            </tr>
            </thead>
            <tbody class="theme-text-blue">
            <tr :class="{'theme-table-selected':item.checked}" v-for="(item, $index) in maintenances">
                <td><input type="checkbox" v-model="item.checked"></td>
                <td @click="clickMaintenance(item)">
                    <a>
                        <div v-text="item.code"></div>
                        <small class="text-muted">报修于: <span v-text="item.create_time.slice(0, 10)"></span></small>
                    </a>
                </td>
                <td v-text="item.city"></td>

                <td><span v-text="item.store"></span>
                    <small class="text-muted">(<span v-text="item.store_no"></span>)</small>
                </td>
                <td>设备</td>
                <td>
                    <div v-text="item.product"></div>
                    <div>
                        <small class="text-muted" v-text="item.brand"></small>
                    </div>
                </td>
                <td>
                    <span v-if="item.state==1">紧急</span>
                    <span v-if="item.state==2">非紧急</span>
                </td>
                <td v-text="item.content"></td>
                <td>
                    <span v-if="item.target_user_name">
                        <div>
                            <span v-text="item.target_user_name"></span>
                            <small class="text-muted    " v-text="item.target_user_mobile"></small>
                        </div>
                        <div><small class="text-muted" v-text="item.target_company"></small></div>

                    </span>
                    <span v-else>未接单</span>
                </td>
                <td v-text="item.status"></td>
                <td>
                    <div v-if="item.status == '已经完成'">
                        <div v-if="!item.settlement || item.settlement < 1">
                            待服务商审核
                        </div>
                        <div v-if="item.settlement==1">
                            <div v-if="item.audit_repair_result">待商家审核</div>
                            <div v-else>服务商审核未通过</div>
                        </div>
                        <div v-if="item.settlement==2">
                            <div v-if="item.audit_merchant_result && item.audit_repair_result">
                                <div v-if="!item.settle_merchant_result">待商家结算</div>
                                <div v-if="!item.settle_repair_result">待服务商结算</div>
                            </div>
                            <div v-else>审核未通过</div>
                        </div>
                        <div v-if="item.settlement>2">结案</div>
                    </div>
                </td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    export default {
        props: ['maintenances'],
        data(){
            return {
                selectedAll: false,
            }
        },
        created: function () {
            var scope = this;
            this.$watch('selectedAll', function (oldVal, newVal) {
                for (var i in scope.maintenances) {
                    scope.maintenances[i].checked = !newVal;
                }
            });
        },
        methods: {
            clickMaintenance(item) {
                this.$router.replace({path: '/maintenance/' + item.id})
            },
        }
    }
</script>