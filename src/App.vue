<template>
    <div id="app">
        <Header></Header>
        <Banner></Banner>
<!--        <router-view></router-view>-->
        <Footer></Footer>
    </div>
</template>

<script>
import Header from "./components/common/Header";
import Footer from "./components/common/Footer";
import Banner from "./components/Banner";

export default {
    name: 'App',
    components: {
        Header: Header,
        Footer: Footer,
        Banner: Banner
    }
}
</script>

<style>

</style>
