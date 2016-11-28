$(function () {
    uiLoad.load(MODULE_CONFIG['directive']).then(function () {
        Vue.config.delimiters = ['%%', '%%'];
        msgComVm = Vue.component('message-list', {
            template: '#message-ul',
            data: function () {
                return {};
            },
            ready: function () {
                $(this.$el).attr('operation');
            },
            props: {
                messagelist: {
                    type: Array,
                    default: function () {
                        return [];
                    }
                },
                actionbtn: {
                    type: String,
                    default: function () {
                        return '1';
                    }
                }
            },
            created: function () {
                alert('com msg created');
                this.actionbtn = !!parseInt(this.actionbtn);
            },
            methods: {
                delete_message: function (index, id) {
//                    console.log("index=" + index);
//                    console.log("删除消息: " + id);
                    $.ajax({
                        url: API_HOST + "push/" + id,
                        type: "DELETE",
                        async: false,
                        data: {},
                    }).done(function (resp) {
                        msgComVm.messagelist.splice(index, 1);
                    });
                },
                accept_message: function (index, id) {
                    $.ajax({
                        url: API_HOST + "push/" + id,
                        type: "PATCH",
                        async: false,
                        data: {
                            "extra": JSON.stringify({"accepted": true}),
                        },
                    }).done(function (resp) {
                        messagelist[index]["extra"]["accepted"] = true;
                    });
                },
                deny_message: function (index, id) {
                    $.ajax({
                        url: API_HOST + "push/" + id,
                        type: "PATCH",
                        async: false,
                        data: {
                            "extra": JSON.stringify({"accepted": false}),
                        },
                    }).done(function (resp) {
                        messagelist[index]["extra"]["accepted"] = false;
                    });
                },
            }
        });
    });
});
