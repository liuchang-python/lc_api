<template>
    <div class="login box">
        <img src="../../static/image/1111.jpg" alt="">
        <div class="login">
            <div class="login-title">
                <img src="../../static/image/logo.png" alt="">
                <p>百知教育给你最优质的学习体验!</p>
            </div>
            <div class="login_box">
                <div class="title">
                    <span @click="login_type=0" :class="login_type===0 ? 'active' : ''">密码登录</span>
                    <span @click="login_type=1" :class="login_type===1 ? 'active' : ''">短信登录</span>
                </div>
                <div class="inp" v-if="login_type===0">
                    <input v-model='username' type="text" placeholder="用户名 / 手机号码 / 邮箱" class="user">
                    <input v-model="password" type="password" name="" class="pwd" placeholder="密码">
                    <div id="geetest1"></div>
                    <div class="rember">
                        <p>
                            <input type="checkbox" class="no" v-model="remember_me"/>
                            <span>记住密码</span>
                        </p>
                        <p>忘记密码</p>
                    </div>
                    <button class="login_btn btn btn-primary" @click="get_captcha">登录</button>
                    <p class="go_login">没有账号
                        <router-link to="/register/">立即注册</router-link>
                    </p>
                </div>
                <div class="inp" v-else>
                    <input v-model="phone" type="text" placeholder="手机号码" class="user" @blur="check_phone">
                    <!--                    <input type="text" class="pwd" placeholder="短信验证码">-->
                    <!--                    <button id="get_code" class="btn btn-primary">获取验证码</button>-->
                    <div class="sms-box">
                        <input v-model="code" type="text" maxlength="6" placeholder="输入验证码" class="user">
                        <div>
                            <span class="sms-btn" v-show="show" @click="get_code">{{ sms_text }}</span>
                            <span class="sms-btn" v-show="!show">{{ count }}</span>
                        </div>
                    </div>
                    <button class="login_btn" @click="message_login">登录</button>
                    <span class="go_login">没有账号
                    <router-link to="/register">立即注册</router-link>
                </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Login",
    data() {
        return {
            phone: "",
            username: "",
            password: "",
            remember_me: false,
            login_type: 0,
            sms_text: "获取验证码",
            flag: false,
            count: "",
            show: true,
            timer: null,
            code: "",

        }
    },
    methods: {
        // 短信登录
        message_login() {
            this.flag = true;
            this.$axios({
                url: this.$settings.HOST + "user/phone/",
                method: 'post',
                data: {
                    phone: this.phone,
                    code: this.code,
                }
            }).then(res => {
                console.log(res.data);
            }).catch(error => {
                console.log(error);
            })
        },
        check_phone() {
            //TODO 判断是手机号是否可用
            let rex = /^1[3456789][0-9]{9}/;
            console.log(rex, rex.test(this.phone));
            if (rex.test(this.phone)) {
                this.flag = true;
                this.$axios({
                    url: this.$settings.HOST + "user/phone/",
                    method: 'get',
                    params: {
                        phone: this.phone
                    }
                }).then(res => {
                    console.log(res.data);
                    this.flag = true;
                    this.$alert('可以登录')
                }).catch(error => {
                    console.log(error);
                    this.$alert('手机号不可用', '警告');
                })
            } else {
                this.flag = false;

            }
        },
        // 为输入正确的手机号获取验证码
        get_code() {
            // TODO 判断当前手机输入的状态是否允许发送短信
            if (!/1[356789]\d{9}/.test(this.phone)) {
                this.$alert("手机号格式有误", "警告");
                return false;
            }
            if (this.flag) {
                this.$axios({
                    url: this.$settings.HOST + "user/message/",
                    method: 'get',
                    params: {
                        phone: this.phone
                    }
                }).then(res => {
                    console.log(res.data);
                    const TIME_COUNT = 60;
                    if (!this.timer) {
                        this.count = TIME_COUNT;
                        this.show = false;
                        this.timer = setInterval(() => {
                            if (this.count > 0 && this.count <= TIME_COUNT) {
                                this.count--;
                            } else {
                                this.show = true;
                                clearInterval(this.timer);
                                this.timer = null;
                            }
                        }, 1000)
                    }
                }).catch(error => {
                    console.log(error);
                })
            } else {
                this.$alert('手机号不可用');
            }
        },
        // 请求验证码的回调函数  完成验证码的验证
        handlerPopup(captchaObj) {
            // 在回调函数中 this的指向会被改变
            let self = this;
            captchaObj.onSuccess(function () {
                let validate = captchaObj.getValidate();
                self.$axios({
                    url: self.$settings.HOST + "user/captcha/",
                    method: "post",
                    data: {
                        username: self.username,
                        geetest_challenge: validate.geetest_challenge,
                        geetest_validate: validate.geetest_validate,
                        geetest_seccode: validate.geetest_seccode
                    },
                }).then(res => {
                    console.log(res.data);
                    // 判断如果返回值为success 则调用登录方法，完成登录
                    self.user_login();
                }).catch(error => {
                    console.log(error);
                })
            });
            // 将原有的滑块验证码置为空
            document.getElementById("geetest1").innerHTML = "";

            // 将验证码加到id为geetest1的元素里
            captchaObj.appendTo("#geetest1");
        },

        // 点击登录按钮，获取验证码
        get_captcha() {
            // 向后端服务器发起请求获取验证码
            this.$axios({
                url: this.$settings.HOST + "user/captcha/",
                method: 'get',
                params: {
                    username: this.username,
                }
            }).then(res => {
                // 获取到了极验返回的challenge
                console.log(res.data);
                let data = JSON.parse(res.data);
                // 使用initGeetest接口
                // 参数1：配置参数
                // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
                initGeetest({
                    gt: data.gt,
                    challenge: data.challenge,
                    product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
                    offline: !data.success, // 表示用户后台检测极验服务器是否宕机，一般不需要关注
                    new_captcha: data.new_captcha
                }, this.handlerPopup);

            }).catch(error => {
                console.log(error);
                this.$message.error("您输入的用户不存在")
            })
        },

        // 用户登录请求
        user_login() {

            this.$axios({
                url: this.$settings.HOST + "user/login/",
                method: 'post',
                data: {
                    username: this.username,
                    password: this.password,
                }
            }).then(res => {
                console.log(res.data);
                // 如果token存在，则代表登录成功
                if (res.data.token) {
                    this.$message({
                        message: "恭喜你，登录成功",
                        type: "success",
                        duration: 1000,
                    })

                    // 将用户的登录信息保存到sessionStorage，方便回显
                    sessionStorage.token = res.data.token;
                    sessionStorage.username = res.data.username;
                    sessionStorage.user_id = res.data.user_id;

                    if (this.remember_me) {
                        // 将用户的登录信息保存到localStorage，方便回显
                        localStorage.username = res.data.username;
                        localStorage.password = this.password;
                    } else {
                        localStorage.clear();
                    }

                    // 登录成功后返回首页
                    this.$router.push("/")
                }
            }).catch(error => {
                this.$message.error("账号或密码错误，请重新输入")
            })
        },
        get_local() {
            this.username = localStorage.getItem('username');
            this.password = localStorage.getItem('password');
        },
    },
    created() {
        this.get_local();
    }
}
</script>

