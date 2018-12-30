<template>
  <div class="ba">
<el-menu
  :default-active="activeIndex"
  class="el-menu-demo"
  mode="horizontal"
  @select="handleSelect"
  background-color="#2d2d2d"
  text-color="#fff"
  active-text-color="#ffd04b">
 
  <el-submenu index="1">
    <template slot="title">功能选择</template>
    <el-menu-item index="/echart1">票房份额</el-menu-item>
    <el-menu-item index="/echart2">变化趋势</el-menu-item>
    <el-menu-item index="/echart3">年度top</el-menu-item>
    <el-menu-item index="/echart4">劳模演员</el-menu-item>
   </el-submenu>
 <el-submenu index="2">
        <template slot="title">生成报表</template>
        <el-menu-item index="main1">将图一加入报表</el-menu-item>
        <el-menu-item index="main2">将图二加入报表</el-menu-item>
        <el-menu-item index="2-3">查看当前报表</el-menu-item>
      </el-submenu>
      <el-submenu index="3" style="float:right;">
        <template slot="title">欢迎你！{{user.name}}</template>
        <el-menu-item index="/">退出</el-menu-item>
      </el-submenu>
</el-menu>
    <div style>
      <h2 style="text-align:center">劳模演员</h2>

      <div style=" margin:auto; width:800px; height:100px;">
        <div id="app1" style=" width:300px; height:100px; float:left; margin-left:10px;">
          <font size="3" face="宋体">年份</font>
          <!-- v-model优先匹配value值，如果没有就直接匹配option的text -->
          <el-select v-model="selected1" placeholder="请选择" @change="change">
            <el-option
              v-for="item in options1"
              :key="item.value"
              :value="item.value"
            ></el-option>
          </el-select>
          <!-- <select
            name
            id
            @change="change"
            v-model="selected1"
            style=" height:30px; width:58px; margin:0 auto"
          >
            <option>2015</option>
            <option>2016</option>
            <option>2017</option>
            <option>2018</option>
          </select> -->
        </div>
        <div id="app2" style=" width:300px; height:100px; float:right; margin-left:10px;">
          <font size="3" face="宋体">排名</font>
          <!-- v-model优先匹配value值，如果没有就直接匹配option的text -->
          <el-select v-model="selected2" placeholder="请选择" @change="change">
            <el-option
              v-for="item in options2"
              :key="item.value"
              :value="item.value"
            ></el-option>
          </el-select>
          <!-- <select
            name
            id
            @change="change"
            v-model="selected2"
            style=" height:30px; width:58px; margin:0 auto"
          >
            <option>1</option>
            <option>2</option>
            <option>3</option>
            <option>4</option>
            <option>5</option>
          </select> -->
        </div>
      </div>
      <div id="main1" style=" width: 700px;height:400px; float:left"></div>
      <div id="main2" style="width: 700px;height:400px; float:left"></div>
    </div>
  </div>
