<style>
    .table td {
        font-weight: normal;
        vertical-align: middle;
    }
</style>
<template>
    <div>
        <table class="table table-striped table-hover">
            <thead class="theme-title-grey text-white">
            <tr v-if="list_type=='audit' ||  list_type=='settlement'">
                <th width="5%"><input type="checkbox" v-model="selectedAll"></th>
                <th width="10%">报修</th>
                <th width="8%">城市</th>
                <th width="9%" v-if="user_category=='service'">商家品牌</th>
                <th width="10%">餐厅</th>
                <th width="8%">维修类别</th>
                <th width="10%">资产</th>
                <th width="6%">时效</th>
                <th width="11%">故障描述</th>
                <th width="10%">金额</th>
                <th width="10%" v-if="user_category=='merchant'">服务商</th>
                <th width="15%"></th>
            </tr>
            <tr v-else>
                <th width="5%"><input type="checkbox" v-model="selectedAll"></th>
                <th width="10%">报修</th>
                <th width="8%">城市</th>
                <th width="9%" v-if="user_category=='service'">商家品牌</th>
                <th width="10%">餐厅</th>
                <th width="9%">维修类别</th>
                <th width="10%">资产</th>
                <th width="6%">时效</th>
                <th width="13%">故障描述</th>
                <th width="13%">维修员</th>
                <th width="11%">状态</th>
            </tr>
            </thead>
            <tbody class="theme-text-blue">
            <tr :class="{'theme-table-selected':item.checked}" v-for="(item, $index) in maintenances">
                <td><input type="checkbox" v-model="item.checked"></td>
                <td @click="clickMaintenance(item)">
                    <a>
                        <div v-text="item.code"></div>
                        <small class="text-muted">报修于: <span v-text="item.create_time"></span></small>
                    </a>
                </td>
                <td v-text="item.city"></td>
                <td v-text="getHeadTypeText(item.head_type)" v-if="user_category=='service'"></td>

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

                <td v-if="list_type=='status'">
                    <div v-if="item.target_user_name">
                        <div>
                            <span v-text="item.target_user_name"></span>
                            <small class="text-muted    " v-text="item.target_user_mobile"></small>
                        </div>
                        <div><small class="text-muted" v-text="item.target_company"></small></div>

                    </div>
                    <div v-else>
                        <div>未接单</div>
                        <div><small class="text-center text-muted" v-text="item.supplier"></small></div>
                    </div>
                </td>
                <td v-text="item.status" v-if="list_type=='status'"></td>
                <td v-if="list_type=='audit' || list_type=='settlement'" v-text="item.bill && item.bill.total"></td>
                <td width="10%" v-if="(list_type=='audit' || list_type=='settlement') && user_category=='merchant'"
                    v-text="item.target_company"></td>
                <td v-if="list_type=='audit' || list_type=='settlement'">
                    <div v-if="item.status == '已经完成'">
                        <div v-if="item.audit_repair_result_save && item.settlement < 1">
                            服务商已确认
                        </div>
                        <div v-if="!item.audit_repair_result_save && item.settlement < 1">
                            <span v-text="item.audit_repair_note_save"></span>
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
        props: ['maintenances', 'list_type'],
        data(){
            return {
                selectedAll: false,
                user: JSON.parse(sessionStorage.getItem('user')) || {},
                user_category: null,
            }
        },
        created: function () {
            var scope = this;
            console.log(this.list_type);
            if (['1', '3', '4', '5'].indexOf(this.user.category) > -1) {
                this.user_category = 'merchant';
            } else if (['0', '2', '6'].indexOf(this.user.category) > -1) {
                this.user_category = 'service';
            }

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
            getHeadTypeText(val){
                var headTypeDict = {
                    1: '个人订单',
                    2: '汉堡王',
                    3: '达美乐',
                    4: '永和大王',
                };
                var text = headTypeDict[val];
                return text || val;
            }
        },
    }
</script>