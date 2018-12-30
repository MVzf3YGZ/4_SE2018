<template>

  <div class="middle" :style="backgroundDiv">

        欢迎!
    <div style="margin-top=500px;"><center><el-button @click="login" class="but">登录</el-button></center></div>
    <center><el-button @click="regist" class="but">注册</el-button></center>
    <center><el-button @click="logasout" class="but">游客登录</el-button></center>

    </div>

</template>

<script>
    export default {
      beforeCreate() {
       document.querySelector('body').setAttribute('style', 'background:#f2f2f2')
       document.querySelector('body').setAttribute('style', 'width:100%;height:100%')
    },
      watch:{
            '$route':function(to,from){
                let token = window.localStorage.getItem('token');
　　　　　　　　   if (to.matched.some(record => record.meta.requiresAuth) && (!token || token === null)) {
　　　　　　　　　　   next({
  　　　　　　　　　　   path: '/login',
  　　　　　　　　　　   query: { redirect: to.fullPath }
　　　　　　　　　　   })
　　　　　　　　   } else {
　　　　　　          next()
　　　　　　　　   }
      　　　}
    　　},
     methods: {
            logasout(){
               var user={}
               user.name="游客"
               user.password=123;
               this.$store.dispatch('login', user).then(() => {
                        this.$notify({
                            type: 'success',
                            message: '欢迎你,' + user.name + '!',
                            duration: 3000
                        })
                        this.$router.replace('/choose')
                    }) 
            },
            login () {
                this.$router.replace('/login')
            },
            regist (){
                this.$router.replace('/regist')
            },

        },
        data() {

    return {
        backgroundDiv: {
            backgroundImage: 'url(' + require('../assets/img/background.png') + ')',
            // text-align: "center";

        }
    }
}
    }
</script>
<style>
  .middle {
    height: 100%;
    width: 100%;
    position: fixed;
    background: no-repeat;
}
.but{
    margin-top: 100px
}

</style>
