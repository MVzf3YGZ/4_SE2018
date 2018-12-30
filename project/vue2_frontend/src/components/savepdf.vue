<template>
<div>
<el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
      background-color="#2d2d2d"
      text-color="#fff"
      active-text-color="#ffd04b"
    >
      <el-submenu index="1">
        <template slot="title">功能选择</template>
        <el-menu-item index="/echart1">票房份额</el-menu-item>
        <el-menu-item index="/echart2">变化趋势</el-menu-item>
        <el-menu-item index="/echart3">年度top</el-menu-item>
        <el-menu-item index="/echart4">劳模演员</el-menu-item>
      </el-submenu>
     
      
      <el-submenu index="3" style="float:right;">
        <template slot="title">欢迎你！{{user.name}}</template>
        <el-menu-item index="/">退出</el-menu-item>
      </el-submenu>
    </el-menu>
    <div>
<el-button type="primary" icon="el-icon-upload" @click="exportpdf"><font color="#000000">导出pdf</font></el-button>

    </div>
<div id="main1" ></div>

</div>        
</template>
<script>
import jsPDF from 'jspdf'
export default {
    name:'pdf',
    data(){
        return{
            activeIndex: "1",
        }
    },
     beforeCreate() {
       document.querySelector('body').setAttribute('style', 'background:#f2f2f2')
       document.querySelector('body').setAttribute('style', 'width:100%;height:100%')
    },
    computed:{
      user(){
        return this.$store.state.user;
      },
      canvas: function () {
        return this.$store.state.canvas;
      },
    },
    mounted(){
       this.savepdf();
    },
     methods: {
      handleSelect(index) {
       
        
         this.$router.replace(index);
      },
      savepdf(){
       
         // alert(this.canvas)
         for(var i=0;i<this.canvas.length;i++){
         var can=this.canvas[i];
         document.getElementById('main1').appendChild(can);
        //  document.body.appendChild(can);
         }
      },
      exportpdf(){
            this.$html2canvas(document.getElementById('main1')).then( (canvas)=> {
          
        

          var contentWidth = canvas.width;
          var contentHeight = canvas.height;

          //一页pdf显示html页面生成的canvas高度;
          var pageHeight = contentWidth / 592.28 * 841.89;
          //未生成pdf的html页面高度
          var leftHeight = contentHeight;
          //页面偏移
          var position = 0;
          //a4纸的尺寸[595.28,841.89]，html页面生成的canvas在pdf中图片的宽高
          var imgWidth = 595.28;
          var imgHeight = 592.28 / contentWidth * contentHeight;

          var pageData = canvas.toDataURL('image/jpeg', 1.0);
        


          var pdf = new jsPDF('', 'pt', 'a4');

          //有两个高度需要区分，一个是html页面的实际高度，和生成pdf的页面高度(841.89)
          //当内容未超过pdf一页显示的范围，无需分页
          if (leftHeight < pageHeight) {
            pdf.addImage(pageData, 'jpeg', 0, 0, imgWidth, imgHeight);
          } else {
            while (leftHeight > 0) {
              pdf.addImage(pageData, 'jpeg', 0, position, imgWidth, imgHeight)
              leftHeight -= pageHeight;
              position -= 841.89;
              //避免添加空白页
              if (leftHeight > 0) {
                pdf.addPage();
              }
            }
          }
 

          pdf.save("content.pdf");


        });
      },
     },
}
</script>
