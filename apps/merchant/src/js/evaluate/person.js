/**
 * Created by ZoeAllen on 16/6/15.
 */


/**
 *  候选人基本信息
 * @constructor
 */
ExamPerson = function () {

    var CV_FILE_UPLOAD_FLAG = false;
    var CV_FILE_NEED = false;

    var degree_mapping = {
        '博士': ['本科', '硕士', '博士'],
        '硕士': ['本科', '硕士'],
        '本科': ['本科'],
        '大专': ['大专'],
        '其他': ['其他'],
    }

    this.bind_event = function () {
        $("#form_degree").on('change', function () {
            $(".extend_degree_div").remove();
            var d = $(this).val();
            d = degree_mapping[d];
            if (d && d.length > 0) {
                $.each(d, function (k, v) {
                    var dom = $("#degree_div");
                    if (k > 0) {
                        var div = dom.clone();
                        div.attr('id', '').addClass('extend_degree_div');
                        div.find('label').text(v);
                        div.find('button').removeClass('hide').addClass('btn-remove');
                        div.find('input[name=school_extend]').val('');
                        div.find('input[name=major_extend]').val('');
                        div.insertBefore($("#save_btn"));
                    } else {
                        dom.find('label').text(v);
                    }
                });
            }
        });
        $("#profile_form").on('click', '.btn-remove', function () {
            $(this).parent().parent().remove();
        });
    }

    this.load_profile = function () {
        // get paper basic info
        $.getJSON(API_HOST + 'user/base/profile', function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                var inputs = MyUtils.form_elements("profile_form");
                MyUtils.fill_form(inputs, data.profile);
                var extend = data.profile.extend;
                if (extend) {
                    extend = JSON.parse(extend);
                    if (extend.cv) {
                        for (var i in extend.cv) {
                            var d = extend.cv[i];
                            $("#my_cv_h4").html('<a href="' + API_HOST + 'user/resume/preview?access_token=' + USER_PROFILE.token + '" target="_blank">' + i + '</a>');
                            $("#size_span").text('大小：' + MyUtils.roundval(d.size / 1024 / 1024, 1) + ' Mb');
                        }
                        $("#my_resume_info_div").removeClass('hide');
                        CV_FILE_UPLOAD_FLAG = true;
                    }
                }
                var education = data.profile.education;
                if (education && education.length > 0) {
                    $.each(education, function (k, v) {
                        var dom = $("#degree_div");
                        if (k > 0) {
                            var div = dom.clone();
                            div.attr('id', '').addClass('extend_degree_div');
                            div.find('button').removeClass('hide').addClass('btn-remove');
                            fill_education(div, v)
                            div.insertBefore($("#save_btn"));
                        } else {
                            fill_education(dom, v)
                        }
                    });
                }
            }
        });
    }

    this.validate_form = function (form_id) {
        var form = $('#' + form_id);
        form.parsley().on('form:submit', function () {
            if (CV_FILE_NEED && !CV_FILE_UPLOAD_FLAG) {
                toastr.warning('请上传10Mb以内的PDF简历文件');
                return false;
            }
            var url = API_HOST + 'user/base/profile';
            var data = form.serializeArray();
            var education = [];
            $.each($(".degree_div"), function (k, v) {
                var div = $(this);
                var degree = div.find('label').text();
                var school = div.find('input[name=school_extend]').val();
                var major = div.find('input[name=major_extend]').val();
                if (school != '') {
                    education.push({degree: degree, school: school, major: major});
                }
            });
            $("#education").val(JSON.stringify(education));
            data.push({name: 'education', value: JSON.stringify(education)});
            $.ajax({
                type: 'POST',
                url: url,
                data: data,
            }).done(function (resp) {
                $.pjax({
                    url: '/view/candidate/paper.html?full=1',
                    container: '#view',
                    fragment: '#view'
                });
            });
            return false;
        });
    }

    this.validate_resume = function () {
        $.getJSON(API_HOST + 'evaluate/paper/ref', function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                for (var i in data) {
                    var d = data[i];
                    if (d.code == 'toc' && d.type == 3) {
                        CV_FILE_NEED = true;
                    }
                }
                // if need cv file upload
                if (CV_FILE_NEED) {
                    $("#resume_form").removeClass('hide');
                    $("#files").on('change', function () {
                        var form = $('#resume_form');
                        var t = form.parsley();
                        if (!t.isValid()) {
                            toastr.warning('请上传10Mb以内的PDF简历文件');
                            return;
                        }
                        var url = API_HOST + 'user/resume';
                        var formData = new FormData(form[0]);
                        $.ajax({
                            type: 'POST',
                            url: url,
                            data: formData,
                            contentType: false,
                            processData: false
                        }).done(function (resp) {
                            var extend = resp.msg_extend;
                            $(".resume_div").fadeOut().remove();
                            var ele = $("#files");
                            for (var i in extend) {
                                var html = [];
                                var d = extend[i];
                                html.push('<div class="box p-a resume_div">');
                                html.push('<div class="pull-left m-r">');
                                html.push('<span class="w-48 rounded  accent">');
                                html.push('<i class="material-icons">assignment</i>');
                                html.push('</span>');
                                html.push('</div>');
                                html.push('<div class="clear">');
                                html.push('<h4 class="m-a-0 text-lg _300" id="my_cv_h4">');
                                html.push('<a href="' + API_HOST + 'user/resume/preview?access_token=' + USER_PROFILE.token + '" target="_blank">' + i + '</a>');
                                html.push('</h4>');
                                html.push('<small class="text-muted" id="size_span">大小：' + MyUtils.roundval(d.size / 1024 / 1024, 1) + ' Mb</small>');
                                html.push('</div>');
                                html.push('</div>');
                                $(html.join('')).insertBefore(ele);
                            }
                            CV_FILE_UPLOAD_FLAG = true;
                        });
                    });
                }
            }
        });

    }

    function fill_education(dom, data) {
        dom.find('label').text(data.degree);
        dom.find('input[name=school_extend]').val(data.school);
        dom.find('input[name=major_extend]').val(data.major);
    }

}


