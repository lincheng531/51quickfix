<template>
    <div class="wrapper m-t-lg">
        <table width="100%" class="center notify" cellspacing="10">
            <tr>
                <td colspan="3">待办事项/提醒</td>
                <td>自定义功能</td>
            </tr>
            <tr>
                <td width="25%">维修</td>
                <td width="25%">采购</td>
                <td width="25%">保养</td>
                <td width="25%">固定资产</td>
            </tr>

        </table>
    </div>
</template>

<style>
    .center {
        text-align: center;
        line-height: 40px;
    }

    .notify {
        width: 100%;
        border-spacing: 20px;
        border-collapse: separate;
    }

    .notify td {
        background-color: #484848;
        border: 1px solid #CCCCCC;
        height: 200px;
        font-size: 24px;
        font-weight: bold;
        color: #fff;
        opacity: 0.2;
    }
</style>