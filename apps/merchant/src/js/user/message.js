ManageMessage = function () {
    // API_HOST="http://172.16.59.112:8000/api/v1/";
    var msgScope = this;
    this.getUnreadCount = function () {
        var url = API_HOST + 'push/overview';
        $.getJSON(url, function (res) {
            var count = res.data.unread;
            $('#unreadMsgCounter').remove();
            if (count) {
                $('#bell').append('<span class="label label-sm up danger" id="unreadMsgCounter">' + count + '</span>');
            }
        });
    };

    this.init = function (obj) {
        var messagelist = [];
        var message_nav_vm = null;

        Vue.filter('timestamptodatetime', function (value) {
            if (typeof(value) == 'string') {
                value = parseInt(value);
            }
            if (value < 2073753874) {
                value = 1000 * value;
            }
            var date = new Date(value);
            return date.toLocaleDateString();
        });

        var readAllMsg = function (clear) {
            // 设置全部消息已读
            $.ajax({
                url: API_HOST + "push/readall",
                type: "PUT",
                async: true,
                data: "",
            }).done(function (resp) {
                if (resp.code == 0) {
                    // console.log("所有的消息已经设置成已读")
                    for (var message of message_list_vm.messagelist) {
                        message.status = 2
                    }
                    msgScope.getUnreadCount();

                    if (clear) {
                        message_list_vm.messagelist = [];
                    }
                }
            });
        };

        var message_list_vm = new Vue({
            el: obj || '#message-box',
            data: {
                'messagelist': messagelist,
                'next': '',
                'previous': '',
                'totalPage': 1,
            },
            methods: {
                readAllMsg: readAllMsg,
            },
            events: {
                'msgDel': function (type, isStar) {
                    message_nav_vm.all -= 1;
                    message_nav_vm[type] -= 1;
                    
                    if (isStar) {
                        message_nav_vm.star -= 1;
                    }
                },
                'msgStar': function (action) {
                    message_nav_vm.star += action ? 1 : -1;
                }
            }
        });

        $.ajax({
            url: API_HOST + "push/overview",
            type: "GET",
            async: true,
            data: {},
            success: function (res) {
                if (!$('#message-nav').length) {
                    return;
                }
                message_nav_vm = new Vue({
                    el: "#message-nav",
                    data: res.data,
                    methods: {
                        show_message: function (type) {
                            var data = {order: 'desc'};

                            switch (type) {
                                case "all":
                                    break;
                                case "star":
                                    data.star = true;
                                    break;
                                default:
                                    data.type = type;
                            }
                            $.ajax({
                                url: API_HOST + "push/",
                                type: "GET",
                                async: true,
                                data: data,
                            }).done(function (resp) {
                                if (resp.code == 0) {
                                    console.log("下一页");
                                    console.log(resp.next);
                                    message_list_vm.next = resp.next
                                    message_list_vm.previous = resp.previous
                                    message_list_vm.messagelist = [];
                                    for (var message of resp.data) {
                                        message['extra'] = JSON.parse(message['extra']);
                                        message_list_vm.messagelist.push(message);
                                    }
                                    $('#pagination').twbsPagination('destroy');
                                    $('#pagination').twbsPagination({
                                      first: "第一页",
                                      prev: "上一页",
                                      next: "下一页",
                                      last: "最后一页",
                                      totalPages: resp.totalPage,
                                      visiblePages: 5,
                                      onPageClick: function(event, page) {
                                        var type = document.getElementById('message-nav').getElementsByClassName('active')[0].getAttribute('value');
                                        data = {
                                          'page': page,
                                          'order': 'desc',
                                          'order_by': 'id',
                                        };
                                        if (type == 'all') {}
                                        else if (type == 'star') {
                                          data['star'] = true
                                        }
                                        else {data['type'] = type}
                                        $.ajax({
                                            url: API_HOST + 'push/',
                                            type: "GET",
                                            async: true,
                                            data: data,
                                        }).done(function (resp) {
                                            message_list_vm.messagelist = [];
                                            if (resp.code == 0) {
                                                message_list_vm.messagelist = [];
                                                for (var message of resp.data) {
                                                    message['extra'] = JSON.parse(message['extra']);
                                                    message_list_vm.messagelist.push(message);
                                                }
                                                message_list_vm.next = resp.next
                                                message_list_vm.previous = resp.previous
                                            }
                                        });
                                      }
                                    });
                                }
                            });
                        },
                        read_all_message: readAllMsg,
                    },
                });
            }
        })

        // 初始化第一页
        this.request = function () {
            $.ajax({
                url: API_HOST + "push/?order=desc",
                type: "GET",
                async: true,
                data: this.params || {},
            }).done(function (resp) {
                if (resp.code == 0) {
                    message_list_vm.messagelist = [];
                    for (var message of resp.data) {
                        message['extra'] = JSON.parse(message['extra']);
                        message_list_vm.messagelist.push(message);
                    }

                    message_list_vm.next = resp.next;
                    message_list_vm.previous = resp.previous;
                    message_list_vm.totalPage = resp.totalPage;
                    $('#pagination').twbsPagination('destroy');
                    $('#pagination').twbsPagination({
                      first: "第一页",
                      prev: "上一页",
                      next: "下一页",
                      last: "最后一页",
                      totalPages: resp.totalPage,
                      visiblePages: 5,
                      onPageClick: function(event, page) {
                        message_list_vm.messagelist = [];
                        var type = document.getElementById('message-nav').getElementsByClassName('active')[0].getAttribute('value');
                        data = {
                          'page': page,
                          'order': 'desc',
                          'order_by': 'id',
                        };
                        if (type == 'all') {}
                        else {data['type'] = type}
                        $.ajax({
                            url: API_HOST + 'push/',
                            type: "GET",
                            async: true,
                            data: data,
                        }).done(function (resp) {
                            if (resp.code == 0) {
                                message_list_vm.messagelist = [];
                                for (var message of resp.data) {
                                    message['extra'] = JSON.parse(message['extra']);
                                    message_list_vm.messagelist.push(message);
                                }
                                message_list_vm.next = resp.next
                                message_list_vm.previous = resp.previous
                            }
                        });
                      }
                    });
                }
            });
        };

        this.request(message_list_vm);
    };
};