ExamPaper = function () {


    this.load_paper = function () {
        $.getJSON(API_HOST + 'user/base/profile', function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                var p = data.profile;
                var d = ['degree', 'education', 'name', 'gmt_birthday'];
                var f = false;
                for (var i in d) {
                    if (MyUtils.is_null(p[d[i]])) {
                        f = true;
                        break
                    }
                }
                if (f) {
                    toastr.info('请先完善个人基本信息');
                    $.pjax({
                        url: '/view/candidate/index.html?full=1',
                        container: '#view',
                        fragment: '#view'
                    });
                } else {
                    init_paper();
                }
            }
        });
    }

    function init_paper() {
        // get paper basic info
        $.getJSON(API_HOST + 'evaluate/paper/ref', function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                var ele = $("#paper_div");
                for (var i in data) {
                    var d = data[i];
                    var html = [];
                    html.push('<a href="' + d.uri + '&key=' + d.id + '"><div class="col-xs-12 col-sm-4">');
                    html.push('<div class="box p-a">');
                    html.push('<div class="pull-left m-r">');
                    html.push('<span class="w-48 rounded accent">');
                    html.push(d.style || '');
                    html.push('</span>');
                    html.push('</div>');
                    html.push('<div class="clear">');
                    html.push('<h4 class="m-a-0 text-lg _300">' + d.name + '</h4>');
                    html.push('<small class="text-muted">go</small>');
                    html.push('</div>');
                    html.push('</div>');
                    html.push('</div></a>');
                    ele.append(html.join(''));
                }
            }
        });
    }

}


/**
 *  邀请测评候选人
 * @constructor
 */
