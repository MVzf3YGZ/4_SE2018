<template>
  <div class="middle" :style="backgroundDiv">
  <el-row type="flex" justify="center">
        <el-form ref="loginForm" :model="user" :rules="rules" status-icon label-width="80px">
            <el-form-item label="用户名" prop="name">
                <el-input v-model="user.name"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
                <el-input v-model="user.password" type="password"></el-input>
            </el-form-item>
            <el-form-item label="验证码" prop="verify">
			    <el-input  id="inputCode" v-model="user.verify"></el-input>
				<div id="checkCode" class="code"  @click="createCode(4)" ></div>
				 <span @click="createCode(4)">生成验证码</span>
				</el-form-item>
            <el-form-item>
                <el-button type="primary" icon="el-icon-upload" @click="login"><font color="#000000">登录</font></el-button>
                <el-button type="primary" icon="el-icon-upload" @click="jump"><font color="#000000">注册</font></el-button>
            </el-form-item>
        </el-form>
    </el-row>
  </div>
</template>

<script>

    //生成验证码的方法
    function createCode(length) {
        var code = "";
        var codeLength = parseInt(length); //验证码的长度
        var checkCode = document.getElementById("checkCode");
        ////所有候选组成验证码的字符
        var codeChars = new Array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
        'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'); 
        //循环组成验证码的字符串
        for (var i = 0; i < codeLength; i++)
        {
            //获取随机验证码下标
            var charNum = Math.floor(Math.random() * 62);
            //组合成指定字符验证码
            code += codeChars[charNum];
        }
        if (checkCode)
        {
            //为验证码区域添加样式名
            checkCode.className = "code";
            //将生成验证码赋值到显示区
            checkCode.innerHTML = code;
        }
    }
 
    //检查验证码是否正确
    function validateCode()
    {
        //获取显示区生成的验证码
        var checkCode = document.getElementById("checkCode").innerHTML;
        //获取输入的验证码
        var inputCode = document.getElementById("inputCode").value;
        //console.log(checkCode);
        //console.log(inputCode);
        if (inputCode.length <= 0)
        {
            alert("请输入验证码！");
			return false
        }
        else if (inputCode.toUpperCase() != checkCode.toUpperCase())
        {
            alert("验证码输入有误！");
            
			
			return false
        }
        else
        {
            alert("验证码正确！");
			return true
        }       
    }  

    export default {
      beforeCreate() {
       document.querySelector('body').setAttribute('style', 'background:#f2f2f2')
       document.querySelector('body').setAttribute('style', 'width:100%;height:100%')
    },
      mounted(){
              this.createCode(4)
        },

        methods: {
            login () {
                // alert(this.user.name);
                // alert(this.user.password);
                this.$refs.loginForm.validate((valid) => {
                    if (valid) {
                             
                           this.$http.get(this.apiurl+'?username=' + this.user.name + '&pwd=' + this.user.password)
        .then((response) => {
            var res = JSON.parse(response.bodyText)
           if(validateCode()==true){
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

           
            } else {
              this.$message.error('用户名或密码错误');
              
            }
           }
            else{
                   createCode(4); 
            }

        })
                     }
                    else {
                        return false
                    }
                })
            },
            jump(){
             this.$router.replace('/regist');


            },
            createCode(length){
                var code = "";
        var codeLength = parseInt(length); //验证码的长度
        var checkCode = document.getElementById("checkCode");
        ////所有候选组成验证码的字符，当然也可以用中文的
        var codeChars = new Array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
        'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'); 
        //循环组成验证码的字符串
        for (var i = 0; i < codeLength; i++)
        {
            //获取随机验证码下标
            var charNum = Math.floor(Math.random() * 62);
            //组合成指定字符验证码
            code += codeChars[charNum];
        }
        if (checkCode)
        {
            //为验证码区域添加样式名
            checkCode.className = "code";
            //将生成验证码赋值到显示区
            checkCode.innerHTML = code;
        }
            }
        },
        data () {
            return {
                user: {},
                apiurl:'http://127.0.0.1:8000/api/login',
                rules: {
                    name: [
                        {required: true, message: '用户名不能为空', trigger: 'blur'}
                    ],
                    password: [
                        {required: true, message: '密码不能为空', trigger: 'blur'}
                    ],
                    verify:[
					     { required:true,message:'验证码不能为空',trigger:'blur'}
						 ]
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
span {
        text-decoration:none;
        font-size:12px;
        color:#288bc4;
        padding-left:10px;
    }
span:hover {
        text-decoration:underline;
        cursor:pointer;
    }
     .code
    {
         font-family:Arial;
         font-style:italic;
         color:blue;
         font-size:30px;
         border:0;
         padding:2px 3px;
         letter-spacing:3px;
         font-weight:bolder;            
         float:left;           
         cursor:pointer;
         width:150px;
         height:50px;
         line-height:60px;
         text-align:center;
         vertical-align:middle;
         background-color:#D8B7E3;
     }
  .middle {
    height: 100%;
    width: 100%;
    position: fixed;
    background: no-repeat;

}
</style>


