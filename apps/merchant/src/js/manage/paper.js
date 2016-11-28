/**
 * Created by ZoeAllen on 16/8/2.
 */
/**
 * 测试限时管理
 * @constructor
 */
ManagePaperTimer = function () {

    var data_select = null;
    var data_table = null;

    this.init_table = function () {
        data_table = $('#data_table').DataTable({
            'language': DATATABLE_LANGUAGE,
            "paging": true,
            "pageLength": 10,
            "searching": true,
            "ordering": true,
            "order": [[0, 'asc']],
            "info": true,
            "autoWidth": true,
            "serverSide": true,
            "responsive": true,
            "select": {
                style: 'os'
            },
            "sAjaxSource": API_HOST + "paper_ma/timer",
            "columns": [
                {
                    "data": "paper", "name": "paper",
                    "mRender": function (data, type, full) {
                        return '<a class="text-primary dk">' + data.name + '</a>';
                    }
                },
                {
                    "data": "part", "name": "part"
                },
                {
                    "data": "timer", "name": "timer",
                    "mRender": function (data, type, full) {
                        return data;
                    }
                },
                {
                    "data": "gmt_update", "name": "gmt_update",
                    "mRender": function (data, type, full) {
                        return to_date('yyyy-MM-dd', data);
                    }
                }
            ],
            "fnServerParams": function (aoData) {
                parse_datatable_params(aoData);
            }
        });
    }

    this.init_select = function () {
        $.getJSON(API_HOST + 'paper/type', function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                var ele = $("#form_paper");
                for (var k in data) {
                    var d = data[k];
                    ele.append('<option data-type="' + d.type + '" value="' + d.id + '">' + d.name + '</option>');
                }
            }
        });

    }

    this.bind_select = function () {
        data_table.on('select', function (e, dt, type, index) {
            data_select = dt.data();
            set_form('data_form', data_select);
        });

        data_table.on('deselect', function (e, dt, type, index) {
            data_select = null;
            set_form('data_form', null);
        });
    }

    this.bind_btn = function () {
        $("#update_btn").on('click', function () {
            if (null == data_select) {
                toastr.warning("请选择记录");
                return;
            }
            var form = $('#data_form');
            var t = form.parsley();
            if (!t.isValid()) {
                toastr.warning('请完善信息');
                return;
            }
            submit_form(form, data_select.id);
        });
        // delete
        $("#delete_btn").on('click', function () {
            if (data_select == null) {
                toastr.warning("请选择记录");
                return;
            }
            $("#confirm_modal").modal('show');
        });
        $("#confirm_btn").on('click', function () {
            $.ajax({
                type: 'DELETE',
                url: API_HOST + 'paper_ma/timer/' + data_select.id,
            }).done(function (resp) {
                $("#confirm_modal").modal('hide');
                if (resp.code == 0) {
                    if (data_table) {
                        data_select = null;
                        data_table.ajax.reload();
                    }
                }
            });
        });
    }

    this.validate_form = function (form_id) {
        var form = $('#' + form_id);
        form.parsley().on('form:submit', function () {
            submit_form(form, null);
            return false;
        });
    }

    function submit_form(form, item_id) {
        var url = API_HOST + 'paper_ma/timer';
        if ('undefined' != typeof item_id && null != item_id && '' != item_id) {
            url += '/' + item_id;
        }
        var paper = $("#form_paper option:selected").val();
        var part = $("#form_part").val();
        var timer = $("#form_timer").val();

        $.ajax({
            type: 'POST',
            url: url,
            data: {paper: paper, part: part, timer: timer}
        }).done(function (resp) {
            if (resp.code == 0) {
                data_select = null;
                data_table.ajax.reload();
            }
        });
    }

    function set_form(form_id, data) {
        if (null == data) {
            $("#" + form_id)[0].reset();
            return;
        }
        var inputs = MyUtils.form_elements(form_id);
        MyUtils.fill_form(inputs, data);
        $("#form_paper").val(data.paper.id);
    }

}


/**
 * 测评邮箱设置
 * @constructor
 */
