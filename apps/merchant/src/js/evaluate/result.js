/**
 * Created by ZoeAllen on 16/7/13.
 */

/**
 * 测试结果管理
 * @constructor
 */
ManageExamResult = function () {

    var data_table = null;
    var data_select = null;

    var flag = $.getUrlParam('flag');
    var access = $.getUrlParam('access');

    this.init_table = function () {
        $.getJSON(API_HOST + 'paper/type', function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                var ele = $("#form_paper");
                for (var k in data) {
                    var d = data[k];
                    ele.append('<option data-type="' + d.type + '" value="' + d.id + '">' + d.name + '</option>');
                }
            }
            if (null != flag && flag == '1') {
                set_filter_div();
            } else {
                init_table();
            }
        });
    }
    this.bindCallBack = function () {
        $("#excel_id").click(function () {
            var rows = data_table.rows({selected: true});
            var data_list = rows.data();
            var user_id_array = new Array();
            if (data_list.length < 1) {
                toastr.warning('请选择项目');
                return;
            }
            var type = {};
            for (var i = 0; i < data_list.length; i++) {
                var d = data_list[i];
                user_id_array.push(d.user_id);
                type[d.paper_type] = null;
            }
            var paper_type = [];
            for (var i in type) {
                paper_type.push(i)
            }
            if (paper_type.length != 1) {
                toastr.warning('请选择同一个类型的测试');
                return;
            }
            var user_id_array_to_string = user_id_array.toString();
            var url = API_HOST + "paper/export/excel?access_token=" + USER_PROFILE.token + "&user_id=" + user_id_array_to_string + "&type=" + paper_type[0];
            $("#excel_id").attr('href', url);
        })
        $("#resume_id").click(function () {
            var rows = data_table.rows({selected: true});
            var data_list = rows.data();
            var user_id_array = new Array();
            if (data_list.length < 1) {
                toastr.warning('请选择项目');
                return;
            }
            for (var i = 0; i < data_list.length; i++) {
                var d = data_list[i];
                user_id_array.push(d.user_id);
            }
            var user_id_array_to_string = user_id_array.toString();
            var url = API_HOST + 'paper_ma/resume' + '?access_token=' + USER_PROFILE.token + "&user_ids=" + user_id_array_to_string;
            // window.open(URL);
            $("#resume_id").attr('href', url);
        })
    }
    this.bind_btn = function () {
        $("#data_table").on('click', '.reset_btn', function () {
            $("#confirm_modal").modal('show');
            var row = data_table.row($(this).parent().parent(), {page: 'current'});
            row.select();
            data_select = row.data()
        });

        $("#confirm_btn").on('click', function () {
            // clean code == toc
            var url = API_HOST + 'paper/' + data_select.paper_code + '/reset/' + data_select.id;
            $.ajax({
                type: 'DELETE',
                url: url
            }).done(function (resp) {
                $("#confirm_modal").modal('hide');
                if (resp.code == 0) {
                    data_table.ajax.reload();
                }
            });
        });

    }

    /**
     * if flag==1 and user has paper_ma permission
     */
    function set_filter_div() {
        var div = $("#filter_div");
        $.getJSON(API_HOST + 'paper_ma/user/leader', function (resp) {
            var html = [];
            html.push('<label class="p-l-sm">邀请人：</label>');
            html.push('<select class="c-select" style="margin-top: -5px;" id="form_owner">');
            html.push('<option value="" selected>全部</option>');
            if (resp.code == 0) {
                var data = resp.data;
                if (data && data.length > 0) {
                    $.each(data, function (k, v) {
                        html.push('<option value="' + v.id + '">' + (v.last_name + v.first_name) || v.username + '</option>');
                    });
                }
            }
            html.push('</select>');
            div.append(html.join(''));
            // bind select change filter event
            $("#form_owner").on('change', function () {
                if (data_table) {
                    data_table.ajax.reload();
                }
            });
            var owner = $.getUrlParam('owner');
            if (owner) {
                $("#form_owner").val(owner);
            }
            init_table();
        });
    }

    function init_table() {
        var url = API_HOST + "paper/result";
        if (null != flag && flag == '1') {
            if (null != access && access == '1') {
                url = API_HOST + "paper_super/result";
            } else {
                url = API_HOST + "paper_ma/result";
            }
        }
        var size = $.getUrlParam('size') || 10;
        var page = parseInt($.getUrlParam('page') || 1);
        var status = $.getUrlParam('status');
        var paper = $.getUrlParam('paper');
        if (paper) {
            $("#form_paper").val(paper);
        }
        if (status) {
            $("#status_select").val(status);
        }
        data_table = $('#data_table').DataTable({
            'language': DATATABLE_LANGUAGE,
            "processing": true,
            "paging": true,
            "pageLength": size,
            "displayStart": (page - 1) * size,
            "searching": true,
            "ordering": true,
            "info": true,
            "autoWidth": true,
            "serverSide": true,
            "responsive": true,
            "select": {
                style: 'os'
            },
            "order": [[5, 'desc']],
            "sAjaxSource": url,
            "columns": [
                {
                    "data": "user", "name": "u.first_name",
                    "mRender": function (data, type, full) {
                        if (full.status == 2 || full.status == 2) {
                            var uri = parse_uri({
                                size: size,
                                page: data_table.page() + 1,
                                status: $("#status_select").val(),
                                paper: $("#form_paper").val(),
                                owner: $("#form_owner").val(),
                                flag: flag,
                                access: access,
                            });
                            return '<a class="text-primary dk" data-pjax href="/view/exam/detail_' + full.paper_type + '.html?key=' + full.id + '&' + uri + '">' + MyUtils.cutstr(full.last_name + full.first_name || full.username, 12) + '</a>';
                        } else {
                            return '<a class="text-primary dk" href="javascript:void(0)">' + MyUtils.cutstr(full.last_name + full.first_name || data, 12) + '</a>';
                        }
                    }
                },
                {
                    "data": "name", "name": "name",
                    "mRender": function (data, type, full) {
                        if (full.status == 2 || full.status == 3) {
                            var uri = parse_uri({
                                size: size,
                                page: data_table.page() + 1,
                                status: $("#status_select").val(),
                                paper: $("#form_paper").val(),
                                owner: $("#form_owner").val(),
                                flag: flag,
                                access: access,
                            });
                            return '<a class="text-primary dk" data-pjax href="/view/exam/detail_' + full.paper_type + '.html?key=' + full.id + '&' + uri + '">' + data + '</a>';
                        } else {
                            return '<a class="text-primary dk" href="javascript:void(0)">' + data + '</a>';
                        }
                    }
                },
                {
                    "data": "status", "name": "status",
                    "mRender": function (data, type, full) {
                        if (data == 2) {
                            return '<span class="label green">已完成</span>';
                        } else if (data == 3) {
                            return '<span class="label green">通关中</span>';
                        } else {
                            return '<span class="label">进行中</span>';
                        }
                    }
                },
                {
                    "data": "score", "name": "score"
                },
                {
                    "data": "cost_time", "name": "cost_time",
                    "mRender": function (data, type, full) {
                        return MyUtils.roundval(data / 60, 0);
                    }
                },
                {
                    "data": "start_time", "name": "start_time",
                    "mRender": function (data, type, full) {
                        return to_date('yyyy-MM-dd hh:mm:ss', data);
                    }
                },
                {
                    "data": "end_time", "name": "end_time",
                    "mRender": function (data, type, full) {
                        if (data) {
                            return to_date('yyyy-MM-dd hh:mm:ss', data);
                        } else {
                            return '';
                        }
                    }
                },
                {
                    "data": "id", "name": "id", "orderable": false,
                    "mRender": function (data, type, full) {
                        var btn = [];
                        if (full.status == 2) {
                            var uri = parse_uri({
                                size: size,
                                page: data_table.page() + 1,
                                status: $("#status_select").val(),
                                paper: $("#form_paper").val(),
                                owner: $("#form_owner").val(),
                                flag: flag,
                                access: access,
                            });
                            btn.push('<a class="btn btn-xs btn-icon btn-default" data-pjax href="/view/exam/detail_' + full.type + '.html?key=' + data + '&' + uri + '"><i class="fa fa-file-text-o"></i></a>');
                        } else {
                            btn.push('<button class="btn btn-xs btn-icon btn-default" disabled><i class="fa fa-file-text-o"></i></button>');
                        }
                        btn.push('<button class="btn btn-xs btn-icon btn-danger m-l-xs reset_btn"><i class="fa fa-trash"></i></button>');
                        return btn.join('');
                    }
                },
            ],
            "fnServerParams": function (aoData) {
                parse_datatable_params(aoData);
                aoData.push({"name": "status", "value": $("#status_select").val()});
                aoData.push({"name": "paper", "value": $("#form_paper").val()});
                aoData.push({"name": "owner", "value": $("#form_owner").val()});
            }
        });

        $("#status_select").on('change', function () {
            if (data_table) {
                data_table.ajax.reload();
            }
        });

        $("#form_paper").on('change', function () {
            if (data_table) {
                data_table.ajax.reload();
            }
        });

        data_table.on('select', function (e, dt, type, index) {
            data_select = dt.data();
        });

        data_table.on('deselect', function (e, dt, type, index) {
            data_select = null;
        });
    }
}

