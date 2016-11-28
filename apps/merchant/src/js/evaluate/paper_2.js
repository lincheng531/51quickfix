/**
 * Created by ZoeAllen on 16/6/15.
 */


/**
 * 试卷2
 * @constructor
 */
Paper2 = function () {

    // parts array
    var part_index = 1;
    // switch time ms
    var switch_time = 1000;
    // 5min
    var part_timer = {};
    var part_timer_default = 60 * 1000 * 5;

    var timer_id = null;
    var paper_id = null;

    this.bind_paper = function () {
        $("#start_btn").on('click', function () {
            if (screenfull.enabled) {
                // screenfull.request();
                $("#main_content").remove();
                $("#part_1").fadeIn();
            }
        });
        // bind button
        $("#data_table").on('click', '.answer_btn', function () {
            // change style
            var btn = $(this);
            btn.siblings().prop('disabled', true).removeClass('answer_btn');
            btn.toggleClass('white info answer_btn');
            // check topics
            btn.parent().removeClass('b-a b-1x b-danger');
            var tr = btn.parent().parent().parent();
            tr.addClass('answered');
            if (tr.is($("#data_table tr").last())) {
                // console.log($("tr[class!='answered']"));
                $("tr[class!='answered']").find('div').addClass('b-a b-1x b-danger');
            }
            // submit answer
            submit_question(btn.text(), btn.parent().attr('data-id'));
        });
    }

    this.init_paper = function (key) {
        // get paper basic info
        $.getJSON(API_HOST + 'evaluate/paper/' + key, function (resp) {
            if (resp.code == 0) {
                var data = resp.data;
                paper_id = data.id;
                var status = data.status;
                $("#paper_title").text(data.name)
                if (status == 1) {
                    $("#paper_desc").fadeIn();
                    // init paper topic
                    $.post(API_HOST + 'top/init/' + key, function () {
                        load_question();
                    });
                } else if (status == 2) {
                    $("#paper_end").fadeIn();
                }
            }
        });
    }

    function load_question() {
        var tbody = $("#data_table tbody");
        tbody.fadeOut();
        $.getJSON(API_HOST + 'top/topic?paper=' + paper_id, function (resp) {
            tbody.empty();
            tbody.fadeIn();
            if (resp.code == 0) {
                var data = resp.data;
                if (null == data || data.length == 0) {
                    paper_end();
                    return;
                }
                for (var i in data) {
                    var d = data[i];
                    var html = [];
                    html.push('<tr>');
                    html.push('<td class="text">' + d.topic.question + '</td>');
                    html.push('<td colspan="2" class="text-center">');
                    html.push('<div class="btn-group" data-id="' + d.id + '">');
                    html.push('<button type="button" class="btn btn-sm white answer_btn">1</button>');
                    html.push('<button type="button" class="btn btn-sm white answer_btn">2</button>');
                    html.push('<button type="button" class="btn btn-sm white answer_btn">3</button>');
                    html.push('<button type="button" class="btn btn-sm white answer_btn">4</button>');
                    html.push('<button type="button" class="btn btn-sm white answer_btn">5</button>');
                    html.push('<button type="button" class="btn btn-sm white answer_btn">6</button>');
                    html.push('</div>');
                    html.push('</td>');
                    html.push('</tr>');
                    tbody.append(html.join(''));
                }
            }
            $("#page_div").text(resp.page + ' / ' + resp.total);
        });
    }


    function submit_question(answer, topic_id) {
        $.ajax({
            type: 'POST',
            url: API_HOST + 'top/topic/' + topic_id,
            data: {answer: answer}
        }).done(function (resp) {
            if (resp.code == 0) {
                // check current status
                if ($(".answer_btn").length == 0) {
                    load_question();
                }
            }
        });
    }

    function paper_end() {
        $("#part_1").fadeOut();
        $("#part_end").fadeIn();
        $.ajax({
            type: 'POST',
            url: API_HOST + 'top/' + paper_id,
        }).done(function () {
            $("#back_btn").on('click', function () {
                window.location.href = "/";
            });
        });
        return;
    }

    function clock() {
        window.clearInterval(timer_id);
        part_index++;
    }

    function set_timer() {
        timer_id = window.setInterval(function () {
            clock();
        }, MyUtils.get_value(part_timer[part_index + 1], part_timer_default));
    }

}