/**
 * Created on 08 22, 2016
 * @author: tolerious
 */


/**
 * Todo管理
 * @constructor
 */

TodoList = function () {
    var show_all_done_tasks = true;
    var has_db_click = true;
    this.init_todo_list = function () {
        Vue.config.delimiters = ['${', '}'];
        /*
         * get group list
         */
        $.getJSON(API_HOST + 'todo/group', function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                vml.grouplist = data;
            }
        });
        todolist = [];
        donelist = [];
        /*
         * get todo list
         */
        $.getJSON(API_HOST + 'todo/', function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                $.each(data, function () {
                    if (this.status == 1 && String(this.parent) == 'null') {
                        todolist.push(this);
                    } else if (this.status == 2 && String(this.parent) == 'null') {
                        donelist.push(this);
                    }
                });
                vml.todolist = todolist;
                vml.donelist = donelist;
            }
        });
        var vml = new Vue({
                el: 'body',
                data: {
                    item: {
                        id: '',
                        user: '',
                        title: 'abc',
                        deadline: '',
                        remindme: '',
                        notes: '',
                        createtime: '',
                        todo: false,
                        done: false,
                        children: [],
                        commentlist: [],
                        is_star: false
                    },
                    todolist: todolist,
                    donelist: donelist,
                    grouplist: [],
                    children: [],
                    commentlist: []
                },
                methods: {
                    todostarclick: function (da, db) {
                        /*
                         not done item switch to done list.
                         */
                        var key = todolist[da].id;
                        var is_star = todolist[da].is_star;
                        if (is_star) {
                            vml.item.is_star = false;
                            is_star = false;
                            todolist[da].is_star = false;
                        } else {
                            vml.item.is_star = true;
                            is_star = true;
                            todolist[da].is_star = true;
                        }

                        /*
                         ajax request begin.
                         */
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
                    donestarclick: function (da, db) {
                        /*
                         done todo switch to not done list.
                         */
                        var key = donelist[da].id;
                        var is_star = donelist[da].is_star;
                        if (is_star) {
                            vml.item.is_star = false;
                            is_star = false;
                            donelist[da].is_star = false;
                        } else {
                            vml.item.is_star = true;
                            is_star = true;
                            donelist[da].is_star = true;
                        }
                        /*
                         ajax request begin
                         */
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

                    showpane: function (da) {
                        if (da.done) {
                            item_obj = da.done;
                            vml.item.done = true;
                            vml.item.todo = false;
                        } else if (da.todo) {
                            item_obj = da.todo;
                            vml.item.todo = true;
                            vml.item.done = false;
                        }
                        var key = item_obj.id;
                        $.getJSON(API_HOST + 'todo/detail/' + key, function (resp) {
                            if (resp.code == 0) {
                                var data = resp.data;
                                vml.item.title = data.title;
                                vml.item.notes = data.notes;
                                $.each(data.review_set, function (index, element) {
                                    var dic = {
                                        content: element
                                    };
                                    vml.item.commentlist.push(dic);
                                });
                            }
                        });
                        /*
                         * get child todo items.
                         *
                         */
                        $.getJSON(API_HOST + 'todo/child/' + key, function (resp) {
                            if (resp.code == 0) {
                                var data = resp.data;
                                vml.children = new Array();
                                $.each(data, function (index, element) {
                                    var dic = {
                                        title: element.title
                                    };
                                    vml.children.push(dic);
                                })
                            }
                        });

                        vml.item.title = item_obj.title;
                        vml.item.notes = item_obj.notes;
                        vml.item.id = item_obj.id;
                        vml.item.deadline = item_obj.deadline;
                        vml.item.user = item_obj.user;
                        vml.item.createtime = item_obj.gmt_create;
                        vml.item.is_star = item_obj.is_star;
                        //todo: item object need to be fill compelitly.

                        if (has_db_click) {
                            $("#item-detail").css('display', 'block');
                            $("#task-list").removeClass('col-md-9');
                            $('#task-list').addClass('col-md-5');
                            has_db_click = false;
                        } else {
                            $("#task-list").removeClass('col-md-5');
                            $('#task-list').addClass('col-md-9');
                            $("#item-detail").css('display', 'none');
                            has_db_click = true;
                        }
                    },
                    showdonetask: function (event) {
                        if (show_all_done_tasks) {
                            $("#all-done-tasks").fadeIn('slow');
                            show_all_done_tasks = false;
                        } else {
                            $("#all-done-tasks").fadeOut('slow');
                            show_all_done_tasks = true;
                        }
                    },
                    addtodo: function (event) {
                        var title = $("#add-task-input").val();
                        todolist.push({
                            title: title
                        });
                        $("#add-task-input").val("");
                        $.ajax({
                            type: 'POST',
                            url: API_HOST + 'todo/',
                            data: {
                                title: title
                            }
                        }).done(function (resp) {
                            console.log(resp.code);
                        })
                    },
                    checkboxclick: function (db, da) {
                        var localdone = false;
                        var localtodo = false;
                        /*
                         done item switch to not done item.
                         */
                        if (da.done) {
                            var key = donelist[db].id;
                            todolist.push(donelist[db]);
                            donelist.splice(db, 1);
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
                        } else if (da.todo) {
                            /*
                             not done item switch to done item.
                             */
                            var key = todolist[db].id;
                            donelist.push(todolist[db]);
                            todolist.splice(db, 1);
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
                        }


                    },
                    blur: function (event) {
                        var deadline = "";
                        var remindme = "";
                        var key = this.item.id;
                        if (this.item.deadline) {
                            deadline = this.item.deadline;
                        } else if (this.item.remindme) {
                            remindme = this.item.remindme;
                        }
                        var notes = $("#notes").html().trim();
                        $.ajax({
                            type: 'PATCH',
                            url: API_HOST + 'todo/detail/' + key,
                            data: {
                                deadline: deadline,
                                notes: notes
                            }
                        }).done(function (resp) {
                            if (resp.code == 0) {

                            }
                        })
                    },
                    addcomment: function (event) {
                        var content = $("#comment-id").val();
                        $("#comment-id").val("");
                        $.ajax({
                            type: 'POST',
                            url: API_HOST + 'todo/review',
                            data: {
                                content: content,
                                todo: vml.item.id,
                                target: vml.item.user
                            }
                        });
                        var dic = {
                            content: content
                        };
                        vml.item.commentlist.push(dic);
                    },
                    panecheckboxclick: function (da) {
                        if (vml.item.todo) {
                            var global_element = '';
                            var gkey = '';
                            var gindex = '';
                            $.each(todolist, function (index, element) {
                                if (element.id == vml.item.id) {
                                    gkey = vml.item.id;
                                    global_element = element;
                                    gindex = index;
                                }
                            });
                            donelist.push(da.item);
                            todolist.splice(gindex, 1);
                            $.ajax({
                                type: 'PATCH',
                                url: API_HOST + 'todo/detail/' + gkey,
                                data: {
                                    status: 2
                                }
                            }).done(function (resp) {
                                if (resp.code == 0) {
                                }
                            });
                            vml.item.todo = false;
                            vml.item.done = true;
                        } else if (vml.item.done) {
                            var gelement = '';
                            var gkey = '';
                            var gindex = '';
                            $.each(donelist, function (index, element) {
                                if (element.id == vml.item.id) {
                                    gkey = vml.item.id;
                                    gelement = element;
                                    gindex = index;
                                }
                            });
                            todolist.push(da.item);
                            donelist.splice(gindex, 1);
                            $.ajax({
                                type: 'PATCH',
                                url: API_HOST + 'todo/detail/' + gkey,
                                data: {
                                    status: 1
                                }
                            }).done(function (resp) {
                                if (resp.code == 0) {
                                }
                            });
                            vml.item.done = false;
                            vml.item.todo = true;
                        }
                    },
                    lefttoright: function (event) {
                        if (has_db_click) {
                            $("#item-detail").css('display', 'block');
                            $("#task-list").removeClass('col-md-9');
                            $('#task-list').addClass('col-md-5');
                            has_db_click = false;
                        } else {
                            $("#task-list").removeClass('col-md-5');
                            $('#task-list').addClass('col-md-9');
                            $("#item-detail").css('display', 'none');
                            has_db_click = true;
                        }
                    },
                    addchild: function (event) {
                        content = $("#clear-child-content").html().replace("<div><br></div>", "");
                        var child = {
                            'title': content
                        };
                        vml.children.push(child);
                        $("#clear-child-content").html("");
                        var parentkey = vml.item.id;
                        $.ajax({
                            type: 'POST',
                            url: API_HOST + 'todo/',
                            data: {
                                title: content,
                                parent: parentkey
                            }
                        }).done(function (resp) {
                            console.log(resp.code);
                        })
                    },
                    clearchildcontent: function (event) {
                        $("#clear-child-content").html("");
                    },
                    childcontentblur: function (event) {
                        $("#clear-child-content").html("添加子任务");
                    }
                }
            })
            ;
    };

    this.bind_btn = function () {
        $("#confirm-add-group").on('click', function () {
            var new_group_name = $("#input-group-name").val();
            if (new_group_name != "") {
                var html_string = "<li class='item-container'>" +
                    "<span class='fa fa-list'>&nbsp;&nbsp;&nbsp;</span>" + new_group_name +
                    "</li>";
                $("#group-container").append(html_string);
                $.ajax({
                    type: 'POST',
                    url: API_HOST + 'todo/group',
                    data: {
                        name: new_group_name
                    }
                }).done(function (resp) {
                    if (resp.code == 0) {
                        console.log("创建Group成功.");
                    }
                })
            } else {
                alert("请输入分组名称");
            }
        });
    }

};