<template>
  <div id="app">
      <keep-alive exclude="needExcludeComponentName">

      </keep-alive>
      <keep-alive v-if="!$route.meta.noKeepAlive">
          <router-view></router-view>
      </keep-alive>
      <router-view v-if="$route.meta.noKeepAlive"></router-view>
  </div>
</template>

<script>
 //import Login from './components/Login.vue'
 //import Login from './components/Login.vue'

export default {
  name: 'App',
  // components: {
  //     // eslint-disable-next-line vue/no-unused-components
  //     Login,
  //     //HelloWorld
  // }
  //   watch:{
  //       '$route'(){
  //       }
  //   },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
