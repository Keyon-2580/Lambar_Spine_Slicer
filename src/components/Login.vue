<template>
    <div class = 'login_box'>
        <div style="display: flex;justify-content: center;margin-top: 150px">
            <el-carousel indicator-position="outside" style="width: 800px; heigh:250px; position: absolute;
      left: 50%; top: 10%; transform: translateX(-50%) translateY(-20%)">
                <el-carousel-item v-for="(img, index) in imgs" :key="index">
                    <img src="../assets/hhh.jpg"  class ="image" />
                </el-carousel-item>
            </el-carousel>

            <el-card style="width: 400px; margin-top: 150px">
                <div slot="header" class="clearfix">
                    <span>用户登录</span>
                </div>
                <table>
                    <tr>
                        <td>用户名 </td>
                        <td>
                            <el-input v-model="user.username"  style = "width:200px ;margin-left: 22px"  placeholder="请输入用户名"></el-input>
                            <el-button @click = "regist" type="text ;margin-right: 50px" >注册用户</el-button>
                        </td>
                    </tr>
                    <tr>

                        <td>密码 </td>
                        <td>
                            <el-input type="password" v-model="user.password" style = "width:200px; margin-left: -35px"   placeholder="请输入密码" @keydown.enter.native="doLogin"></el-input>
                            <!-- @keydown.enter.native="doLogin"当按下enter键的时候也会执行doLogin方法-->
                        </td>
                    </tr>
                    <tr>
                        <!-- 占两行-->
                        <td colspan="2">
                            <!-- 点击事件的两种不同的写法v-on:click和 @click-->
                            <!--<el-button style="width: 300px" type="primary" v-on:click="doLogin">登录</el-button>-->
                            <el-button style="width:100px" type="primary" @click="doLogin">登录</el-button>

                        </td>
                    </tr>
                </table>
            </el-card>
<!--            <router-link to  = "/Main">user</router-link>-->
<!--            <router-link to  = "/Login">hhh</router-link>-->
        </div>
    </div>

</template>
<script>
    //import { Toast } from 'mint-ui';
    //import { MessageBox } from 'element-ui';
    export default {
        name :"Login",
        //单页面中不支持前面的data:{}方式
        data() {

            //相当于以前的function data(){},这是es5之前的写法，新版本可以省略掉function
            return{
                user:{
                    username:'1234',
                    password:'1234',
                    //为了登录方便，可以直接在这里写好用户名和密码的值
                },
                imgs: ["../assets/hhh.jpg","../assets/hhh.jpg"]
                //item["sss",'sss','dd','dd']
            }
        },

        methods:{
            doLogin(){//一点击登录按钮，这个方法就会执行

                this.axios.get('/login?username=' + this.user.username + '&pwd='
                        + this.user.password).then(res => {
                    if(res.data.code === '200'){
                        console.log(res.data)
                        sessionStorage.setItem('user_name', res.data.doctor_name);
                        sessionStorage.setItem('sex', res.data.doctor_sex);
                        sessionStorage.setItem('tel', res.data.doctor_tel);
                        sessionStorage.setItem('department', res.data.doctor_department);
                        sessionStorage.setItem('job', res.data.doctor_job);
                        sessionStorage.setItem('doctor_id', res.data.doctor_id);
                        console.log("登陆成功")
                        this.$router.push('main');
                        this.$message({
                            type: 'success',
                            message: '登陆成功'
                        })
                        sessionStorage.setItem('token', 'true');

                    } else {
                        this.$message({
                            type: 'info',
                            message: '账号密码错误.'
                        });
                    }
                }).catch(error => {
                    this.$message({
                        type: 'info',
                        message: '网络异常.'
                    });
                    // eslint-disable-next-line no-console
                    console.log(error);
                })
            },



            regist(){
                console.log("xxx")
            },

        },
    }
</script>
<style>
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
    img {
        width:100%;
    }
</style>

