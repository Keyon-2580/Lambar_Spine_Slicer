<template>
     <div class="login clearfix">
            <div class="login-wrap">
                <el-row type="flex" justify="center">
                    <el-form ref="loginForm" :model="user" status-icon label-width="80px">
                        <h3>注册</h3>
                        <hr>
                        <el-form-item prop="username" label="用户名">
                            <el-input v-model="user.username" placeholder="请输入用户名"></el-input>
                        </el-form-item>
                        <el-form-item prop="email" label="邮箱">
                            <el-input v-model="user.email" placeholder="请输入邮箱"></el-input>
                        </el-form-item>
                        <el-form-item prop="password" label="设置密码">
                            <el-input v-model="user.password" show-password placeholder="请输入密码"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" icon @click="doRegister()">注册账号</el-button>
                        </el-form-item>
                    </el-form>
                </el-row>
            </div>
     </div>


</template>

<script>
    export default {
        name: "Regist"
    }
</script>

<style scoped>

</style>