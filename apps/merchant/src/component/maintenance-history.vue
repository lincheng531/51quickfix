<template>
    <div>
        <table id="timeline" v-for="stat in res.status_list">
            <tr v-if="stat.head_type==-1">
                <td class="center"><img src="/static/images/time_dot_2.png"/></td>
                <td colspan="2" class="f1">{{stat.create_time}}</td>
            </tr>
            <tr v-if="stat.head_type==1">
                <td style="width: 60px"><span class="icon">报修</span></td>
                <td><p class="f3">{{stat.must_time}}到修(合约)</p>
                    <p>{{stat.name}}</p>
                    <p class="f3">{{stat.mobile}}</p>
                </td>
                <td valign="top" class="f3">{{stat.create_time}}</td>
            </tr>
            <tr v-if="stat.head_type==2">
                <td><span class="icon">通知</span></td>
                <td>
                    <p class="f3">{{stat.company}} {{stat.city}}{{stat.count}}人</p>
                    <p>{{stat.name}}(主管)</p>
                    <p class="f3">{{stat.mobile}}</p>
                </td>
                <td valign="top" class="f3">{{stat.create_time}}</td>
            </tr>
            <tr v-if="stat.head_type==3">
                <td class="center"><img src="/static/images/time_dot.png"/></td>
                <td>
                    <p class="f3">{{stat.company}} {{stat.city}}</p>
                    <p>{{stat.to_name}}</p>
                    <p class="f3">{{stat.to_mobile}}</p>
                </td>
                <td valign="top" class="f3">{{stat.create_time}}</td>
            </tr>
            <tr v-if="stat.head_type==4">
                <td class="center"><img src="/static/images/time_dot.png"/></td>
                <td>
                    <p class="f3">{{stat.company}} {{stat.city}}</p>
                    <p>{{stat.to_name}}</p>
                    <p class="f3">{{stat.to_mobile}}</p>
                </td>
                <td valign="top" class="f3">{{stat.create_time}}</td>
            </tr>
            <tr v-if="stat.head_type==5">
                <td class="center"><img src="/static/images/time_dot.png"/></td>
                <td>
                    <p class="f3">{{stat.company}} 总部</p>
                    <p>{{stat.to_name}}</p>
                    <p class="f3">{{stat.to_mobile}}</p>
                </td>
                <td valign="top" class="f3">{{stat.create_time}}</td>
            </tr>
            <tr v-if="stat.head_type==6">
                <td><span class="icon">接单</span></td>
                <td>
                    <p class="f3">预计{{stat.must_time}}时候到店</p>
                    <p>{{stat.to_name}}({{stat.company}}{{stat.city}})</p>
                    <p class="f3">{{stat.to_mobile}}</p>
                </td>
                <td valign="top" class="f3">{{stat.create_time}}</td>
            </tr>
            <tr v-if="stat.head_type==7">
                <td><span class="icon">到店</span></td>
                <td>
                    <p>实际到店</p>
                    {% if stat.later %}
                    <p class="f3">迟到原因:{{stat.later}}</p>
                    {% endif %}
                </td>
                <td class="f3" valign="top">{{stat.arrival_time}}</td>
            </tr>
            <tr v-if="stat.head_type==8">
                <td><span class="icon">维修</span></td>
                <td>
                    预计{{stat.create_time}}修复
                </td>
                <td></td>
            </tr>
            <tr v-if="stat.head_type==12">
                <td><span class="icon">暂停</span></td>
                <td>
                    {{stat.title}}
                    <p>{{stat.content}}</p>
                </td>
                <td valign="top" class="f3">{{stat.stop_time}}</td>
            </tr>
            <tr v-if="stat.head_type==9">
                <td></td>
                <td>
                    <p>{{stat.msg}}</p>
                </td>
                <td valign="top" class="f3">{{stat.create_time}}</td>
            </tr>
            <tr v-if="stat.head_type==10">
                <td><span class="icon">确认修单</span></td>
                <td>
                    <p>{{stat.msg}}</p>
                </td>
                <td valign="top" class="f3">{{stat.create_time}}</td>
            </tr>
            <tr v-if="stat.head_type==11">
                <td><span class="icon">24H</span></td>
                <td>
                    <p>{{stat.msg|safe}}</p>
                </td>
                <td valign="top" class="f3">{{stat.create_time}}</td>
            </tr>
        </table>
    </div>
</template>

<script>
    export default {
        data(){
            return {
                res: {status_list:[]},
            }
        },
        props: ['id'],
        created(){

        }
    }
</script>