/**
 * 测试结果详情
 * @constructor
 */
ManageExamDetail = function () {

    var paper_id = null;

    this.bind_btn = function () {
        $(".print_btn").on('click', function () {
            print_pdf();
        });
        $(".switch_btn").on('click', function () {
            $("#charts_div").toggleClass('hide');
            $("#table_div").toggleClass('hide');
        });
        $(".reset_btn").on('click', function () {
            $("#confirm_modal").modal('show');
        });
        $("#confirm_btn").on('click', function () {
            // clean code == toc
            var url = API_HOST + 'paper/toc/extend/reset/' + paper_id;
            $.ajax({
                type: 'DELETE',
                url: url
            }).done(function (resp) {
                $("#confirm_modal").modal('hide');
            });
        });
    }

    this.load_detail_1 = function (item_id) {
        // load toc paper only
        // TODO: for tmp user only
        $.ajax({
            type: 'GET',
            url: API_HOST + 'paper/toc/' + item_id,
        }).done(function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                paper_id = data.id;
                if (data.status == 3) {
                    $(".reset_btn").removeClass('hide');
                }
                fill_basic(data);
                fill_chart_1(data.extend);
                fill_detail_1(data.extend);
            }
        });
    }

    this.load_detail_2 = function (item_id) {
        // load toc paper only
        // TODO: for tmp user only
        $.ajax({
            type: 'GET',
            url: API_HOST + 'paper/top/' + item_id,
        }).done(function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                fill_basic(data);
                fill_detail_2(data.extend);
            }
        });
    }

    function fill_basic(data) {
        var nickname = data.user.last_name + data.user.first_name;
        data.nickname = nickname || data.user.username;
        data.start_time = to_date('yyyy-MM-dd hh:mm:ss', data.start_time);
        data.end_time = to_date('yyyy-MM-dd hh:mm:ss', data.end_time);
        $.each($("#paper_box .auto_fill"), function () {
            var e = $(this);
            e.text(data[e.attr('data-id')])
        });
        var toc_extend = data.toc_extend;
        if (toc_extend) {
            $("#toc_extend_div").removeClass('hide');
            $("#ratio_a").html(MyUtils.roundval(toc_extend.right / toc_extend.total, 2) * 100 + '<span class="text-sm">%</span>')
            $("#ratio_detail").html('答对数：' + toc_extend.right);
            var topic = toc_extend.topic;
            if (topic && topic.length > 0) {
                var ul = $("#topic_ul");
                $.each(topic, function (k, v) {
                    var html = [];
                    html.push('<li class="list-item">');
                    html.push('<div class="clear">');
                    html.push('<h5 class="m-a-0 m-b-sm"><a>' + v.topic + '</a></h5>');
                    html.push('<p class="text">' + v.answer + '</p>');
                    html.push('</p>');
                    html.push('</div>');
                    html.push('</li>');
                    ul.append(html.join(''));
                });
            }
        }
    }

    function fill_chart_1(data) {
        var d = [];
        var indicator = [];
        for (var n in data) {
            $.each(data[n], function (k, v) {
                d.push(v.rank);
                indicator.push({name: k, max: 100});
            });
        }
        var myChart = echarts.init(document.getElementById('chart_div'));
        // 指定图表的配置项和数据
        var option = {
            tooltip: {},
            radar: {
                // shape: 'circle',
                indicator: indicator
            },
            series: [{
                type: 'radar',
                data: [
                    {
                        value: d,
                        name: '百分位'
                    },
                ]
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    }

    function fill_detail_1(data) {
        var tbody = $("#data_table tbody");
        if (null == data || data.length == 0) {
            return;
        }
        $.each(data, function (i, v) {
            var html = [];
            for (var k in v) {
                var d = v[k];
                html.push('<tr>');
                html.push('<td>' + k + '</td>');
                html.push('<td>' + MyUtils.get_value(d.rank, 0) + '</td>');
                html.push('<td>' + MyUtils.get_value(d.total, 0) + '</td>');
                html.push('<td>' + MyUtils.get_value(d.correct, 0) + '</td>');
                html.push('<td>' + MyUtils.get_value(d.wrong, 0) + '</td>');
                html.push('<td>' + MyUtils.get_value(d.score, 0) + '</td>');
                html.push('</tr>');
            }
            tbody.append(html.join(''));
        });
        init_table();
    }

    function fill_detail_2(data) {
        var tbody = $("#data_table tbody");
        if (null == data || data.length == 0) {
            return;
        }
        var index = 0;
        var charts_div = $("#charts_div");
        $.each(data, function (c, r) {
            var html = [];
            var yAxis = [];
            var series = [];
            for (var s in r) {
                var d = r[s];
                html.push('<tr>');
                html.push('<td>' + c + '</td>');
                html.push('<td>' + s + '</td>');
                html.push('<td>' + MyUtils.get_value(d.total, 0) + '</td>');
                html.push('<td>' + MyUtils.get_value(d.correct, 0) + '</td>');
                html.push('<td>' + MyUtils.get_value(d.wrong, 0) + '</td>');
                html.push('<td>' + MyUtils.get_value(d.score, 0) + '</td>');
                html.push('</tr>');
                yAxis.push(s);
                series.push(d.score);
            }
            // fill chart
            index++;
            init_chart(index, c, yAxis, series, charts_div);
            // fill table
            tbody.append(html.join(''));
        });
        init_table();
    }

    function init_chart(index, c, yAxis, series, charts_div) {
        var chart_id = 'chart_' + index;
        charts_div.append(create_chart_div(chart_id));
        var myChart = echarts.init(document.getElementById(chart_id));
        // 指定图表的配置项和数据
        var option = {
            title: {
                text: c,
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            grid: {
                left: 'center'
            },
            xAxis: {
                type: 'value',
                boundaryGap: [0, 0.01],
                max: 5
            },
            yAxis: {
                type: 'category',
                data: yAxis,
                axisTick: {
                    show: false
                }
            },
            series: [
                {
                    type: 'bar',
                    barWidth: 10,
                    data: series
                }
            ],
            color: ['#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074', '#546570', '#c4ccd3']
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    }

    function init_table() {
        $("#data_table").DataTable({
            paging: false,
            searching: false,
            info: false,
            autoWidth: false,
            responsive: true,
            order: []
        });
    }

    function print_pdf() {
        var btn = $(".print_header");
        btn.hide();
        window.print();
        btn.show();
    }

    function create_chart_div(dom_id) {
        return '<div id="' + dom_id + '" class="col-sm-12 col-md-6 col-lg-6" style="min-height:200px;"></div>';
    }

}


/**
 * 测试结果分析
 * @constructor
 */
AnalyseExamWord = function () {

    var data_table = null;

    this.init_table = function () {
        init_table();
    }

    function init_table() {
        data_table = $('#data_table').DataTable({
            'language': DATATABLE_LANGUAGE,
            "paging": true,
            "pageLength": 100,
            "searching": true,
            "ordering": true,
            "info": false,
            "autoWidth": true,
            "responsive": true,
            "order": [[5, "desc"]],
            "ajax": {
                "url": API_HOST + "paper_ma/analyse/word",
                "dataSrc": "data"
            },
            "columns": [
                {
                    "data": "word", "name": "word",
                    'mRender': function (data, type, full) {
                        return data[0];
                    }
                },
                {
                    "data": "word", "name": "word",
                    'mRender': function (data, type, full) {
                        return data[1];
                    }
                },
                {
                    "data": "word", "name": "word",
                    'mRender': function (data, type, full) {
                        return data[2];
                    }
                },
                {
                    "data": "total", "name": "total"
                },
                {
                    "data": "correct", "name": "correct"
                },
                {
                    "data": "ratio", "name": "ratio",
                    "mRender": function (data, type, full) {
                        return MyUtils.roundval(data * 100, 2) + '%';
                    }
                },
            ],
        });

    }
}
