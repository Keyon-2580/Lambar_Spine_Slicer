<script src='https://cdn.jsdelivr.net/npm/imagvue@0.0.5/dist/imagvue.min.js'></script>
<template>
<div>
    <el-header>
        <h1>
            查看病人CT及处理过的模型
        </h1>
    </el-header>
    <el-container>
        <el-main>
            <el-row>
                <el-col  :span="8">
                    <div class="block">
                        <el-slider
                                v-model="lebel0"
                                :max="this.imgnum"
                                style="width: 300px"
                                show-input>
                        </el-slider>
                    </div>
                </el-col>
                <el-col  :span="8">
                    <div class="block">
                        <el-slider
                                v-model="lebel1"
                                :max="this.imgnum"
                                style="width: 300px"
                                show-input>
                        </el-slider>
                    </div>
                </el-col>
                <el-col  :span="8">
                    <div class="block">
                        <el-slider
                                v-model="lebel2"
                                :max="this.imgnum"
                                style="width: 300px"
                                show-input>
                        </el-slider>
                    </div>
                </el-col>
            </el-row>
            <el-row>
                <el-col  :span="8">
                    <div class="block"  >
<!--                        <span class="demonstration">{{ fit }}</span>-->
                        <el-image
                                style="width: 300px; height: 300px ;margin-right: 50%"
                                :src="'data:image/png;base64,'+ this.url[this.lebel0]"  ></el-image>
                        <el-button  style="margin-right: 50%" type="primary" @click="readImg" >
                            读取图片
                        </el-button>
                    </div>
                </el-col>
                <el-col  :span="8">
                    <el-image
                            style="width: 300px; height: 300px ;margin-right: 50%"
                            :src="'data:image/png;base64,'+ this.url[this.lebel1]"  ></el-image>
                </el-col>
                <el-col  :span="8">
                    <el-image
                            style="width: 300px; height: 300px ;margin-right: 50%"
                            :src="'data:image/png;base64,'+ this.url[this.lebel2]"  ></el-image>
                </el-col>
            </el-row>


        </el-main>
    </el-container>


</div>

</template>

<script>
    export default {
        name: "Diagnosis",
        data() {
            return {
                lebel0: 0,
                lebel1: 0,
                lebel2: 0,
                imgnum:200,
                data:{
                    filename:'祖儿4.jpg'
                },
                url:[]
            }
        },

        created(){
            this.readImg()

        },


        methods:{
            readImg() {
                this.$axios.post('/read_img/',this.data,{
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        responseType: 'image/png'
                }

                ).then(res=>{
                    this.url = res.data.split(',++')
                    this.imgnum = this.url.length - 2
                    console.log( this.url.length)

                })


            }
            }
    }
</script>
<style scoped>
    .el-header, .el-footer {
        background-color: #9d09ec;
        color: #333;
        text-align: center;
        line-height: 50px;
    }

    .el-aside {
        background-color: #D3DCE6;
        color: #333;
        text-align: center;
        line-height: 20px;
        font-size: 12px;
        text-align: left;
    }

    .el-main {
        background-color: #E9EEF3;
        color: #333;
        text-align: center;
        line-height: 100px;
    }
</style>