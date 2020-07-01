<template>

        <div style="display: flex;justify-content: center;margin-top: 150px">
            <el-carousel indicator-position="outside" style="width: 800px; heigh:250px; position: absolute;
                    left: 50%; top: 10%; transform: translateX(-50%) translateY(-20%)">
                <el-carousel-item v-for="index in imgs" :key="index.url">
                    <img :src="index.url"  class ="image" />

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
            <el-dialog title="医生注册" :visible.sync="dialogFormVisible" >
                <el-form :model="form" :rules="rules"  ref="form">
                    <el-form-item label="姓名" :label-width="formLabelWidth" prop="name">
                        <el-input v-model="form.name" style="width: 220px" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="性别" :label-width="formLabelWidth" prop="sex">
                        <el-select v-model="form.sex" placeholder="请选择性别">
                            <el-option label="男" value="男"></el-option>
                            <el-option label="女" value="女"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="账户" :label-width="formLabelWidth" prop="account">
                        <el-input v-model="form.account" style="width: 220px" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" :label-width="formLabelWidth" prop="pwd">
                        <el-input v-model="form.pwd"  style="width: 220px" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="确认密码" :label-width="formLabelWidth" prop="pwd_0">
                        <el-input v-model="form.pwd_0" style="width: 220px" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="手机号" :label-width="formLabelWidth" prop="tel">
                        <el-input v-model="form.tel" style="width: 200px" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="部门" :label-width="formLabelWidth" prop="department">
                        <el-select v-model="form.department" placeholder="请选择部门">
                            <el-option label="放射科" value="放射科"></el-option>
                            <el-option label="骨外科" value="骨外科"></el-option>
                            <el-option label="儿科" value="儿科"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="职务" :label-width="formLabelWidth" prop="job">
                        <el-select v-model="form.job" placeholder="请选择职务">
                            <el-option label="主任医师" value="主任医师"></el-option>
                            <el-option label="副主任医师" value="副主任医师"></el-option>
                            <el-option label="主治医师" value="主治医师"></el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false; resetForm('form')" >取 消</el-button>
                    <el-button type="primary" @click="dialogFormVisible = false; submitForm('form')">确 定</el-button>
                </div>
            </el-dialog>
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
                imgs: [
                    { url: require("../assets/bg0.jpg") },
                    { url: require("../assets/bg1.jpg") },

                ],
                //item["sss",'sss','dd','dd']
                dialogFormVisible:false,
                form: {
                    name: '',
                    sex: '',
                    date1: '',
                    date2: '',
                    account: '',
                    pwd: '',
                    pwd_0: '',
                    tel: '',
                    department: '',
                    job: '',
                },
                rules: {
                    name: [{ required: true, message: 'Please input Activity name', trigger: 'blur' }],
                    sex: [{ required: true, message: 'Please input Activity sex', trigger: 'blur' }],
                    account: [{ required: true, message: 'Please input Activity account', trigger: 'blur' }],
                    pwd: [{ required: true, message: 'Please input Activity password', trigger: 'blur' }],
                    pwd_0: [{ required: true, message: 'Please input Activity password_0', trigger: 'blur' }],
                    tel: [{ required: true, message: 'Please input Activity tel', trigger: 'blur' }],
                    department: [{ required: true, message: 'Please input Activity department', trigger: 'blur' }],
                    job: [{ required: true, message: 'Please input Activity job', trigger: 'blur' }],
                },
                formLabelWidth: '120px'
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
                this.dialogFormVisible=true
            },
            submitForm(form) {
                this.$refs[form].validate((valid) => {
                    if (valid ) {
                        console.log('---------------------')
                        this.$axios.post('/regist/',this.form).then(
                            res=>{
                                if(res.data.code==200){
                                    this.$message({
                                        type: 'success',
                                        message: '提交成功.'
                                    });
                                }
                            }
                        )
                    } else if(this.form.pwd != this.form.pwd_0) {
                        this.dialogFormVisible=true
                        this.$message({
                            type: 'info',
                            message: '验证密码不对.'
                        });
                        return false;
                    }
                    else{
                        this.dialogFormVisible=true
                        this.$message({
                            type: 'info',
                            message: '有信息未填写.'
                        });
                        return false;
                    }
                });
            },
            resetForm(form) {
                this.$refs[form].resetFields();
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

