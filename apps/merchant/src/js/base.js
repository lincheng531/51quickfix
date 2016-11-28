/**
 * Created by ZoeAllen on 16/6/14.
 */

// set request header
$(document).ajaxSend(function (event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }

    var USER_PROFILE = JSON.parse(sessionStorage.getItem('user'));
    if (USER_PROFILE) {
        xhr.setRequestHeader("Authorization", 'Token ' + USER_PROFILE.token);
    }
});

$(document).ajaxComplete(function (event, request, settings) {
    var resp = request.responseJSON;
    if (typeof resp != 'undefined') {
        if (!resp.msg) {
            return;
        }
        var msg = resp.msg;
        if (resp.code == 0) {
            if (resp.status > 200) {
                var detail = resp.msg_extend || '';
                if (detail != '') {
                    toastr.success(detail, msg);
                } else {
                    toastr.success(msg);
                }
            }
        } else {
            if (status == 500) {
                toastr.error(msg);
            } else {
                var detail = [resp.msg_extend];
                for (var i in resp.data) {
                    detail.push(i + ' ' + resp.data[i]);
                }
                detail = detail.join('\n');
                toastr.warning(detail, msg);
            }
        }
    }
});


var DATATABLE_LANGUAGE = {
    "sProcessing": "处理中...",
    "sLengthMenu": "每页 _MENU_ ",
    "sZeroRecords": "没有匹配结果",
    "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
    "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
    "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
    "sInfoPostFix": "",
    "sSearch": "搜索:",
    "sUrl": "",
    "sEmptyTable": "没有对应记录",
    "sLoadingRecords": "载入中...",
    "sInfoThousands": ",",
    "oPaginate": {
        "sFirst": "首页",
        "sPrevious": "上一页",
        "sNext": "下一页",
        "sLast": "末页"
    },
    "oAria": {
        "sSortAscending": ": 以升序排列此列",
        "sSortDescending": ": 以降序排列此列"
    }
}

function parse_datatable_params(aoData) {
    if (aoData.columns != null && aoData.columns.length > 0) {
        var columns = aoData['columns'];
        aoData.columns = [];
        aoData.page = aoData['start'] / aoData['length'] + 1;
        aoData.size = aoData['length'];
        aoData.order_by = columns[aoData.order[0].column].name;
        aoData.order = aoData.order[0].dir;
        aoData.search = aoData['search'].value;
    } else {
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
    return aoData;
}

/**
 * @param  {string} format    格式
 * @param  {int}    timestamp 要格式化的时间 默认为当前时间
 * @return {string}           格式化的时间字符串
 */
function to_date(format, timestamp) {
    var date = timestamp ? new Date(timestamp * 1000) : new Date();
    var o = {
        "M+": date.getMonth() + 1, //month
        "d+": date.getDate(), //day
        "h+": date.getHours(), //hour
        "m+": date.getMinutes(), //minute
        "s+": date.getSeconds(), //second
        "q+": Math.floor((date.getMonth() + 3) / 3), //quarter
        "S": date.getMilliseconds() //millisecond
    }

    if (/(y+)/.test(format)) {
        format = format.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length));
    }

    for (var k in o) {
        if (new RegExp("(" + k + ")").test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length));
        }
    }
    return format;
}


function format_level(level, cls) {
    if ('undefined' == typeof cls || null == cls || '' == cls) {
        cls = '';
    }
    if (level == 1) {
        return '<span class="label ' + cls + '">最低</span>'
    } else if (level == 3) {
        return '<span class="label ' + cls + '">低</span>'
    } else if (level == 5) {
        return '<span class="label primary ' + cls + '">中</span>'
    } else if (level == 7) {
        return '<span class="label warning ' + cls + '">高</span>'
    } else if (level == 9) {
        return '<span class="label danger ' + cls + '">最高</span>'
    } else {
        return '<span class="label ' + cls + '">无</span>'
    }
}

