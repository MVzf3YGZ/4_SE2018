<template>
  <div class="ba">
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

    <div id="pdfDom">
      <h2 style="text-align:center">票房份额</h2>

      <div style=" height:100px;">
        <div id="app1" style="float:left;width:550px; height:100px;">
          <font size="3" face="宋体">年份</font>
          <!-- v-model优先匹配value值，如果没有就直接匹配option的text -->
          <el-select v-model="selected[0]" placeholder="请选择" @change="change">
            <el-option
              v-for="item in options1"
              :key="item.value"
              :value="item.value"
            ></el-option>
          </el-select>
     
          <p>选择的是：{{ selected[0] }}</p>
        </div>
        <div id="app2" style="float:left;width:550px; height:100px;">
          <font size="3" face="宋体">季度</font>
          <!-- v-model优先匹配value值，如果没有就直接匹配option的text -->
          <el-select v-model="selected[1]" placeholder="请选择" @change="change">
            <el-option
              v-for="item in options2"
              :key="item.value"
              :value="item.value"
            ></el-option>
          </el-select>

          <p>选择的是：{{ selected[1] }}</p>
        </div>
        <div id="app3" style="float:left; width:550px; height:100px;">
          <font size="3" face="宋体">月份</font>
          <!-- v-model优先匹配value值，如果没有就直接匹配option的text -->
          <el-select v-model="selected[2]" placeholder="请选择" @change="change">
            <el-option
              v-for="item in options3"
              :key="item.value"
              :value="item.value"
            ></el-option>
          </el-select>

          <p>选择的是：{{ selected[2] }}</p>
        </div>
      </div>

       
      <div id="main1" style=" width: 950px;height:400px; float:left"></div>
      <div id="main2" style="width: 750px;height:400px; float:left"></div>
       

    </div>
  </div>
