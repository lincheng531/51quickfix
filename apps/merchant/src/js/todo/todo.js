/**
 * Created on 08 30, 2016
 * @author: tolerious
 */

/**
 * Todo管理
 * @constructor
 */

TodoItem = function () {
    id = '';
    title = '';
    user = '';
    deadline_timestamp = '';
    deadline_string = '';
    executor = '';
    gmt_create_timestamp = '';
    gmt_create_string = '';
    gmt_update_timestamp = '';
    gmt_update_string = '';
    group = '';
    is_done = false;
    is_star = false;
    notes = '';
    parent = '';
    partner = '';
    priority = '';
    review_set = [];
    status = '';
    timestamp = '';
    //timestamp  是Python时间
    this.format_timestamp = function (timestamp, version) {
        var _t = timestamp;
        if (version == 'now') {
            var _l = new Date();
            _t = _l.getTime();
        }
        var _d = new Date(_t);
        var _w = '';
        var arr = {
            '0': '天',
            '1': '一',
            '2': '二',
            '3': '三',
            '4': '四',
            '5': '五',
            '6': '六'
        };
        if (version == 'normal') {
            _w = _d.getDay();
        } else {
            _w = arr[_d.getDay()];
        }
        var _rd = {
            'year': _d.getFullYear(),
            'month': _d.getMonth() + 1,
            'day': _d.getDate(),
            'week': _w,
            'hour': _d.getHours(),
            'minute': _d.getMinutes(),
            'second': _d.getSeconds()
        };
        return _rd;
    };
    this.todoitem_timestring = function () {
        if (this.timestamp) {
            var _d = this.format_timestamp(this.timestamp);
            var day = _d.day;
            var month = _d.month;
            if (day < 10) {
                day = '0' + day;
            }
            if (month < 10) {
                month = '0' + month;
            }
            return month + "月" + day + '日' + " 周" + _d.week;
        } else {
            return '';
        }

    };
    this.get_today_timestamp = function () {
        var _d = new Date();
        var day = _d.getDate();
        var year = _d.getFullYear();
        var month = _d.getMonth() + 1;
        var time_string = year + '-' + month + '-' + day + ' ' + "23:59:59";
        var d = new Date(time_string);
        return d.getTime();
    };
    this.get_tomorrow_timestamp = function () {
        var _d = new Date();
        var day = _d.getDate() + 1;
        var year = _d.getFullYear();
        var month = _d.getMonth() + 1;
        var time_string = year + '-' + month + '-' + day + ' ' + "23:59:59";
        var d = new Date(time_string);
        return d.getTime();
    };
    this.doneitem_timestring = function () {
        if (this.timestamp) {
            var _d = this.format_timestamp(this.timestamp);
            var day = _d.day;
            var month = _d.month;
            if (day < 10) {
                day = '0' + day;
            }
            if (month < 10) {
                month = '0' + month;
            }
            return month + "月" + day + '日';
        } else {
            return '';
        }
    };
    this.child_timestring = function () {
        if (this.timestamp) {
            var _d = this.format_timestamp(this.timestamp);
            return _d.month + "月" + _d.day + '日';
        } else {
            return '';
        }
    };
    this.tododetail_timestring = function () {
        if (this.timestamp) {
            var _d = this.format_timestamp(this.timestamp);
            return _d.year + '-' + (_d.month < 10 ? "0" + _d.month : _d.month) + '-' + (_d.day < 10 ? "0" + _d.day : _d.day) + " " + (_d.hour < 10 ? "0" + _d.hour : _d.hour) + ":" + (_d.minute < 10 ? "0" + _d.minute : _d.minute);
        } else {
            return '';
        }

    };
    this.tododetail_deadline_timestring = function () {
        if (this.timestamp) {
            var _d = this.format_timestamp(this.timestamp);
            return _d.year + '-' + (_d.month < 10 ? "0" + _d.month : _d.month) + '-' + (_d.day < 10 ? "0" + _d.day : _d.day);

        } else {
            return '';
        }
    }
};

