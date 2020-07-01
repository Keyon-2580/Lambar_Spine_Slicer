<template>
    <div>
        <el-button @click="linkDownload">百度</el-button>
    </div>
</template>

<script>
    export default {
        name: "STL",
        methods:{
            linkDownload(){
                // 新窗口打开外链接
                console.log("xinchuangkou")
                // window.open("http://localhost:63343/vue_test001/src/public/STL.html")
                window.open("http://localhost:8000/models/")
            }
        },
        data() {

        }
    }
</script>

<style scoped>

</style>