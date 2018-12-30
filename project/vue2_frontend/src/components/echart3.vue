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
        <el-menu-item index="main1">加入报表</el-menu-item>
        <el-menu-item index="2-3">查看当前报表</el-menu-item>
      </el-submenu>
      <el-submenu index="3" style="float:right;">
        <template slot="title">欢迎你！{{user.name}}</template>
        <el-menu-item index="/">退出</el-menu-item>
      </el-submenu>
</el-menu>
    <div style>
      <h2 style="text-align:center">年度top电影</h2>

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
       
        </div>
        <div id="app2" style=" width:300px; height:100px; float:right; margin-left:10px;">
          <font size="3" face="宋体">票房排名</font>
          <!-- v-model优先匹配value值，如果没有就直接匹配option的text -->
           <el-select v-model="selected2" placeholder="请选择"  @change="change">
            <el-option
              v-for="item in options2"
              :key="item.value"
              :value="item.value"
            ></el-option>
          </el-select>
       
        </div>
      </div>
      <div id="main1" style="width: 900px;height:500px;"></div>
    </div>
  </div>
</template>
<script>
import jsPDF from 'jspdf';
export default {
  name: "main1",
  data() {
    return {
      selected1: "2015",
      selected2: "1",
      pie: [],
      myChart: {},
      activeIndex:'/echart3',
      options1: [{value: "2015",},{value: "2016",},{value: "2017",},{value: "2018",}],
      options2: [{value: "1",},{value: "2",},{value: "3",},{value: "4",},{value: "5",},{value: "6",},
      {value: "7",},{value: "8",},{value: "9",},{value: "10",}],
    };
  },
  mounted() {
    this.init();
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
          alert("此功能暂不对游客开放，谢谢合作！");
          return null;
        }
          this.convertCanvasToImage();
          // alert(2);
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
    change() {
       if(this.user.name=="游客")
        {
          alert("此功能暂不对游客开放，谢谢合作！");
            this.selected1='2015'
          this.selected2='1'
          return null;
        }
      this.updateData();
    },
    convertCanvasToImage() {

        this.$html2canvas(document.getElementById('main1')).then( (canvas)=> {
      
          var _t=this;
          _t.$store.dispatch('add',canvas).then(() => {
            
            
          });


        });
     

      },
      savepdf(){
        this.$router.replace('/savepdf');
      
      },
    init() {
      let myChart = this.$echarts.init(document.getElementById("main1"));
      this.myChart = myChart;
      this.myChart.showLoading();
      var _t = this;
      this.updateData();
      this.myChart.hideLoading();
    },
    updateData() {
      var apiurl =
        "http://127.0.0.1:8000/func/function4?year=" + this.selected1;
      apiurl = apiurl + "&num=" + this.selected2;
      var _t = this;
      _t.$http.get(apiurl).then(response => {
        var res = JSON.parse(response.bodyText);
        if (res.error_num == 0) {
          var _there = this;
          var str1 = "func4-" + this.selected1 + ".json";
          var apiurl1 =
            "http://127.0.0.1:8000/func/function_get?file_name=" + str1;
          _there.pie = [];
          return _there.$ajax.get(apiurl1).then(res2 => {
            var res1 = res2.data.index;
            if (res1 != 1) {
              for (var j = 0; j < res1.length; j++) {
                _there.pie.push(res1[j]);
              }
              _there.updateChart();
            }
          });
        } else {
          this.$message.error("数据不存在");
          alert(res.error_num);
        }
      });
    },
    updateChart() {
      this.myChart.setOption({
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
          orient: "vertical",
          right: "right"
        },
        title: {
          text: this.selected1 + "年 TOP" + this.selected2 + "电影",
          x: "center",
          y: "top"
        },
        series: [
          {
            name: "年度TOP" + this.selected2,
            type: "pie",
            radius: ["50%", "70%"],
            avoidLabelOverlap: false,
            label: {
              normal: {
                show: false,
                position: "center"
              },
              emphasis: {
                show: true,
                textStyle: {
                  fontSize: "30",
                  fontWeight: "bold"
                }
              }
            },
            labelLine: {
              normal: {
                show: false
              }
            },
            data: this.pie
          }
        ]
      });
    }
  }
};
</script>
<style>
.ba{
  background-color: "#f2f2f2"
}
</style>