TodoList = function () {
    function swap_array_element(attr, index1, index2) {
        attr[index1] = attr.splice(index2, 1, attr[index1])[0];
        return attr;
    }

    function format_timestamp(timestamp, version) {
        var d = new Date(timestamp);
        var week = '';
        var arr = {
            '0': '天',
            '1': '一',
            '2': '二',
            '3': '三',
            '4': '四',
            '5': '五',
            '6': '六'
        };
        if (version == 'normal') {
            week = d.getDay();
        } else {
            week = arr[d.getDay()];
        }
        var dic = {
            'year': d.getFullYear(),
            'month': d.getMonth() + 1,
            'day': d.getDate(),
            'week': week,
            'hour': d.getHours(),
            'minute': d.getMinutes(),
            'second': d.getSeconds()
        };
        return dic;
    }

    function get_real_timestamp(timestamp) {
        return timestamp - 8 * 60 * 60 * 1000;
    }

    function setSelectionRange(input, selectionStart, selectionEnd) {
        if (input.setSelectionRange) {
            input.focus();
            input.setSelectionRange(selectionStart, selectionEnd);
        } else if (input.createTextRange) {
            var range = input.createTextRange();
            range.collapse(true);
            range.moveEnd('character', selectionEnd);
            range.moveStart('character', selectionStart);
            range.select();
        }
    }

    function setCaretToPos(input, pos) {
        setSelectionRange(input, pos, pos);
    }


    function doGetCaretPosition(oField) {

        // Initialize
        var iCaretPos = 0;

        // IE Support
        if (document.selection) {

            // Set focus on the element
            oField.focus();

            // To get cursor position, get empty selection range
            var oSel = document.selection.createRange();

            // Move selection start to 0 position
            oSel.moveStart('character', -oField.value.length);

            // The caret position is selection length
            iCaretPos = oSel.text.length;
        }

        // Firefox support
        else if (oField.selectionStart || oField.selectionStart == '0')
            iCaretPos = oField.selectionStart;

        // Return results
        return iCaretPos;
    }

    //Vue directive start.
    Vue.directive('sliver', {
        twoWay: true,
        bind: function () {
            var self = this;
            $(this.el).datetimepicker().on('changeDate', function (ev) {
                self.set(ev.date.valueOf())
            })
        },
        update: function (newValue, oldValue) {

        },
        unbind: function () {

        }
    });
    Vue.directive('gavatar', {
        bind: function () {
            // console.log("绑定了avatar指令");
        },
        update: function (user) {
            if (user) {
                if (user.avatar) {
                    // TODO 现在用固定图片，之后改成动态的。
                    // this.el.innerHTML = '<span class="w-40 circle warning avatar"><img src=' + 'http://img.allen.xin/avatar/20160908/61a469f2a29052f4181a6d05e00f91cd_128x128.jpg' + ' alt="..."></span>';
                    this.el.innerHTML = '<span class="w-32 circle avatar"><img src=' + IMAGE_URL + user.avatar.replace('.', '_128x128.') + ' alt="..." onerror="on_avatar_error()"></span>';
                }
                else {
                    this.el.innerHTML = '<span class="w-32 circle warning avatar"> <span>' + user.username[0] + '</span> <i class="on b-white"></i> </span>';
                }
            }
        },
    });
    Vue.directive('generate-avatar', {
        params: ['size'],
        update: function (newval, oldval) {
            var size = this.params.size;
            var user = {'username': newval};
            this.el.innerHTML = get_user_random_avatar(user, null, size);
        }
    });
    //Vue directive end.
    // Vue filter start.
    Vue.filter('comment_time_string', function (timestamp) {
        real_timestamp = timestamp * 1000;
        moment.locale('zh-cn');
        var str = moment(real_timestamp).fromNow();
        return str;
    });
    Vue.filter('to_item_timestring', function (timestamp) {
        var d = new TodoItem();
        if (timestamp) {
            // timestamp = get_real_timestamp(timestamp * 1000);
            d.timestamp = timestamp * 1000;
            return d.todoitem_timestring();
        } else {
            return '';
        }

    });
    Vue.filter('to_done_item_timestring', function (timestamp) {
        var d = new TodoItem();
        if (timestamp) {
            timestamp = get_real_timestamp(timestamp * 1000);
            d.timestamp = timestamp;
            return d.doneitem_timestring();
        } else {
            return '';
        }
    });
    Vue.filter('normal_count', function (val) {
        if (val > 100) {
            return '99+';
        } else {
            return val;
        }
    });
    Vue.filter('cut_title_words', function (text) {
        if (text.length > 20) {
            return text.substring(0, 20) + '...';
        } else {
            return text;
        }
    });
    Vue.filter('group_name_cut', function (text) {
        if (text.length > 8) {
            return text.substring(0, 5);
        } else {
            return text;
        }
    });
    Vue.filter('two_way_todo_detail_timestring', {
        read: function (timestamp) {
            var d = new TodoItem();
            timestamp = get_real_timestamp(timestamp * 1000);
            d.timestamp = timestamp;
            return d.tododetail_timestring();
        },
        write: function (new_t) {
            var d = new Date(new_t);
            var year = d.getFullYear();
            var month = d.getMonth() + 1;
            var day = d.getDate();
            var hour = d.getHours();
            var minute = d.getMinutes();
            var second = d.getSeconds();
            if (month < 10) {
                month = '0' + month;
            }
            if (hour < 10) {
                hour = '0' + hour;
            }
            if (minute < 10) {
                minute = '0' + minute;
            }
            var str = year + '-' + month + '-' + day + ' ' + hour + ':' + minute;
            return str;
        }
    });
    Vue.filter('to_child_timestring', function (timestamp) {
        var d = new TodoItem();
        timestamp = get_real_timestamp(timestamp * 1000);
        d.timestamp = timestamp;
        return d.child_timestring();
    });
    Vue.filter('to_tododetail_timestring', function (timestamp) {
        var d = new TodoItem();
        timestamp = get_real_timestamp(timestamp * 1000);
        d.timestamp = timestamp;
        return d.tododetail_timestring();
    });
    Vue.filter('filter_null', function (val) {
        if (val == null || val == '') {
            return '';
        }
    });
    // Vue filter end.
    function init_datetime_picker() {
        $('#datetimepicker').datetimepicker({
            format: 'yyyy-mm-dd hh:ii',
            timezone: 'CST',
            // autoclose: true,
            clearBtn: true,
            minView: 2
            // todayBtn: true
        });
        $('#child_datetimepicker').datetimepicker({
            format: 'yyyy-mm-dd',
            timezone: 'CST',
            // autoclose: true,
            clearBtn: true,
            minView: 2
            // todayBtn: true

        });
        $('#remind_datetimepicker').datetimepicker({
            format: 'yyyy-mm-dd hh:ii',
            timezone: 'CST',
            // autoclose: true,
            // todayBtn: true
            clearBtn: true
            //
        });
        // $('#son_calendar').datetimepicker({
        //     format: 'yyyy-mm-dd hh:ii',
        //     timezone: 'CST',
        //     // autoclose: true,
        //     // todayBtn: true,
        //     clearBtn: true
        // });
        // $("#son_calendar").datetimepicker().on('hide', function (ev) {
        //     var da = ev.date;
        //     var timestamp = get_real_timestamp(da.getTime());
        //     vml.current_child_timestamp = timestamp;
        //     var d = new TodoItem();
        //     d.timestamp = timestamp;
        //     $("#child_calendar").html(d.child_timestring());
        // });
        $('#datetimepicker').datetimepicker().on('hide', function (ev) {
            var da = ev.date;
            var timestamp = get_real_timestamp(da.getTime());
            vml.global_timestamp = timestamp;
        });
        $('#remind_datetimepicker').datetimepicker().on('hide', function (ev) {
            var da = ev.date;
            var timestamp = get_real_timestamp(da.getTime());

            vml.detail.remindme = timestamp / 1000;
            var d = new TodoItem();
            d.timestamp = timestamp;
            vml.detail.remindme_string = d.tododetail_timestring();
            vml.detail.remindme = timestamp / 1000;
            if (vml.backup_group_id != -1 && vml.backup_group_id != -2) {
                if (vml.detail.is_done) {
                    var item_obj = vml.donelist[vml.detail.index];
                } else {
                    var item_obj = vml.todolist[vml.detail.index];
                }
                var key = vml.detail.id;
                item_obj.remindme = timestamp / 1000;
                $.ajax({
                    type: 'PATCH',
                    url: API_HOST + 'todo/detail/' + key,
                    data: {
                        remindme: timestamp / 1000
                    }
                }).done(function (resp) {
                    if (resp.code == 0) {
                        // item_obj.remindme = resp.data.remindme;
                    }
                })
            } else {
                $.ajax({
                    type: 'PATCH',
                    url: API_HOST + 'todo/detail/' + vml.todo_global_id,
                    data: {
                        remindme: timestamp / 1000
                    }
                }).done(function (resp) {
                    if (resp.code == 0) {
                        $.each(vml.stodolist, function (index, element) {
                            $.each(element.children, function (s_index, s_element) {
                                if (s_element.id == vml.todo_global_id) {
                                    s_element.remindme = timestamp / 1000;
                                }
                            })
                        })
                    }
                })
            }
        });
        $('#child_datetimepicker').datetimepicker().on('hide', function (ev) {
            var da = ev.date;
            da_now = new Date();
            var da_now_day = new Date(da_now.getFullYear() + '-' + (da_now.getMonth() + 1) + '-' + da_now.getDate() + ' 23:59:59');
            var end_day = new Date(da.getFullYear() + '-' + (da.getMonth() + 1) + '-' + da.getDate() + ' 23:59:59');
            id_list = new Array();
            $.each(vml.today_todo_list, function (index, element) {
                id_list.push(element.id);
            });
            if (end_day.getTime() < da_now_day.getTime()) {
                // delay
                console.log('delay...');

                if (id_list.indexOf(vml.todo_global_id) > -1) { // in list
                    var local_obj;
                    $.each(vml.today_todo_list, function (index, element) {
                        if (element.id == vml.todo_global_id) {
                            if (element.delay) {// is delay

                            } else {
                                element.delay = true;
                                vml.today_delay_count += 1;
                            }
                        }
                    })
                } else { // out of list
                    var obj = new Object();
                    obj.id = vml.todo_global_id;
                    obj.delay = true;
                    obj.today = true;
                    vml.today_todo_list.push(obj);
                    vml.today_delay_count += 1;
                    vml.today_all_count += 1;
                }
            } else if (end_day.getTime() == da_now_day.getTime()) {
                //on today, does not delay
                if (id_list.indexOf(vml.todo_global_id) > -1) { // in list
                    var local_obj;
                    $.each(vml.today_todo_list, function (index, element) {
                        if (element.id == vml.todo_global_id) {
                            if (element.delay) {
                                element.delay = false;
                                if (vml.today_delay_count > 0) {
                                    vml.today_delay_count -= 1;
                                }
                            } else {
                                // pass , nothing to do
                            }
                        }
                    })
                } else { // out of list
                    var obj = new Object();
                    obj.id = vml.todo_global_id;
                    obj.delay = false;
                    obj.today = true;
                    vml.today_todo_list.push(obj);
                    vml.today_all_count += 1;
                }
            } else {
                //not on today
                console.log('other day...');
                var local_index;
                if (id_list.indexOf(vml.todo_global_id) > -1) { // in list
                    $.each(vml.today_todo_list, function (index, element) {
                        if (element.id == vml.todo_global_id) {
                            local_index = index;
                            element.delay = false;
                            element.today = false;
                            if (vml.today_all_count > 0) {
                                vml.today_all_count -= 1;
                            }
                            if (vml.today_delay_count > 0) {
                                vml.today_delay_count -= 1;
                            }
                        }
                    });
                    vml.today_todo_list.splice(local_index, 1);
                } else { //out of list
                    // nothing to do
                }
            }
            if (!da) {
                return;
            }
            var timestamp = get_real_timestamp(da.getTime());
            var d = new TodoItem();
            vml.detail.deadline = timestamp / 1000;
            d.timestamp = timestamp;
            vml.detail.deadline_string = d.tododetail_deadline_timestring();
            if (vml.backup_group_id != -1 && vml.backup_group_id != -2) {
                if (vml.detail.is_done) {
                    var item_obj = vml.donelist[vml.detail.index];
                } else {
                    var item_obj = vml.todolist[vml.detail.index];
                }
                var key = vml.detail.id;
                item_obj.deadline = end_day.getTime() / 1000;
                // $('.item_weekday_' + key).html(item_obj.deadline_string);
                $.ajax({
                    type: 'PATCH',
                    url: API_HOST + 'todo/detail/' + key,
                    data: {
                        deadline: timestamp / 1000
                    }
                }).done(function (resp) {
                    if (resp.code == 0) {
                    }
                });
            } else {
                $.ajax({
                    type: 'PATCH',
                    url: API_HOST + 'todo/detail/' + vml.todo_global_id,
                    data: {
                        deadline: end_day.getTime() / 1000
                    }
                }).done(function (resp) {
                    if (resp.code == 0) {
                        $.each(vml.stodolist, function (index, element) {
                            $.each(element.children, function (s_index, s_element) {
                                if (s_element.id == vml.todo_global_id) {
                                    s_element.deadline = timestamp / 1000;
                                }
                            })
                        })
                    }
                });
            }
        });

        $("#datetimepicker").datetimepicker().on('hide', function (ev) {
            var da = ev.date;
            var temp = da.getTime();
            var timestamp = get_real_timestamp(temp);
            vml.detail.timestamp = timestamp;
            var t = new Date(timestamp);
            var month = t.getMonth() + 1;
            var day = t.getDate();
            var week = t.getDay();
            var year = t.getFullYear();
            var dic = {
                '0': '天',
                '1': '一',
                '2': '二',
                '3': '三',
                '4': '四',
                '5': '五',
                '6': '六'
            };
            var new_week = dic[week];
            var time_string = month + "月" + day + "日" + " 周" + new_week;
            $("#middle_deadline").html(time_string);
        });
    }

    function show_pane(boo) {
        if (boo == 'normal') { // normal pane show
            vml.show_normal = true;
            vml.show_special = false;
            vml.show_search = false;
        } else if (boo == 'special') { // special pane show
            vml.show_special = true;
            vml.show_normal = false;
            vml.show_search = false;
        } else if (boo == 'search') { // search pane show
            vml.show_search = true;
            vml.show_special = false;
            vml.show_normal = false;
        }
    }

    function bubble_sort(array, key) {
        for (var i = 0; i < array.length; i++) {
            for (var j = i; j < array.length; j++) {
                if (array[i][key] < array[j][key]) {
                    var temp = array[i];
                    array[i] = array[j];
                    array[j] = temp;
                }
            }
        }
    }

    function getParameterByName(name, url) {
        if (!url) {
            url = window.location.href;
        }
        name = name.replace(/[\[\]]/g, "\\$&");
        var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

    global_at_name_list = [];
    global_at_id_list = [];
    new_ll = new Array();
    function init_at_list(at_start, keyword) {
        var at_start = "@";
        $('#add_todo_input').atwho({
            at: '@',
            delay: 400,
            // data: 'http://localhost:8000/api/v1/user/search?search=',
            displayTpl: "<li><span class='fa fa-user-md'></span> ${name}</li>",
            callbacks: {
                remoteFilter: function (query, callback) {
                    ll = new Array();
                    $.getJSON(API_HOST + 'user/search?search=' + query, function (resp) {
                        if (resp.code == 0) {
                            $.each(resp.data, function (index, element) {
                                s_username = element.username.toLowerCase();
                                s_name = element.name;
                                s_name = s_name.replace(' ', '').toLowerCase();
                                if (element.username == element.name || s_username == s_name) {
                                    ll.push({id: element.id, name: element.username})
                                    new_ll.push({id: element.id, name: element.username})
                                } else {
                                    ll.push({id: element.id, name: element.username});
                                    ll.push({id: element.id, name: element.name});
                                    // ll.push({id: element.id, name: element.name});
                                    new_ll.push({id: element.id, name: element.username});
                                    new_ll.push({id: element.id, name: element.name});
                                    // new_ll.push({id: element.id, name: element.name});
                                }
                            });
                            callback(ll);
                        }
                    })
                },
            }
        });


        $("#add_todo_input").on("hidden.atwho", function (event) {
        });
        $("#add_todo_input").on("matched.atwho", function (event, flag, query) {
            // console.log(event);
            // console.log(flag);
            // console.log(query);
        });
        $("#add_todo_input").on("inserted.atwho", function (j_event, el, b_event) {
            // console.log(el[0].innerText);
            var text = $.trim(el[0].innerText);
            $.each(ll, function (index, element) {
                if (element.name == text) {
                    global_at_id_list.push(element.id);
                }
            });
            global_at_name_list.push(text);
            vml.can_add_todo = false;
            vml.choose_at_item_list = false;
        })
    }

    this.clear_data = function () {
        if (vml.g_datetimepicker == 'remindme') {
            $.ajax({
                type: 'PATCH',
                url: API_HOST + 'todo/detail/' + vml.todo_global_id,
                data: {
                    remindme: 'st'
                }
            }).done(function (resp) {
                if (resp.code == 0) {
                    $.each(vml.todolist, function (index, element) {
                        if (element.id == vml.detail.id) {
                            element.remindme = '';
                        }
                    })
                }
            });
        } else if (vml.g_datetimepicker == 'deadline') {
            $.ajax({
                type: 'PATCH',
                url: API_HOST + 'todo/detail/' + vml.todo_global_id,
                data: {
                    deadline: 'st'
                }
            }).done(function (resp) {
                if (resp.code == 0) {
                    $(".item_weekday_" + vml.detail.id).html('');
                    $.each(vml.todolist, function (index, element) {
                        if (element.id == vml.detail.id) {
                            element.deadline = '';
                        }
                    })
                }
            });
        }
    };
    this.init_todo_list = function () {
        // init_context_menu();
        /*
         global variable start
         */
        todolist = [];
        donelist = [];
        has_click = false;

        /*
         global variable end
         */

        Vue.config.delimiters = ['${', '}'];
        //init group sortable items.
        $('.sortable').sortable();
        $('textarea').flexText();
        init_at_list('@', '');
        var sortable_el = document.getElementById('group_ul');
        sortable = new Sortable(sortable_el, {
            onStart: function (evt) {
            },
            onEnd: function (evt) {
                var ll = $('.group_item_container');
                var local_list = [];
                $.each(ll, function (index, element) {
                    var id = element.id.split("_")[2];
                    local_list.push(id);
                });
                var pre_index = evt.oldIndex;
                var aft_index = evt.newIndex;
                if (pre_index == aft_index) {

                } else {
                    var post_data = {
                        'g_list': JSON.stringify(local_list)
                    };
                    $.ajax({
                        type: 'POST',
                        url: API_HOST + 'todo/group/order/',
                        data: post_data
                    }).done(function (resp) {

                    })
                }
            },
            onAdd: function (evt) {
            }
        });
        //init datetime picker
        init_datetime_picker();
        setTimeout(function () {
            init_datetime_picker();
        }, 300);
        //get use group
        $.getJSON(API_HOST + 'todo/group', function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                // vml.grouplist = data;
                vml.sub_grouplist = data;
                var request_group_id;
                $.each(data, function (index, element) {
                    // var l_dic = new Array();
                    // l_dic[element.id] = '';
                    if (element.status == 2) {
                        request_group_id = element.id;
                        vml.groupid = request_group_id;
                        vml.default_group_id = element.id;
                    }
                    if (element.sort != -2) {
                        vml.grouplist.push(element);
                    } else if (element.sort == -1) {
                        vml.inbox_group = element;
                        vml.inbox_group_id = element.id;
                        vml.groupid = element.id;
                        // $(".todo_header_name").html(element.name);
                    }
                    if (element.sort == -2) {
                        vml.send_delay_count = element.delay_cnt;
                        vml.send_all_count = element.todo_cnt;
                        vml.outbox_group = element;
                        vml.outbox_group_id = element.id;
                    }
                });
                // vml.groupid = vml.grouplist[0].id;
                vml.groupindex = 0;
                // $.getJSON(API_HOST + 'todo/group/' + vml.inbox_group_id, function (resp) {
                //     if (resp.code == 0) {
                //         var data = resp.data;
                //         var todo_l = data.todolist_set;
                //         $.each(todo_l, function (index, element) {
                //             if (this.status == 1 && String(this.parent) == 'null') {
                //                 vml.todolist.push(this);
                //             } else if (this.status == 2 && String(this.parent) == 'null') {
                //                 vml.donelist.push(this);
                //             }
                //         });
                //     }
                // });
                vml.backup_group_id = 0;
                var query_group_id = getParameterByName('group');
                if (query_group_id) {
                    $.each(vml.grouplist, function (index, element) {
                        if (element.id == query_group_id) {
                            $('.todo_header_name').html(element.name);
                        } else if (query_group_id == vml.outbox_group_id) {
                            $('.todo_header_name').html('发件箱');
                        } else if (query_group_id == 'star') {
                            $('.todo_header_name').html('已加星标');
                        } else if (query_group_id == 'today') {
                            $('.todo_header_name').html('今天');
                        } else if (query_group_id == 'inbox') {
                            $('.todo_header_name').html('收件箱');
                        }
                        else {
                            $('.todo_header_name').html('不存在此分组');
                        }
                    });
                    if (query_group_id == 'star' || query_group_id == 'today') {
                        $.getJSON(API_HOST + 'todo/item/?type=' + query_group_id, function (resp) {
                            if (resp.code == 0) {
                                var data = resp.data;
                                vml.stodolist = data;
                                if (query_group_id == vml.outbox_group_id) {
                                    $("#group_send").addClass('group_bk');
                                } else if (query_group_id == 'outbox') {
                                    show_pane('normal');
                                    $("#group_send").addClass('group_bk');
                                } else if (query_group_id == 'today') {
                                    show_pane('special');
                                    $("#add_todo_input").attr('placeholder', '添加今天到期的任务...');
                                    $("#group_today").addClass('group_bk');
                                } else if (query_group_id == 'star') {
                                    show_pane('special');
                                    $("#add_todo_input").attr('placeholder', '添加一个星标任务...');
                                    $("#group_star").addClass('group_bk');
                                }
                            }
                        })
                    } else if (query_group_id == 'inbox') {
                        $("#group_inbox").addClass('group_bk');
                        $.getJSON(API_HOST + 'todo/relation', function (resp) {
                            if (resp.code == 0) {
                                show_pane('normal');
                                var data = resp.data;
                                $.each(data, function (index, element) {
                                    if (element.status == 1) {
                                        vml.todolist.push(element);
                                    } else {
                                        vml.donelist.push(element);
                                    }
                                })
                            }
                        })
                    }
                    else {
                        $.getJSON(API_HOST + 'todo/group/' + query_group_id, function (resp) {
                            if (resp.code == 0) {
                                show_pane('normal');
                                var data = resp.data.todolist_set;
                                $.each(data, function (index, element) {
                                    if (element.status == 1) {
                                        vml.todolist.push(element);
                                    } else {
                                        vml.donelist.push(element);
                                    }
                                });
                                var query_group_id = getParameterByName('group');
                                if (query_group_id) {
                                    if (query_group_id == vml.outbox_group_id) {
                                        $("#group_send").addClass('group_bk');
                                    } else if (query_group_id == 'outbox') {
                                        $("#group_send").addClass('group_bk');
                                    } else if (query_group_id == 'today') {
                                        $("#group_today").addClass('group_bk');
                                    } else if (query_group_id == 'star') {
                                        $("#group_star").addClass('group_bk');
                                    }
                                    else {
                                        $("#group_item_" + query_group_id).addClass('group_bk');
                                    }
                                } else {
                                    $("#group_item_" + request_group_id).addClass('group_bk');

                                }
                            }
                        });

                    }
                } else {
                    $('.todo_header_name').html('默认分组');
                    $("#add_todo_input").attr('placeholder', '添加一个任务...');
                    $.getJSON(API_HOST + 'todo/group/' + request_group_id, function (resp) {
                        if (resp.code == 0) {
                            show_pane('normal');
                            var data = resp.data.todolist_set;
                            $.each(data, function (index, element) {
                                if (element.status == 1) {
                                    vml.todolist.push(element);
                                } else {
                                    vml.donelist.push(element);
                                }
                            });
                            var query_group_id = getParameterByName('group');
                            if (query_group_id) {
                                if (query_group_id == vml.outbox_group_id) {
                                    $("#group_send").addClass('group_bk');
                                } else {
                                    $("#group_item_" + query_group_id).addClass('group_bk');
                                }
                            } else {
                                $("#group_item_" + request_group_id).addClass('group_bk');

                            }
                        }
                    });
                }

                vml.item.showallcollapse = true;
                vml.show_calendar = true;
                // $.getJSON(API_HOST + 'todo/item/?type=today', function (resp) {
                //     if (resp.code == 0) {
                //         show_pane('special');
                //         var data = resp.data;
                //         vml.stodolist = data;
                //         $('.todo_item_collapse').fadeOut('slow');
                //         $.each(data, function (index, element) {
                //             $.each(element.children, function (index, element) {
                //                 // local_todolist.push(element);
                //             })
                //         })
                //     }
                // });
                $.getJSON(API_HOST + 'todo/item/', function (resp) {
                    if (resp.code == 0) {
                        var data = resp.data;
                        vml.star_delay_count = data.star_delay_count;
                        vml.star_all_count = data.star_count;
                        vml.today_delay_count = data.today_delay_count;
                        vml.today_all_count = data.today_count;
                        vml.receive_delay_count = data.receive_delay_count;
                        vml.receive_all_count = data.receive_all_count;
                        $.each(data.today_id_list, function (index, element) {
                            var obj = new Object();
                            if (data.today_delay_id_list.indexOf(element) > -1) {
                                obj.id = element;
                                obj.delay = true;
                                obj.today = true;
                                vml.today_todo_list.push(obj);
                            } else {
                                obj.id = element;
                                obj.delay = false;
                                obj.today = true;
                                vml.today_todo_list.push(obj);
                            }
                        })
                    }
                })
            }
        });

        vml = new Vue({
            el: '#todo_total_container',
            data: {
                modal: {
                    value: '',
                    title: '',
                    eventname: '',
                    modal_input: false,
                    modal_p: false,
                    placeholder: ''
                },
                icon: {
                    today: '',
                    tomorrow: ''
                },
                show_move_sub_menu: true,
                today_todo_list: [],
                tend_delete_todo_obj: '',
                default_group_id: '',
                global_timestamp: '',
                show_calendar: false,
                post_comment_to_child: false,
                parent_comment_index: false,
                parent_comment_id: '',
                child_comment_user_id: '',
                g_datetimepicker: '',
                add_todo_input_keydown_val: '',
                add_todo_old_val: '',
                add_todo_new_val: '',
                add_todo_old_keycode: '',
                add_todo_new_keycode: '',
                choose_at_item_list: false,
                can_add_todo: true,
                group_delete_id: '',
                todo_global_id: '',
                todo_global_obj: '',
                todo_global_index: '',
                todolist: todolist,
                donelist: donelist,
                searchlist: [],
                stodolist: [],
                grouplist: [],
                sub_grouplist: [],  // for generate move submenus
                current_child_timestamp: '',
                groupid: '',
                groupindex: '',
                group_edit: true,
                group_edit_not: false,
                show_normal: false,
                show_special: true,
                show_search: false,
                current_group_title: '',
                inbox_group: '',
                inbox_group_id: '',
                outbox_group: '',
                outbox_group_id: '',
                backup_group_id: ' ',  // 用来指示是点击'已加星标'跟'今天'两个选项中的一个.
                star_delay_count: 0,
                star_all_count: 0,
                today_delay_count: 0,
                global_group_obj: '',
                today_all_count: 0,
                send_delay_count: 0,
                send_all_count: 0,
                receive_delay_count: 0,
                receive_all_count: 0,
                item: {
                    donecollapsed: false,
                    showdoneitem: false,
                    showallcollapse: false
                },
                styleclass: {
                    group_item: {},
                    white_color: true,
                    normal_color: true
                },
                detail: {
                    id: '',
                    title: '',
                    deadline: '',
                    deadline_string: '',
                    remindme: '',
                    remindme_string: '',
                    gmt_create: '',
                    gmt_update: '',
                    gmt_complete: '',
                    children: [],
                    notes: '',
                    status: '',
                    comment_list: [],
                    user: '',
                    is_done: false,
                    is_star: false,
                    index: '',
                    groupid: '',
                }
            },
            computed: {
                group_item_name_class: function () {
                    var color_class = {
                        'white_color': this.white_color,
                        'normal_color': this.normal_color
                    };
                    if (this.styleclass.selected) {
                        // return ['white_color'];
                        return color_class;
                    } else {
                        // return ['normal_color'];
                        return color_class;
                    }
                }
            },
            watch: {
                'item.showdoneitem': function (val, oldval) {
                    if (val) {
                        $('.done_item').fadeIn();
                    } else {
                        $('.done_item').fadeOut();
                    }
                },
                'item.showallcollapse': function (val, oldval) {
                    if (val) {
                    } else {
                    }
                }
            },
            methods: {
                calculate_modal: function () {
                    var w_width = $(document.body).width();
                    var t_width = (w_width - 600) / 2;
                    $('.my_modal').css('left', t_width);
                },
                show_add_group: function () {
                    vml.modal.title = '创建新分组';
                    vml.modal.eventname = 'addgroup';
                    vml.modal.modal_input = true;
                    vml.modal.modal_p = false;
                    vml.modal.placeholder = '请输入新分组名称';
                    vml.modal.value = '';
                    vml.calculate_modal();
                    vml.show_input_modal();
                },
                addgroup: function () {
                    var new_group_name = $.trim($("#input-group-name").val());
                    if (new_group_name) {
                        //  nothing
                    } else {
                        toastr.warning("分组名称不能为空.");
                        return;
                    }
                    $.ajax({
                        type: 'POST',
                        url: API_HOST + 'todo/group',
                        data: {
                            name: new_group_name
                        }
                    }).done(function (resp) {
                        if (resp.code == 0) {
                            vml.grouplist.push(resp.data);
                        }
                    });
                    $("#input-group-name").val("");
                },
                other_group_item_click: function (parm) {
                    vml.todolist = [];
                    vml.donelist = [];
                    $("#search_todo").val('');
                    $("#sort_title").html("按字母顺序排序");
                    $('#right_pane').addClass('hide');
                    has_click = false;
                    vml.styleclass.selected = true;
                    $('#group_inbox').removeClass('group_bk');
                    $('#group_star').removeClass('group_bk');
                    $('#group_today').removeClass('group_bk');
                    $('#group_send').removeClass('group_bk');
                    $("#" + parm).addClass('group_bk');
                    $.each(vml.grouplist, function (index, element) {
                        $('#group_item_' + element.id).removeClass('group_bk');
                    });
                    if (parm == 'group_inbox') {
                        $("#add_todo_input").attr('placeholder', '添加一个任务...');
                        vml.show_calendar = true;
                        $("#add_todo_input").attr('placeholder', '添加任务后请到默认分组中查看...');
                        $('#sort_title').removeClass('sort_style');
                        $("#sort_title").attr('data-toggle', 'dropdown');
                        vml.groupid = vml.inbox_group_id;
                        vml.backup_group_id = 0;
                        show_pane('normal');
                        vml.item.showallcollapse = true;
                        $('.todo_header_name').html('收件箱');
                        vml.todolist = [];
                        vml.donelist = [];
                        $.getJSON(API_HOST + 'todo/relation', function (resp) {
                            if (resp.code == 0) {
                                var data = resp.data;
                                $.each(data, function (index, element) {
                                    if (element.status == 1) {
                                        vml.todolist.push(element);
                                    } else {
                                        vml.donelist.push(element);
                                    }
                                })
                            }
                        })

                    } else if (parm == 'group_star') {
                        $("#add_todo_input").attr('placeholder', '添加一个星标任务...');
                        vml.show_calendar = true;
                        $("#sort_title").addClass('sort_style');
                        $("#sort_title").attr('data-toggle', '');
                        $("#drop_down_menu").removeClass('open');
                        vml.backup_group_id = -1;
                        $('.todo_header_name').html('已加星标');
                        show_pane('special');
                        vml.item.showallcollapse = false;
                        vml.groupid = vml.inbox_group_id;
                        var local_todolist = [];
                        $('.todo_item_collapse').fadeOut('slow');
                        $.getJSON(API_HOST + 'todo/item/?type=star', function (resp) {
                            if (resp.code == 0) {
                                var data = resp.data;
                                vml.stodolist = data;
                                $.each(data, function (index, element) {
                                    $.each(element.children, function (index, element) {
                                        local_todolist.push(element);
                                    })
                                })
                            }
                        });
                        vml.todolist = local_todolist;
                        setTimeout(function () {
                            init_datetime_picker();
                        }, 300);
                    } else if (parm == 'group_today') {
                        $("#add_todo_input").attr('placeholder', '添加今天到期的任务...');
                        vml.show_calendar = false;
                        $("#sort_title").addClass('sort_style');
                        $("#sort_title").attr('data-toggle', '');
                        $("#drop_down_menu").removeClass('open');
                        vml.backup_group_id = -2;
                        vml.item.showallcollapse = false;
                        $('.todo_header_name').html('今天');
                        show_pane('special');
                        vml.groupid = vml.default_group_id;
                        var local_todolist = [];
                        $('.todo_item_collapse').fadeOut('slow');
                        $.getJSON(API_HOST + 'todo/item/?type=today', function (resp) {
                            if (resp.code == 0) {
                                var data = resp.data;
                                vml.stodolist = data;
                                $.each(data, function (index, element) {
                                    $.each(element.children, function (index, element) {
                                        local_todolist.push(element);
                                    })
                                })
                            }
                        })
                    } else if (parm == 'group_send') {
                        $("#add_todo_input").attr('placeholder', '添加任务后请到默认分组中查看...');
                        vml.show_calendar = true;
                        // $("#sort_title").addClass('sort_style');
                        // $("#sort_title").attr('data-toggle', '');
                        // $("#drop_down_menu").removeClass('open');
                        vml.backup_group_id = -3;
                        vml.item.showallcollapse = false;
                        $('.todo_header_name').html('发件箱');
                        vml.item.showallcollapse = true;
                        show_pane('normal');
                        vml.todolist = [];
                        vml.donelist = [];
                        $.getJSON(API_HOST + 'todo/group/' + vml.outbox_group_id, function (resp) {
                            if (resp.code == 0) {
                                var data = resp.data.todolist_set;
                                $.each(data, function (index, element) {
                                    if (element.status == 1) {
                                        vml.todolist.push(element);
                                    } else {
                                        vml.donelist.push(element);
                                    }
                                })
                            }
                        });
                    }
                },
                groupitemclick: function (db, da) {
                    $("#sort_title").html("那字母顺序排序");
                    vml.todolist = [];
                    vml.donelist = [];
                    $("#search_todo").val('');
                    vml.show_calendar = true;
                    $("#add_todo_input").attr('placeholder', '添加一个任务...');
                    $('#sort_title').removeClass('sort_style');
                    $("#sort_title").attr('data-toggle', 'dropdown');
                    $('#right_pane').addClass('hide');
                    has_click = false;
                    show_pane('normal');
                    $('.todo_item_collapse').fadeIn('slow');
                    vml.item.showallcollapse = true;
                    vml.backup_group_id = 0;
                    var group_obj = vml.grouplist[db];
                    var key = group_obj.id;
                    vml.groupid = key;
                    vml.groupindex = db + 1;
                    var todo_list = [];
                    var done_list = [];
                    $.each(vml.grouplist, function (index, element) {
                        $('#group_item_' + element.id).removeClass('group_bk');
                    });
                    $('#group_inbox').removeClass('group_bk');
                    $('#group_star').removeClass('group_bk');
                    $('#group_today').removeClass('group_bk');
                    $('#group_send').removeClass('group_bk');
                    vml.styleclass.selected = false;
                    $('#group_item_' + key).addClass('group_bk');
                    vml.current_group_title = group_obj.name;
                    $('.todo_header_name').html(group_obj.name);
                    $.getJSON(API_HOST + 'todo/group/' + key, function (resp) {
                        if (resp.code == 0) {
                            var data = resp.data.todolist_set;
                            $.each(data, function (index, element) {
                                if (this.status == 1 && String(this.parent) == 'null') {
                                    todo_list.push(this);
                                } else if (this.status == 2 && String(this.parent) == 'null') {
                                    done_list.push(this);
                                }
                            });
                            vml.todolist = todo_list;
                            vml.donelist = done_list;
                        }
                    });
                    setTimeout(function () {
                        init_datetime_picker();
                    }, 300);
                },
                done_is_star: function (db) {
                    var done_obj = vml.donelist[db];
                    if (done_obj.is_star == '1') {
                        return true;
                    } else {
                        return false;
                    }
                },
                clickaddtodo: function (da) {
                    $("#addtodo").html("");
                },
                addtodo: function () {
                    $("#middle_deadline").html("");
                    if (vml.can_add_todo) {

                    } else {
                        return;
                    }
                    var title = $('#add_todo_input').val();
                    var is_star = false;
                    if (title == "") {
                        toastr.warning('标题不能为空');
                        return;
                    }
                    if (vml.detail.timestamp) {

                    } else {
                        var d = new Date();
                        vml.detail.timestamp = d.getTime();
                    }
                    $("#add_todo_input").val("");
                    if (vml.backup_group_id == -1 || vml.backup_group_id == -2) {
                        vml.groupid = vml.inbox_group_id;
                        if (vml.backup_group_id == -1) { // 已加星标分组
                            is_star = true;
                            vml.star_all_count += 1;
                            vml.inbox_group.todo_cnt += 1;
                        } else { // 今天分组
                            vml.today_all_count += 1;
                            vml.inbox_group.todo_cnt += 1;
                        }
                    } else {

                    }
                    if (vml.groupid == vml.inbox_group_id && vml.backup_group_id != -1 && vml.backup_group_id != -2) { //说明是在收件箱中
                        vml.inbox_group.todo_cnt += 1;
                    }
                    if (vml.backup_group_id == 0 && vml.groupid != vml.inbox_group_id) { // 说明是普通组
                        var group_obj;
                        // $.each(vml.grouplist, function (index, element) {
                        //     if (element.id == vml.groupid) {
                        //         group_obj = element;
                        //         group_obj.todo_cnt += 1;
                        //     }
                        // })
                    }
                    if (vml.backup_group_id == -2) {
                        var d = new Date();
                        $.ajax({
                            type: 'POST',
                            url: API_HOST + 'todo/',
                            data: {
                                title: title,
                                group: vml.default_group_id,
                                is_star: is_star,
                                deadline: d.getTime() / 1000
                            }
                        }).done(function (resp) {
                            vml.global_timestamp = '';
                            var data = resp.data;
                            // vml.todolist.push(data);
                            vml.add_group_count(vml.default_group_id);
                            var has_default_group = false;
                            $.each(vml.stodolist, function (index, element) {
                                if (element.group.id == vml.default_group_id) {
                                    has_default_group = true;
                                }
                            })
                            if (has_default_group) {
                                // vml.stodolist[0].children.unshift(data);
                                // vml.stodolist[0].children[0].deadline = data.deadline;
                                $.each(vml.stodolist, function (index, element) {
                                    if (element.group.id == vml.default_group_id) {
                                        element.children.unshift(data);
                                    }
                                    // if (element.group.id == vml.default_group_id) {
                                    //     console.log('abc');
                                    // element.children.unshift(data);
                                    // s_element.deadline = data.deadline;
                                    // }
                                })
                            } else {
                                var group_obj;
                                $.each(vml.grouplist, function (index, element) {
                                    if (element.id == vml.default_group_id) {
                                        group_obj = element;
                                    }
                                });
                                var dic = {
                                    children: [],
                                    group: group_obj
                                };
                                dic.children.push(data);
                                vml.stodolist.push(dic);
                            }
                            var index = vml.groupindex;
                            var group_obj = vml.grouplist[index];
                        })
                    } else if (vml.backup_group_id == -1) {
                        if (vml.global_timestamp) {
                            $.ajax({
                                type: 'POST',
                                url: API_HOST + 'todo/',
                                data: {
                                    title: title,
                                    group: vml.default_group_id,
                                    is_star: is_star,
                                    deadline: vml.global_timestamp / 1000
                                }
                            }).done(function (resp) {
                                vml.global_timestamp = '';
                                var data = resp.data;
                                vml.add_group_count(vml.default_group_id);
                                // vml.todolist.push(data);
                                if (vml.stodolist.length > 0) {
                                    // vml.stodolist[0].children.unshift(data);
                                    // vml.stodolist[0].children[0].deadline = data.deadline;
                                    $.each(vml.stodolist, function (index, element) {
                                        if (element.group.id == vml.default_group_id) {
                                            element.children.unshift(data);
                                        }
                                    })
                                } else {
                                    var group_obj;
                                    $.each(vml.grouplist, function (index, element) {
                                        if (element.id == vml.default_group_id) {
                                            group_obj = element;
                                        }
                                    });
                                    var dic = {
                                        children: [],
                                        group: group_obj
                                    };
                                    dic.children.push(data);
                                    vml.stodolist.push(dic);
                                }
                                var index = vml.groupindex;
                                var group_obj = vml.grouplist[index];
                            })
                        } else {
                            $.ajax({
                                type: 'POST',
                                url: API_HOST + 'todo/',
                                data: {
                                    title: title,
                                    group: vml.default_group_id,
                                    is_star: is_star
                                }
                            }).done(function (resp) {
                                var data = resp.data;
                                // vml.todolist.push(data);
                                vml.add_group_count(vml.default_group_id);
                                if (vml.stodolist.length > 0) {
                                    // vml.stodolist[0].children.unshift(data);
                                    // vml.stodolist[0].children[0].deadline = data.deadline;
                                    $.each(vml.stodolist, function (index, element) {
                                        if (element.group.id == vml.default_group_id) {
                                            element.children.unshift(data);
                                        }
                                    })
                                } else {
                                    var group_obj;
                                    $.each(vml.grouplist, function (index, element) {
                                        if (element.id == vml.default_group_id) {
                                            group_obj = element;
                                        }
                                    });
                                    var dic = {
                                        children: [],
                                        group: group_obj
                                    };
                                    dic.children.push(data);
                                    vml.stodolist.push(dic);
                                }
                                var index = vml.groupindex;
                                var group_obj = vml.grouplist[index];
                            })
                        }

                    }
                    else {
                        var local_group_id = '';
                        if (vml.groupid) {
                            local_group_id = vml.groupid;
                        } else {
                            local_group_id = vml.default_group_id;
                        }
                        if (vml.global_timestamp) { // has timestamp
                            $.ajax({
                                type: 'POST',
                                url: API_HOST + 'todo/',
                                data: {
                                    title: title,
                                    group: local_group_id,
                                    is_star: is_star,
                                    deadline: vml.global_timestamp / 1000
                                }
                            }).done(function (resp) {
                                vml.global_timestamp = '';
                                if (vml.groupid) {
                                    var data = resp.data;
                                    // vml.todolist.push(data);
                                    vml.todolist.unshift(data);
                                    if (vml.stodolist.length > 0) {
                                        vml.stodolist[0].children.unshift(data);
                                    }
                                    var index = vml.groupindex;
                                    var group_obj = vml.grouplist[index];
                                }
                                vml.add_group_count(local_group_id);

                            })
                        } else {  // does not has timestamp
                            $.ajax({
                                type: 'POST',
                                url: API_HOST + 'todo/',
                                data: {
                                    title: title,
                                    group: local_group_id,
                                    is_star: is_star
                                }
                            }).done(function (resp) {
                                if (vml.groupid) {
                                    var data = resp.data;
                                    // vml.todolist.push(data);
                                    vml.todolist.unshift(data);
                                    if (vml.stodolist.length > 0) {
                                        vml.stodolist[0].children.unshift(data);
                                    }
                                    var index = vml.groupindex;
                                    var group_obj = vml.grouplist[index];
                                }
                                vml.add_group_count(local_group_id);
                            })
                        }
                    }

                },
                specialstarclick: function (db, da, id) {
                    var g_index;
                    var g_element;
                    var g_is_star;
                    $.each(vml.stodolist, function (index, element) {
                        $.each(element.children, function (s_index, s_element) {
                            if (s_element.id == id) {
                                g_index = s_index;
                                g_element = element;
                                g_is_star = s_element.is_star;
                            }
                        })
                    });
                    console.log(g_is_star);
                    $.ajax({
                        type: 'PATCH',
                        url: API_HOST + 'todo/detail/' + id,
                        data: {
                            is_star: !g_is_star
                        }
                    }).done(function (resp) {
                        if (resp.code == 0) {
                            g_element.children.splice(g_index, 1);
                        }
                    });
                },
                todostarclick: function (db, da) {
                    var todo_obj = vml.todolist[db];
                    var key = todo_obj.id;
                    if (todo_obj.is_star) {
                        vml.todolist[db].is_star = false;
                    } else {
                        vml.todolist[db].is_star = true;
                    }
                    var is_star = vml.todolist[db].is_star;
                    $.ajax({
                        type: 'PATCH',
                        url: API_HOST + 'todo/detail/' + key,
                        data: {
                            is_star: is_star
                        }
                    }).done(function (resp) {
                        if (resp.code == 0) {

                        }
                    });
                },
                donestarclick: function (db, da) {
                    var done_obj = vml.donelist[db];
                    var key = done_obj.id;
                    if (done_obj.is_star) {
                        vml.donelist[db].is_star = false;
                    } else {
                        vml.donelist[db].is_star = true;
                    }
                    var is_star = vml.donelist[db].is_star;
                    $.ajax({
                        type: 'PATCH',
                        url: API_HOST + 'todo/detail/' + key,
                        data: {
                            is_star: is_star
                        }
                    }).done(function (resp) {
                        if (resp.code == 0) {

                        }
                    })

                },
                todocheckclick: function (db, dd) {
                    if (vml.backup_group_id == -1 || vml.backup_group_id == -2) {
                        var g_index;
                        var g_id;
                        $.each(vml.stodolist, function (index, element) {
                            $.each(element.children, function (s_index, s_element) {
                                var l_group = element.group;
                                if (s_element.id == dd) {
                                    g_index = s_index;
                                    $.each(vml.grouplist, function (index, element) {
                                        if (element.id == l_group.id) {
                                            element.todo_cnt -= 1;
                                            if (vml.backup_group_id == -2) {
                                                vml.today_all_count -= 1;
                                            } else {
                                                vml.star_all_count -= 1;
                                            }
                                        }
                                    });
                                    $.ajax({
                                        type: 'PATCH',
                                        url: API_HOST + 'todo/detail/' + dd,
                                        data: {
                                            status: 2
                                        }
                                    }).done(function (resp) {
                                        if (resp.code == 0) {
                                            vml.detail.is_done = true;
                                            vml.detail.status = 2;
                                            var g_obj = vml.grouplist[vml.groupindex];
                                            vml.stodolist[index].children.splice(s_index, 1);
                                            if (vml.stodolist[index].children.length < 1) {
                                                $("#group_" + element.group.id).addClass('hide');
                                            }
                                        }
                                    });
                                }
                            })
                        })
                    } else {
                        var todo_obj = vml.todolist[db];
                        todo_obj.is_done = true;
                        var key = todo_obj.id;
                        vml.donelist.push(todo_obj);
                        vml.todolist.splice(db, 1);
                        $.ajax({
                            type: 'PATCH',
                            url: API_HOST + 'todo/detail/' + key,
                            data: {
                                status: 2
                            }
                        }).done(function (resp) {
                            if (resp.code == 0) {
                                vml.detail.is_done = true;
                                vml.detail.status = 2;
                                var g_obj = vml.grouplist[vml.groupindex];
                                console.log(vml.groupid);
                                $.each(vml.grouplist, function (index, element) {
                                    if (element.id == vml.groupid) {
                                        element.todo_cnt -= 1;
                                    }
                                })
                            }
                        });
                    }
                },
                donecheckclick: function (db) {
                    var done_obj = vml.donelist[db];
                    var key = done_obj.id;
                    done_obj.is_done = false;
                    vml.todolist.push(done_obj);
                    vml.donelist.splice(db, 1);
                    $.ajax({
                        type: 'PATCH',
                        url: API_HOST + 'todo/detail/' + key,
                        data: {
                            status: 1
                        }
                    }).done(function (resp) {
                        if (resp.code == 0) {
                            vml.detail.is_done = false;
                            vml.detail.status = 1;
                            var g_obj = vml.grouplist[vml.groupindex];
                            $.each(vml.grouplist, function (index, element) {
                                if (element.id == vml.groupid) {
                                    element.todo_cnt += 1;
                                }
                            })
                        }
                    })
                },
                detailcheckclick: function () {
                    var key = vml.detail.id;
                    var index = vml.detail.index;
                    if (vml.detail.is_done) {
                        var status = 1;
                        vml.detail.is_done = false;
                        var item_obj = '';
                        var item_index = '';
                        $.each(vml.donelist, function (index, element) {
                            if (element.id == key) {
                                item_obj = element;
                                item_index = index;
                            }
                        });
                        vml.todolist.push(item_obj);
                        vml.donelist.splice(item_index, 1);
                    } else {
                        var status = 2;
                        vml.detail.is_done = true;
                        var item_obj = '';
                        var item_index = '';
                        $.each(vml.todolist, function (index, element) {
                            if (element.id == key) {
                                item_obj = element;
                                item_index = index;
                            }
                        });
                        vml.donelist.push(item_obj);
                        vml.todolist.splice(item_index, 1);
                    }
                    $.ajax({
                        type: 'PATCH',
                        url: API_HOST + 'todo/detail/' + key,
                        data: {
                            status: status
                        }
                    }).done(function (resp) {
                        if (resp.code == 0) {
                            var data = resp.data;
                            if (data.status == 2) {

                            } else {

                            }
                        }
                    })
                },
                donecollapsedclick: function () {
                    if (vml.item.showdoneitem) {
                        vml.item.showdoneitem = false;
                    } else {
                        vml.item.showdoneitem = true;
                    }
                },
                doneitemclick: function (db) {
                    var item_obj = vml.donelist[db];
                    var key = item_obj.id;
                    //    detail init
                    $.each(vml.donelist, function (index, element) {
                        $("#done_item_" + element.id).removeClass('todo_bk');
                        $("#done_item_" + element.id).addClass('done_item');
                    });
                    $.each(vml.todolist, function (index, element) {
                        $("#todo_item_" + element.id).removeClass('todo_bk');
                    });
                    $("#done_item_" + key).removeClass('done_item');
                    $("#done_item_" + key).addClass('todo_bk');
                    if (has_click) {
                        var review_list;
                        $.getJSON(API_HOST + 'todo/detail/' + key, function (resp) {
                            var data = resp.data;
                            review_list = resp.data.review_list;
                            vml.detail.title = item_obj.title;
                            vml.detail.deadline = item_obj.deadline;
                            vml.detail.notes = item_obj.notes;
                            vml.detail.id = item_obj.id;
                            vml.detail.status = item_obj.status;
                            vml.detail.groupid = item_obj.groupid;
                            vml.detail.user = item_obj.user;
                            vml.detail.comment_list = review_list;
                            vml.detail.children = data.children;
                            vml.detail.gmt_create = item_obj.gmt_create;
                            vml.detail.index = db;
                            vml.detail.gmt_update = item_obj.gmt_update;
                            var d = new TodoItem();
                            d.timestamp = item_obj.deadline * 1000;
                            vml.detail.deadline_string = d.tododetail_deadline_timestring();
                            if (item_obj.remindme) {
                                d.timestamp = item_obj.remindme * 1000;
                                vml.detail.remindme = item_obj.remindme * 1000;
                                vml.detail.remindme_string = d.tododetail_timestring();
                            }
                        });
                    }
                    for (var i = 0; i < 2; i++) {
                        setTimeout(function () {
                            $('#title_textarea').trigger('click');
                        }, 100);
                    }
                    if (item_obj.status == 2) {
                        vml.detail.is_done = true;
                    } else {
                        vml.detail.is_done = false;
                    }
                },
                specialitemclick: function (da) {
                    var todo = da.todo;
                    var key = todo.id;
                    var item_obj = todo;
                    vml.todo_global_id = key;
                    $.each(vml.stodolist, function (index, element) {
                        $.each(element.children, function (index, n_element) {
                            $("#todo_item_" + n_element.id).removeClass('todo_bk');
                            $("#special_todo_item_" + n_element.id).removeClass('todo_bk');
                        });
                    });
                    $("#special_todo_item_" + key).addClass('todo_bk');
                    if (has_click) {
                        var review_list;
                        $.getJSON(API_HOST + 'todo/detail/' + key, function (resp) {
                            var data = resp.data;
                            review_list = resp.data.review_list;
                            vml.detail.title = item_obj.title;
                            vml.detail.deadline = item_obj.deadline_timestamp;
                            if (item_obj.notes) {
                                vml.detail.notes = item_obj.notes;
                            } else {
                                vml.detail.notes = '';
                            }
                            vml.detail.id = item_obj.id;
                            vml.detail.children = data.children;
                            vml.detail.status = item_obj.status;
                            vml.detail.user = item_obj.user;
                            vml.detail.groupid = item_obj.group;
                            vml.detail.comment_list = review_list;
                            vml.detail.gmt_create = item_obj.gmt_create;
                            // vml.detail.index = db;
                            vml.detail.gmt_update = item_obj.gmt_update;
                            var d = new TodoItem();
                            d.timestamp = item_obj.deadline * 1000;
                            vml.detail.deadline_string = d.tododetail_deadline_timestring();
                            d.timestamp = item_obj.remindme * 1000;
                            if (item_obj.remindme) {
                                vml.detail.remindme = item_obj.remindme * 1000;
                                vml.detail.remindme_string = d.tododetail_timestring();
                            } else {
                                vml.detail.remindme = '';
                                vml.detail.remindme_string = '';
                            }
                        });
                    }
                    for (var i = 0; i < 2; i++) {
                        setTimeout(function () {
                            $('#title_textarea').trigger('click');
                        }, 100);
                    }
                    if (item_obj.status == 2) {
                        vml.detail.is_done = true;
                    } else {
                        vml.detail.is_done = false;
                    }
                },
                itemclick: function (db) {
                    var item_obj = vml.todolist[db];
                    var key = item_obj.id;
                    vml.todo_global_id = key;
                    vml.todo_global_obj = item_obj;
                    //    detail init
                    $.each(vml.todolist, function (index, element) {
                        $("#todo_item_" + element.id).removeClass('todo_bk');
                    });
                    $.each(vml.donelist, function (index, element) {
                        $("#done_item_" + element.id).removeClass('todo_bk');
                        $("#done_item_" + element.id).addClass('done_item')
                    });
                    $("#todo_item_" + key).addClass('todo_bk');
                    var review_list = [];
                    if (has_click) {
                        $.getJSON(API_HOST + 'todo/detail/' + key, function (resp) {
                            var data = resp.data;
                            review_list = resp.data.review_list;
                            vml.detail.title = item_obj.title;
                            if (item_obj.notes) {
                                vml.detail.notes = data.notes;
                            } else {
                                vml.detail.notes = '';
                            }
                            vml.detail.id = data.id;
                            vml.detail.status = data.status;
                            vml.detail.children = data.children;
                            vml.detail.user = data.user;
                            vml.detail.comment_list = review_list;
                            vml.detail.gmt_create = item_obj.gmt_create;
                            vml.detail.index = db;
                            vml.detail.gmt_update = item_obj.gmt_update;
                            vml.detail.deadline = item_obj.deadline;
                            vml.detail.groupid = data.group;
                            var d = new TodoItem();
                            d.timestamp = item_obj.deadline * 1000;
                            vml.detail.deadline_string = d.tododetail_timestring();
                            if (item_obj.remindme) {
                                d.timestamp = item_obj.remindme * 1000;
                                vml.detail.remindme = item_obj.remindme * 1000;
                                vml.detail.remindme_string = d.tododetail_timestring();
                            } else {
                                vml.detail.remindme = '';
                                vml.detail.remindme_string = '';
                            }
                        });

                    }
                    if (item_obj.status == 2) {
                        vml.detail.is_done = true;
                    } else {
                        vml.detail.is_done = false;
                    }
                    for (var i = 0; i < 2; i++) {
                        setTimeout(function () {
                            $('#title_textarea').trigger('click');
                        }, 100);
                    }
                },
                itemrightclick: function (e, da, db) {
                    // Todo: use async menu create.
                    var todo = da.todo;
                    vml.todo_global_obj = todo;
                    vml.todo_global_index = db;
                    // console.log(todo);
                    console.log(todo.title + ';;;' + todo.id);
                    vml.tend_delete_todo_obj = todo;
                    vml.todo_global_id = todo.id;
                    var d = new Date();
                    var day = d.getDate();
                    vml.icon.today = day.toString();
                    vml.icon.tomorrow = (day + 1).toString();
                    $.contextMenu('destroy');
                    vml.generate_sub_menu();
                    e.preventDefault();
                },
                doneitemrightclick: function (e, da, db) {
                    var todo = da.done;
                    vml.todo_global_obj = todo;
                    vml.todo_global_index = db;
                    vml.todo_global_id = todo.id;
                    var d = new Date();
                    var day = d.getDate();
                    vml.icon.today = day.toString();
                    vml.icon.tomorrow = (day + 1).toString();
                    $.contextMenu('destroy');
                    vml.show_move_sub_menu = false;
                    vml.generate_sub_menu();
                    e.preventDefault();
                },
                specialitemdbclick: function (db, da) {
                    if (vml.detail.notes) {

                    } else {
                        $("#todo-textarea").val('');
                    }
                    var todo = da.todo;
                    var key = todo.id;
                    vml.todo_global_id = key;
                    var item_obj = todo;
                    $.each(vml.todolist, function (index, element) {
                        $("#special_todo_item_" + element.id).removeClass('todo_bk');
                        $("#todo_item_" + element.id).removeClass('todo_bk');
                    });
                    $("#special_todo_item_" + key).addClass('todo_bk');
                    //detail init
                    var review_list = [];
                    $.getJSON(API_HOST + 'todo/detail/' + key, function (resp) {
                        var data = resp.data;
                        review_list = data.review_list;
                        vml.detail.title = item_obj.title;
                        vml.detail.deadline = item_obj.deadline;
                        if (item_obj.notes) {
                            vml.detail.notes = item_obj.notes;
                        }
                        vml.detail.id = item_obj.id;
                        vml.detail.status = item_obj.status;
                        vml.detail.user = item_obj.user;
                        vml.detail.comment_list = review_list;
                        vml.detail.gmt_create = item_obj.gmt_create;
                        vml.detail.gmt_update = item_obj.gmt_update;
                        vml.detail.gmt_complete = item_obj.gmt_complete;
                        vml.detail.remindme = item_obj.remindme;
                        vml.detail.index = db;
                        vml.detail.groupid = item_obj.group;
                        if (item_obj.status == 2) {
                            vml.detail.is_done = true;
                        }
                        if (has_click) {
                            has_click = false;
                            $('#right_pane').addClass('hide');
                        } else {
                            $('#right_pane').removeClass('hide');
                            has_click = true;
                        }
                        setTimeout(function () {
                            $('#title_textarea').trigger('click');
                        }, 30);
                        vml.detail.is_done = item_obj.is_done;
                        var d = new TodoItem();
                        if (item_obj.deadline) {
                            d.timestamp = item_obj.deadline * 1000;
                        }
                        vml.detail.deadline_string = d.tododetail_deadline_timestring();
                        if (item_obj.remindme) {
                            d.timestamp = item_obj.remindme * 1000;
                            vml.detail.remindme_string = d.tododetail_timestring();
                        }
                        if (item_obj.status == 2) {
                            vml.detail.is_done = true;
                        }
                    })
                },
                itemdbclick: function (db, da) {
                    if (vml.detail.notes) {

                    } else {
                        $("#todo-textarea").val('');
                    }
                    if (da.todo) {
                        var item_obj = vml.todolist[db];
                        vml.todo_global_obj = item_obj;
                    } else {
                        var item_obj = vml.donelist[db];
                    }
                    var key = item_obj.id;
                    var key = item_obj.id;
                    vml.todo_global_id = key;
                    vml.todo_global_index = db;
                    //  active item style.
                    $.each(vml.todolist, function (index, element) {
                        $("#todo_item_" + element.id).removeClass('todo_bk');
                    });
                    $("#todo_item_" + key).addClass('todo_bk');

                    if (item_obj.status == 2) {
                        $("#detail_icon").attr('src', '/static/image/todo/donebox.png');
                    }
                    /*
                     detail init.
                     */
                    var review_list = [];
                    $.getJSON(API_HOST + 'todo/detail/' + key, function (resp) {
                        if (resp.code == 0) {
                            var data = resp.data;
                            review_list = data.review_list;
                            vml.detail.title = item_obj.title;
                            vml.detail.deadline = item_obj.deadline;
                            if (item_obj.notes) {
                                vml.detail.notes = item_obj.notes;
                            }
                            vml.detail.id = item_obj.id;
                            vml.detail.status = item_obj.status;
                            vml.detail.children = data.children;
                            vml.detail.user = item_obj.user;
                            vml.detail.comment_list = review_list;
                            vml.detail.gmt_create = item_obj.gmt_create;
                            vml.detail.gmt_update = item_obj.gmt_update;
                            vml.detail.remindme = item_obj.remindme;
                            vml.detail.index = db;
                            var d = new TodoItem();
                            if (item_obj.deadline) {
                                d.timestamp = item_obj.deadline * 1000;
                                vml.detail.deadline_string = d.tododetail_deadline_timestring();
                            }
                            if (item_obj.remindme) {
                                d.timestamp = item_obj.remindme * 1000;
                                vml.detail.remindme_string = d.tododetail_timestring();
                            }
                            if (item_obj.status == 2) {
                                vml.detail.is_done = true;
                            }
                            if (has_click) {
                                has_click = false;
                                $('#right_pane').addClass('hide');
                            } else {
                                $('#right_pane').removeClass('hide');
                                has_click = true;
                            }
                            setTimeout(function () {
                                $('#title_textarea').trigger('click');
                            }, 30);
                            vml.detail.is_done = item_obj.is_done;
                        }
                    });
                },
                childclick: function (db) {
                    var child_item = vml.detail.children[db];
                    if (child_item.is_done) {
                        var status = 1;
                    } else {
                        var status = 2;
                    }
                    var key = vml.detail.children[db].id;
                    $.ajax({
                        type: 'PATCH',
                        url: API_HOST + 'todo/detail/' + key,
                        data: {
                            status: status
                        }
                    }).done(function (resp) {
                        if (resp.code == 0) {
                            var data = resp.data;
                            if (data.status == 2) {
                                child_item.is_done = true;
                            } else {
                                child_item.is_done = false;
                            }
                        }
                    })

                },
                clearchild: function () {
                    $("#add_child").html("");
                },
                addchild: function () {
                    var parent_id = vml.detail.id;
                    var title = $.trim($('#child_title').val());
                    var deadline = '';
                    if (vml.current_child_timestamp) {
                        deadline = vml.current_child_timestamp;
                        var data = {
                            title: title,
                            parent: parent_id,
                            deadline: deadline / 1000
                        }
                    } else {
                        var data = {
                            title: title,
                            parent: parent_id,
                        }
                    }
                    if (title) {

                    } else {
                        toastr.warning("标题不能为空.");
                        return;
                    }
                    $('#child_title').val("");
                    $.ajax({
                        type: 'POST',
                        url: API_HOST + 'todo/',
                        data: data
                    }).done(function (resp) {
                        vml.detail.children.push(resp.data);
                    })
                },
                addcomment: function () {
                    if (vml.post_comment_to_child) {
                        var content = $.trim($("#add_comment").val());
                        if (content) {

                        } else {
                            toastr.warning("评论不能为空.");
                            return;
                        }
                        $("#add_comment").val('');
                        var d = new Date();
                        $.ajax({
                            type: 'POST',
                            url: API_HOST + 'todo/review',
                            data: {
                                content: content,
                                todo: vml.detail.id,
                                target: vml.detail.user,
                                gmt_create: d.getTime() / 1000,
                                parent: vml.parent_comment_id
                            }
                        }).done(function (resp) {
                            // vml.detail.comment_list.push(resp.data);
                            vml.detail.comment_list[vml.parent_comment_index].children.push(resp.data);
                            vml.post_comment_to_child = false;
                            $('#add_comment').attr('placeholder', '添加评论');
                        })
                    } else {
                        var content = $.trim($("#add_comment").val());
                        if (content) {

                        } else {
                            toastr.warning("评论不能为空.");
                            return;
                        }
                        $("#add_comment").val('');
                        var d = new Date();
                        $.ajax({
                            type: 'POST',
                            url: API_HOST + 'todo/review',
                            data: {
                                content: content,
                                todo: vml.detail.id,
                                target: vml.detail.user,
                                gmt_create: d.getTime() / 1000
                            }
                        }).done(function (resp) {
                            var new_d = resp.data;
                            new_d['children'] = [];
                            vml.detail.comment_list.push(new_d);
                        })
                    }
                },
                blur: function () {
                    var deadline = vml.detail.deadline;
                    var key = vml.detail.id;
                    $.ajax({
                        type: 'PATCH',
                        url: API_HOST + 'todo/detail/' + key,
                        data: {
                            deadline: deadline
                        }
                    }).done(function (resp) {
                        if (resp.code == 0) {

                        }
                    })
                },
                left_to_right: function () {
                    $('#right_pane').addClass('hide');
                    has_click = false;
                },
                childblur: function (db, event) {
                    var child = vml.detail.children[db];
                    var title = $("#child_" + child.id).html();
                    $("#child_" + child.id).html(title);
                    var key = child.id;
                    $.ajax({
                        type: 'PATCH',
                        url: API_HOST + 'todo/detail/' + key,
                        data: {
                            title: title
                        }
                    }).done(function (resp) {
                        if (resp.code == 0) {

                        }
                    })
                },
                titleblur: function (da) {
                    var index = vml.detail.index;
                    var title = $("#title_textarea").val();
                    if (vml.backup_group_id != -2 && vml.backup_group_id != -1) { // common group
                        if (vml.detail.status == 1) {
                            //todo
                            var item_obj = vml.todolist[index];
                            var key = item_obj.id;

                            item_obj.title = title;
                            // vml.todolist.$set(index, {'title': title});
                        } else {
                            //done
                            var item_obj = vml.donelist[index];
                            var key = item_obj.id;
                            item_obj.title = title;
                            // vml.donelist.$set(index, {title: title});
                        }

                        $.ajax({
                            type: 'PATCH',
                            url: API_HOST + 'todo/detail/' + key,
                            data: {
                                title: title
                            }
                        }).done(function (resp) {
                            if (resp.code == 0) {
                                // vml.todolist[index] = a;
                            }
                        });
                    } else { // special group
                        $.ajax({
                            type: 'PATCH',
                            url: API_HOST + 'todo/detail/' + vml.todo_global_id,
                            data: {
                                title: title
                            }
                        }).done(function (resp) {
                            if (resp.code == 0) {
                                $.each(vml.stodolist, function (index, element) {
                                    $.each(element.children, function (s_index, s_element) {
                                        if (s_element.id == vml.todo_global_id) {
                                            s_element.title = title;
                                        }
                                    })
                                })
                            }
                        })
                    }

                },
                detailcheckboxclick: function (db, da) {
                    var child_obj = vml.detail.children[db];
                    var key = child_obj.id;
                    if (child_obj.status == 1) {
                        child_obj.status = 2;
                        $("#img_" + child_obj.id).attr('src', '/static/image/todo/donebox.png')
                        $.ajax({
                            type: 'PATCH',
                            url: API_HOST + 'todo/detail/' + key,
                            data: {
                                status: 2
                            }
                        }).done(function (resp) {
                            if (resp.code == 0) {

                            }
                        })
                    } else {
                        child_obj.status = 1;
                        $("#img_" + child_obj.id).attr('src', '/static/image/todo/checkboxe.png')
                        $.ajax({
                            type: 'PATCH',
                            url: API_HOST + 'todo/detail/' + key,
                            data: {
                                status: 1
                            }
                        }).done(function (resp) {
                            if (resp.code == 0) {

                            }
                        })
                    }
                },
                child_not_done: function (db) {
                    var child_obj = vml.detail.children[db];
                    if (child_obj.status == 1) {
                        return true;
                    } else {
                        return false;
                    }
                },
                clearnotes: function () {
                    $("#write_notes").html("");
                },
                submitnotes: function () {
                    var notes = $('#todo-textarea').val().trim('');
                    vml.detail.notes = notes;
                    if (vml.backup_group_id != -1 && vml.backup_group_id != -2) {
                        var key = vml.detail.id;
                        $("#todo-textarea").val(notes);
                        $.ajax({
                            type: 'PATCH',
                            url: API_HOST + 'todo/detail/' + key,
                            data: {
                                notes: notes
                            }
                        }).done(function (resp) {
                            if (resp.code == 0) {
                                if (vml.is_done) {
                                    vml.donelist[vml.detail.index].notes = resp.data.notes;
                                } else {
                                    vml.todolist[vml.detail.index].notes = resp.data.notes;
                                }
                            }
                        })
                    } else {
                        $.ajax({
                            type: 'PATCH',
                            url: API_HOST + 'todo/detail/' + vml.todo_global_id,
                            data: {
                                notes: notes
                            }
                        }).done(function (resp) {
                            if (resp.code == 0) {
                                $.each(vml.stodolist, function (index, element) {
                                    $.each(element.children, function (s_index, s_element) {
                                        if (s_element.id == vml.todo_global_id) {
                                            s_element.notes = notes;
                                        }
                                    })
                                })
                            }
                        })
                    }

                },
                edit_group: function () {
                    if (vml.group_edit) {
                        vml.group_edit = false;
                        vml.group_edit_not = true;
                    } else {
                        vml.group_edit = true;
                        vml.group_edit_not = false;
                    }
                },
                delete_group: function (db) {
                    var group_obj = vml.grouplist[db];
                    var key = group_obj.id;
                    $.ajax({
                        type: 'DELETE',
                        url: API_HOST + 'todo/group/' + key,
                        data: {}
                    }).done(function (resp) {
                        if (resp.code == 0) {
                            setTimeout(function () {
                                vml.grouplist.splice(db, 1);
                            }, 1000);
                        } else {
                        }
                    })
                },
                deletedetail: function () {
                    vml.modal.title = '删除条目';
                    vml.modal.eventname = 'delete_item';
                    vml.modal.modal_input = false;
                    vml.modal.modal_p = true;
                    vml.modal.value = "是否要删除条目?";
                    vml.calculate_modal();
                    vml.show_input_modal();
                },
                deletetodo: function () {
                    if (vml.backup_group_id != -1 && vml.backup_group_id != -2) {
                        var item_obj = vml.detail;
                        var key = item_obj.id;
                        $.ajax({
                            type: 'DELETE',
                            url: API_HOST + 'todo/detail/' + key,
                            data: {}
                        }).done(function (resp) {
                            if (resp.code == 0) {
                                var db = vml.detail.index;
                                var item_obj = vml.detail;
                                if (item_obj.is_done) {
                                    vml.donelist.splice(db, 1);
                                } else {
                                    vml.todolist.splice(db, 1);
                                }
                                $('#right_pane').addClass('hide');
                                has_click = false;
                                var g_obj = vml.grouplist[vml.groupindex];
                            }
                        });
                    } else {
                        var group_id = vml.detail.groupid;
                        $.each(vml.stodolist, function (index, element) {
                            if (element.group.id == group_id) {
                                var item_obj = element.children[vml.detail.index];
                                var key = item_obj.id;
                                element.children.splice(vml.detail.index, 1);
                                $.ajax({
                                    type: 'DELETE',
                                    url: API_HOST + 'todo/detail/' + key,
                                    data: {}
                                }).done(function (resp) {
                                    if (resp.code == 0) {
                                        $('#right_pane').addClass('hide');
                                        has_click = false;
                                    }
                                });
                            }
                        })
                    }
                },
                search_button_click: function () {
                    $("#search_todo")[0].focus();
                },
                search_todo: function () {
                    $.each(vml.grouplist, function (index, element) {
                        $('#group_item_' + element.id).removeClass('group_bk');
                    });
                    show_pane('search');
                    var title = $.trim($("#search_todo").val());
                    $(".todo_header_name").html('搜索结果');
                    $.ajax({
                        type: 'POST',
                        url: API_HOST + 'todo/search/',
                        data: {
                            title: title
                        }
                    }).done(function (resp) {
                        if (resp.code == 0) {
                            var data = resp.data;
                            var todolist = [];
                            var donelist = [];
                            $.each(data, function (index, element) {
                                if (element.status == 1) {
                                    todolist.push(element);
                                } else if (element.status == 2) {
                                    donelist.push(element);
                                }
                            });
                            vml.todolist = todolist;
                            vml.donelist = donelist;
                        }
                    })
                },
                groupitemright_click: function (e, da, db) {
                    vml.group_delete_id = da.group.id;
                    var index = db + 1;
                    vml.groupindex = index;
                    var group = da.group;
                    var n_list = ['2', '3', '4', '6', 2, 3, 4, 6];
                    if ($.inArray(group.status, n_list) > 0) {
                        vml.init_con_menu_bak();
                    } else {
                        vml.init_con_menu();
                    }
                    e.preventDefault();
                },
                generate_sub_menu: function () {
                    var sub_menus = {};
                    $.each(vml.sub_grouplist, function (index, element) {
                        sub_menus[element.id] = {"name": element.name, "vid": element.id}
                    });
                    $.contextMenu({
                        selector: '.todo_item',
                        classNames: {
                            icon: 'context-menu-icon'
                        },
                        callback: function (key, options) {
                            console.log(key);
                            switch (key) {
                                case 'done':
                                    $.ajax({
                                        type: 'PATCH',
                                        url: API_HOST + 'todo/detail/' + vml.todo_global_id,
                                        data: {
                                            status: 2
                                        }
                                    }).done(function (resp) {
                                        if (resp.code == 0) {
                                            vml.donelist.push(vml.todolist[vml.todo_global_index]);
                                            vml.todolist.splice(vml.todo_global_index, 1);
                                        }
                                    });
                                    break;
                                case 'star':
                                    $.ajax({
                                        type: 'PATCH',
                                        url: API_HOST + 'todo/detail/' + vml.todo_global_id,
                                        data: {
                                            is_star: true
                                        }
                                    }).done(function (resp) {
                                        if (resp.code == 0) {
                                            if (vml.backup_group_id == 0) { //普通组
                                                if (vml.todo_global_obj.is_done) {
                                                    $.each(vml.donelist, function (index, element) {
                                                        if (element.id == vml.todo_global_id) {
                                                            element.is_star = true;
                                                        }
                                                    })
                                                } else {
                                                    $.each(vml.todolist, function (index, element) {
                                                        if (element.id == vml.todo_global_id) {
                                                            element.is_star = true;
                                                        }
                                                    })
                                                }
                                            } else if (vml.backup_group_id == -2) { // 特殊组
                                                if (vml.todo_global_obj.is_done) {
                                                    //never reach here.
                                                } else {
                                                    $.each(vml.stodolist, function (index, element) {
                                                        $.each(element.children, function (index, t_element) {
                                                            if (t_element.id == vml.todo_global_obj.id) {
                                                                t_element.is_star = true;
                                                            }
                                                        })
                                                    })
                                                }
                                            }
                                        }
                                    });
                                    break;
                                case 'today':
                                    var d = new TodoItem();
                                    var timestamp = d.get_today_timestamp();
                                    if (vml.backup_group_id == 0) { //普通组
                                        $.each(vml.todolist, function (index, element) {
                                            if (element.id == vml.todo_global_id) {
                                                element.deadline = timestamp / 1000;
                                            }
                                        })
                                    } else {  //特殊组
                                        $.each(vml.stodolist, function (index, element) {
                                            $.each(element.children, function (index, t_element) {
                                                if (t_element.id == vml.todo_global_obj.id) {
                                                    console.log(timestamp);
                                                    t_element.deadline = timestamp / 1000;
                                                }
                                            })
                                        })
                                    }
                                    $.ajax({
                                        type: 'PATCH',
                                        url: API_HOST + 'todo/detail/' + vml.todo_global_id,
                                        data: {
                                            deadline: timestamp / 1000
                                        }
                                    }).done(function (resp) {
                                        if (resp.code == 0) {

                                        }
                                    });
                                    break;
                                case 'tomorrow':
                                    var d = new TodoItem();
                                    var timestamp = d.get_tomorrow_timestamp();
                                    if (vml.backup_group_id == 0) { //普通组
                                        $.each(vml.todolist, function (index, element) {
                                            if (element.id == vml.todo_global_id) {
                                                element.deadline = timestamp / 1000;
                                            }
                                        })
                                    } else {  //特殊组
                                        $.each(vml.stodolist, function (index, element) {
                                            $.each(element.children, function (index, t_element) {
                                                if (t_element.id == vml.todo_global_obj.id) {
                                                    console.log(timestamp);
                                                    t_element.deadline = timestamp / 1000;
                                                }
                                            })
                                        })
                                    }
                                    $.ajax({
                                        type: 'PATCH',
                                        url: API_HOST + 'todo/detail/' + vml.todo_global_id,
                                        data: {
                                            deadline: timestamp / 1000
                                        }
                                    }).done(function (resp) {
                                        if (resp.code == 0) {

                                        }
                                    });
                                    break;
                                case 'remove':
                                    if (vml.backup_group_id == 0) { //普通组
                                        $.each(vml.todolist, function (index, element) {
                                            if (element.id == vml.todo_global_id) {
                                                element.deadline = timestamp / 1000;
                                            }
                                        })
                                    } else {  //特殊组
                                        $.each(vml.stodolist, function (index, element) {
                                            $.each(element.children, function (index, t_element) {
                                                if (t_element.id == vml.todo_global_obj.id) {
                                                    console.log(timestamp);
                                                    t_element.deadline = timestamp / 1000;
                                                }
                                            })
                                        })
                                    }
                                    $.ajax({
                                        type: 'PATCH',
                                        url: API_HOST + 'todo/detail/' + vml.todo_global_id,
                                        data: {
                                            deadline: 'st'
                                        }
                                    }).done(function (resp) {
                                        if (resp.code == 0) {

                                        }
                                    });
                                    break;
                                case 'delete':
                                    vml.modal.title = '删除条目';
                                    vml.modal.eventname = 'delete_item';
                                    vml.modal.modal_input = false;
                                    vml.modal.modal_p = true;
                                    vml.modal.value = "是否要删除条目?";
                                    vml.calculate_modal();
                                    vml.show_input_modal();
                                    break;
                                default:
                                    console.log(key);
                                    console.log(vml.groupid);
                                    vml.reduce_group_count(vml.groupid);
                                    vml.add_group_count(key);
                                    $.ajax({
                                        type: 'PATCH',
                                        url: API_HOST + 'todo/detail/' + vml.todo_global_obj.id,
                                        data: {
                                            group: key
                                        }
                                    }).done(function (resp) {
                                        if (vml.backup_group_id == 0) { //普通组
                                            if (vml.todo_global_obj.is_done) {
                                                var done_obj = '';
                                                var g_index = '';
                                                $.each(vml.donelist, function (index, element) {
                                                    if (element.id == vml.todo_global_obj.id) {
                                                        done_obj = element;
                                                        g_index = index;
                                                    }
                                                });
                                                vml.donelist.splice(g_index, 1);
                                            } else {
                                                var todo_obj = '';
                                                var g_index = '';
                                                $.each(vml.todolist, function (index, element) {
                                                    if (element.id == vml.todo_global_obj.id) {
                                                        todo_obj = element;
                                                        g_index = index;
                                                    }
                                                });
                                                vml.todolist.splice(g_index, 1);
                                            }
                                        } else if (vml.backup_group_id == -1 || vml.backup_group_id == -2) {
                                            if (vml.todo_global_obj.is_done) {
                                                var done_obj = '';
                                                var g_index = '';
                                                $.each(vml.stodolist, function (index, element) {
                                                    $.each(element.children, function (t_index, t_element) {
                                                        if (t_element.id == vml.todo_global_obj.id) {
                                                            done_obj = element;
                                                            g_index = t_index;
                                                        }
                                                    })
                                                });
                                                done_obj.children.splice(g_index, 1);
                                            } else {
                                                var todo_obj = '';
                                                var g_index = '';
                                                $.each(vml.stodolist, function (index, element) {
                                                    $.each(element.children, function (t_index, t_element) {
                                                        if (t_element.id == vml.todo_global_obj.id) {
                                                            todo_obj = element;
                                                            g_index = t_index;
                                                        }
                                                    })
                                                });
                                                console.log(todo_obj);
                                                todo_obj.children.splice(g_index, 1);
                                            }
                                        }
                                    });
                            }
                        },
                        items: {
                            "done": {"name": "标记为已完成", "icon": "finished"},
                            "star": {"name": "标记为星标", "icon": "star"},
                            "sep1": "---------",
                            "today": {"name": "今天到期", "icon": vml.icon.today},
                            "tomorrow": {"name": "明天到期", "icon": vml.icon.tomorrow},
                            "remove": {"name": "移除到期日", "icon": "remove_date"},
                            // "create": {"name": "从任务创建一个新清单", "icon": "plus"},
                            "move": {
                                "name": "移动任务到...",
                                "icon": "move",
                                "items": sub_menus,
                                "visible": vml.show_move_sub_menu
                            },
                            "sep2": "---------",
                            // "copy": {"name": "复制任务", "icon": "copy"},
                            "delete": {"name": "删除任务", "icon": "delete"}
                        }
                    });
                },
                show_input_modal: function () {
                    $('.my_modal').css('display', 'block');
                    $('.pane').css('display', 'block');
                },
                hide_input_modal: function () {
                    $('.my_modal').css('display', 'none');
                    $('.pane').css('display', 'none');
                },
                init_con_menu_bak: function () {
                    //init jquery context Menu
                    $.contextMenu({
                        selector: '.context_menu',
                        trigger: 'right',
                        classNames: {
                            icon: 'context-menu-icon context-menu-icon--fa'
                        },
                        build: function ($trigger, e) {
                            return {
                                callback: function (key, options) {
                                    console.log(key);
                                    if (key == 'rename_bak') {
                                        vml.modal.title = '重命名分组';
                                        vml.modal.eventname = 'rename_group';
                                        vml.modal.modal_input = true;
                                        vml.modal.modal_p = false;
                                        vml.modal.placeholder = '请输入分组的新名称';
                                        vml.calculate_modal();
                                        vml.show_input_modal();
                                    }
                                },
                                items: {
                                    "rename_bak": {name: "重命名分组", icon: "fa fa-edit"},
                                    // "sep1": "---------",
                                    // "copy": {name: "复制分组", icon: "fa fa-copy"},
                                    // "delete": {name: "删除分组", icon: "fa fa-trash-o"}
                                }
                            }
                        },

                    });
                },
                init_con_menu: function () {
                    $.contextMenu({
                        selector: '.fucking_bak',
                        trigger: 'right',
                        classNames: {
                            icon: 'context-menu-icon context-menu-icon--fa'
                        },
                        callback: function (key, options) {
                            console.log(key);
                            if (key == 'delete') { // 删除清单
                                vml.modal.title = '删除分组';
                                vml.modal.eventname = 'delete_group';
                                vml.modal.modal_input = false;
                                vml.modal.modal_p = true;
                                var group = vml.grouplist[vml.groupindex - 1];
                                vml.modal.value = "是否要删除分组" + "'" + group.name + "'?";
                                vml.calculate_modal();
                                vml.show_input_modal();
                            } else if (key == 'rename') {
                                vml.modal.title = '重命名分组';
                                vml.modal.eventname = 'rename_group';
                                vml.modal.modal_input = true;
                                vml.modal.modal_p = false;
                                vml.modal.value = '';
                                vml.modal.placeholder = '请输入分组的新名称';
                                vml.calculate_modal();
                                vml.show_input_modal();
                            }
                        },
                        items: {
                            "rename": {name: "重命名分组", icon: "fa fa-edit"},
                            "sep1": "---------",
                            // "copy": {name: "复制分组", icon: "fa fa-copy"},
                            "delete": {name: "删除分组", icon: "fa fa-trash-o"}
                        }
                    });
                },
                modal_cancel: function () {
                    vml.hide_input_modal();
                    vml.modal.value = '';
                    vml.modal.placeholder = '';
                },
                modal_confirm: function () {
                    switch (vml.modal.eventname) {
                        case 'rename_group':
                            var group = vml.grouplist[vml.groupindex - 1];
                            var key = group.id;
                            if ($.trim(vml.modal.value)) {

                            } else {
                                toastr.warning("分组名称不能为空");
                                return;
                            }
                            $.ajax({
                                type: 'PUT',
                                url: API_HOST + 'todo/group/' + key,
                                data: {
                                    name: vml.modal.value
                                }
                            }).done(function (resp) {
                                if (resp.code == 0) {
                                    group.name = vml.modal.value;
                                    vml.hide_input_modal();
                                }
                            });
                            break;
                        case 'delete_group':
                            var idd = vml.group_delete_id;
                            $.ajax({
                                type: 'DELETE',
                                url: API_HOST + 'todo/group/' + idd,
                                data: {}
                            }).done(function (resp) {
                                if (resp.code == 0) {
                                    vml.grouplist.splice(vml.groupindex - 1, 1);
                                    vml.hide_input_modal();
                                }
                                $(".todo_header_name").html("收件箱");
                                var inbox_group_key = vml.inbox_group_id;
                                $.getJSON(API_HOST + 'todo/group/' + inbox_group_key, function (resp) {
                                    if (resp.code == 0) {
                                        vml.todolist = resp.data.todolist_set;
                                        vml.groupid = vml.inbox_group_id;
                                        vml.modal.value = '';
                                    }
                                })
                            });
                            break;
                        case 'delete_item':
                            var key = vml.todo_global_id;
                            if (vml.backup_group_id != -1 && vml.backup_group_id != -2) {
                                $.ajax({
                                    type: 'DELETE',
                                    url: API_HOST + 'todo/detail/' + key,
                                    data: {}
                                }).done(function (resp) {
                                    var g_index;
                                    var todo;
                                    if (resp.code == 0) {
                                        $.each(vml.todolist, function (index, element) {
                                            if (element.id == vml.todo_global_id) {
                                                todo = true;
                                                g_index = index;
                                            }
                                        });
                                        $.each(vml.donelist, function (index, element) {
                                            if (element.id == vml.todo_global_id) {
                                                todo = false;
                                                g_index = index;
                                            }
                                        });
                                        if (todo) {
                                            vml.todolist.splice(g_index, 1);
                                        } else {
                                            vml.donelist.splice(g_index, 1);
                                        }
                                        vml.hide_input_modal();
                                        vml.modal.value = '';
                                        vml.modal.placeholder = '';
                                    }
                                    if (vml.backup_group_id == -1) {
                                        vml.star_all_count -= 1;
                                        $.each(vml.grouplist, function (index, element) {
                                            if (element.id == vml.tend_delete_todo_obj.group) {
                                                element.todo_cnt -= 1;
                                            }
                                        })
                                    } else if (vml.backup_group_id == -2) { // today group
                                        vml.today_all_count -= 1;
                                        $.each(vml.grouplist, function (index, element) {
                                            if (element.id == vml.tend_delete_todo_obj.group) {
                                                element.todo_cnt -= 1;
                                            }
                                        })
                                    } else if (vml.backup_group_id == -3) {
                                        vml.send_delay_count -= 1;
                                        $.each(vml.grouplist, function (index, element) {
                                            if (element.id == vml.tend_delete_todo_obj.group) {
                                                element.todo_cnt -= 1;
                                            }
                                        })
                                    } else {
                                        $.each(vml.grouplist, function (index, element) {
                                            if (element.id == vml.tend_delete_todo_obj.group) {
                                                element.todo_cnt -= 1;
                                            }
                                        })
                                    }
                                });
                                $('#right_pane').addClass('hide');
                                has_click = false;
                            } else {
                                console.log('other delete.');
                                console.log(key);
                                var g_index;
                                var gg_index;
                                $.each(vml.stodolist, function (index, element) {
                                    $.each(element.children, function (c_index, c_element) {
                                        if (c_element.id == key) {
                                            g_index = index;
                                            gg_index = c_index;
                                        }
                                    })
                                });
                                vml.stodolist[g_index].children.splice(gg_index, 1);
                                $.ajax({
                                    type: 'DELETE',
                                    url: API_HOST + 'todo/detail/' + key,
                                    data: {}
                                }).done(function (resp) {
                                    if (resp.code == 0) {
                                        vml.todolist.splice(vml.todo_global_index, 1);
                                        vml.hide_input_modal();
                                        vml.modal.value = '';
                                        vml.modal.placeholder = '';
                                    }
                                });
                                $('#right_pane').addClass('hide');
                                has_click = false;
                                if (vml.backup_group_id == -1) {
                                    vml.star_all_count -= 1;
                                    $.each(vml.grouplist, function (index, element) {
                                        if (element.id == vml.tend_delete_todo_obj.group) {
                                            element.todo_cnt -= 1;
                                        }
                                    })
                                } else if (vml.backup_group_id == -2) { // today group
                                    vml.today_all_count -= 1;
                                    $.each(vml.grouplist, function (index, element) {
                                        if (element.id == vml.tend_delete_todo_obj.group) {
                                            element.todo_cnt -= 1;
                                        }
                                    })
                                } else if (vml.backup_group_id == -3) {
                                    vml.send_delay_count -= 1;
                                    $.each(vml.grouplist, function (index, element) {
                                        if (element.id == vml.tend_delete_todo_obj.group) {
                                            element.todo_cnt -= 1;
                                        }
                                    })
                                } else {
                                    $.each(vml.grouplist, function (index, element) {
                                        if (element.id == vml.tend_delete_todo_obj.group) {
                                            element.todo_cnt -= 1;
                                        }
                                    })
                                }
                            }
                            break;
                        case 'addgroup':
                            var new_group_name = $.trim(vml.modal.value);
                            if (new_group_name) {
                                // nothing
                            } else {
                                toastr.warning("分组名称不能为空.");
                                return;
                            }
                            $.ajax({
                                type: 'POST',
                                url: API_HOST + 'todo/group',
                                data: {
                                    name: new_group_name
                                }
                            }).done(function (resp) {
                                if (resp.code == 0) {
                                    vml.grouplist.push(resp.data);
                                    vml.sub_grouplist.push(resp.data);
                                }
                                vml.hide_input_modal();
                            });
                            vml.modal.value = '';
                            break;
                    }
                },
                todo_sort: function (key) {
                    var t_dolist = vml.todolist.concat([]);
                    switch (key) {
                        case 'deadline':
                            bubble_sort(t_dolist, 'deadline');
                            vml.todolist = t_dolist;
                            $("#sort_title").html("按到期日排序");
                            break;
                        case 'gmt_create':
                            bubble_sort(t_dolist, 'gmt_create');
                            vml.todolist = t_dolist;
                            $("#sort_title").html("按创建日期排序");
                            break;
                        case 'remindme':
                            bubble_sort(t_dolist, 'remindme');
                            vml.todolist = t_dolist;
                            $("#sort_title").html("按提醒日期排序");
                            break;
                        default:
                            console.log('never reach here.');
                    }
                },
                addheartbeat: function (db) {
                    var id_string = "heart_" + vml.detail.comment_list[db].id;
                    $("#" + id_string).addClass('beat_class');
                    setTimeout(function () {
                        $("#" + id_string).removeClass('beat_class');
                    }, 500);
                    if (vml.detail.comment_list[db].praise_cnt > 0) {

                    } else {
                        vml.detail.comment_list[db].praise_cnt += 1;
                    }
                },
                heartbeat: function (db) {
                    var id_string = "heart_" + vml.detail.comment_list[db].id;
                    console.log(id_string);
                    $("#" + id_string).addClass('beat_class');
                    if (vml.detail.comment_list[db].praise_cnt > 0) {

                    } else {
                        vml.detail.comment_list[db].praise_cnt += 1;
                    }
                    setTimeout(function () {
                        $("#" + id_string).removeClass('beat_class');
                    }, 500);
                    $.ajax({
                        type: 'POST',
                        url: API_HOST + 'todo/review/praise',
                        data: {
                            review: vml.detail.comment_list[db].id
                        }
                    }).done(function (resp) {
                        console.log(resp);
                    })
                },
                setcursor_position: function (db) {
                    if (vml.detail.notes) {

                    } else {
                        setCaretToPos($("#todo-textarea")[0], 0);
                    }
                },
                todo_change: function () {
                    var todo_input_val = $('#add_todo_input').val();
                    var obj = document.getElementById('add_todo_input');
                    vml.add_todo_input_keydown_val = todo_input_val;
                },
                todo_change_keyup: function () {
                    var todo_input_val = $('#add_todo_input').val();
                    vml.add_todo_input_keydown_val = todo_input_val;
                    var at_aplice = todo_input_val.split("@");
                    var search_item = at_aplice[at_aplice.length - 1];
                    if (search_item) {
                        // console.log('true');
                        // init_at_list('@', search_item);
                    } else {
                        // console.log('false');
                        // init_at_list('@', ' ');
                    }
                },
                add_todo_keydown: function (e) {
                    var keycode = e.keyCode;
                    if (keycode == 13) {

                    } else {
                        vml.can_add_todo = true;
                    }
                    var val = $("#add_todo_input").val();
                    vml.add_todo_old_val = val;
                    vml.add_todo_old_keycode = keycode;
                    // console.log("key code: " + e.keyCode + ", key value: " + val);
                },
                judge_if_contain_at_string: function (str) {

                },
                add_todo_keyup: function (e) {
                    var keycode = e.keyCode;
                    var val = $("#add_todo_input").val();
                    // console.log("key code: " + e.keyCode + ", key value: " + val);
                    if (keycode != 13) {
                        vml.choose_at_item_list = true;
                    }
                    if (val == vml.add_todo_old_val && keycode == vml.add_todo_old_keycode) {
                        // console.log('equal.');
                        if (keycode == 13) {
                            if ((/(@.*?(?= ))/g).test(val)) { // contain valid @ string
                                // console.log('enter send message...');
                                // var name_list = val.match(/@\w+\s/g);
                                // var name_list = val.match(/@[^\s]+/g);
                                var name_list = val.match(/(@.*?(?= ))/g);
                                var final_id_list = new Array();
                                var message = val;
                                console.log(global_at_name_list);
                                if (global_at_name_list.length < 1) {
                                    var post_group_id;
                                    var is_star = false;
                                    if (vml.backup_group_id == -1 || vml.backup_group_id == -2) {
                                        post_group_id = vml.default_group_id;
                                        if (vml.backup_group_id == -1) {
                                            is_star = false;
                                        }
                                    } else if (vml.backup_group_id == -3) {
                                        post_group_id = vml.default_group_id;
                                    } else if (vml.backup_group_id == 0) {
                                        post_group_id = vml.groupid;
                                    }
                                    if (vml.global_timestamp) {
                                        $.ajax({
                                            type: 'POST',
                                            url: API_HOST + 'todo/',
                                            data: {
                                                title: $("#add_todo_input").val(),
                                                group: post_group_id,
                                                is_star: is_star,
                                                deadline: vml.global_timestamp / 1000
                                            }
                                        }).done(function () {
                                            if (vml.backup_group_id == 0) {
                                                vml.todolist.unshift(resp.data);
                                            }
                                        })

                                    } else {
                                        $.ajax({
                                            type: 'POST',
                                            url: API_HOST + 'todo/',
                                            data: {
                                                title: $("#add_todo_input").val(),
                                                group: post_group_id,
                                                is_star: is_star
                                            }
                                        }).done(function (resp) {
                                            if (vml.backup_group_id == 0) {
                                                vml.todolist.unshift(resp.data);
                                            }
                                        })
                                    }
                                    return;
                                }
                                $.each(name_list, function (index, element) {
                                    if (global_at_name_list.indexOf($.trim(element).replace('@', '')) > -1) {
                                        $.each(new_ll, function (index, n_element) {
                                            var vvv = $.trim(element).replace('@', '');
                                            if (n_element.name == vvv) {
                                                if (final_id_list.indexOf(n_element.id) > -1) {

                                                } else {
                                                    final_id_list.push(n_element.id);
                                                }
                                            }
                                        })
                                    }
                                });
                                $.each(name_list, function (index, element) {
                                    var n_element = element.replace('@', '');
                                    message = message.replace(n_element, '');
                                });
                                message = $.trim(message.replace(/@/g, ''));
                                // console.log('message is:' + message);
                                if (message && vml.choose_at_item_list) { // check if real need send message.
                                    // console.log('should send message...');
                                    $.ajax({
                                        type: 'POST',
                                        url: API_HOST + 'todo/',
                                        data: {
                                            title: message,
                                            group: vml.outbox_group_id,
                                            relation: true
                                        }
                                    }).done(function (resp) {
                                        data = resp.data;
                                        var l_id = data.id;
                                        var d = {
                                            type: 'todo',
                                            channel: 1,
                                            content: message,
                                            extra: {id: l_id},
                                            user_ids: final_id_list
                                        };
                                        $.ajax({
                                            type: 'POST',
                                            url: API_HOST + 'push/',
                                            contentType: "application/json; charset=utf-8",
                                            data: JSON.stringify(d)
                                        }).done(function (resp) {
                                            if (resp.code == 0) {
                                                $("#add_todo_input").val('');
                                            }
                                        });
                                    });
                                }
                                //replace @ string
                            } else {   // do not contain valid @ string, post todo
                                vml.addtodo();
                            }
                        }
                    }
                },
                input_click: function (val) {
                    if (val == 'remindme') {
                        vml.g_datetimepicker = 'remindme';
                    } else if (val == 'deadline') {
                        vml.g_datetimepicker = 'deadline';
                    }
                },
                comment_to: function (db) {
                    vml.parent_comment_index = db;
                    vml.post_comment_to_child = true;
                    var l_comment_list = vml.detail.comment_list;
                    var comment_obj = l_comment_list[db];
                    vml.parent_comment_id = comment_obj.id;
                    $('#add_comment').attr('placeholder', '评论给:' + comment_obj.user.name);
                },
                add_group_count: function (g_id) {
                    if (vml.backup_group_id == -1 || vml.backup_group_id == -2) {
                        console.log('haha');
                        $.each(vml.grouplist, function (index, element) {
                            if (element.id == vml.default_group_id) {
                                element.todo_cnt += 1;
                            }
                        })
                    } else if (vml.backup_group_id == -3) {
                        console.log('enen');
                        $.each(vml.grouplist, function (index, element) {
                            if (element.id == vml.default_group_id) {
                                element.todo_cnt += 1;
                            }
                        })
                    } else {
                        console.log('nihao');
                        $.each(vml.grouplist, function (index, element) {
                            if (element.id == g_id) {
                                element.todo_cnt += 1;
                            }
                        })
                    }
                },
                reduce_group_count: function (g_id) {
                    if (vml.backup_group_id == -1 || vml.backup_group_id == -2) {

                    } else if (vml.backup_group_id == -3) {

                    } else {
                        $.each(vml.grouplist, function (index, element) {
                            if (element.id == g_id) {
                                element.todo_cnt -= 1;
                            }
                        })
                    }
                }
            }
        });
    }
};