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
                <th width="13%">报修</th>
                <th width="8%">城市</th>
                <th width="10%">餐厅</th>
                <th width="7%">类别</th>
                <th width="10%">资产</th>
                <th width="8%">时效</th>
                <th width="15%">故障描述</th>
                <th width="11%">维修员</th>
                <th width="13%">状态</th>
            </tr>
            </thead>
            <tbody class="theme-text-blue">
            <tr :class="{'theme-table-selected':item.checked}" v-for="item in maintenances"
                @click="clickMaintenance(item)">
                <td><input type="checkbox" v-model="item.checked" @click.stop.prevent="1"></td>
                <td>
                    <div v-text="item.code"></div>
                    <small class="text-muted">报修于: <span v-text="item.create_time.slice(0, 10)"></span></small>
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
            </tr>
            </tbody>
        </table>
        <div><ul id="maintenance-pagination"></ul></div>
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
            setPagination(totalPage, status) {
                $('#maintenance-pagination').twbsPagination({
                    first: "第一页",
                    prev: "上一页",
                    next: "下一页",
                    last: "最后一页",
                    totalPages: totalPage,  // 一共的页数
                    visiblePages: 10,
                    startPage: scope.currentPage || 1,
                    initiateStartPageClick: false,
                    onPageClick: function (event, page) {
                        scope.currentPage = page;
                        scope.projectTodoList.call(this, {
                            is_project: 1,
                            status: status,
                            page: page,
                        }, function (data, res) {
                            scope.todos = data;
                            scope.selectedTodo = this.todos[0];
                            scope.setPagination(res.totalPage, status, page);
                        });
                    }
                });
            },
            clickMaintenance(item) {
                this.$router.replace({path: '/maintenance/' + item.id})
            }
        }
    }
</script>