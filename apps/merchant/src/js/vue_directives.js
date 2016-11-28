// Xiang Wang @ 2016-09-30 13:48:04

Vue.directive('avatar', {
    bind: function () {
        // console.log("绑定了avatar指令");
    },
    update: function (user) {
        if (user) {
            var userAvatar = user.avatar || (user.profile && user.profile.avatar);
            if (userAvatar) {
                // TODO 现在用固定图片，之后改成动态的。
                // this.el.innerHTML = '<span class="w-40 circle warning avatar"><img src=' + 'http://img.allen.xin/avatar/20160908/61a469f2a29052f4181a6d05e00f91cd_128x128.jpg' + ' alt="..."></span>';
                this.el.innerHTML = '<span class="w-40 circle avatar"><img src=' + IMAGE_URL + userAvatar.replace('.', '_128x128.') + ' alt="..." onerror="on_avatar_error()"></span>';
            }
            else {
                var name = user.name || (user.profile && user.profile.name) || user.username;
                  try {
                    this.el.innerHTML = '<span class="w-40 circle warning"> <span>' + name[0] + '</span> <i class="on b-white"></i> </span>';
                  } catch(err) {
                    this.el.innerHTML = '<span class="w-40 circle warning"> <span>' + "U" + '</span> <i class="on b-white"></i> </span>';
                  }
            }
        }
    },
});
