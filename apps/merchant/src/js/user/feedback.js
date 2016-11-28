// Xiang Wang @ 2016-10-24 17:32:46


MyFeedback = function() {
  var feedback_data = {
    feedbacks: [
    ],
    next: API_HOST + "user/feedback",
  }
  this.init = function() {
    submit_feedback_btn = document.getElementById('submit_feedback')
    submit_feedback_btn.onclick = this.submit_feedback
    // 反馈列表加载: 开始
      add_more = false  // 这个用来判定当前是否正在发送请求，避免多次重复触发瀑布流
      Vue.filter('timestamptodatetime', function (value) {
          if (typeof(value) == 'string') {
              value = parseInt(value);
          }
          if (value < 2073753874) {
              value = 1000 * value;
          }
          var date = new Date(value);
          return date.toLocaleDateString();
      });
      var vm = new Vue({
        el: "#feedback_ul",
        data: feedback_data,
      })
      document.getElementById("more_feedback").onclick=this.add_more_feedback;
      // 初始化页面
      this.add_more_feedback()
    // 反馈列表加载: 结束
  }
  this.scroll_message = function (){  // 如果页面处于低端，就继续发送请求或者反馈
    pos = window.innerHeight + document.scrollingElement.scrollTop
    if (pos + 1 >= document.scrollingElement.scrollHeight && add_more && feedback_data['next']) {
      add_more = false;
      this.add_more_feedback();
    }
  }
  this.add_more_feedback = function(){
    $.ajax({
      type: "GET",
      url: feedback_data['next'],
      async: true,
      data: {
        "size": 5,
        "order": "desc",
      },
      success: function(responseTxt) {
        feedback_data['feedbacks'] = feedback_data['feedbacks'].concat(responseTxt['data'])
        feedback_data['next'] = responseTxt['next']
        add_more = true;
        // setInterval(scroll_message, 100);  // 页面在里面了，用瀑布流改成点击加载
      },
    })
  }
  this.submit_feedback = function () {
    data = $("#feedback_form").serializeArray();
    if (!(data[0]["value"] && data[1]["value"])) {
      toastr.warning("请填充完整")
      return false
    }else{
      // changeBy xjx 2016年10月25日16:09:49     提交后删除文本内容
      $("#feedback_form")[0].reset();
    }
    
    $.ajax({
      url: API_HOST + "user/feedback",
      type: "POST",
      async: true,
      data: data,
      success: function(responseTxt){
        $("#myModal").modal("show");
        feedback_data['feedbacks'] = feedback_data['feedbacks'].concat([responseTxt['data'],])
      },
    });


  }
}
