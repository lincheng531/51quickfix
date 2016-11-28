ManageProfile = function () {
    var avatar_filename = "";
    this.init = function () {
        var avatar_file = document.getElementById("avatar_file");
        avatar_file.onchange = this.avatar_load;
        var avatar_button = document.getElementById("avatar_button");
        avatar_button.onclick = this.submit_avatar;

        var birthday = $("#birthday").datetimepicker({
            
            format: "yyyy-mm-dd",
            autoclose: true,
            startView: 'month',
            minView: 'month',
        });
        
        profile_form_vm = new Vue({  // 用来显示个人信息的 vue
          el: '#profile_form',
          data: {
            'profile': {},
            'email': '',
          },
        });

        $.ajax({  // 载入页面后显示个人信息
          url: API_HOST + "user/base/profile",
          type: "GET",
          async: true,
          data: {},
        }).done(function (resp) {
          profile_form_vm.profile = resp.data.profile;
          profile_form_vm.email = resp.data.email
        });

        $("#profile_form").parsley().on('field:validated', function() {
            console.log("准备校验");
            var ok = $(".parsley-error").length === 0;
        })
        .on('form:submit', function() {
            submit_profile()
            return false;
        });

        $("#change_password_form").parsley().on('field:validated', function() {
            console.log("准备校验");
            var ok = $(".parsley-error").length === 0;
        })
        .on('form:submit', function() {
            change_password();
            return false;
        });

    };

    this.avatar_load = function () {
        var avatar_file = document.getElementById("avatar_file");
        var image_file = avatar_file.files[0];
        avatar_filename = image_file.name
        var r = new FileReader();
        r.onloadend = function () {
            var image_dom = document.getElementById("avatar_image");
            image_dom.src = r.result;
            // $("#avatar_image").cropper.destroy()
            try {
                $("#avatar_image").cropper('destroy');
            }
            catch (e) {
                console.log("第一次载入图片，无法destroy");
            }
            $("#avatar_image").cropper({
                aspectRatio: 1/1,
                preview: "#preview_avatar", 
                crop: function (e) {
                    var canvas = $("#avatar_image").cropper("getCroppedCanvas");
                },
            });
            // 裁剪图片
        }
        r.readAsDataURL(image_file);
    };

    this.submit_avatar = function () {
        var image_data = $("#avatar_image").cropper("getCroppedCanvas").toDataURL();
        if (image_data.length<80) {
            toastr.warning("请选择图片");
        }
        else {
            $.ajax({
                url: API_HOST + "user/avatar",
                type: "POST",
                async: false,
                data: {
                    "avatar": image_data,
                    "filename": avatar_filename
                },
                success: function(responseTxt){
                  USER_PROFILE['user']['profile']['avatar'] = responseTxt['data']['avatar'];
                  $.ajax({
                    url: "/refresh/profile",
                    type: "GET",
                    success: function(response) {
                      document.getElementById("avatar_span").getElementsByTagName('img')[0].src = IMAGE_URL + USER_PROFILE['user']['profile']['avatar']
                    }
                  })
                }
            });
        }
        return false;
    };

    function submit_profile() {
        data = $("#profile_form").serialize();
        $.ajax({
            url: API_HOST + "user/base/profile",
            type: "POST",
            async: false,
            data: data,
        });
    };

    function change_password() {
        var form = document.getElementById("change_password_form");
        if (! (form.password_new.value == form.password_new2.value)) {
            toastr.warning("两次密码输入不一致");
            return false;
        }
        data = $("#change_password_form").serialize();
        $.ajax({
            url: API_HOST + "user/passwd",
            type: "POST",
            async: false,
            data: {
                password: form.password.value,
                password_new: form.password_new2.value,
            },
        });
    };
};
