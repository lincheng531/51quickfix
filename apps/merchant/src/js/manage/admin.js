/**
 * Created by ZoeAllen on 16/7/13.
 */

/**
 * 公司管理
 * @constructor
 */
ManageCompany = function () {

    var data_select = null;
    var data_table = null;
    var last_select = null;
    var admin_role = null;
    var company_id = null;

    this.init_table = function () {
        data_table = $('#data_table').DataTable({
            'language': DATATABLE_LANGUAGE,
            "paging": true,
            "pageLength": 10,
            "searching": true,
            "ordering": true,
            "info": true,
            "autoWidth": true,
            "serverSide": true,
            "responsive": true,
            "select": {
                style: 'os'
            },
            "sAjaxSource": API_HOST + "company/basic",
            "columns": [
                {
                    "data": "name", "name": "name",
                    "mRender": function (data, type, full) {
                        return '<a class="text-primary dk info_btn">' + data + '</a>';
                    }
                },
                {
                    "data": "code", "name": "code"
                },
                {
                    "data": "address", "name": "address",
                    "mRender": function (data, type, full) {
                        return data;
                    }
                },
                {
                    "data": "info", "name": "info",
                    "mRender": function (data, type, full) {
                        return data;
                    }
                },
                {
                    "data": "id", "name": "id", "orderable": false,
                    "mRender": function (data, type, full) {
                        return '<a class="btn btn-xs btn-icon white" data-pjax href="/view/manage/company_init.html?full=1&key=' + full.id + '"><i class="fa fa-fire"></i></a>';
                    }
                },
                {
                    "data": "gmt_create", "name": "gmt_create",
                    "mRender": function (data, type, full) {
                        return to_date('yyyy-MM-dd', data);
                    }
                }
            ],
            "fnServerParams": function (aoData) {
                var params = {};
                $.each(aoData, function (k, v) {
                    params[v.name] = v.value;
                });
                var sColumns = params['sColumns'].split(',');
                aoData.push({"name": "page", "value": params['iDisplayStart'] / params['iDisplayLength'] + 1});
                aoData.push({"name": "size", "value": params['iDisplayLength']});
                aoData.push({"name": "order_by", "value": sColumns[params['iSortCol_0']]});
                aoData.push({"name": "order", "value": params['sSortDir_0']});
                aoData.push({"name": "search", "value": params['sSearch']});
            }
        });
    }

    this.bind_select = function () {
        data_table.on('select', function (e, dt, type, index) {
            data_select = dt.data();
            last_select = dt.data();
        });

        data_table.on('deselect', function (e, dt, type, index) {
            data_select = null;
            set_form('data_form', null);
        });
    }

    this.bind_btn = function () {
        $("#insert_btn").on('click', function () {
            $("#edit_modal_title").text('新增公司');
            set_form('data_form', null);
            $("#edit_modal").modal('show');
        });
        $("#data_table").on('click', 'a.info_btn', function () {
            open_edit(last_select);
        });
        $("#update_btn").on('click', function () {
            open_edit(data_select);
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
                url: API_HOST + 'company/basic/' + data_select.id,
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
        // init
        $("#init_btn").on('click', function () {
            if (null == data_select) {
                toastr.warning("请选择记录");
                return;
            }
            $.pjax({
                url: '/view/manage/company_init.html?full=1&key=' + data_select.id,
                container: '#view',
                fragment: '#view'
            });
        });
    }

    this.validate_form = function (form_id) {
        var form = $('#' + form_id);
        form.parsley().on('form:submit', function () {
            submit_form(form, form.attr('data-id'));
            return false;
        });
    }

    this.init_company = function (item_id) {

        $.getJSON(API_HOST + 'company/basic/' + item_id, function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                init_role(data.company.id);
                $("#user_form").attr('data-id', data.company.id);
                init_user(resp.data);
            }
        });

    }

    this.validate_user_form = function (form_id) {
        var form = $('#' + form_id);
        form.parsley().on('form:submit', function () {
            var company_id = form.attr('data-id');
            if (null == company_id || '' == company_id || typeof company_id == 'undefined') {
                return;
            }
            var data = form.serializeArray();
            data.push({name: 'company', value: company_id});
            $.ajax({
                type: 'POST',
                url: API_HOST + 'company/user',
                data: data
            }).done(function (resp) {
                if (resp.code == 0) {
                    $.getJSON(API_HOST + 'company/basic/' + company_id, function (basic_resp) {
                        if (basic_resp.code == 0) {
                            init_user(basic_resp.data);
                        }
                    });
                }
            });
            return false;
        });
    }

    this.init_menu = function () {
        $.ajax({
            type: 'GET',
            url: API_HOST + 'company/menu?size=50',
        }).done(function (resp) {
            if (resp.code == 0) {
                var tbody = $("#menu_table tbody")
                $.each(resp.data, function (k, v) {
                    var html = [];
                    // data-json=\'' + JSON.stringify(v) + '\'>
                    html.push('<tr>');
                    html.push('<td>');
                    html.push('<label class="ui-check m-a-0">');
                    html.push('<input type="checkbox" name="menu_chx" class="has-value" value="' + v.id + '">');
                    html.push('<i class="dark-white"></i>');
                    html.push('</label>');
                    html.push('</td>');
                    html.push('<td class="t_s">' + v.name + '</td>');
                    html.push('<td class="t_s">' + format_level(v.user_level, 'pull-right') + '</td>');
                    html.push('</tr>');
                    tbody.append(html.join(''));
                });
            }
        });
    }

    this.bind_init_btn = function (company_id) {
        $("#user_div_toggle").on('click', function () {
            $("#user_div").toggleClass('hide');
        });

        // for menu all checkbox
        $("#menu_all_chx").on('change', function () {
            var flag = $(this).prop('checked');
            $.each($("#menu_table tbody").find('input[type=checkbox]'), function () {
                $(this).prop('checked', flag);
            });
        });

        $("#menu_table tbody").on('click', 'tr', function () {
            var chx = $(this).find('input[type=checkbox]');
            chx.prop('checked', !chx.prop('checked'));
        });

        $("#menu_ref_btn").on('click', function () {
            if (null == admin_role) {
                toastr.warning("无效的管理员角色");
                return;
            }
            var menus = [];
            $.each($("#menu_table tbody").find('input[type=checkbox]'), function () {
                var chx = $(this);
                if (chx.prop('checked')) {
                    menus.push(chx.val());
                }
            });
            $.ajax({
                type: 'POST',
                url: API_HOST + 'company/menu/ref',
                data: {role: admin_role.id, menu: menus.join(','), company: company_id}
            }).done(function () {
                // pass
            });
        });

        $("#clean_ref_btn").on('click', function () {
            $.each($("#menu_table tbody").find('input[type=checkbox]'), function () {
                $(this).prop('checked', false);
            });
        });

        $("#refresh_btn").on('click', function () {
            $.ajax({
                type: 'DELETE',
                url: API_HOST + 'company/menu',
            }).done(function (resp) {

            });
        });

    }

    function init_role(company_id) {
        $.getJSON(API_HOST + 'company/role?company=' + company_id, function (resp) {
            var data = resp.data;
            $("#form_role").append('<option selected value="' + data.id + '">' + data.name + '</option>');
            admin_role = data;
        });
        $.getJSON(API_HOST + 'company/menu/ref?company=' + company_id, function (ref_resp) {
            var ref_data = ref_resp.data;
            set_menu_ref(ref_data);
        });
    }

    function init_user(data) {
        var t = $("#user_div");
        t.empty();
        if (null == data.users || 0 == data.users.length) {
            t.append('<a class="list-group-item">无</a>');
        }
        $.each(data.users, function (k, v) {
            t.append('<span class="list-group-item">' + v.username + '</a>');
        });
        $("#user_div_toggle").find('span').text(data.users.length || 0);
        $("#company_title").text(data.company.name);
    }

    function set_menu_ref(data) {
        if (null == data || data.length == 0) {
            return;
        }
        $.each(data, function (k, v) {
            $('#menu_table input[type=checkbox][value=' + v.menu + ']').prop("checked", true);
        })
    }

    function open_edit(data) {
        if (null == data) {
            toastr.warning("请选择记录");
            return;
        }
        $("#edit_modal_title").text('修改公司');
        set_form("data_form", data);
        $("#edit_modal").modal('show');
    }

    function submit_form(form, item_id) {
        var url = API_HOST + 'company/basic';
        if ('undefined' != typeof item_id && null != item_id && '' != item_id) {
            url += '/' + item_id;
        }
        var data = form.serializeArray();
        $.ajax({
            type: 'POST',
            url: url,
            data: data
        }).done(function (resp) {
            $("#edit_modal").modal('hide');
            if (resp.code == 0) {
                data_select = null;
                data_table.ajax.reload();
            }
        });
    }

    function set_form(form_id, data) {
        if (null == data) {
            $("#" + form_id)[0].reset();
            $("#" + form_id).attr('data-id', '');
            return;
        }
        $("#" + form_id).attr('data-id', data.id);
        var inputs = MyUtils.form_elements(form_id);
        $.each(inputs, function (k, v) {
            if (v['type'] == "radio") {
                $("#" + v['name'] + "_" + data[v['name']]).prop("checked", true);
            } else {
                $("#" + v['id']).val(data[v['name']]);
            }
        });
    }

}


