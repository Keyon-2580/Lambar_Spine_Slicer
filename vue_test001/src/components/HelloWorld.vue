<template>
  <div class = 'login_box'>
    <div style="display: flex;justify-content: center;margin-top: 150px">
      <div style="width: 300px; position: absolute; left: 50%; top: 20%; transform: translateX(-50%) translateY(-20%)">
        <img src="../assets/hhh.jpg" style="width: 500px; height: 200px;  left: 50%; top: 50%" />
      </div>
<!--      <el-carousel indicator-position="outside" style="width: 800px; heigh:250px; position: absolute;-->
<!--      left: 50%; top: 10%; transform: translateX(-50%) translateY(-20%)">-->
<!--        <el-carousel-item v-for="(img, index) in imgs" :key="index">-->
<!--          <img src="../assets/hhh.jpg"  class ="image" />-->
<!--        </el-carousel-item>-->
<!--      </el-carousel>-->

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
    </div>
  </div>

</template>
<script>
  export default {
    name:"HelloWorld",
    //单页面中不支持前面的data:{}方式
    data() {

      //相当于以前的function data(){},这是es5之前的写法，新版本可以省略掉function
      return{
        //之前是在里面直接写username，password等等，但是这里要写return
        //因为一个组件不管要不要被其他组件用，只要这样定义了，它就会认为可能这个组件会在其他的组件中使用
        //比如说在这里定义了一个变量，然后把这个组件引入到A组件中，A组件中修改了这个变量
        //同时这个组件也在B组件中引用了，这时候A里面一修改，B里面也变了，它们用的是一个值
        //可是一般来说可能希望在不同的组件中引用的时候，使用不同的值，所以这里要用return
        //这样在A组件和B组件分别引用这个变量的时候是不会互相影响的

        user:{
          username:'',
          password:'',
          //为了登录方便，可以直接在这里写好用户名和密码的值
        },
        imgs: ["../assets/hhh.jpg","../assets/hhh.jpg"]
        //item["sss",'sss','dd','dd']
      }
    },
    methods:{
      doLogin(){//一点击登录按钮，这个方法就会执行
        alert(JSON.stringify(this.user))//可以直接把this.user对象传给后端进行校验用户名和密码
      },
      regist(){
        console.log("xxx")
      },

    }
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


