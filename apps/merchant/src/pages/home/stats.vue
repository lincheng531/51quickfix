<style>
    .opacity-7 {
        opacity: 0.7;
    }
</style>
<template>
    <div class="wrapper m-t-lg" id="stats-overview">
        <div class="light">
            <table class="b-a" width="100%">
                <tr>
                    <td class="p-t-md p-b-md text-center" width="36%">
                        <div class="p-b-sm text-muted text-md"><span class="opacity">今日维修概况</span></div>
                        <div class="no-border b-r b-dashed">
                            <div class="p-a-md">累计报修 <span class="text-orange text-md">{{ data.total_today }}</span> 单
                            </div>
                            <div class="p-b text-sm opacity-7">
                                <p>未接工单 {{ data.unfix_today }} 单</p>
                                <p>正在维修 {{ data.fixing_today }} 单</p>
                                <p>维修完成 {{ data.fixed_today }} 单</p>
                                <p>已取消报修 {{ data.cancelled_today }} 单</p>
                            </div>
                        </div>
                    </td>
                    <td class="p-t-md p-b-md text-center" width="36%">
                        <div class="p-b-sm text-muted text-md"><span class="opacity">历史维修概况</span></div>
                        <div>
                            <div class="p-a-md">历史报修累计 <span class="text-orange text-md">{{ data.total }}</span> 单</div>
                            <div class="p-b text-sm opacity-7">
                                <p>未处理工单累计 {{ data.unfix }} 单</p>
                                <p>维修中工单累计 {{ data.fixing }} 单</p>
                                <p>已完成工单累计 {{ data.fixed }} 单</p>
                                <p>已取消报修累计 {{ data.cancelled }} 单</p>
                            </div>
                        </div>
                    </td>
                    <td class="white" width="28%">
                        <div class="p-a m-t m-l m-r">
                            <div>
                                <p>累计入驻品牌 <span class="text-orange text-md">{{ data.head_type }}</span> 家</p>
                            </div>
                            <div class="text-sm _500 opacity-7">
                                <p>注册商户 {{ data.stores }} 家</p>
                                <p>上海区商户 {{ data.stores_sh }} 家</p>
                                <p>注册餐厅工作人员 {{ data.merchant }} 名</p>
                            </div>
                        </div>
                        <hr>
                        <div class="p-a m-l m-r">
                            <div>
                                <p>累计入驻服务商 <span class="text-orange text-md">{{ data.service }}</span> 家</p>
                            </div>
                            <div class="text-sm _500 opacity-7">
                                <p>注册维修员 {{ data.repairer }} 名</p>
                            </div>

                        </div>
                    </td>
                </tr>
            </table>
        </div>
    </div>
</template>

<script>
    export default {
        data(){
            return {
                data: {}
            }
        },
        created(){
            var scope = this;
            $.getJSON(global.API_HOST + '/maintenance/stats', function (data) {
                if (data.status) {
                    scope.data = data.info.result
                }
            });
        },
    }
</script>