/**
 * 用户管理
 * @constructor
 */
ManageCompanyUser = function (flag) {

    var data_table = null;

    this.init_table = function () {
        var url = API_HOST + "company/user/all";
        data_table = $('#data_table').DataTable({
            'language': DATATABLE_LANGUAGE,
            "paging": true,
            "pageLength": 10,
            "searching": true,
            "ordering": true,
            "info": true,
            "autoWidth": true,
            "serverSide": true,
            "responsive": true,
            "select": {
                style: 'os'
            },
            "sAjaxSource": url,
            "columns": [
                {
                    "data": "username", "name": "username",
                    "mRender": function (data, type, full) {
                        return '<a class="text-primary dk">' + data + '</a>';
                    }
                },
                {
                    "data": "company_name", "name": "cc.name",
                    "mRender": function (data, type, full) {
                        return '<a class="text-primary dk">' + data + '</a>';
                    }
                },
                {
                    "data": "username", "name": "m.last_name",
                    "mRender": function (data, type, full) {
                        return full.last_name + full.first_name || data;
                    }
                },
                {
                    "data": "role_name", "name": "ur.name"
                },
                {
                    "data": "level", "name": "rf.level",
                    "mRender": function (data, type, full) {
                        return format_level(data, '');
                    }
                },
                {
                    "data": "status", "name": "up.status",
                    "mRender": function (data, type, full) {
                        if (data == 1) {
                            return '<span class="label green">启用</span>';
                        } else {
                            return '<span class="label red">禁用</span>';
                        }
                    }
                },
            ],
            "fnServerParams": function (aoData) {
                var params = {};
                $.each(aoData, function (k, v) {
                    params[v.name] = v.value;
                });
                var sColumns = params['sColumns'].split(',');
                aoData.push({"name": "page", "value": params['iDisplayStart'] / params['iDisplayLength'] + 1});
                aoData.push({"name": "size", "value": params['iDisplayLength']});
                aoData.push({"name": "order_by", "value": sColumns[params['iSortCol_0']]});
                aoData.push({"name": "order", "value": params['sSortDir_0']});
                aoData.push({"name": "search", "value": params['sSearch']});
            }
        });

        $("#filter_select").on('change', function () {
            if (data_table) {
                data_table.ajax.reload();
            }
        });
    }

}


