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
        <el-menu-item index="main">加入报表</el-menu-item>
        <el-menu-item index="2-3">查看当前报表</el-menu-item>
      </el-submenu>
      <el-submenu index="3" style="float:right;">
        <template slot="title">欢迎你！{{user.name}}</template>
        <el-menu-item index="/">退出</el-menu-item>
      </el-submenu>
    </el-menu>
    <div id="">
      <h2 style="text-align:center">票房变化趋势</h2>
      <div style=" margin:auto; width:1600px; height:100px;">
        <div id="app1" style=" width:300px; height:100px; float:left; margin-left:10px;">
          <font size="3" face="宋体">年份</font>
          <!-- v-model优先匹配value值，如果没有就直接匹配option的text -->
          <el-select v-model="selected[0]" placeholder="请选择" @change="changetest(selected[0])">
            <el-option
              v-for="item in options1"
              :key="item.value"
              :value="item.value"
            ></el-option>
          </el-select>
       
        </div>
        <div id="app2" style=" width:300px; height:100px; float:left; margin-left:10px;">
          <font size="3" face="宋体">年份</font>
          <!-- v-model优先匹配value值，如果没有就直接匹配option的text -->
          <el-select v-model="selected[1]" placeholder="请选择" @change="changetest(selected[1])">
            <el-option
              v-for="item in options1"
              :key="item.value"
              :value="item.value"
            ></el-option>
          </el-select>

        </div>
        <div id="app3" style=" width:300px; height:100px; float:left; margin-left:10px;">
          <font size="3" face="宋体">年份</font>
          <!-- v-model优先匹配value值，如果没有就直接匹配option的text -->
          <el-select v-model="selected[2]" placeholder="请选择" @change="changetest(selected[2])">
            <el-option
              v-for="item in options1"
              :key="item.value"
              :value="item.value"
            ></el-option>
          </el-select>

        </div>
      </div>
      <div>
        <div id="app4" style=" width:300px; height:100px; float:left; margin-left:10px;">
          <font size="3" face="宋体">起始月</font>
          <!-- v-model优先匹配value值，如果没有就直接匹配option的text -->
          <el-select v-model="startm" placeholder="请选择" @change="change">
            <el-option
              v-for="item in options2"
              :key="item.value"
              :value="item.value"
            ></el-option>
          </el-select>

        </div>
        <div id="app5" style=" width:300px; height:100px; float:left; margin-left:10px;">
          <font size="3" face="宋体">终止月</font>
          <!-- v-model优先匹配value值，如果没有就直接匹配option的text -->
          <el-select v-model="endm" placeholder="请选择" @change="change">
            <el-option
              v-for="item in options2"
              :key="item.value"
              :value="item.value"
            ></el-option>
          </el-select>

        </div>
      </div>

      <div id="main" style="width: 800px;height:500px; margin:100px auto; "></div>


    </div>
  </div>
