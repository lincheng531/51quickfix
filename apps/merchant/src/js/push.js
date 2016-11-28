$(function () {
    var pushMessage = function () {
        var SCHEMA = WSS_SCHEMA;
        var HOST = WSS_HOST;
        var PORT = WSS_PORT;

        if (!window.WebSocket) {
            toastr.error('该浏览器不支持推送');
        }

        var reconnect = function (ws) {
            ws = null;
            setTimeout(function () {
                if (!ws) {
                    console.log('ws reconnect...')
                    ws = connect();
                }
            }, 10000);
        };

        var connect = function () {
            var ws = new WebSocket(SCHEMA + HOST + ':' + PORT + '/pushserver?user=' + USER_PROFILE.user.id);
            ws.onopen = function (e) {
                console.log('ws connected...');
            };

            ws.onmessage = function (e) {
                var data = e.data;

                if (data != 'success') {

                    data = JSON.parse(data);
                    if (!MyUtils.get_value(data.is_push_msg, true)) {
                        if (data.type == 'sync' && data.channel == 'process') {
                            var dom_ele = $("#process_div");
                            if (dom_ele) {
                                var percent = MyUtils.get_value(data.data, {}).percent;
                                percent = parseFloat(percent) * 100;
                                dom_ele.find('div.primary').attr('style', 'width: ' + percent + '%').text(percent + '%');
                            }
                        }
                        return;
                    }
                    var messager = new ManageMessage();
                    messager.getUnreadCount();

                    toastr.info('亲, 有新消息来了');
                    $('#bell').addClass('bell-shake');
                    console.log(data.id);
                }
            };

            ws.onclose = function () {
                console.log('ws closed...')
                reconnect(ws);
            };

            ws.onerror = function () {
                console.log('ws error occurred...');
            };

            return ws;
        };

        connect();
    };

    if (WSS_ON) {
        pushMessage();
    }
});