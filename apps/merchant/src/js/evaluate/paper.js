/**
 * Created by ZoeAllen on 16/6/15.
 */


/**
 * 试卷1
 * @constructor
 */
Paper = function () {
    // stop refresh
    window.onbeforeunload = function () {
        return "You work will be lost.";
    };
    var extend_flag = null;
    // parts array
    // var part = MyUtils.shuffle([1, 2, 3, 4, 5]);
    var part = [1, 2, 3, 4, 5];
    // set part6 to end
    part.push(6);
    var part_index = 0;
    var part_mapping = {
        1: '逻辑思维',
        2: '感知速度',
        3: '数字敏感',
        4: '语义理解',
        5: '空间想象',
    }
    // load question mapping
    var load_mapping = {
        1: load_question1,
        2: load_question2,
        3: load_question3,
        4: load_question4,
        5: load_question5,
    }

    // switch time ms
    var switch_time = 1000;
    // part time config
    var part_timer = {};
    var part_timer_default = 60 * 1000 * 2;

    var timer_id = null;
    // paper
    var paper_id = null;
    // current question
    var question = null;
    // 1:demo 0:real
    var demo_status = null;
    // correct count
    var demo_count = 0;
    var demo_correct_count = 3;
    var random_name = [['n1', 'n2'], ['n2', 'n1']];

    this.bind_paper = function () {
        $("#paper_desc").on('click', function () {
            $(this).hide();
            $("#paper_desc_2").fadeIn();
        });
        $("#start_btn").on('click', function () {
            if (screenfull.enabled) {
                $("#aside").addClass('hide');
                // $("#header_div").addClass('hide');
                $("#main_content").fadeOut().remove();
                // screenfull.request();
                start_part();
            }
        });
        bind_paper_show();
    }

    this.init_paper = function (key, flag) {
        // set global
        extend_flag = flag;
        // key is paper id
        // get paper basic info
        $.getJSON(API_HOST + 'evaluate/paper/' + key, function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                paper_id = data.id;
                var status = data.status;
                $("#paper_title").text(data.name)
                if (status == 1) {
                    $("#paper_desc").fadeIn();
                } else if (status == 2) {
                    $("#paper_end").fadeIn();
                } else if (status == 3) {
                    $("#main_content").fadeOut();
                    get_extend();
                }
            }
        });
        // load part timer config
        $.getJSON(API_HOST + 'evaluate/timer/' + key, function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                for (var i in data) {
                    part_timer[parseInt(data[i].part)] = data[i].timer * 60 * 1000;
                }
            }
        });

    }

    function start_part() {
        var index = part[part_index];
        $("#part_" + index).fadeIn();
        window.setTimeout(function () {
            $('#part' + index + '_title').remove();
            $('#part' + index + '_show_1').fadeIn();
        }, switch_time);
    }

    function load_question1() {
        var n = random_name[Math.floor(Math.random() * 2)];
        $.getJSON(API_HOST + 'toc/logic?paper=' + paper_id + '&demo=' + demo_status, function (resp) {
            toastr.clear();
            if (resp.code == 0) {
                var data = resp.data;
                question = data;
                question.msg_extend = resp.msg_extend;
                var html = [];
                html.push('<div class="part1_desc p-a center" style="width: 100%;">' + data.description.str + '</div>');
                html.push('<div style="display: none" id="part1_question_body">');
                html.push('<p class="m-b-lg">' + data.question + '?</p>');
                html.push('<button class="m-r btn btn-lg btn-outline b-black text-black _700 text-lg answer_btn">' + data.description.json[n[0]] + '</button>');
                html.push('<button class="m-l btn btn-lg btn-outline b-black text-black _700 text-lg answer_btn">' + data.description.json[n[1]] + '</button>');
                html.push('</div>');
                $("#part1_question").empty().append(html.join('')).fadeIn();
            }
        });
    }

    function load_question2() {
        $.getJSON(API_HOST + 'toc/chars?paper=' + paper_id + '&demo=' + demo_status, function (resp) {
            toastr.clear();
            if (resp.code == 0) {
                var data = resp.data;
                question = data;
                question.msg_extend = resp.msg_extend;
                var html = [];
                html.push('<div class="m-a">');
                html.push('<div class="m-b-md _500">');
                var c = data.description.c;
                for (var i in c) {
                    html.push('<div class="label-lte m-a p-a">' + i + '<br>' + c[i] + '</div>');
                }
                html.push('</div>');
                html.push('<div class="m-b">');
                var range = data.description.range;
                for (var i in range) {
                    html.push('<button class="btn md-btn md-flat m-b-sm w-xs answer_btn">' + i + '</button>');
                }
                html.push('</div>');
                html.push('</div>');
                $("#part2_question").empty().append(html.join('')).fadeIn();
            }
        });
    }

    function load_question3() {
        $.getJSON(API_HOST + 'toc/number?paper=' + paper_id + '&demo=' + demo_status, function (resp) {
            toastr.clear();
            if (resp.code == 0) {
                var data = resp.data;
                question = data;
                question.msg_extend = resp.msg_extend;
                var html = [];
                html.push('<div class="m-a">');
                html.push('<div class="m-b-lg _500">');
                var c = data.description.n;
                for (var i in c) {
                    html.push('<button class="btn md-btn md-flat m-b-sm w-xs answer_btn">' + c[i] + '</button>');
                }
                html.push('</div>');
                html.push('</div>');
                $("#part3_question").empty().append(html.join('')).fadeIn();
            }
        });
    }

    function load_question4() {
        $.getJSON(API_HOST + 'toc/words?paper=' + paper_id + '&demo=' + demo_status, function (resp) {
            toastr.clear();
            if (resp.code == 0) {
                var data = resp.data;
                question = data;
                question.msg_extend = resp.msg_extend;
                var html = [];
                html.push('<div class="col-sm-12 col-md-8 col-md-offset-2 col-lg-6 col-lg-offset-3">');
                html.push('<table class="table _700 text-left" style="font-size: 21px;">');
                html.push('');
                html.push('');
                var c = data.description;
                for (var i in c) {
                    html.push('<tr><td class="p-a-xs"><button class="btn md-btn md-flat w-40 answer_btn">' + i + '</button></td>');
                    $.each(c[i], function (k, v) {
                        html.push('<td>' + v + '</td>');
                    });

                    html.push('</tr>');
                }
                html.push('</table>');
                html.push('</div>');
                $("#part4_question").empty().append(html.join('')).fadeIn();
            }
        });
    }

    function load_question5() {
        $.getJSON(API_HOST + 'toc/space?paper=' + paper_id + '&demo=' + demo_status, function (resp) {
            toastr.clear();
            if (resp.code == 0) {
                var data = resp.data;
                question = data;
                question.msg_extend = resp.msg_extend;
                var html = [];
                var c = data.description;
                for (var i in c) {
                    html.push('<div class="label-lte m-a">');
                    $.each(c[i], function (k, v) {
                        html.push('<img src="' + v + '" class="r_img">');
                        html.push('<br>');
                    });
                    html.push('</div>');
                }
                html.push('<h1 class="m-b m-t">');
                html.push('<button class="btn md-btn md-flat m-b-sm w-xs answer_btn">0</button>');
                html.push('<button class="btn md-btn md-flat m-b-sm w-xs answer_btn">1</button>');
                html.push('<button class="btn md-btn md-flat m-b-sm w-xs answer_btn">2</button>');
                html.push('</h1>');
                $("#part5_question").empty().append(html.join('')).fadeIn();
            }
        });
    }

    function bind_paper_show() {
        var index = part[part_index];
        var title = part_mapping[part[part_index]];
        var load_func = load_mapping[part[part_index]];
        $("#part" + index + "_show_1").on('click', function () {
            $(this).hide();
            $("#paper_promotion").text(title + '-演示').fadeIn();
            $("#part" + index + "_demo").fadeIn();
        });

        $("#part" + index + "_show_2").on('click', function () {
            $(this).hide();
            demo_status = 1;
            try {
                load_func();
            } catch (err) {

            }
        });

        $("#part" + index + "_show_3").on('click', function () {
            $(this).hide();
            demo_status = 0;
            // start real timer for partX
            toastr.clear();
            set_timer();
            try {
                load_func();
            } catch (err) {

            }
        });

        $("#part" + index + "_demo").on('click', '.demo_div', function () {
            var div = $(this);
            $(div.hide().next()[0]).fadeIn();
        });

        $("#part" + index + "_demo").on('click', '.btn', function () {
            if ($(this).attr('data-next')) {
                $("#part" + index + "_demo").hide();
                $("#paper_promotion").text(title + '-模拟').fadeIn();
                $("#part" + index + "_show_2").fadeIn();
            }
        });

        $("#part" + index + "_question").on('click', '.part1_desc', function () {
            $(this).hide();
            $("#part" + index + "_question_body").fadeIn();
        });

        $("#part" + index + "_question").on('click', '.answer_btn', function () {
            var btn = $(this);
            btn.removeClass('answer_btn').prop('disabled', true);
            var answer = btn.text();
            if (null != demo_status && demo_status == 1) {
                // demo
                if (check_answer(answer)) {
                    demo_count++;
                }
                if (demo_count >= demo_correct_count) {
                    // end demo status
                    $("#part" + index + "_question").hide();
                    $("#part" + index + "_show_3").fadeIn();
                    $("#paper_promotion").text(title + '-正式').fadeIn();
                    question = null;
                    demo_status = 0;
                } else {
                    try {
                        load_func();
                    } catch (err) {

                    }
                }
            } else {
                // real
                submit_question(answer, index)
            }
        });
    }

    function check_answer(answer) {
        if (answer.toString() == question.msg_extend.toString()) {
            toastr.success('恭喜，答对了！');
            return true;
        }
        toastr.warning('抱歉，答错了！');
        return false;
    }

    function submit_question(answer, index) {
        var load_func = load_mapping[index];
        $.ajax({
            type: 'POST',
            async: false,
            url: API_HOST + 'toc/topic/' + question.id,
            data: {answer: answer},
            error: function () {
                question = null;
                load_func();
            }
        }).done(function (resp) {
            try {
                load_func();
            } catch (err) {
                question = null;
            }
        });
    }

    function next_part() {
        try {
            $("#paper_promotion").fadeOut();
            $("#part_" + part[part_index - 1]).remove();
            $("#part_" + part[part_index]).fadeIn();
            if (part_index >= (part.length - 1)) {
                $.ajax({
                    type: 'POST',
                    url: API_HOST + 'toc/' + paper_id,
                }).done(function (resp) {
                    // set button
                    if (extend_flag) {
                        var flag = false;
                        if (resp.code == 0) {
                            var data = resp.data;
                            var extend = data.extend;
                            flag = data.extend_flag;
                            function sortNumber(a, b) {
                                return a - b
                            }

                            var rank = [];
                            var tmp = {};
                            for (var i in extend) {
                                var d = extend[i];
                                d.part = i;
                                rank.push(d.rank);
                                tmp[d.rank] = d;
                            }
                            rank = rank.sort(sortNumber);
                            if (rank.length > 0) {
                                data.part1 = part_mapping[parseInt(tmp[rank[rank.length - 1]].part)];
                                data.part2 = part_mapping[parseInt(tmp[rank[0]].part)];
                                $.each($(".auto_fill"), function () {
                                    var s = $(this);
                                    s.text(data[s.attr('data-id')]);
                                });
                            }
                        }
                        var btn = $("#back_btn");
                        // if pass
                        if (flag) {
                            $(".go-next").removeClass('hide');
                            btn.text('通关密码');
                            btn.on('click', function () {
                                get_extend();
                            });
                        } else {
                            $(".no-pass").removeClass('hide');
                            btn.text('返回');
                            btn.on('click', function () {
                                window.location.href = "/view/candidate/paper.html";
                            });
                        }
                        btn.removeClass('hide');
                    } else {
                        $("#back_btn").on('click', function () {
                            window.location.href = "/view/candidate/paper.html";
                        });
                    }
                });
                return;
            }
            demo_count = 0;
            bind_paper_show();
            start_part();
        } catch (err) {
        }
    }

    function clock() {
        window.clearInterval(timer_id);
        part_index++;
        next_part();
    }

    function set_timer() {
        // console.log(part_timer[part_index + 1]);
        timer_id = window.setInterval(function () {
            clock();
        }, MyUtils.get_value(part_timer[part_index + 1], part_timer_default));
    }

    function bind_extend() {
        $("#extend_ul select.select_textarea").on('change', function () {
            var dom = $(this);
            var text = dom.siblings('textarea');
            text.attr('placeholder', dom.val());
            text.focus();
        });
    }

    function get_extend() {
        $.ajax({
            type: 'GET',
            url: API_HOST + 'toc/extend?paper=' + paper_id,
            statusCode: {
                400: function (resp) {
                    $.pjax({
                        url: '/view/candidate/paper.html',
                        container: '#view',
                        fragment: '#view'
                    });
                }
            }
        }).done(function (resp) {
            set_extend(resp.data);
            $("#part_6").fadeOut();
            $("#part_extend").fadeIn();
            $('#timer').startTimer({
                onComplete: function (element) {
                    element.addClass('is-complete');
                    submit_extend();
                }
            });
            $("#timer_div").removeClass('hide');
        });
    }

    function set_extend(data) {
        var extend_mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D'};
        var ul = $("#extend_ul");
        for (var i in data) {
            var d = data[i];
            var index = parseInt(i) + 1;
            var html = [];
            var type = d.topic.description.type;
            html.push('<li class="list-item">');
            html.push('<div class="list-body" id="radio_div_' + index + '">');
            html.push('<div class="text p-b-xs">' + index + '. ' + d.topic.description.desc + '</div>');
            var option = d.topic.description.option;
            if (type == 'radio') {
                if (option && option.length > 0) {
                    $.each(option, function (k, v) {
                        html.push('<div class="p-t-xs">');
                        html.push('<label class="md-check p-r-lg">');
                        html.push('<input type="radio" value="' + extend_mapping[k] + '" name="radio_' + d['id'] + '">');
                        html.push('<i class="blue"></i>');
                        html.push(extend_mapping[k] + '. ' + v);
                        html.push('</label>');
                        html.push('</div>');
                    });
                }
            } else if (type == "select_text") {
                html.push('<div class="text p-t-xs">');
                html.push('<select class="form-control c-select select_textarea" name="select_' + d['id'] + '" required>');
                if (option && option.length > 0) {
                    $.each(option, function (k, v) {
                        html.push('<option value="' + v + '">' + v + '</option>');
                    });
                }
                html.push('</select>');
                html.push('<textarea name="textarea_' + d['id'] + '" class="form-control m-t-sm select_textarea" required  maxlength="5120" placeholder="高考之前需要学习12年，你觉得是不是太长了？" rows="10"></textarea>');
                html.push('</div>');
            }
            html.push('</div>');
            html.push('</div>');
            html.push('</li>');
            ul.append(html.join(''));
        }
        bind_extend();
        var form = $('#extend_form');
        form.parsley().on('form:submit', function () {
            $("#confirm_modal").modal('show');
            return false;
        });

        $("#confirm_btn").on('click', function () {
            $("#confirm_modal").modal('hide');
            submit_extend();
        });
    }

    function submit_extend() {
        $("#submit_btn").prop('disabled', true);
        $("#timer_div").hide();
        var form = $('#extend_form');
        var data = form.serializeArray();
        var answer = {};
        for (var i in data) {
            var d = data[i];
            var name = d.name;
            name = name.split('_')[1];
            var t = answer[name] || [];
            t.push(d.value);
            answer[name] = t;
        }
        $.ajax({
            type: 'POST',
            url: API_HOST + 'toc/extend',
            data: {answer: JSON.stringify(answer), paper: paper_id},
        }).done(function (resp) {
            $("#submit_btn").prop('disabled', false);
            $("#part_extend").fadeOut();
            $("#part_finally").fadeIn();
        });
    }

}