<template>
<div class="middle" :style="backgroundDiv">
<h2 align="center">注册</h2>
    <el-row type="flex" justify="center">
        <el-form ref="loginForm" :model="user" :rules="rules" status-icon label-width="80px">
            <el-form-item label="用户名" prop="name">
                <el-input v-model="user.name"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
                <el-input v-model="user.password" type="password"></el-input>
            </el-form-item>
            <el-form-item>
		<el-button type="primary" icon="el-icon-upload" @click="regist"><font color="#000000">注册</font></el-button>
            </el-form-item>  
			
        </el-form>
    </el-row>
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
  methods:{
		    regist(){
			       this.$refs.loginForm.validate((valid) =>
				   {  
				        if(valid)
						{
                           this.$http.get('http://127.0.0.1:8000/api/regist?username='+ this.user.name + '&pwd=' + this.user.password)
                           .then((response) => {
                           var res = JSON.parse(response.bodyText)
                            if (res.error_num == 0) 
                           {
                                 this.$store.dispatch('login', this.user).then(() => {
                        this.$notify({
                            type: 'success',
                            message: '欢迎你,' + this.user.name + '!',
                            duration: 3000
                        })
                        this.$router.replace('/choose')
                    })
                           }
                           else{
                            this.$message.error('用户名已存在');
            } 
                           
                           
                           })
						
						}
						else
						{
						  return false;
						
						}
				   
				   
				   })
			}
		
		},
          data () {
            return {
                user: {},
                rules: {
                    name: [
                        {required: true, message: '用户名不能为空', trigger: 'blur'}
                    ],
                    password: [
                        {required: true, message: '密码不能为空', trigger: 'blur'}
                    ],
					
                },
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
</style>