(function ($) {
    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) {
            return decodeURI(r[2]);
        }
        return null;
    }

    $.getUrlParams = function () {
        var vars = [], hash;
        var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
        for (var i = 0; i < hashes.length; i++) {
            hash = hashes[i].split('=');
            vars[hash[0]] = hash[1];
        }
        return vars;
    }

    $.splitName = function (fullname) {
        var is_chinese = true;
        var pattern = /[\u4E00-\u9FA5]|[\uFE30-\uFFA0]/gi;
        if (!pattern.exec(fullname)) {
            is_chinese = false;
        }
        var lastname = '', firstname = '';
        if (is_chinese) {
            // split chinese name
            var hyphenated = ['欧阳', '太史', '端木', '上官', '司马', '东方', '独孤', '南宫', '万俟', '闻人', '夏侯', '诸葛', '尉迟', '公羊', '赫连', '澹台', '皇甫',
                '宗政', '濮阳', '公冶', '太叔', '申屠', '公孙', '慕容', '仲孙', '钟离', '长孙', '宇文', '城池', '司徒', '鲜于', '司空', '汝嫣', '闾丘', '子车', '亓官',
                '司寇', '巫马', '公西', '颛孙', '壤驷', '公良', '漆雕', '乐正', '宰父', '谷梁', '拓跋', '夹谷', '轩辕', '令狐', '段干', '百里', '呼延', '东郭', '南门',
                '羊舌', '微生', '公户', '公玉', '公仪', '梁丘', '公仲', '公上', '公门', '公山', '公坚', '左丘', '公伯', '西门', '公祖', '第五', '公乘', '贯丘', '公皙',
                '南荣', '东里', '东宫', '仲长', '子书', '子桑', '即墨', '达奚', '褚师'];
            var vLength = fullname.length;
            if (vLength > 2) {
                var preTwoWords = fullname.substr(0, 2);
                if ($.inArray(preTwoWords, hyphenated) > -1) {
                    lastname = preTwoWords;
                    firstname = fullname.substr(2);
                } else {
                    lastname = fullname.substr(0, 1);
                    firstname = fullname.substr(1);
                }
            } else if (vLength == 2) {
                lastname = fullname.substr(0, 1);
                firstname = fullname.substr(1);
            } else {
                lastname = fullname;
            }
        } else {
            var name = fullname.split(' ');
            lastname = name.pop();
            firstname = name.join(' ');
        }
        return [lastname, firstname];
    }

})(jQuery);

