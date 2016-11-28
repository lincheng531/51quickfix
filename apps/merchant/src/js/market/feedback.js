// Xiang Wang @ 2016-10-24 18:27:31


market_feedback = function () {
  var feedback_data = {
    feedbacks: [
    ],
    next: API_HOST + "manage/feedback",
  }
  var add_more = true;
  var scope = this;
  this.init = function() {
    var add_more = false  // 这个用来判定当前是否正在发送请求，避免多次重复触发瀑布流
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
      methods: {
        reply_feedback: function (index) {
          var scope = this;
          var feedback = this.feedbacks[index]
          var reply=feedback._reply;
          $.ajax({
            url: API_HOST + "manage/feedback/reply/" + feedback.id.toString(),
            type: "PATCH",
            data: { "reply": reply },
            success: function(response) {
              feedback.reply = reply;
              scope.feedbacks.$set(index, feedback);
            },
          });
        },
      }
    })
    this.add_more_feedback()
    setInterval(this.scroll_message, 100);
  };
  this.add_more_feedback = function(){
    add_more = false;
    $.ajax({
      type: "GET",
      url: feedback_data['next'],
      async: true,
      data: {
        "order": "desc",
        "size": 10,
      },
      success: function(responseTxt) {
        console.log(window.location.protocol)
        feedback_data['feedbacks'] = feedback_data['feedbacks'].concat(responseTxt['data'])
        if (responseTxt['next']) {
          if (responseTxt['next'].slice(0, 5) == 'https') {
            feedback_data['next'] = responseTxt['next']
          }
          else {
            feedback_data['next'] = responseTxt['next'].replace('http:', window.location.protocol)
          }
        }
        else {
          feedback_data['next'] = null
        }
        add_more = true;
      },
    })
  };
  this.scroll_message = function(){  // 如果页面处于低端，就继续发送请求或者反馈
    pos = window.innerHeight + document.scrollingElement.scrollTop
    if (pos + 1 >= document.scrollingElement.scrollHeight && add_more && feedback_data['next']) {
      add_more = false;
      scope.add_more_feedback();
    }
  }
}
