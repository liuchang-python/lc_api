<template>
    <div class="footer">
        <ul>
            <li v-for="(foot,key) in foot_list" :key="key">
                <span v-if="foot.is_site"><a :href="foot.link">{{ foot.title }}</a></span>
                <span v-else><a @click="to_common(foot.link)">{{ foot.title }}</a></span>
            </li>
        </ul>
    </div>
</template>

<script>
export default {
    name: "Footer",
    data() {
        return {
            foot_list: [],    // 所有的头部链接数据
        }
    },
    methods: {
        // 获取头部链接的数据
        get_foot() {
            this.$axios({
                url: this.$settings.HOST + "home/foot/",
                method: 'get'
            }).then(res => {
                console.log(res.data);
                this.foot_list = res.data;
            }).catch(error => {
                console.log(error);
            })
        },
        to_common(link) {
            console.log(link);
            this.$router.push(link);
        },
    },
    created() {
        this.get_foot();
    },
}
</script>

<style scoped>
.footer {
    width: 100%;
    height: 128px;
    background: #25292e;
    color: #fff;
}

.footer ul {
    margin: 0 auto 16px;
    padding-top: 38px;
    width: 810px;
}

.footer ul li {
    float: left;
    width: 112px;
    margin: 0 10px;
    text-align: center;
    font-size: 14px;
}

.footer ul::after {
    content: "";
    display: block;
    clear: both;
}

.footer p {
    text-align: center;
    font-size: 12px;
}

a {
    color: white;
}
</style>