NewExamPerson = function () {

    var data_select = null;
    var data_table = null;

    this.init_table = function () {
        var url = API_HOST + "paper/user";
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
                    "data": "username", "name": "m.last_name",
                    "mRender": function (data, type, full) {
                        return full.last_name + full.first_name || data;
                    }
                },
                {
                    "data": "paper", "name": "paper", "orderable": false,
                    "mRender": function (data, type, full) {
                        var tag = [];
                        for (var i in data) {
                            tag.push(data[i].paper_name)
                        }
                        return '<small>' + tag.join(',') + '</small>';
                    }
                },
                {
                    "data": "status", "name": "up.status",
                    "mRender": function (data, type, full) {
                        if (data == 1) {
                            return '<span class="label green">已邀请</span>';
                        } else {
                            return '<span class="label red">禁用</span>';
                        }
                    }
                },
                {
                    "data": "last_login", "name": "last_login",
                    "mRender": function (data, type, full) {
                        if (data) {
                            return to_date('yyyy-MM-dd hh:mm:ss', data);
                        } else {
                            return '';
                        }
                    }
                },
            ],
            "fnServerParams": function (aoData) {
                parse_datatable_params(aoData);
            }
        });

        data_table.on('select', function (e, dt, type, index) {
            data_select = dt.data();
            data_select.name = data_select.last_name + data_select.first_name || data_select.username;
            toggle_btn(data_select);
            set_form('profile_form', data_select);
        });

        data_table.on('deselect', function (e, dt, type, index) {
            data_select = null;
            toggle_btn(null);
            set_form('profile_form', null);
        });

    }

    this.bind_event = function () {
        $("#form_name").on('change', function () {
            $.getJSON(API_HOST + 'common/pinyin?name=' + $(this).val(), function (resp) {
                if (resp.code == 0) {
                    var data = resp.data;
                    $("#form_username").val(data.pinyin.join(''))
                }
            });
        });
        $("#resend_btn").click(function () {
            var rows = data_table.rows({selected: true}).data();
            if (rows.length == 0) {
                toastr.warning("请选择有效的记录");
                return;
            }
            var ele = $("#invite_user_ul");
            ele.empty();
            for (var index = 0; index < rows.length; index++) {
                var d = rows[index];
                var html = [];
                html.push('<li class="list-item">');
                html.push('<a herf="javascript:void(0)" class="list-left">');
                html.push('<span class="w-40 circle warning avatar">');
                html.push('<span>' + d.username.substring(0, 1).toUpperCase() + '</span>');
                html.push('</span>');
                html.push('</a>');
                html.push('<div class="list-body">');
                html.push('<div><a href="javascript:void(0)">' + (d.last_name + d.first_name) || d.username + '</a></div>');
                html.push('<small class="text-muted text-ellipsis">' + d.username + '</small>');
                html.push('</div>');
                html.push('</div>');
                html.push('</li>');
                ele.append(html.join(''));
            }
            $("#resent_modal").modal('show');
        });
        $("#download_resume_btn").click(function () {
            console.log("开始下载简历");
            var rows = data_table.rows({selected: true}).data();
            if (rows.length == 0) {
                toastr.warning("请选择有效的记录");
                return;
            }
            var keys = [];
            for (var index = 0; index < rows.length; index++) {
                keys.push(rows[index].id);
            }
            URL = API_HOST + 'paper_ma/resume' + '?access_token=' + USER_PROFILE.token + '&user_ids=' + keys.join(',');
            window.open(URL);
        });
        $("#confirm_resent_btn").click(function () {
            var rows = data_table.rows({selected: true}).data();
            var keys = [];
            for (var index = 0; index < rows.length; index++) {
                keys.push(rows[index].id);
            }
            var paper = [];
            $.each($("input[type=checkbox][name=paper_chx]:checked"), function () {
                paper.push($(this).attr('value'));
            });
            var data = {user: keys.join(','), paper: paper.join(',')};
            $.post(API_HOST + 'paper/user/remail', data, function (resp) {
                data_table.ajax.reload();
                $("#resent_modal").modal('hide');
            });
        });

    }

    this.load_role = function () {
        $.getJSON(API_HOST + 'user/role?level=5', function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                var ele = $("#form_role");
                for (var i in data) {
                    var d = data[i];
                    ele.append('<option value="' + d.id + '">' + d.name + '</option>')
                }
            }
        });
    }

    this.validate_form = function (form_id) {
        var form = $('#' + form_id);
        form.parsley().on('form:submit', function () {
            var url = API_HOST + 'paper/user';
            var user_id = $("#submit_btn").attr('data-id');
            if (user_id != '') {
                url += '/' + user_id;
            }
            var data = form.serializeArray();
            var paper = $("#form_paper").val();
            if (null != paper && 'undefined' != typeof paper) {
                data.push({name: 'paper', value: paper.join(',')});
            }
            $.ajax({
                type: 'POST',
                url: url,
                data: data
            }).done(function (resp) {
                form[0].reset();
                $("#form_paper").empty().trigger('change');
                data_table.ajax.reload();
            });
            return false;
        });
    }

    this.init_paper = function (dom_id) {
        var ele = $("#" + dom_id);
        ele.select2({
            placeholder: '选择该用户的测试',
            theme: 'bootstrap',
            allowClear: true,
            minimumResultsForSearch: Infinity,
            ajax: {
                url: API_HOST + 'paper/type',
                processResults: function (resp) {
                    var res = [];
                    $.each(resp.data, function (k, v) {
                        res.push({id: v.id, text: v.name});
                    });
                    return {
                        results: res
                    };
                },
                cache: true
            }
        });
        var chx = $("#modal_chx_div");
        $.getJSON(API_HOST + 'paper/type', function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                $.each(data, function (k, v) {
                    // init checkbox
                    var html = [];
                    html.push('<label class="md-check p-l-md">');
                    html.push('<input type="checkbox" checked name="paper_chx" data-parsley-excluded=""');
                    html.push('value="' + v.id + '" data-parsley-multiple="paper_chx">');
                    html.push('<i class="indigo"></i>');
                    html.push(v.name);
                    html.push('</label>');
                    chx.append(html.join(''));
                });
            }
        });
    }

    this.import_user = function () {
        form = $("#import_data_form")[0];
        form.action = API_HOST + "paper/import" + "?access_token=" + USER_PROFILE.token;

        var options = {
            success: function (data, status, code) {
                toastr.success('数据已成功导入')
            },
            error: function (response) {
            },
        }
        $("#import_data_form").ajaxForm(options);
    }

    function toggle_btn(data) {
        var btn = $("#submit_btn");
        var input = $(".dy_input");
        if (null == data) {
            btn.text('邀请').attr('data-id', "");
            input.prop('disabled', false);
        } else {
            btn.text('修改').attr('data-id', data.id);
            input.prop('disabled', true);
        }
    }

    function set_form(form_id, data) {
        var select = $("#form_paper");
        if (null == data) {
            $("#" + form_id)[0].reset();
            select.empty().trigger('change');
            return;
        }
        var inputs = MyUtils.form_elements(form_id);
        MyUtils.fill_form(inputs, data);
        var paper = data.paper;
        if (null != paper && paper.length > 0) {
            $.each(paper, function (k, v) {
                select.append('<option selected value="' + v.paper_id + '">' + (v.paper_name) + '</option>');
            });
            select.trigger('change');
        } else {
            select.empty().trigger('change');
        }
    }

}