</template>
<script>
  import jsPDF from 'jspdf';
  export default {
    name: "chart2",
    data() {
      return {
        selected: ["2016", "2017", "2018"],
        startm: "01",
        endm: "12",
        myChart: {},
        month: {f2015: [], f2016: [], f2017: [], f2018: []},
        value: {f2015: [], f2016: [], f2017: [], f2018: []},
        activeIndex: '/echart2',
        options1: [{value: "2015",}, {value: "2016",}, {value: "2017",}, {value: "2018",}],
        options2: [{value: "01",}, {value: "02",}, {value: "03",}, {value: "04",}, {value: "05",}, {value: "06",},
          {value: "07",}, {value: "08",}, {value: "09",}, {value: "10",}, {value: "11",}, {value: "12",},],
        htmlTitle: '页面导出PDF文档名',
      };
    },
    beforeCreate() {
      document.querySelector('body').setAttribute('style', 'background:#f2f2f2')
    },
    mounted() {
      this.init();
    },
    computed:{
      user(){
        return this.$store.state.user;
      },
      
    },
    methods: {
      convertCanvasToImage() {

        this.$html2canvas(document.getElementById('main')).then( (canvas)=> {
      
          var _t=this;
          _t.$store.dispatch('add',canvas).then(() => {
            
            
          });


        });
     

      },
      savepdf(){
         this.$router.replace('/savepdf');
      },
      handleSelect(index) {
        
        if (index == "main") {
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
      changetest(year) {
         if(this.user.name=="游客")
        {
          alert("此功能暂不对游客开放，谢谢合作！");
          this.selected=["2016", "2017", "2018"]
          return null;
        }
        this.updateData(year);
      },

      change() {
         if(this.user.name=="游客")
        {
          alert("此功能暂不对游客开放，谢谢合作！");
          this.startm="01";
          this.endm="12";
          return null;
        }
        this.updateall();

      },
      updateall() {
        var apiurl1 =
          "http://127.0.0.1:8000/func/func2_1?year1=" +
          this.selected[0] +
          "&year2=" +
          this.selected[1] +
          "&year3=" +
          this.selected[2];
        apiurl1 = apiurl1 + "&start_month=" + this.startm + "&end_month=" + this.endm;
        this.$http.get(apiurl1).then(response => {
          var res = JSON.parse(response.bodyText);
          if (res.error_num == 0) {

            var _there = this;
            var str1 = "func2-" + this.selected[0] + ".json";
            var str2 = "func2-" + this.selected[1] + ".json";
            var str3 = "func2-" + this.selected[2] + ".json";
            var apiurl1 = "http://127.0.0.1:8000/func/function_get3?file_name1=" + str1 + "&file_name2=" + str2 + "&file_name3=" + str3;
            return _there.$ajax.get(apiurl1).then(resall => {
              var res1 = resall.data.index1;
              var res2 = resall.data.index2;
              var res3 = resall.data.index3;

              if (res1 != 1) {
                _there.month['f' + this.selected[0]] = [];
                _there.value['f' + this.selected[0]] = [];
                for (var j = 0; j < res1.length; j++) {
                  _there.month['f' + this.selected[0]].push(res1[j].month);
                  _there.value['f' + this.selected[0]].push(res1[j].box_sum);

                }

              }
              if (res2 != 1) {
                _there.month['f' + this.selected[1]] = [];
                _there.value['f' + this.selected[1]] = [];
                for (var j = 0; j < res2.length; j++) {
                  _there.month['f' + this.selected[1]].push(res2[j].month);
                  _there.value['f' + this.selected[1]].push(res2[j].box_sum);

                }

              }
              if (res3 != 1) {
                _there.month['f' + this.selected[2]] = [];
                _there.value['f' + this.selected[2]] = [];
                for (var j = 0; j < res3.length; j++) {
                  _there.month['f' + this.selected[2]].push(res3[j].month);
                  _there.value['f' + this.selected[2]].push(res3[j].box_sum);

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
      updateData(year) {
        var apiurl = "http://127.0.0.1:8000/func/func2?year=";

        apiurl = apiurl + year;
        this.$http
          .get(apiurl + "&start_month=" + this.startm + "&end_month=" + this.endm)
          .then(response => {
            var res = JSON.parse(response.bodyText);
            if (res.error_num == 0) {
              var _there = this;
              var str1 = "func2-" + year + ".json";
              var apiurl1 = "http://127.0.0.1:8000/func/function_get?file_name=" + str1
              _there.month['f' + year] = [];
              _there.value['f' + year] = [];
              return _there.$ajax.get(apiurl1).then(res2 => {
                var res1 = res2.data.index;

                if (res1 != 1) {
                  for (var j = 0; j < res1.length; j++) {
                    _there.month['f' + year].push(res1[j].month);
                    _there.value['f' + year].push(res1[j].box_sum);
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
      init() {
        let myChart = this.$echarts.init(document.getElementById("main"));
        this.myChart = myChart;
        this.myChart.showLoading();

        var _t = this;
        _t.value['f' + _t.selected[0]] = [];
        _t.month['f' + _t.selected[0]] = [];

        _t.$ajax.get("./static/data/func2-2016.json").then(res => {
          for (var j = 0; j < res.data.length; j++) {
            _t.value['f' + _t.selected[0]].push(res.data[j].box_sum);
            _t.month['f' + _t.selected[0]].push(res.data[j].month);
          }
          _t.updateChart();
        });
        var _th = this;
        _th.value['f' + _t.selected[1]] = [];
        _th.month['f' + _t.selected[1]] = [];
        _t.$ajax.get("./static/data/func2-2017.json").then(res => {
          for (var j = 0; j < res.data.length; j++) {
            _th.value['f' + _th.selected[1]].push(res.data[j].box_sum);
            _th.month['f' + _th.selected[1]].push(res.data[j].month);

          }
          _t.updateChart();
        });
        _t.value['f' + _t.selected[2]] = [];
        _t.month['f' + _t.selected[2]] = [];
        _t.$ajax.get("./static/data/func2-2018.json").then(res => {
          for (var j = 0; j < res.data.length; j++) {
            _t.value['f' + _t.selected[2]].push(res.data[j].box_sum);
            _t.month['f' + _t.selected[2]].push(res.data[j].month);
          }
          _t.updateChart();
          _t.myChart.hideLoading();
        });
      },
      updateChart() {
        this.myChart.setOption({
          title: {
            text:
              this.selected[0] + "年、" + this.selected[1] + "年、及" + this.selected[2] + "年票房变化趋势",
            x: "40%"
          },
          tooltip: {
            trigger: "axis"
          },
          legend: {
            data: [this.selected[0], this.selected[1], this.selected[2]],

            left: "left",

            orient: "vertical",

            height: 50
          },
          grid: {
            left: "3%",
            right: "4%",
            bottom: "3%",
            containLabel: true
          },
          toolbox: {
            feature: {
              saveAsImage: {
                show: true,

                excludeComponents: ["toolbox"],

                pixelRatio: 2
              }
            }
          },
          xAxis: {
            type: "category",
            boundaryGap: false,
            data: this.month['f' + this.selected[0]]
          },
          yAxis: {
            type: "value"
          },
          series: [
            {
              name: this.selected[0],
              type: "line",
              data: this.value['f' + this.selected[0]]
            },
            {
              name: this.selected[1],
              type: "line",
              data: this.value['f' + this.selected[1]]
            },
            {
              name: this.selected[2],
              type: "line",
              data: this.value['f' + this.selected[2]]
            }
          ]
        });
      }
    }
  };


</script>