ManagePaperMail = function () {

    var data_table = null;
    var vue_form = null;

    var admin_flag = $.getUrlParam('admin');
    if (null != admin_flag && admin_flag == "1") {
        $("#admin_notify").removeClass('hide');
    }

    vue_form = new Vue({
        el: '#data_form',
        created: function () {
            $.getJSON(API_HOST + 'paper/type', function (resp) {
                if (resp.code == 0) {
                    var data = resp.data;
                    var ele = $("#form_paper");
                    for (var k in data) {
                        var d = data[k];
                        ele.append('<option data-type="' + d.type + '" value="' + d.id + '">' + d.name + '</option>');
                    }
                }
            });
        },
        data: {
            item_selected: {paper: {}}
        },
        methods: {
            updateMailHost: function () {
                var form = $('#data_form');
                submit_form(form, false);
            },
            deleteMailHost: function () {
                if ('undefined' == vue_form.item_selected || null == vue_form.item_selected) {
                    toastr.warning('请选择记录');
                    return;
                }
                $("#confirm_modal").modal('show');
            }
        }
    });

    this.validate_form = function () {
        var form = $('#data_form');
        form.parsley().on('form:submit', function () {
            submit_form(form, true);
            return false;
        });
    }

    this.init_table = function () {
        var url = API_HOST + "paper/mail/host";
        if (null != admin_flag && admin_flag == "1") {
            url = API_HOST + "paper_ma/mail/host";
        }
        data_table = $('#data_table').DataTable({
            'language': DATATABLE_LANGUAGE,
            "paging": true,
            "pageLength": 10,
            "order": [[0, 'asc']],
            "autoWidth": true,
            "serverSide": true,
            "select": {
                style: 'os'
            },
            "sAjaxSource": url,
            "columns": [
                {
                    "data": "name", "name": "name",
                    "mRender": function (data, type, full) {
                        return '<a class="text-primary dk">' + data + '</a>';
                    }
                },
                {
                    "data": "paper", "name": "paper",
                    "mRender": function (data, type, full) {
                        if (data) {
                            return '<a class="text-primary dk">' + data.name + '</a>';
                        }
                        return '';
                    }
                },
                {
                    "data": "host", "name": "host",
                    "mRender": function (data, type, full) {
                        return '<a class="text-primary dk">' + data + '</a>';
                    }
                },
                {
                    "data": "gmt_update", "name": "gmt_update",
                    "mRender": function (data, type, full) {
                        return to_date('yyyy-MM-dd', data);
                    }
                }
            ],
            "fnServerParams": function (aoData) {
                parse_datatable_params(aoData);
            }
        });
        data_table.on('select', function (e, dt, type, index) {
            vue_form.$set('item_selected', dt.data());
        });
        data_table.on('deselect', function (e, dt, type, index) {
            vue_form.$set('item_selected', {paper: {}});
        });

        $("#confirm_btn").on('click', function () {
            var item_id = vue_form.item_selected.id;
            var url = API_HOST + "paper/mail/host/" + item_id;
            if (null != admin_flag && admin_flag == "1") {
                url = API_HOST + "paper_ma/mail/host/" + item_id;
            }
            $.ajax({
                type: 'DELETE',
                url: url,
            }).done(function (resp) {
                if (resp.code == 0) {
                    $("#confirm_modal").modal('hide');
                    vue_form.$set('item_selected', null);
                    data_table.ajax.reload();
                }
            });
        });
    }

    function submit_form(form, is_new) {
        var url = API_HOST + "paper/mail/host";
        if (null != admin_flag && admin_flag == "1") {
            url = API_HOST + "paper_ma/mail/host";
        }
        if (!is_new) {
            var item_id = vue_form.item_selected.id;
            if ('undefined' != typeof item_id && null != item_id && '' != item_id) {
                url += '/' + item_id;
            } else {
                toastr.warning('请选择记录');
                return;
            }
        }
        var t = form.parsley();
        if (!t.isValid()) {
            toastr.warning('请完善信息');
            return;
        }
        var data = $("#data_form").serialize();
        $.ajax({
            type: 'POST',
            url: url,
            data: data
        }).done(function (resp) {
            if (resp.code == 0) {
                vue_form.$set('item_selected', null);
                data_table.ajax.reload();
            }
        });
    }

}


