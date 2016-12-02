<style>
    .table td {
        vertical-align: middle;
    }
</style>
<template>
    <div>
        <table class="table table-striped">
            <thead class="theme-title-grey text-white">
            <tr>
                <th><input class="m-r-xs" type="checkbox">全选</th>
                <th>报修</th>
                <th>城市</th>
                <th>餐厅</th>
                <th>类别</th>
                <th>资产</th>
                <th>时效</th>
                <th>故障描述</th>
                <th>维修员</th>
                <th>状态</th>
            </tr>
            </thead>
            <tbody class="theme-text-blue">
            <tr class="theme-table-selected" v-for="item in maintenances" @click="clickMaintenance(item)">
                <td><input type="checkbox" v-model="item.checked"></td>
                <td class="text-center">
                    <div v-text="item.no"></div>
                    <small class="text-muted">报修于: <span v-text="item.create_time.slice(0, 10)"></span></small>
                </td>
                <td v-text="item.city"></td>

                <td v-text="item.store_name"></td>
                <td v-text="item.category"></td>
                <td>
                    <div v-text="item.device"></div>
                    <div>
                        <small class="text-muted" v-text="item.brand_name"></small>
                    </div>
                </td>
                <td>
                    <span v-if="item.state==1">紧急</span>
                    <span v-if="item.state==2">非紧急</span>
                </td>
                <td v-text="item.content"></td>
                <td v-text="item.grab_user"></td>
                <td v-text="item.status"></td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    export default {
        props: ['maintenances'],
        methods: {
            clickMaintenance(item) {
                if (!sessionStorage.getItem('maintenance'+item.id)){
                    sessionStorage.setItem('maintenance'+item.id, JSON.stringify(item));
                }
                this.$router.replace({path:'/maintenance/'+item.id})
            }
        }
    }
</script>