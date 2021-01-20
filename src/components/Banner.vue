<template>
    <el-carousel height="720px" :interval="3000" arrow="always">
        <el-carousel-item v-for="(banner, key) in banner_list" :key="key">
            <a :href="banner.link"><img :src="banner.img" alt=""></a>
        </el-carousel-item>
    </el-carousel>
</template>

<script>
    export default {
        name: "Banner",
        data() {
            return {
                banner_list: [],    // 所有的轮播图数据
            }
        },
        methods: {
            // 获取轮播图的数据
            get_banner() {
                this.$axios({
                    url: this.$settings.HOST + "home/banner/",
                    method: 'get'
                }).then(res => {
                    console.log(res);
                    this.banner_list = res.data;
                }).catch(error => {
                    console.log(error);
                })
            },
        },
        created() {
            this.get_banner();
        },
    }
</script>

<style scoped>
    .el-carousel__item h3 {
        color: #475669;
        font-size: 18px;
        opacity: 0.75;
        line-height: 300px;
        margin: 0;
    }

    .el-carousel__item:nth-child(2n) {
        background-color: #99a9bf;
    }

    .el-carousel__item:nth-child(2n+1) {
        background-color: #d3dce6;
    }
</style>