/**
 * 测评邮件模板设置
 * @constructor
 */
ManagePaperMailTpl = function () {

    var data_table = null;
    var vue_form = null;
    var editor = null;

    var admin_flag = $.getUrlParam('admin');
    if (null != admin_flag && admin_flag == "1") {
        $("#admin_notify").removeClass('hide');
    }
    // set href
    $("#new_tpl_a").attr('href', '/view/exam/mail.tpl.form.html?admin=' + admin_flag);
    $("#back_tpl_a").attr('href', '/view/exam/mail.tpl.html?admin=' + admin_flag);

    var mail_tpl_default = '<p><b>{name}，您好：</b></p><p><b>欢迎句</b></p><p>现在邀请你完成<b> 测评名称</b>，请用Chrome浏览器打开以下链接进入（或将网址复制到浏览器）</p><p><a href="http://test.allen.xin" target="_blank"><font color="#3984c6"><b>http://test.allen.xin</b></font></a></p><p>请用以下账号登录：</p><p>用户：<b>{username}</b></p><p>密码：<b>{password}</b></p><p><b>说明：</b></p><ol><li><b>这是对测评的说明</b></li></ol><p>Good Luck!</p>';

    $("#confirm_btn").on('click', function () {
        var item_id = vue_form.item_selected.id;
        var url = API_HOST + "paper/mail/tpl/" + item_id;
        if (null != admin_flag && admin_flag == "1") {
            url = API_HOST + "paper_ma/mail/tpl/" + item_id;
        }
        $.ajax({
            type: 'DELETE',
            url: url,
        }).done(function (resp) {
            if (resp.code == 0) {
                $("#confirm_modal").modal('hide');
                vue_form.$set('item_selected', null);
                if (null != data_table) {
                    data_table.ajax.reload();
                }
            }
        });
    });

    this.init_table = function () {
        vue_form = new Vue({
            el: '#op_div',
            data: {
                item_selected: {paper: {}}
            },
            methods: {
                updateMailTpl: function () {
                    if ('undefined' == vue_form.item_selected || null == vue_form.item_selected) {
                        toastr.warning('请选择记录');
                        return;
                    }
                    $.pjax({
                        url: '/view/exam/mail.tpl.form.html?key=' + vue_form.item_selected.id + '&admin=' + admin_flag,
                        container: '#view',
                        fragment: '#view'
                    });
                },
                deleteMailTpl: function () {
                    if ('undefined' == vue_form.item_selected || null == vue_form.item_selected) {
                        toastr.warning('请选择记录');
                        return;
                    }
                    $("#confirm_modal").modal('show');
                }
            }
        });

        var url = API_HOST + "paper/mail/tpl";
        if (null != admin_flag && admin_flag == "1") {
            url = API_HOST + "paper_ma/mail/tpl";
        }

        data_table = $('#data_table').DataTable({
            'language': DATATABLE_LANGUAGE,
            "paging": true,
            "pageLength": 10,
            "order": [[0, 'asc']],
            "autoWidth": true,
            "serverSide": true,
            "select": {
                style: 'os'
            },
            "sAjaxSource": url,
            "columns": [
                {
                    "data": "name", "name": "name",
                    "mRender": function (data, type, full) {
                        return '<a class="text-primary dk" data-pjax href="/view/exam/mail.tpl.form.html?key=' + full.id + '&admin=' + admin_flag + '">' + data + '</a>';
                    }
                },
                {
                    "data": "paper", "name": "paper",
                    "mRender": function (data, type, full) {
                        if (data) {
                            return data.name;
                        }
                        return '';
                    }
                },
                {
                    "data": "title", "name": "title"
                },
                {
                    "data": "gmt_update", "name": "gmt_update",
                    "mRender": function (data, type, full) {
                        return to_date('yyyy-MM-dd', data);
                    }
                },
                {
                    "data": "id", "name": "id",
                    "mRender": function (data, type, full) {
                        var btn = [];
                        btn.push('<a class="btn btn-xs btn-icon btn-default" data-pjax href="/view/exam/mail.tpl.form.html?key=' + data + '&admin=' + admin_flag + '"><i class="fa fa-edit"></i></a>');
                        btn.push('<button class="btn btn-xs btn-icon btn-danger m-l-xs delete_btn"><i class="fa fa-trash"></i></button>');
                        return btn.join('');
                    }
                }
            ],
            "fnServerParams": function (aoData) {
                parse_datatable_params(aoData);
            }
        });
        data_table.on('select', function (e, dt, type, index) {
            vue_form.$set('item_selected', dt.data());
        });
        data_table.on('deselect', function (e, dt, type, index) {
            vue_form.$set('item_selected', {paper: {}});
        });

        $("#data_table").on('click', '.delete_btn', function () {
            var row = data_table.row($(this).parent().parent(), {page: 'current'});
            row.select();
            vue_form.$set('item_selected', row.data());
            $("#confirm_modal").modal('show');
        });

    }

    this.validate_form = function () {
        vue_form = new Vue({
            el: '#data_form',
            created: function () {
                $.getJSON(API_HOST + 'paper/type', function (resp) {
                    if (resp.code == 0) {
                        var data = resp.data;
                        var ele = $("#form_paper");
                        for (var k in data) {
                            var d = data[k];
                            ele.append('<option data-type="' + d.type + '" value="' + d.id + '">' + d.name + '</option>');
                        }
                    }
                });
            },
            data: {
                item_selected: {paper: {}}
            },
            methods: {
                deleteMailTpl: function () {
                    if ('undefined' == vue_form.item_selected || null == vue_form.item_selected) {
                        toastr.warning('请选择记录');
                        return;
                    }
                    $("#confirm_modal").modal('show');
                },
                previewMailTpl: function () {
                    var content = $('#tpl_editor').summernote('code');
                    $("#preview_pre").empty().html(content);
                    $("#subject_pre").empty().text('邮件主题：' + $("#form_title").val());
                    $("#preview_modal").modal('show');
                }
            }
        });
        var form = $('#data_form');
        form.parsley().on('form:submit', function () {
            submit_form(form);
            return false;
        });
    }

    this.init_editor = function () {
        editor = $("#tpl_editor").summernote({
            lang: 'zh-CN',
            height: 300,
            minHeight: 200,
            focus: false,
            toolbar: [
                // [groupName, [list of button]]
                ['style', ['style', 'bold', 'italic', 'underline', 'clear']],
                ['font', ['fontname', 'fontsize']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['insert', ['link', 'picture', 'video', 'table', 'hr']],
                ['height', ['height']],
                ['misc', ['fullscreen', 'codeview', 'undo', 'redo', 'help']]
            ],
        });
        var item_id = $.getUrlParam('key');
        if (null != item_id) {
            var url = API_HOST + "paper/mail/tpl/" + item_id;
            if (null != admin_flag && admin_flag == "1") {
                url = API_HOST + "paper_ma/mail/tpl/" + item_id;
            }
            // load tpl detail
            $.ajax({
                type: 'GET',
                url: url,
                statusCode: {
                    404: function () {
                        window.history.back();
                    }
                }
            }).done(function (resp) {
                var data = resp.data;
                var paper = data.paper;
                if (null == paper) {
                    data.paper = {id: ""};
                }
                vue_form.$set('item_selected', data);
                $('#tpl_editor').summernote('code', data.content)
            });
        } else {
            $('#tpl_editor').summernote('code', mail_tpl_default)
        }
    }

    function submit_form(form) {
        var url = API_HOST + "paper/mail/tpl";
        if (null != admin_flag && admin_flag == "1") {
            url = API_HOST + "paper_ma/mail/tpl";
        }
        var item_id = vue_form.item_selected.id;
        if ('undefined' != typeof item_id && null != item_id && '' != item_id) {
            url += '/' + item_id;
        }
        var content = $('#tpl_editor').summernote('code');
        var t = form.parsley();
        if (!t.isValid() || 'undefined' == typeof content) {
            toastr.warning('请完善信息');
            return;
        }
        var data = $("#data_form").serializeArray();
        data.push({name: 'content', value: content});
        $.ajax({
            type: 'POST',
            url: url,
            data: data
        }).done(function (resp) {

        });
    }

}