/**
 * 用户管理
 * @constructor
 */
ManageUser = function (flag) {

    var data_select = null;
    var data_table = null;

    var permission_uri = 'manage';

    this.init_table = function () {
        var url = API_HOST + permission_uri + "/user";
        data_table = $('#data_table').DataTable({
            'language': DATATABLE_LANGUAGE,
            "paging": true,
            "pageLength": 10,
            "searching": true,
            "ordering": true,
            "info": true,
            "autoWidth": false,
            "serverSide": true,
            "select": {
                style: 'os'
            },
            "sAjaxSource": url,
            "columns": [
                {
                    "data": "username", "name": "username",
                    "mRender": function (data, type, full) {
                        return '<a class="text-primary dk">' + MyUtils.cutstr(data, 16) + '</a>';
                    }
                },
                {
                    "data": "username", "name": "m.last_name",
                    "mRender": function (data, type, full) {
                        return MyUtils.cutstr(full.name || (full.last_name + full.first_name) || data, 16);
                    }
                },
                {
                    "data": "role_name", "name": "ur.name"
                },
                {
                    "data": "dept", "name": "dept", "orderable": false,
                    "mRender": function (data, type, full) {
                        if (null != data && data.length > 0) {
                            var d = [];
                            $.each(data, function (i) {
                                var label = '<span class="label label-sm warning">领导</span>';
                                if (data[i].dept_is_leader == 0) {
                                    label = '<span class="label label-sm primary">员工</span>';
                                }
                                d.push(data[i].dept_name + ' ' + label);
                            });
                            return d.join(' ');
                        }
                        return '';
                    }
                },
                {
                    "data": "status", "name": "up.status",
                    "mRender": function (data, type, full) {
                        if (data == 1) {
                            return '<span class="label green">启用</span>';
                        } else {
                            return '<span class="label red">禁用</span>';
                        }
                    }
                },
            ],
            "fnServerParams": function (aoData) {
                var params = {};
                $.each(aoData, function (k, v) {
                    params[v.name] = v.value;
                });
                var sColumns = params['sColumns'].split(',');
                aoData.push({"name": "page", "value": params['iDisplayStart'] / params['iDisplayLength'] + 1});
                aoData.push({"name": "size", "value": params['iDisplayLength']});
                aoData.push({"name": "order_by", "value": sColumns[params['iSortCol_0']]});
                aoData.push({"name": "order", "value": params['sSortDir_0']});
                aoData.push({"name": "search", "value": params['sSearch']});
                aoData.push({"name": "dept", "value": $("#dept_select").val()});
                aoData.push({"name": "type", "value": $("#type_select").val()});
            }
        });

        $("#dept_select").on('change', function () {
            if (data_table) {
                data_table.ajax.reload();
            }
        });
        $("#type_select").on('change', function () {
            if (data_table) {
                data_table.ajax.reload();
            }
        });
    }

    this.bind_select = function () {
        data_table.on('select', function (e, dt, type, index) {
            data_select = dt.data();
            data_select.nickname = data_select.last_name + data_select.first_name || data_select.username;
            set_form('user_form', data_select);
            toggle_btn_status(data_select);
        });

        data_table.on('deselect', function (e, dt, type, index) {
            data_select = null;
            set_form('user_form', data_select);
            toggle_btn_status(null);
        });
    }

    this.init_role = function (dom_id) {
        $.ajax({
            type: 'GET',
            url: API_HOST + 'user/role',
        }).done(function (resp) {
            if (resp.code == 0) {
                var t = $("#" + dom_id);
                t.append('<option value=""></option>');
                $.each(resp.data, function (k, v) {
                    t.append('<option value="' + v.id + '">' + v.name + '</option>');
                });
            }
        });
    }

    this.init_dept = function (dom_id) {
        $.ajax({
            type: 'GET',
            url: API_HOST + 'manage/dept',
        }).done(function (resp) {
            if (resp.code == 0) {
                var t = $("#" + dom_id);
                var s = $("#dept_select");
                t.append('<option value=""></option>');
                $.each(resp.data, function (k, v) {
                    t.append('<option value="' + v.id + '">' + v.name + '</option>');
                    if (s) {
                        s.append('<option value="' + v.id + '">' + v.name + '</option>');
                    }
                });
            }
        });
    }

    this.init_user_ref = function (dom_id) {
        $("#" + dom_id).select2({
            placeholder: '选择该用户的上级用户',
            theme: 'bootstrap',
            allowClear: true,
            maximumInputLength: 20,
            minimumResultsForSearch: 20,
            ajax: {
                url: API_HOST + 'manage/user/all',
                data: function (params) {
                    var curr_userid = '';
                    if (data_select) {
                        curr_userid = data_select.id
                    }
                    var query = {
                        search: params.term,
                        size: 100,
                        exclude: curr_userid
                    }
                    return query;
                },
                delay: 250,
                processResults: function (resp) {
                    var res = [];
                    $.each(resp.data, function (k, v) {
                        var name = v.user.last_name + v.user.first_name || v.user.username;
                        res.push({id: v.user.id, text: name});
                    });
                    return {
                        results: res
                    };
                }
            }
        });
    }

    this.bind_btn = function () {
        $("#update_btn").on('click', function () {
            if (null == data_select) {
                toastr.warning("请选择记录");
                return;
            }
            update_user(data_select.id);
        });
        $(".status_btn").on('click', function () {
            if (null == data_select) {
                toastr.warning("请选择记录");
                return;
            }
            var status = $(this).attr('data-status');
            update_user_status(data_select.id, status);
        });
        $("#passwd_btn").on('click', function () {
            if (null == data_select) {
                toastr.warning("请选择记录");
                return;
            }
            update_password(data_select.id);
        });
        $("#form_name").on('change', function () {
            $.getJSON(API_HOST + 'common/pinyin?name=' + $(this).val().replace(/ /g, ""), function (resp) {
                if (resp.code == 0) {
                    var data = resp.data;
                    $("#form_username").val(data.pinyin.join(''))
                }
            });
        });
        $("#user_form").on('click', '.add_dept_btn', function () {
            var index = $(".dept_div").length;
            if (index > 4) {
                toastr.warning("添加了太多部门");
                return;
            }
            add_dept_div(index);
        });
        $("#user_form").on('click', '.delete_dept_btn', function () {
            var index = $(".dept_div").length;
            if (index == 1) {
                return;
            }
            $(this).parent().parent().remove();
            // update dept index
            $.each($(".dept_index"), function (k) {
                $(this).text(k + 1);
            });
        });
    }

    this.validate_form = function (form_id) {
        // MyUtils.form_elements(form_id);
        var form = $('#' + form_id);
        form.parsley().on('form:submit', function () {
            var data = form.serializeArray();
            var leader = $("#form_user_ref").val();
            if (null != leader && 'undefined' != typeof leader) {
                data.push({name: 'leader', value: leader.join(',')});
            }
            var dept = parse_dept();
            if (dept.length > 0) {
                data.push({name: 'dept', value: JSON.stringify(dept)});
            }
            // format user nickname
            var name = $("#form_name").val();
            name = $.splitName(name);
            if (name && name.length == 2) {
                data.push({name: 'last_name', value: name[0]});
                data.push({name: 'first_name', value: name[1]});
            }
            $.ajax({
                type: 'POST',
                url: API_HOST + permission_uri + '/user',
                data: data
            }).done(function (resp) {
                // reset form
                if (resp.code == 0) {
                    form[0].reset();
                    $("#form_user_ref").empty().trigger('change');
                    remove_dept_div();
                }
            });
            return false;
        });
    }

    this.import_user = function () {

        var vue_div = new Vue({
            el: '#import_status_div',
            data: {
                status_list: []
            }
        });

        var form = $("#import_data_form")[0];
        form.action = API_HOST + "manage/user/import" + "?access_token=" + USER_PROFILE.token;
        var options = {
            beforeSubmit: function(){
                vue_div.$set('status_list', []);
            },
            success: function (resp) {
                toastr.success('导入完成');
                vue_div.$set('status_list', resp.data || []);
            },
            error: function (response) {

            },
        }

        $("#import_data_form").ajaxForm(options);
    }

    function add_dept_div(index) {
        var dept = $("#dept_div");
        var dept_new = dept.clone();
        dept_new.attr('id', '').attr('name', 'extend_dept_div');
        dept_new.find('.delete_dept_btn').removeClass('hide');
        dept_new.find('.dept_index').text(index + 1);
        dept_new.insertBefore($("#role_div"));
        return dept_new;
    }

    function remove_dept_div() {
        $("div[name=extend_dept_div]").remove();
    }

    function parse_dept() {
        var dept_data = [];
        $.each($(".dept_div"), function () {
            var div = $(this);
            var dept = $(div.find('select[name=dept]')[0]).val();
            var role = $(div.find('input[name=dept_role]')[0]).val();
            var is_leader = $(div.find('input[type=checkbox][name=is_leader]:checked')[0]).attr('value');
            dept_data.push({dept: dept, role: role, is_leader: is_leader});
        });
        return dept_data;
    }

    function set_form(form_id, data) {
        var select = $("#form_user_ref");
        remove_dept_div();
        if (null == data) {
            $("#" + form_id)[0].reset();
            select.empty().trigger('change');
            return;
        }
        var inputs = MyUtils.form_elements(form_id);
        $.each(inputs, function (k, v) {
            if (v['type'] == "radio") {
                $("#" + v['name'] + "_" + data[v['name']]).prop("checked", true);
            } else {
                $("#" + v['id']).val(data[v['name']]);
            }
        });
        var parent = data.parent;
        if (null != parent && parent.length > 0) {
            $.each(parent, function (k, v) {
                select.append('<option selected value="' + v.user_id + '">' + (v.nickname || v.username) + '</option>');
            });
            select.trigger('change');
        } else {
            select.empty().trigger('change');
        }
        // set dept
        var dept = data.dept;
        if (null != dept && dept.length > 0) {
            $.each(dept, function (k, v) {
                if (k == 0) {
                    var dept_new = $("#dept_div");
                } else {
                    // add div
                    var dept_new = add_dept_div(k);
                }
                // set dept input value
                $(dept_new.find('select[name=dept]')).val(v.dept_id);
                $(dept_new.find('input[name=dept_role]')).val(v.dept_role);
                $(dept_new.find('input[type=checkbox][name=is_leader]')).prop('checked', v.dept_is_leader == 1);
            });
        }
    }

    function update_user(user_id) {
        var leader = $("#form_user_ref").val() || [];
        var dept = parse_dept();
        if (dept.length > 0) {
            dept = JSON.stringify(dept);
        }
        var data = {
            'leader': leader.join(','),
            'role': $("#form_role").val(),
            'level': $("#form_level").val(),
            'dept': dept || ''
        }
        $.ajax({
            type: 'POST',
            url: API_HOST + permission_uri + '/user/' + user_id,
            data: data
        }).done(function (resp) {
            if (resp.code == 0) {
                data_select = null;
                data_table.ajax.reload();
            }
        });
    }

    function update_user_status(user_id, status) {
        $.ajax({
            type: 'PUT',
            url: API_HOST + permission_uri + '/user/' + user_id,
            data: {flag: status}
        }).done(function (resp) {
            if (resp.code == 0) {
                data_select = null;
                data_table.ajax.reload();
            }
        });
    }

    function toggle_btn_status(data) {
        if (null == data) {
            $("#btn_div button").attr('disabled', 'disabled');
        } else {
            $("#update_btn").removeAttr('disabled');
            $("#status_btn").removeAttr('disabled');
            var status = data.status;
            if (status == 0) {
                $("#update_btn").attr('disabled', 'disabled');
                $("#status_1_btn").removeAttr('disabled');
            } else {
                $("#status_0_btn").removeAttr('disabled');
            }
        }
    }

    function update_password(user_id) {
        var p1 = $("#form_password").val();
        var p2 = $("#form_password_2").val();
        if ('' == p1) {
            toastr.warning("请输入想要重置的用户密码");
            return;
        } else if ('' == p2) {
            toastr.warning("请重复想要重置的用户密码");
            return;
        } else if (p1 != p2) {
            toastr.warning("请确保二次密码一致");
            return;
        }
        $.ajax({
            type: 'POST',
            url: API_HOST + permission_uri + '/user/passwd/' + user_id,
            data: {password_new: p1}
        }).done(function (resp) {

        });
    }
}