<style scoped>
.box {
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
}

.box img {
    width: 100%;
    min-height: 100%;
}

.box .login {
    position: absolute;
    width: 500px;
    height: 400px;
    top: 0;
    left: 0;
    margin: auto;
    right: 0;
    bottom: 0;
    top: -338px;
}

.login .login-title {
    width: 100%;
    text-align: center;
}

.login-title img {
    width: 190px;
    height: auto;
}

.login-title p {
    font-family: PingFangSC-Regular;
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}

.login_box {
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
}

.login_box .title {
    font-size: 20px;
    color: #9b9b9b;
    letter-spacing: .32px;
    border-bottom: 1px solid #e6e6e6;
    display: flex;
    justify-content: space-around;
    padding: 50px 60px 0 60px;
    margin-bottom: 20px;
    cursor: pointer;
}

.login_box .title .active {
    color: #4a4a4a;
    border-bottom: 2px solid #84cc39;
}

.inp {
    width: 350px;
    margin: 0 auto;
}

.inp input {
    border: 0;
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}

.inp input.user {
    margin-bottom: 16px;
}

.inp .rember {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
}

.inp .rember p:first-of-type {
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
}

.inp .rember p:nth-of-type(2) {
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
}

.inp .rember input {
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}

.inp .rember p span {
    display: inline-block;
    font-size: 12px;
    width: 100px;
    /*position: absolute;*/
    /*left: 20px;*/

}

#geetest {
    margin-top: 20px;
}

.login_btn {
    width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
}

.inp .go_login {
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
}

.inp .go_login span {
    color: #84cc39;
    cursor: pointer;
}

.sms-box {
    position: relative;
}

.sms-btn {
    font-size: 14px;
    color: #ffc210;
    letter-spacing: .26px;
    position: absolute;
    right: 16px;
    top: 10px;
    cursor: pointer;
    overflow: hidden;
    background: #fff;
    border-left: 1px solid #484848;
    padding-left: 16px;
    padding-bottom: 4px;
}
</style>