</template>
<script>
import jsPDF from 'jspdf';
  export default {
    name: "chart",
    data() {
      return {
        selected: ["2015", "1", "01"],
        myChart1: {},
        myChart2: {},
        data1: [],
        name1: [],
        base641: [],
        pie1: [],
        activeIndex: "/echart1",
        options2: [{value: "1",}, {value: "2",}, {value: "3",}, {value: "4",}],
        options1: [{value: "2015",}, {value: "2016",}, {value: "2017",}, {value: "2018",}],
        options3: [{value: "01",}, {value: "02",}, {value: "03",}, {value: "04",}, {value: "05",}, {value: "06",},
          {value: "07",}, {value: "08",}, {value: "09",}, {value: "10",}, {value: "11",}, {value: "12",},],
        htmlTitle: '页面导出PDF文档名',
        backgroundDiv: {
            backgroundImage: 'url(' + require('../assets/img/background.png') + ')',
            // text-align: "center";

        }

      };
    },
    beforeCreate() {
       document.querySelector('body').setAttribute('style', 'background:#f2f2f2')
       document.querySelector('body').setAttribute('style', 'width:100%;height:100%')
    },
    mounted() {
      this.init1();
      this.init2();
    },
    computed:{
      user(){
        return this.$store.state.user;
      },
      canvas: function () {
        return this.$store.state.canvas;
      },
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
          
        }
        else this.$router.replace(index);
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
      change() {
         if(this.user.name=="游客")
        {
          alert("此功能暂不对游客开放，谢谢合作！");
          this.selected=["2015", "1", "01"]
          return null;
        }
        this.updatealldata();
      },
      change1() {
        this.updateData1();
      },
      change2() {
        this.updateData2();
      },
      updatealldata() {
        var apiurl = "http://127.0.0.1:8000/func/function1?year=";
        apiurl =
          apiurl +
          this.selected[0] +
          "&month=" +
          this.selected[2] +
          "&quarter=" +
          this.selected[1];
        this.$http.get(apiurl).then(response => {
          var res = JSON.parse(response.bodyText);
          if (res.error_num == 0) {
            var _there = this;
            var str1 = "func1-1-" + this.selected[0] + this.selected[1] + ".json";
            var str2 = "func1-2-" + this.selected[0] + this.selected[2] + ".json";
            var apiurl1 =
              "http://127.0.0.1:8000/func/function_get2?file_name1=" +
              str1 +
              "&file_name2=" +
              str2;

            _there.data1 = [];
            _there.name1 = [];
            return _there.$ajax.get(apiurl1).then(res3 => {
              var res1 = res3.data.index1;
              var res2 = res3.data.index2;

              if (res1 != 1) {
                for (var j = 0; j < res1.length; j++) {
                  _there.data1.push(res1[j].value);
                  _there.name1.push(res1[j].name);
                }
                _there.updateChart1();
              }
              if (res2 != 1) {
                _there.pie1 = [];
                for (var j = 0; j < res2.length; j++) {
                  _there.pie1.push(res2[j]);
                }
                _there.updateChart2();
              }
            });
          } else {
            this.$message.error("数据不存在");
            alert(res.error_num);
          }
        });
      },
      updateData1() {
        var apiurl = "http://127.0.0.1:8000/func/function1?year=";
        apiurl =
          apiurl +
          this.selected[0] +
          "&month=" +
          this.selected[2] +
          "&quarter=" +
          this.selected[1];
        this.$http.get(apiurl).then(response => {
          var res = JSON.parse(response.bodyText);
          if (res.error_num == 0) {
            var _there = this;
            var str1 = "func1-1-" + this.selected[0] + this.selected[1] + ".json";
            var apiurl1 =
              "http://127.0.0.1:8000/func/function_get?file_name=" + str1;
            _there.data1 = [];
            _there.name1 = [];
            return _there.$ajax.get(apiurl1).then(res2 => {
              var res1 = res2.data.index;

              if (res1 != 1) {
                for (var j = 0; j < res1.length; j++) {
                  _there.data1.push(res1[j].value);
                  _there.name1.push(res1[j].name);
                }
                _there.updateChart1();
              }
            });
          } else {
            this.$message.error("数据不存在");
            alert(res.error_num);
          }
        });
      },
      updateData2() {
        var apiurl = "http://127.0.0.1:8000/func/function1?year=";
        apiurl =
          apiurl +
          this.selected[0] +
          "&month=" +
          this.selected[2] +
          "&quarter=" +
          this.selected[1];
        this.$http.get(apiurl).then(response => {
          var res = JSON.parse(response.bodyText);
          if (res.error_num == 0) {
            var _there = this;
            var str1 = "func1-2-" + this.selected[0] + this.selected[2] + ".json";
            var apiurl1 =
              "http://127.0.0.1:8000/func/function_get?file_name=" + str1;
            _there.pie1 = [];
            return _there.$ajax.get(apiurl1).then(res2 => {
              var res1 = res2.data.index;

              if (res1 != 1) {
                for (var j = 0; j < res1.length; j++) {
                  _there.pie1.push(res1[j]);
                }
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
        _t.$ajax.get("./static/func1-1-20151.json").then(res => {
          _t.pie = [];
          for (var j = 0; j < res.data.length; j++) {
            _t.data1.push(res.data[j].value);
            _t.name1.push(res.data[j].name);
          }
          _t.updateChart1();
          _t.myChart1.hideLoading();
        });
      },
      init2() {
        let myChart2 = this.$echarts.init(document.getElementById("main2"));
        this.myChart2 = myChart2;
        this.myChart2.showLoading();
        var _th = this;
        _th.$ajax.get("./static/func1-2-201501.json").then(res => {
          for (var j = 0; j < res.data.length; j++) {
            _th.pie1.push(res.data[j]);
          }
          _th.updateChart2();
          _th.myChart2.hideLoading();
        });
      },
      updateChart1() {
        this.myChart1.setOption({
          title: {
            text:
              this.selected[0] + "年第" + this.selected[1] + "季度题材票房比例"
          },
          color: ["#3398DB"],
          tooltip: {
            trigger: "axis",
            feature: {
              saveAsImage: {}
            },
            axisPointer: {
              type: "shadow" // 默认为直线，可选为：'line' | 'shadow'
            }
          },
          grid: {
            left: "3%",
            right: "4%",
            bottom: "3%",
            containLabel: true
          },
          xAxis: [
            {
              type: "category",
              data: this.name1,
              axisTick: {
                alignWithLabel: true
              },
              axisLabel: {
                interval: 0,
                rotate: 45,
              },
            }
          ],
          yAxis: [
            {
              type: "value"
            }
          ],
          series: [
            {
              name: "票房份额",
              type: "bar",
              barWidth: "60%",
              data: this.data1
            }
          ]
        });
      },
      updateChart2() {
        this.myChart2.setOption({
          title: {
            text: this.selected[0] + "年" + this.selected[2] + "月题材票房比例",

            x: "center"
          },
          tooltip: {
            trigger: "item",
            formatter: "{a} <br/>{b} : {c} ({d}%)"
          },
          legend: {
            orient: "vertical",
            left: "left",
            data: this.pie1.name
          },
          series: [
            {
              name: "票房份额",
              type: "pie",
              radius: "55%",
              center: ["50%", "60%"],
              data: this.pie1,
              itemStyle: {
                emphasis: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: "rgba(0, 0, 0, 0.5)"
                }
              }
            }
          ]
        });
      }
    }
  };
</script>