</template>
<script>
import jsPDF from 'jspdf';
export default {
  name: "chart4",
  data() {
    return {
      selected1: "2015",
      selected2: "1",
      myChart1:{},
      myChart2:{},
      pie1:[],
      pie2:[],
      activeIndex:'/echart4',
      options1: [{value: "2015",},{value: "2016",},{value: "2017",},{value: "2018",}],
      options2: [{value: "1",},{value: "2",},{value: "3",},{value: "4",},{value: "5",}],
    };
  },
  mounted() {
    this.init1();
    this.init2();
  },
  computed:{
      user(){
        return this.$store.state.user;
      }
    },
  methods: {
    handleSelect(index) {
       
        if (index == "main1") {
          if(this.user.name=="游客")
        {
          alert("此功能暂不对游客开放，谢谢合作！")
          return null;
        }
          this.convertCanvasToImage('main1');
          // alert(2);
        } 
        else if(index== "main2")
        {
           if(this.user.name=="游客")
        {
          alert("此功能暂不对游客开放，谢谢合作！")
          return null;
        }
          this.convertCanvasToImage('main2');
        }
        else if(index=="2-3")
        {
              if(this.user.name=="游客")
        {
          alert("此功能暂不对游客开放，谢谢合作！")
          return null;
        }
           this.savepdf();
          //this.convertCanvasToImage();
        }
        else this.$router.replace(index);
      },
    change(){
       if(this.user.name=="游客")
        {
          alert("此功能暂不对游客开放，谢谢合作！");
            this.selected1='2015'
          this.selected2='1'
          return null;
        }
      this.updatealldata();
    },
    convertCanvasToImage(index) {

       this.$html2canvas(document.getElementById(index)).then( (canvas)=> {
          var _t=this;
          _t.$store.dispatch('add',canvas).then(() => {
            
            
          });
       


        });


      },
      savepdf(){
        this.$router.replace('/savepdf');
      
      },
    updatealldata(){
     var apiurl = "http://127.0.0.1:8000/func/function3?year="+this.selected1+'&num='+this.selected2;
      this.$http
        .get(apiurl)
        .then(response => {
          var res = JSON.parse(response.bodyText);
          if (res.error_num == 0) {
           var _there = this;
            var str1 = "func3-M-" + this.selected1+ ".json";
            var str2 = "func3-F-" + this.selected1+ ".json";
            var apiurl1="http://127.0.0.1:8000/func/function_get2?file_name1="+str1+'&file_name2='+str2;
            _there.pie1=[];
            _there.pie2=[];
            return _there.$ajax.get(apiurl1).then(res3 => {
              var res1=res3.data.index1
              var res2=res3.data.index2
              if(res1!=1){
                _there.pie1=res1;
                _there.updateChart1();
            }
              if(res2!=1){
                _there.pie2=res2;
                _there.updateChart2();
              }
            });

          } else {
            this.$message.error("数据不存在");
            alert(res.error_num);
          }
        });
    },
     updateData1(){

           var apiurl = "http://127.0.0.1:8000/func/function3?year="+this.selected1+'&num='+this.selected2;
          this.$http
        .get(apiurl)
        .then(response => {
          var res = JSON.parse(response.bodyText);
          if (res.error_num == 0) {
            var _there = this;
            var str1 = "func3-M-" + this.selected1+ ".json";
            var apiurl1="http://127.0.0.1:8000/func/function_get?file_name="+str1
           _there.pie1=[];
            return _there.$ajax.get(apiurl1).then(res2 => {
              var res1=res2.data.index;
              if(res1!=1){
                _there.pie1=res1;
                _there.updateChart1();
            }
            });

          } else {
            this.$message.error("数据不存在");
            alert(res.error_num);
          }
        });

    },
    updateData2(){
           
           var apiurl = "http://127.0.0.1:8000/func/function3?year="+this.selected1+'&num='+this.selected2;
          this.$http
        .get(apiurl)
        .then(response => {
          var res = JSON.parse(response.bodyText);
          if (res.error_num == 0) {
            var _there = this;
            var str1 = "/static/func3-F-" + this.selected1+ ".json";
            var apiurl1="http://127.0.0.1:8000/func/function_get?file_name="+str1
           _there.pie2=[];
            return _there.$ajax.get(apiurl1).then(res => {
             var res1=res.data.index;
              if(res1!=1){
                _there.pie2=res1;
                _there.updateChart2();
            }
            });
          } else {
            this.$message.error("数据不存在");
            alert(res.error_num);
          }
        });

    },
    init1() {
        let myChart1 = this.$echarts.init(document.getElementById("main1"));
        this.myChart1 = myChart1;
        this.myChart1.showLoading();
        var _t = this;
        _t.updatealldata();
        _t.myChart1.hideLoading();

    },
    init2() {
      let myChart2 = this.$echarts.init(document.getElementById("main2"));
      this.myChart2 = myChart2;
      this.myChart2.showLoading();
      var _th = this;
      _th.updatealldata()
      _th.myChart2.hideLoading();

    },
    updateChart1() {
      
      this.myChart1.setOption({
        title: {
          text: this.selected1 + "年TOP" + this.selected2 + "男演员",
          x:'center'
        },

         tooltip: {
          trigger: "item",
          formatter: "{b} : 出演{c}次"
        },
        series: [{
        type: 'wordCloud',
        gridSize: 20,
        sizeRange: [12, 50],
        rotationRange: [0, 0],
        shape: 'circle',
        textStyle: {
            normal: {
                color: function() {
                    return 'rgb(' + [
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160)
                    ].join(',') + ')';
                }
            },
            emphasis: {
                shadowBlur: 10,
                shadowColor: '#333'
            }
        },
        data:this.pie1,

    }]
      });
    },
    updateChart2(){
     
      this.myChart2.setOption({
        title: {
          text: this.selected1 + "年TOP" + this.selected2 + "女演员",
          top: "top",
          left: "center"
        },
        tooltip: {
          trigger: "item",
          formatter: "{b} : 出演{c}次"
        },
        toolbox: {
          show: true,
          orient: "vertical",
          top: "center",
          feature: {
            saveAsImage: {
              show: true
            }
          }
        },
    series: [{
        type: 'wordCloud',
        gridSize: 20,
        sizeRange: [12, 50],
        rotationRange: [0, 0],
        shape: 'circle',
        textStyle: {
            normal: {
                color: function() {
                    return 'rgb(' + [
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160)
                    ].join(',') + ')';
                }
            },
            emphasis: {
                shadowBlur: 10,
                shadowColor: '#333'
            }
        },
        data:this.pie2,

    }]
      });
    }
  }
};
</script>

