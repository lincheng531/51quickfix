TodoAnalysis = function () {
  userlist = [];
  // API_HOST="http://172.16.59.189:8000/api/v1/";
  this.init = function () {
    user_list_vm = new Vue({
      el: '#todo_analysis_table',
      data: {
        'userlist': userlist,
      },
      methods: {
        delete_message: function(index, id) {
          console.log("index="+index);
          console.log("删除消息: " + id);
          $.ajax({
            url: API_HOST + "push/" + id,
            type: "DELETE",
            async: false,
            data: {
            },
          }).done(function (resp) {
            message_nav_vm['all'] -= 1;
            message_nav_vm[message_list_vm.messagelist[index].type] -= 1;
            message_list_vm.messagelist.splice(index, 1);
          });
        },
        accept_message: function(index, id) {
          console.log("接受任务")
          console.log("index="+index)
          $.ajax({
            url: API_HOST + "push/" + id,
            type: "PATCH",
            async: false,
            data: {
              "extra": JSON.stringify({"accepted":true}),
            },
          }).done(function (resp) {
            messagelist[index]["extra"]["accepted"] = true;
          });
        },
        deny_message: function(index, id) {
          console.log("拒绝任务")
          console.log("index="+index)
          $.ajax({
            url: API_HOST + "push/" + id,
            type: "PATCH",
            async: false,
            data: {
              "extra": JSON.stringify({"accepted":false}),
            },
          }).done(function (resp) {
            messagelist[index]["extra"]["accepted"] = false;
          });
        },
      }
    });
    console.log("进入分析todo使用率的页面，正在初始化页面...");
    console.log("发送请求获取 message ");
    $.ajax({
      url: API_HOST + "push/",
      type: "GET",
      async: false,
      data: {
      },
    }).done(function (resp) {
      if (resp.code == 0) {
        message_list_vm.messagelist = [];
        for ( var message of resp.data ) {
          message['extra'] = JSON.parse(message['extra']);
          message_list_vm.messagelist.push(message);
        };
        message_nav_vm['all'] = 0
        for ( var cnt of resp.count) {
          message_nav_vm[cnt['type']] = cnt['cnt'];
          message_nav_vm['all'] += cnt['cnt'];
        };
      }
    });
  };
};
