import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        // 购物车数量
        cart_length: 0,
    },
    mutations: {
        // 监测提交的动作
        change_length(state, data) {
            state.cart_length = data;
        },
    }
})