var MyUtils = {
    cutstr: function (str, len, default_str) {
        if (str == null) {
            return "";
        }
        if (default_str == null) {
            default_str = "...";
        }
        var str_length = 0;
        var str_len = str.length;
        var str_cut = new String();
        for (var i = 0; i < str_len; i++) {
            a = str.charAt(i);
            str_length++;
            if (escape(a).length > 4) {
                str_length++;
            }
            str_cut = str_cut.concat(a);
            if (str_length >= len) {
                str_cut = str_cut.concat(default_str);
                return str_cut;
            }
        }
        if (str_length < len) {
            return str;
        }
    },
    roundval: function (x, e) {
        var t = 1;
        //var e=1;
        for (; e > 0; t *= 10, e--);
        for (; e < 0; t /= 10, e++);
        return (Math.round(x * t) / t);
    },
    timestamp2date: function (nS) {
        if (nS == null) {
            return "";
        }
        return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日/g, " ");
    },
    ts2date: function (value) {
        if (!value) {
            return '';
        }
        //convert timestamp to date string
        var dateObj = new Date(parseInt(value) * 1000);
        return moment(dateObj).format('YYYY-MM-DD');
    },
    str2date: function (v) {
        return new Date(v).toLocaleString();
    },
    form_elements: function (form_id) {
        var eles = [];
        $.each($("#" + form_id + " input"), function () {
            var d = $(this);
            eles.push({id: d.attr('id'), name: d.attr('name'), type: d.attr('type')});
        });
        $.each($("#" + form_id + " select"), function () {
            var d = $(this);
            eles.push({id: d.attr('id'), name: d.attr('name'), type: 'select'});
        });
        $.each($("#" + form_id + " textarea"), function () {
            eles.push({id: $(this).attr('id'), name: $(this).attr('name')});
        });
        return eles;
    },
    fill_form: function (inputs, data) {
        $.each(inputs, function (k, v) {
            if (v['type'] == "radio") {
                $("#" + v['name'] + "_" + data[v['name']]).prop("checked", true);
            } else {
                $("#" + v['id']).val(data[v['name']]);
            }
        });
    },
    is_null: function (val) {
        if (typeof(val) != "undefined" && val != '' && val != null) {
            return false;
        }
        return true;
    },
    get_value: function (val, default_value) {
        if (typeof(val) != "undefined" && null != val) {
            return val;
        }
        return default_value;
    },
    highlight: function (id, words, class_name) {
        var pucl = $("#" + id);
        // if("" == keyword) return;
        var temp = pucl.html();
        var htmlReg = new RegExp("\<.*?\>", "i");
        var arrA = new Array();
        // 替换HTML标签
        for (var i = 0; true; i++) {
            var m = htmlReg.exec(temp);
            if (m) {
                arrA[i] = m;
            } else {
                break;
            }
            temp = temp.replace(m, "{[(" + i + ")]}");
        }
        if (class_name == null) {
            class_name = "#ec5956";
        }
        // words = unescape(keyword.replace(/\+/g, ' ')).split(/\s+/);
        // 替换关键字
        var size = words.length;
        for (w = 0; w < size; w++) {
            var r = new RegExp("(" + words[w].replace(/[(){}.+*?^$|\\\[\]]/g, "\\$&") + ")", "ig");
            temp = temp.replace(r, "<b style='color:" + class_name + "'>$1</b>");
        }
        // 恢复HTML标签
        for (var i = 0; i < arrA.length; i++) {
            temp = temp.replace("{[(" + i + ")]}", arrA[i]);
        }
        pucl.html(temp);
    },
    isIE: function (ver) {
        var b = document.createElement('ie')
        b.innerHTML = '<!--[if IE ' + ver + ']><i></i><![endif]-->';
        return b.getElementsByTagName('i').length === 1;
    },
    getIEVersion: function () {
        var sAgent = window.navigator.userAgent;
        var Idx = sAgent.indexOf("MSIE");
        // If IE, return version number.
        if (Idx > 0) {
            return parseInt(sAgent.substring(Idx + 5, sAgent.indexOf(".", Idx)));
        }
        // If IE 11 then look for "Trident" in user agent string.
        else if (!!navigator.userAgent.match(/trident/gi)) {
            return 11;
        }
        // If IE Edge then look for "Edge" in user agent string.
        else if (!!navigator.userAgent.match(/edge/gi)) {
            return 13;
        }
        else {
            return 0;
        }
    },
    getRandomVal: function (list) {
        if (null != list && list.length > 0) {
            return list[Math.floor(Math.random() * list.length)]
        }
        return null;
    },
    shuffle: function (list) {
        /**
         * shuffle a list
         */
        for (var j, x, i = list.length; i; j = parseInt(Math.random() * i), x = list[--i], list[i] = list[j], list[j] = x);
        return list;
    }
}
function getCookieValue(cookieName)  // get cookie value
{
    var cookieValue = document.cookie;
    var cookieStartAt = cookieValue.indexOf("" + cookieName + "=");
    if (cookieStartAt == -1) {
        cookieStartAt = cookieValue.indexOf(cookieName + "=");
    }
    if (cookieStartAt == -1) {
        cookieValue = null;
    }
    else {
        cookieStartAt = cookieValue.indexOf("=", cookieStartAt) + 1;
        cookieEndAt = cookieValue.indexOf(";", cookieStartAt);
        if (cookieEndAt == -1) {
            cookieEndAt = cookieValue.length;
        }
        cookieValue = unescape(cookieValue.substring(cookieStartAt, cookieEndAt));//解码latin-1
    }
    return cookieValue;
}

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}


function parse_uri(vals) {
    var uris = [];
    for (var i in vals) {
        uris.push(i + '=' + vals[i]);
    }
    return uris.join('&');
}


function on_avatar_error() {
    var USER_PROFILE = JSON.parse(sessionStorage.getItem('user'));
    var span = $("#avatar_span");
    span.html(get_user_random_avatar(USER_PROFILE.user));
}


function set_user_avatar() {
    var USER_PROFILE = JSON.parse(sessionStorage.getItem('user'));
    var span = $("#avatar_span");
    var color = window.app.random_color;
    if (span.length == 1 && span.children().length == 0) {
        var avatar = null;
        if (USER_PROFILE) {
            avatar = USER_PROFILE.user.profile.avatar;
        }
        if (null == avatar || avatar == '') {
            var html = get_user_random_avatar(USER_PROFILE.user, color);
        } else {
            var t = avatar.split('.')
            var src = t[0] + '_128x128.' + t[1];
            var html = '<span class="avatar w-32"><img src="' + IMAGE_URL + src + '" onerror="on_avatar_error()" alt="..."></span>';
        }
        span.html(html);
    }
}

function get_user_random_avatar(user, color, size) {
    if (!color) {
        color = MyUtils.getRandomVal(window.app.color_list);
    }
    if (!size) {
        size = 'w-32';
    }
    return '<span class="' + size + ' circle ' + color + ' avatar"><span>' + (user.username || user || '').substring(0, 1).toUpperCase() + '</span></span>';
}

module.exports = MyUtils;