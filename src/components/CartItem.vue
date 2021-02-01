<template>
    <div class="cart_item">
        <div class="cart_column column_1">
            <el-checkbox class="my_el_checkbox" v-model="course.selected"></el-checkbox>
        </div>
        <div class="cart_column column_2">
            <img :src="course.course_image" alt="">
            <span><router-link :to="'/detail/'+course.id">{{ course.name }}</router-link></span>
        </div>
        <div class="cart_column column_3">

            <el-select v-model="course.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
                <el-option v-for="item in course.expire_text" :label="item.expire_text" :value="item.id"
                           :key="item.id"></el-option>
            </el-select>
        </div>
        <div class="cart_column column_4">¥ {{ course.price }}</div>
        <div class="cart_column column_4">
            <el-button @click="del_cart" type="danger" icon="el-icon-delete" round size="mini"></el-button>
            删除
        </div>
    </div>
</template>

<script>
export default {
    name: "CartItem",
    props: ['course'],
    watch: {
        // 监听selected是否发生了变化
        "course.selected": function () {
            this.change_selected();
        },
        // 监测课程对应的有效期id是否发生了改变
        "course.expire_id": function () {
            this.change_expire();
        },
    },
    methods: {
        // 发起请求，修改redis中的有效期
        change_expire() {
            // 向后端发起请求，修改有效期，并获取有效期对应的价格
            let token = sessionStorage.token || localStorage.token;

            this.$axios.put(this.$settings.HOST + "cart/option/", {
                // 要修改的有效期id  要修改redis中哪本课程
                expire_id: this.course.expire_id,
                course_id: this.course.id
            }, {
                headers: {
                    // 添加购物车需要认证，写到token才能请求到后台
                    "Authorization": "jwt " + token
                }
            }).then(res => {
                console.log(res.data);
                // 获取到有效期对应的价格并展示
                this.course.price = res.data.price;
                // 当有效期切换时  向父组件提交事件来修改总价
                this.$emit("change_expire")
                this.$message.success("切换有效期成功")
            }).catch(error => {
                console.log(error);
            })
        },
        // 在访问购物车之前判断用户是否已经登录
        check_user_login() {
            let token = sessionStorage.token || localStorage.token;
            if (!token) {
                let self = this;
                this.$confirm("对不起，请登录后再添加购物车", {
                    callback() {
                        self.$router.push("/login");
                    }
                })
                return false
            }
            return token
        },
        // 发起请求，修改redis中购物车的勾选状态
        change_selected() {
            let token = this.check_user_login();
            this.$axios.post(this.$settings.HOST + "cart/change/", {
                course_id: this.course.id,
                select: this.course.selected,

            }, {
                headers: {
                    // 更改购物车需要认证，写到token才能请求到后台
                    "Authorization": "jwt " + token
                }
            }).then(res => {
                console.log(res.data);
                this.$message('修改状态成功')
            }).catch(error => {
                console.log(error);
            })
        },
        // 删除购物车课程
        del_cart() {
            let token = this.check_user_login();
            this.$axios.post(this.$settings.HOST + "cart/del/", {
                course_id: this.course.id,
            }, {
                headers: {
                    // 更改购物车需要认证，写到token才能请求到后台
                    "Authorization": "jwt " + token
                }
            }).then(res => {
                console.log(res.data);
                this.$message('删除成功');
                this.$router.go(0);
            }).catch(error => {
                console.log(error);
            })
        },
    }
}
</script>

<style scoped>
.cart_item::after {
    content: "";
    display: block;
    clear: both;
}

.cart_column {
    float: left;
    height: 250px;
}

.cart_item .column_1 {
    width: 88px;
    position: relative;
}

.my_el_checkbox {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    margin: auto;
    width: 16px;
    height: 16px;
}

.cart_item .column_2 {
    padding: 67px 10px;
    width: 520px;
    height: 200px;
}

.cart_item .column_2 img {
    width: 400px;
    height: 200px;
    margin-right: 30px;
    vertical-align: middle;
}

.cart_item .column_3 {
    width: 197px;
    position: relative;
    padding-left: 10px;
}

.my_el_select {
    width: 117px;
    height: 28px;
    position: absolute;
    top: 0;
    bottom: 0;
    margin: auto;
}

.cart_item .column_4 {
    padding: 67px 10px;
    height: 116px;
    width: 142px;
    line-height: 116px;
}

</style>
