<template>
    <div class="app" id="login">

        <!-- ############ LAYOUT START-->
        <div class="center-block w-xxl w-auto-xs p-y-md">
            <div class="navbar">
                <div class="pull-center m-t">
                    <a class="navbar-brand" v-if="is_yihui">
                        <img src='../../assets/images/logo_yihui.png' style="max-height: 40px">
                    </a>
                    <a class="navbar-brand" v-else>
                        <img src="../../assets/images/logo.png" alt=".">
                        <img src="../../assets/images/logo.png" alt="." class="hide">
                        <span class="hidden-folded inline" v-text="app.name"></span>
                    </a>
                </div>
            </div>
            <div class="p-a-md box-color r box-shadow-z1 text-color m-a">
                <form name="form">
                    <div class="alert alert-danger" id="error" role="alert" v-if="error">
                        <span v-text="error"></span>
                    </div>

                    <div class="md-form-group float-label">
                        <input class="md-input" id="username" name="username" v-model="form.username" required>
                        <label>用户</label>
                    </div>
                    <div class="md-form-group float-label">
                        <input type="password" class="md-input" id="password" v-model="form.password" required>
                        <label>密码</label>
                    </div>
                    <button type="submit" class="btn btn-block p-x-md" style="background-color: #CE1C0C; color: white"
                            v-if="is_yihui" @click.prevent="submit">登&nbsp;&nbsp;&nbsp;&nbsp;录
                    </button>
                    <button type="submit" class="btn danger btn-block p-x-md" v-else @click.prevent="submit">
                        登&nbsp;&nbsp;&nbsp;&nbsp;录
                    </button>
                </form>
            </div>

            <div class="p-v-lg text-center hide">
                <div class="m-b">
                    <a ui-sref="access.forgot-password" href="#" class="text-primary _600">忘记密码?</a>
                </div>
            </div>
        </div>
        <!-- ############ LAYOUT END-->
    </div>
</template>
<script>
    import {mapActions} from 'vuex'

    export default {
        data() {
            return {
                app,
                form: {
                    username: '',
                    password: '',
                },
                is_yihui: false
            }
        },
        methods: {
            ...mapActions(['SIGNIN']),
            ...mapActions(['SIGNOUT']),
            login(data, fnSucess) {
                $.ajax({
                    type: 'POST',
                    url: global.API_HOST + '/login',
                    data: data,
                    crossDomain: true,
                }).done(function (response) {
                    if (response.status === 1) {
                        if (fnSucess) {
                            fnSucess(response.info);
                        }
                    }else{
                        toastr.error(response.alert);
                    }
                });
            },
            submit() {
                var scope = this;
                if (!this.form.username || !this.form.password) return;
                scope.SIGNOUT();
                this.login(this.form, function (data) {
                    scope.SIGNIN(data);
                    scope.$router.replace({path: '/home'});
                });
            },
        }
    }
</script>