/**
 * 角色管理
 * @constructor
 */
ManageRole = function () {

    var data_select = null;
    var data_table = null;

    this.init_table = function () {
        data_table = $('#data_table').DataTable({
            "paging": true,
            "pageLength": 10,
            "searching": true,
            "ordering": true,
            "info": true,
            "autoWidth": true,
            "serverSide": true,
            "responsive": true,
            "select": {
                style: 'os'
            },
            "sAjaxSource": API_HOST + "manage/role",
            "columns": [
                {
                    "data": "name", "name": "name",
                    "mRender": function (data, type, full) {
                        return '<a class="text-primary dk">' + data + '</a>';
                    }
                },
                {
                    "data": "code", "name": "code"
                },
                {
                    "data": "level", "name": "level",
                    "mRender": function (data, type, full) {
                        return format_level(data);
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
                var params = {};
                $.each(aoData, function (k, v) {
                    params[v.name] = v.value;
                });
                var sColumns = params['sColumns'].split(',');
                aoData.push({"name": "page", "value": params['iDisplayStart'] / params['iDisplayLength'] + 1});
                aoData.push({"name": "size", "value": params['iDisplayLength']});
                aoData.push({"name": "order_by", "value": sColumns[params['iSortCol_0']]});
                aoData.push({"name": "order", "value": params['sSortDir_0']});
                aoData.push({"name": "search", "value": params['sSearch']});
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
                url: API_HOST + 'manage/role/' + data_select.id,
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
        var url = API_HOST + 'manage/role';
        if ('undefined' != typeof item_id && null != item_id && '' != item_id) {
            url += '/' + item_id;
        }
        var data = form.serializeArray();
        $.ajax({
            type: 'POST',
            url: url,
            data: data
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
        $.each(inputs, function (k, v) {
            if (v['type'] == "radio") {
                $("#" + v['name'] + "_" + data[v['name']]).prop("checked", true);
            } else {
                $("#" + v['id']).val(data[v['name']]);
            }
        });
    }

}


/**
 * 菜单管理
 * @constructor
 */
ManageMenu = function () {

    var role_list = [];
    var menu_list = [];

    this.init_data = function () {
        // load menu
        $.ajax({
            type: 'GET',
            url: API_HOST + 'manage/menu?size=50',
        }).done(function (resp) {
            if (resp.code == 0) {
                fill_menu(resp.data);
                menu_list = resp.data;
            }
        });
        // load role
        if (role_list.length == 0) {
            $.ajax({
                type: 'GET',
                url: API_HOST + 'user/role',
            }).done(function (resp) {
                if (resp.code == 0) {
                    role_list = resp.data;
                    fill_role(role_list);
                }
            });
        }
    }

    this.bind_event = function () {
        // for menu all checkbox
        $("#menu_all_chx").on('change', function () {
            set_menu_check($(this).prop('checked'));
        });

        $("#menu_table tbody").on('click', 'tr', function () {
            var chx = $(this).find('input[type=checkbox]');
            chx.prop('checked', !chx.prop('checked'));
        });

        $("#role_list").on('click', 'div.list-item', function () {
            var div = $(this);
            div.toggleClass('light-blue').siblings().removeClass('light-blue');
            if (div.hasClass('light-blue')) {
                var data = JSON.parse(div.attr('data-json'));
                load_menu_ref(data.id);
            }
        });

        $("#update_btn").on('click', function () {
            var menus = [];
            $.each($("#menu_table tbody").find('input[type=checkbox]'), function () {
                var chx = $(this);
                if (chx.prop('checked')) {
                    menus.push(chx.val());
                }
            });
            // check
            var d = $("#role_list div.light-blue").attr('data-json');
            if ('undefined' == typeof d) {
                toastr.warning("请选择系统角色");
                return;
            }
            d = JSON.parse(d);
            update(d.id, menus);
        });

        $("#refresh_btn").on('click', function () {
            $.ajax({
                type: 'DELETE',
                url: API_HOST + 'manage/menu',
            }).done(function (resp) {
                // pass
            });
        });

        $("#reset_btn").on('click', function () {
            set_menu_check(false);
        });
    }

    function set_menu_check(flag) {
        $.each($("#menu_table tbody").find('input[type=checkbox]'), function () {
            $(this).prop('checked', flag);
        });
    }

    function fill_menu(data) {
        var tbody = $("#menu_table tbody")
        $.each(data, function (k, v) {
            var html = [];
            // data-json=\'' + JSON.stringify(v) + '\'>
            html.push('<tr>');
            html.push('<td>');
            html.push('<label class="ui-check m-a-0">');
            html.push('<input type="checkbox" name="menu_chx" class="has-value" value="' + v.id + '">');
            html.push('<i class="dark-white"></i>');
            html.push('</label>');
            html.push('</td>');
            html.push('<td class="t_s">' + v.name + '</td>');
            html.push('<td class="t_s">' + format_level(v.user_level, 'pull-right') + '</td>');
            html.push('</tr>');
            tbody.append(html.join(''));
        });
    }

    function fill_role(data) {
        $.each(data, function (k, v) {
            var html = [];
            html.push('<div class="list-item" data-json=\'' + JSON.stringify(v) + '\'>');
            html.push('<div class="list-body">');
            html.push('<a class="col-sm-12">' + v.name);
            html.push(format_level(v.level, 'pull-right'));
            html.push('</a>');
            html.push('</div>');
            html.push('</div>');
            $("#role_list").append(html.join(''));
        });
    }

    function load_menu_ref(menu_id) {
        set_menu_check(false);
        $.ajax({
            type: 'GET',
            url: API_HOST + 'manage/menu/ref/' + menu_id,
        }).done(function (resp) {
            if (resp.code == 0) {
                fill_menu_ref(resp.data);
            }
        });
    }

    function fill_menu_ref(data) {
        $.each(data, function (k, v) {
            $('#menu_table input[type=checkbox][value=' + v.menu + ']').prop("checked", true);
        });
    }

    function update(role_id, menus) {
        $.post(API_HOST + 'manage/menu/ref/' + role_id, {menu: menus.join(',')});
    }

}
